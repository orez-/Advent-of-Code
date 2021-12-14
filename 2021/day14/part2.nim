import std/sequtils
import std/strutils
import std/tables

type
    Polymer = CountTable[string]
    Rules = Table[string, (string, string)]

proc parseFile: (Polymer, Rules) =
    let polymerStr = stdin.readLine()
    var polymer: Polymer

    # Chunk the polymer string by twos, and keep the count of each pair
    for i, chr in polymerStr[0..^2]:
        let substr = polymerStr[i..i+1]
        polymer[substr] = succ polymer[substr]

    # Blank line
    discard stdin.readLine()

    # "AC -> B" becomes {"AC": ("AB", "BC")}
    var rules: Rules
    for line in stdin.lines():
        let pieces = line.split(" -> ")
        let before = pieces[0]
        let middle = pieces[1]
        let left = before[0]
        let right = before[1]
        rules[before] = (left & middle, middle & right)
    return (polymer, rules)

proc stepPolymer(polymer: Polymer, rules: Rules): Polymer =
    for key, count in polymer:
        let (a, b) = rules[key]
        result[a] = result[a] + count
        result[b] = result[b] + count

proc main =
    var (polymer, rules) = parseFile()
    for i in 1..40:
        polymer = stepPolymer(polymer, rules)

    # Once we've stepped the polymer enough we need the char counts,
    # which means totaling the char counts from the two-char format,
    # then *halving* it, since each character has been counted twice*
    var letters: CountTable[char]
    for key, v in polymer:
        for k in key:
            letters[k] = letters[k] + v

    # *...each character, that is, except the first and last characters.
    # We're fudging it a little bit: for my input both first and last
    # are 'V'.
    letters['V'] = letters['V'] + 2
    let values = toSeq(letters.values())
    let most = values.max()
    let least = values.min()
    echo (most - least) div 2

main()
