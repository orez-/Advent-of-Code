IDENTIFICATION DIVISION.
PROGRAM-ID. PART2.

DATA DIVISION.
    WORKING-STORAGE SECTION.
    01 FILE-CONTENTS.
        02 GENERATOR-LINE PIC X(12) OCCURS 1000 TIMES.
        02 SCRUBBER-LINE PIC X(12) OCCURS 1000 TIMES.
    01 IN-DATA PICTURE X(12).
    *> 9(x) indicates an x-bit integer
    01 TOTAL PICTURE 9(32).
    01 IDX PICTURE 9(32).
    01 BIT-IDX PICTURE 9(32).
    01 BIT-TOTAL PIC 9(32).
    01 GOAL-BIT PIC X(1).
    01 BIT-VALUE PIC 9(32) VALUE 1.
    01 GENERATOR-STR PIC X(12).
    01 GENERATOR-VALUE PIC 9(32).
    01 SCRUBBER-STR PIC X(12).
    01 SCRUBBER-VALUE PIC 9(32).
    *> This wild type strips the leading 0s from the integer display
    *> but.. still right-aligns it for some reason. Fine.
    01 ANSWER PIC Z(17)9.

PROCEDURE DIVISION.
    *> Maintain two copies of the file from stdin
    PARA.
    ACCEPT IN-DATA
    PERFORM VARYING IDX FROM 1 BY 1 UNTIL IN-DATA=SPACES
        SET GENERATOR-LINE(IDX) TO IN-DATA
        SET SCRUBBER-LINE(IDX) TO IN-DATA
        ACCEPT IN-DATA
    END-PERFORM

    *> Find O2 Generator value
    PERFORM VARYING BIT-IDX FROM 1 BY 1 UNTIL BIT-IDX=13
        *> Find the most common value for this bit
        SET TOTAL TO 0
        SET BIT-TOTAL TO 0
        PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
            IF GENERATOR-LINE(IDX) NOT = SPACES
                ADD 1 TO TOTAL
                SET IN-DATA TO GENERATOR-LINE(IDX)
                IF IN-DATA(BIT-IDX:1)="1"
                    ADD 2 TO BIT-TOTAL
                END-IF
            END-IF
        END-PERFORM
        IF TOTAL <= BIT-TOTAL THEN
            SET GOAL-BIT TO "1"
        ELSE
            SET GOAL-BIT TO "0"
        END-IF

        *> Remove all values that do not have this bit set
        PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
            SET IN-DATA TO GENERATOR-LINE(IDX)
            IF IN-DATA(BIT-IDX:1) NOT = GOAL-BIT THEN
                SET GENERATOR-LINE(IDX) TO SPACES
            END-IF
        END-PERFORM
    END-PERFORM

    *> Only remaining value is our value.
    *> Pray (but do not verify) that there is only one.
    PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
        IF GENERATOR-LINE(IDX) NOT = SPACES
            SET GENERATOR-STR TO GENERATOR-LINE(IDX)
        END-IF
    END-PERFORM

    *> ---

    *> Find CO2 Scrubber value
    PERFORM VARYING BIT-IDX FROM 1 BY 1 UNTIL BIT-IDX=13
        *> Find the most common value for this bit
        SET TOTAL TO 0
        SET BIT-TOTAL TO 0
        PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
            IF SCRUBBER-LINE(IDX) NOT = SPACES
                ADD 1 TO TOTAL
                SET IN-DATA TO SCRUBBER-LINE(IDX)
                IF IN-DATA(BIT-IDX:1)="1"
                    ADD 1 TO BIT-TOTAL
                END-IF
            END-IF
        END-PERFORM
        *> This is a little tricky: if over half the bits are 1 we'll want
        *> to pick 0, UNLESS they're all 1.
        IF BIT-TOTAL = TOTAL THEN
            SET GOAL-BIT TO "1"
        ELSE IF BIT-TOTAL = 0 THEN
            SET GOAL-BIT TO "0"
        ELSE
            MULTIPLY 2 BY BIT-TOTAL
            IF TOTAL <= BIT-TOTAL THEN
                SET GOAL-BIT TO "0"
            ELSE
                SET GOAL-BIT TO "1"
            END-IF
        END-IF
        END-IF

        *> Remove all values that do not have this bit set
        PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
            SET IN-DATA TO SCRUBBER-LINE(IDX)
            IF IN-DATA(BIT-IDX:1) NOT = GOAL-BIT THEN
                SET SCRUBBER-LINE(IDX) TO SPACES
            END-IF
        END-PERFORM
    END-PERFORM

    *> Only remaining value is our value.
    *> Pray (but do not verify) that there is only one.
    PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX = 1000
        IF SCRUBBER-LINE(IDX) NOT = SPACES
            SET SCRUBBER-STR TO SCRUBBER-LINE(IDX)
        END-IF
    END-PERFORM

    *> Convert the two binary strings to numbers
    PERFORM VARYING IDX FROM 12 BY -1 UNTIL IDX=0
        IF GENERATOR-STR(IDX:1) = "1" THEN
            ADD BIT-VALUE TO GENERATOR-VALUE
        END-IF
        IF SCRUBBER-STR(IDX:1) = "1" THEN
            ADD BIT-VALUE TO SCRUBBER-VALUE
        END-IF
        MULTIPLY 2 BY BIT-VALUE
    END-PERFORM
    MULTIPLY GENERATOR-VALUE BY SCRUBBER-VALUE GIVING ANSWER
    DISPLAY ANSWER
STOP RUN.
