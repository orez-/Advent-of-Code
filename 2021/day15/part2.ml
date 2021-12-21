open Printf

type board = {width: int; height: int; cells: ((int * int), int) Hashtbl.t}

(* Via https://ocaml.org/releases/4.00/htmlman/manual004.html *)
module PrioQueue =
  struct
    type priority = int
    type 'a queue = Empty | Node of priority * 'a * 'a queue * 'a queue
    let empty = Empty
    let rec insert queue prio elt =
      match queue with
        Empty -> Node(prio, elt, Empty, Empty)
      | Node(p, e, left, right) ->
          if prio <= p
          then Node(prio, elt, insert right p e, left)
          else Node(p, e, insert right prio elt, left)
    exception Queue_is_empty
    let rec remove_top = function
        Empty -> raise Queue_is_empty
      | Node(prio, elt, left, Empty) -> left
      | Node(prio, elt, Empty, right) -> right
      | Node(prio, elt, (Node(lprio, lelt, _, _) as left),
                        (Node(rprio, relt, _, _) as right)) ->
          if lprio <= rprio
          then Node(lprio, lelt, remove_top left, right)
          else Node(rprio, relt, left, remove_top right)
    let extract = function
        Empty -> raise Queue_is_empty
      | Node(prio, elt, _, _) as queue -> (prio, elt, remove_top queue)
  end;;

let to_digit byte = (Char.code byte) - (Char.code '0');;
let normalize_risk risk offset = (risk + offset - 1) mod 9 + 1
let five = [0;1;2;3;4]

let read_board =
  let x = ref 0 in
  let y = ref 0 in
  let cells = Hashtbl.create (100 * 100 * 5) in
  try
    let add_line s =
      let once = List.init (String.length s) (fun i -> to_digit (String.get s i)) in
      let row = List.map (fun r -> List.map (normalize_risk r) once) five in
      List.iteri (fun x c -> (Hashtbl.add cells (x, !y) c)) (List.flatten row) in
    let s = read_line () in
    add_line s;
    x := String.length s * 5;
    y := 1;
    while true do
      let s = read_line () in
      add_line s;
      y := !y + 1
    done;
    { width = 0; height = 0; cells = cells}  (* no `never` type? *)
  with
    End_of_file ->
      let height = !y in
      let full_cells = Hashtbl.create (100 * 100 * 25) in
      Hashtbl.iter (fun (x, y) p ->
        List.iter (fun r ->
          let risk = normalize_risk p r in
          Hashtbl.add full_cells (x, y + r * height) risk;
        ) five;
      ) cells;
      { width = !x; height = height * 5; cells = full_cells}

let at board x y = Hashtbl.find board.cells (x, y)
let neighbors board x y =
  let in_bounds c = Option.is_some (Hashtbl.find_opt board.cells c) in
  let coords = List.filter in_bounds [(x - 1, y); (x, y - 1); (x, y + 1); (x + 1, y)] in
  List.map (fun ((x, y)) -> ((at board x y), (x, y))) coords

let bfs board =
  let queue = PrioQueue.empty in
  let rec step queue =
    let p, (x, y), queue' = PrioQueue.extract queue in
    if x + 1 == board.width && y + 1 == board.height then
      p
    else
      let agg q n =
        let (p', (nx, ny)) = n in
        Hashtbl.remove board.cells (nx, ny);
        (PrioQueue.insert q (p + p') (nx, ny)) in
      let queue'' = List.fold_left agg queue' (neighbors board x y) in
      step queue'' in
  step (PrioQueue.insert queue 0 (0, 0));;

let answer = bfs read_board
let () = printf "%d\n" answer
