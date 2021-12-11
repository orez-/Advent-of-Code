# Part 1: Jelly, 61 bytes

```jelly
œṣØ[FœṣØ(FœṣØ<FœṣØ{F
ɠÇÐLḟ“([{<”Ḣi@“)]}>”ị“£“8“¤Ġ“c⁸“’
Ç98Ð¡S
```

## How it works

```
Ç98Ð¡S  Main link. No arguments.

Ç       Call the line parsing helper link..
 98Ð¡   ..98 times, and collect the results
     S  Sum the results
```

```
ɠÇÐLḟ“([{<”Ḣi@“)]}>”ị“£“8“¤Ġ“c⁸“’  Line parsing helper link. No arguments.

ɠ                                  Read a single line from STDIN.
 Ç                                 Call the chunkstripper link..
  ÐL                               ..on loop until the value stops changing
     “([{<”                        The literal string ([{<
    ḟ                              Filter; remove any ([{< from our line,
                                     leaving us only with )]}>
           Ḣ                       Head; grab the first element
              “)]}>”               The literal string )]}>
            i@                     The index of our offending character in the literal
                     “£“8“¤Ġ“c⁸“’  An integer list literal.
                                     This is equivalent to [3,57,1197,25137,0].
                    ị              List access; the score of our offending character
```

```
œṣØ[FœṣØ(FœṣØ<FœṣØ{F  Chunkstripper link. One argument: the line from the input

  Ø[   Ø(   Ø<   Ø{   String constants. [], (), <>, and {}, respectively
œṣ                    Split the line by []..
    F                 ..and flatten the results back into a single string.
                        This results in all []s being removed from the string.
     œṣ               Split the line by ()..
         F            ..and flatten the results.
          œṣ  F       Same for <>
               œṣ  F  Same for {}
```


# Part 2: Jelly, 69 bytes

```jelly
i@€“([{<”Ė5*$1¦€×/€S÷5
œṣØ[FœṣØ(FœṣØ<FœṣØ{F
ɠÇÐL
Ç98Ð¡ḟ“([{<”$Ðḟ1Ŀ€Æṁ
```

## How it works

```
Ç98Ð¡ḟ“([{<”$Ðḟ1Ŀ€Æṁ  Main link. No arguments.

Ç                     Call the line parsing helper link..
 98Ð¡                 ..98 times, and collect the results
             Ðḟ       Filter; discard all items that match..
            $         ..the previous two links as a monad, which are..
      “([{<”          ..the literal string ([{<
     ḟ                ..filter; remove the characters ([{< from the string
                        All together, this block removes lines which,
                        when condensed, contain closing characters.
                        ie: corrupted lines.
               1Ŀ€    Map the scoring link over the condensed incomplete lines
                  Æṁ  Median; take the middle value
```

```
ɠÇÐL  Line parsing helper link. No arguments.

ɠ     Read a single line from STDIN.
 Ç    Call the chunkstripper link..
  ÐL  ..on loop until the value stops changing.
        Note that the chunkstripper link is identical to part 1
```

```
i@€“([{<”Ė5*$1¦€×/€S÷5  Scoring link. One argument: a condensed, incomplete line
                          Note that condensed incomplete lines contain only ([{<

   “([{<”               Literal string ([{<
i@                      The index within that literal string..
  €                     ..of each character of the incomplete line.
                          this operation is basically:
                          "[<{(" -> [2,4,3,1]
         Ė              Enumerate; [[1,2],[2,4],[3,3],[4,1]]
               €        For each element of our enumeration, [i,n]..
             1¦         ..apply to i..
            $           ..a monad of the previous two links, which are..
          5*            ..5^i
                          All together, this gives us:
                          [[5,2],[25,4],[125,3],[625,1]]
                  €     For each element..
                 /      ..Reduce..
                ×       ..with multiplication.
                          ie, get the product of each element:
                          [10,100,375,625]
                   S    Sum; 1110
                    ÷5  Divided by 5. Since Enumerate started counting us
                          from 1, all of our 5-powers have been off.
```
