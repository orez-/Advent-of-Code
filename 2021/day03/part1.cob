IDENTIFICATION DIVISION.
PROGRAM-ID. PART1.

DATA DIVISION.
    WORKING-STORAGE SECTION.
    01 IN-DATA PICTURE X(12).
    *> 9(x) indicates an x-bit integer
    01 TOTAL PICTURE 9(32).
    01 IDX PICTURE 9(32).
    *> Table definition. We can use this as an array
    01 BIT-COUNTS.
        02 COUNTS PIC 9(32) OCCURS 12 TIMES.
    01 GAMMA PICTURE 9(32) VALUE 0.
    01 EPSILON PICTURE 9(32) VALUE 0.
    01 BIT-VALUE PIC 9(32) VALUE 1.
    *> This wild type strips the leading 0s from the integer display
    *> but.. still right-aligns it for some reason. Fine.
    01 ANSWER PIC Z(17)9.

PROCEDURE DIVISION.
    *> Read line-by-line from stdin and track the count of 1s for each column
    PARA.
    ACCEPT IN-DATA
    PERFORM VARYING TOTAL FROM 0 BY 1 UNTIL IN-DATA=SPACES
        PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX=13
            IF IN-DATA(IDX:1)="1" THEN
                ADD 1 TO COUNTS(IDX)
            END-IF
        END-PERFORM
        ACCEPT IN-DATA
    END-PERFORM

    *> Convert counts to the two binary numbers
    PERFORM VARYING IDX FROM 12 BY -1 UNTIL IDX=0
        MULTIPLY 2 BY COUNTS(IDX)
        IF COUNTS(IDX) > TOTAL THEN
            ADD BIT-VALUE TO GAMMA
        ELSE
            ADD BIT-VALUE TO EPSILON
        END-IF
        MULTIPLY 2 BY BIT-VALUE
    END-PERFORM
    MULTIPLY GAMMA BY EPSILON GIVING ANSWER
    DISPLAY ANSWER
STOP RUN.
