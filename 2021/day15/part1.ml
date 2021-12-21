open Printf

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

let read_board =
  let x = ref 0 in
  let y = ref 0 in
  let map = ref (Hashtbl.create (100 * 100)) in
  try
    let add_line s = String.iteri (fun x c -> (Hashtbl.add !map (x, !y) (to_digit c))) s in
    let s = read_line () in
    add_line s;
    x := String.length s;
    y := 1;
    while true do
      let s = read_line () in
      add_line s;
      y := !y + 1
    done;
    (0, 0, !map)  (* no `never` type? *)
  with
    End_of_file -> (!x, !y, !map)

let at board x y = Hashtbl.find board (x, y)
let neighbors board x y =
  let in_bounds c = Option.is_some (Hashtbl.find_opt board c) in
  let coords = List.filter in_bounds [(x - 1, y); (x, y - 1); (x, y + 1); (x + 1, y)] in
  List.map (fun ((x, y)) -> ((at board x y), (x, y))) coords

let bfs board_data =
  let (width, height, board) = board_data in
  let queue = PrioQueue.empty in
  let rec step queue =
    let p, (x, y), queue' = PrioQueue.extract queue in
    if x + 1 == width && y + 1 == height then
      p
    else
      let agg q n =
        let (p', (nx, ny)) = n in
        Hashtbl.remove board (nx, ny);
        (PrioQueue.insert q (p + p') (nx, ny)) in
      let queue'' = List.fold_left agg queue' (neighbors board x y) in
      step queue'' in
  step (PrioQueue.insert queue 0 (0, 0));;

let answer = bfs read_board
let () = printf "%d\n" answer
