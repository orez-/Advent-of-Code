Module: day04
Synopsis: 
Author: 
Copyright: 

define constant $width = 5;
define constant $height = 5;

define class <board> (<object>)
  sealed slot cells :: <array>,
    required-init-keyword: cells:;
  slot done :: <boolean>,
    init-value: #f;
end;

define function read-board ()
  let output = read-line(*standard-input*, on-end-of-stream: #f);
  let cells = make(<array>, dimensions: #(5, 5));

  block(return)
    for (y from 0 below $height)
      let line = read-line(*standard-input*, on-end-of-stream: #f);

      if (~line)
        return(#f);
      end;
      let x = 0;
      for ( elem in split(line, " ", remove-if-empty?: #t) )

        cells[y,x] := string-to-integer(elem);
        x := x + 1;
      end;
    end;
    make(<board>, cells: cells);
  end block;
end function read-board;


// Call a number and return the score of the board if you've got Bingo.
// Otherwise return false.

define method call-number (num :: <number>, board :: <board>)
  let output = #f;
  if (~board.done)
    let idx = find-key(board.cells, curry(\=, num));
    if (idx)
      board.cells[idx] := #f;
      // no methods to operate over rows / columns?
      // ...why am i using the 2d array class, then?
      let col = modulo(idx, $width);
      let row = truncate/(idx, $width);
      let full_row = every?(\~, map(method (y) board.cells[y, col] end, range(from: 0, to: 4)));
      let full_col = every?(\~, map(method (x) board.cells[row, x] end, range(from: 0, to: 4)));

      if (full_row | full_col)
        board.done := #t;
        output := reduce(\+, 0, choose(identity, board.cells)) * num;
      end;
    end;
  end;
  output;
end method call-number;

define function find-winner(boards, nums)
  block(return)
    for (num in nums)
      let score = any?(curry(call-number, num), boards);
      if (score)
        return(score);
      end;
    end;
  end block;
end function;

define function find-loser(boards, nums)
  let last-score = 0;
  for (num in nums)
    for (board in boards)
      let score = call-number(num, board);
      if (score)
        last-score := score;
      end;
    end;
  end;
  last-score
end function;

define function main
    (name :: <string>, arguments :: <vector>)
  let nums = map(string-to-integer, split(read-line(*standard-input*), ","));
  let boards = make(<stretchy-vector>);
  let board = read-board();
  while (board)
    add!(boards, board);
    board := read-board();
  end;

  let score = 0;
  select (arguments[0] by \=)
    "part1" => score := find-winner(boards, nums);
    "part2" => score := find-loser(boards, nums);
    otherwise =>
      error("Please specify 'part1' or 'part2', not '%s'\n", arguments[0]);
  end;
  format-out("%s\n", score);
  exit-application(0);
end function main;

main(application-name(), application-arguments());
