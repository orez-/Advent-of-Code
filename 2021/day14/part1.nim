import std/sequtils
import std/strutils
import std/tables

proc parseFile: (string, Table[string, string]) =
    let polymer = stdin.readLine()
    discard stdin.readLine()
    var rules: Table[string, string]
    for line in stdin.lines():
        let pieces = line.split(" -> ")
        let left = pieces[0]
        let right = pieces[1]
        rules[left] = right
    return (polymer, rules)

proc stepPolymer(polymer: string, rules: Table[string, string]): string =
    for i, chr in polymer[0..^2]:
        result.add(chr)
        result.add(rules[polymer[i..i+1]])
    result.add(polymer[^1])

proc main =
    var (polymer, rules) = parseFile()
    for i in 1..10:
        polymer = stepPolymer(polymer, rules)
    var counts: CountTable[char]
    for c in polymer:
        counts[c] = succ counts[c]
    let values = toSeq(counts.values())
    let most = values.max()
    let least = values.min()
    echo most - least

main()
