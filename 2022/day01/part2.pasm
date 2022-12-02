PUSH 0 0 0 0 0 0
:AGAIN
PUSH 0 0
:TOP
MUL 10
INCHAR
DUP
SUB 10
NOT
JUMPIF NEW_LINE
SUB 48
ADD
JUMP TOP

:NEW_LINE
# Our read number ends up x10, but we happen to have a 10
# from the ascii newline. Divide to get our real number.
DIV
ADD
PUSH 0
INCHAR
DUP
NOT
JUMPIF MAX
ADD
DUP
SUB 10
NOT
JUMPIF MAX
SUB 48
JUMP TOP

:MAX
# bury a bool at the bottom of the stack for if we're done
# after this `max`. 0 when done, 10 (ᖍ(ツ)ᖌ) when not done.
ROLL 8 1
DUP
ROLL 3 1
GREATER
JUMPIF NO_KEEP
# better than smallest
# advance and kill smallest
ROLL 2 1
POP
DUP
ROLL 3 1
GREATER
JUMPIF THIRD
# better than new smallest; roll
DUP
ROLL 3 2
DUP
ROLL 6 2
ROLL 3 1
GREATER
JUMPIF SECOND
# youdabes
DUP
ROLL 5 2
DUP
ROLL 4 2
JUMP CHECK_DONE
:NO_KEEP  # no good. beat it.
POP
DUP
JUMP CHECK_DONE
:THIRD
ROLL 2 1
DUP
ROLL 3 2
DUP
JUMP CHECK_DONE
:SECOND
ROLL 2 1
DUP
ROLL 3 2
DUP
ROLL 6 4
:CHECK_DONE
ROLL 7 6  # check that buried bool to see if we're done
JUMPIF AGAIN
POP
ROLL 5 4
ADD
ADD
OUTNUM
