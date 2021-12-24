'use strict'

type Cell = number
// js key munging utilities
type Key = string
const toKey = (arr: [number, number]): Key => `${arr[0]}_${arr[1]}`
const fromKey = (key: Key): [number, number] => {
    let [x, y] = key.split("_")
    return [+x, +y]
}

const fs = require('fs')
const file = fs.readFileSync('/dev/stdin').toString().split('\n')
const numberLookup = (() => {
    let answer = []
    for (let c of file[0]) { answer.push(c === '#' ? 1 : 0) }
    return answer
})()

let image = new Map<Key, Cell>()
for (let [y, line] of file.slice(2).entries()) {
    for (let [x, c] of [...line].entries()) {
        image.set(toKey([x, y]), c === '#' ? 1 : 0)
    }
}

const step = (image: Map<Key, Cell>, all: Cell) => {
    let newImage = new Map()
    let newCoords = new Set<Key>()
    // Find all the positions that need filling
    for (let key of image.keys()) {
        let [x, y] = fromKey(key)
        for (let dy of [-1, 0, 1]) {
            for (let dx of [-1, 0, 1]) {
                newCoords.add(toKey([x + dx, y + dy]))
            }
        }
    }
    // Fill positions
    for (let key of newCoords) {
        let [x, y] = fromKey(key)
        let num = 0
        for (let dy of [-1, 0, 1]) {
            for (let dx of [-1, 0, 1]) {
                num <<= 1
                num += image.get(toKey([x + dx, y + dy])) ?? all
            }
        }
        newImage.set(toKey([x, y]), numberLookup[num])
    }
    return newImage
}

const litPixels = (image: Map<Key, Cell>): number =>
    Array.from(image.values()).reduce((a: number, b: number) => a + b)

let iterate;
switch (process.argv[2]) {
    case 'part1':
        iterate = 1
        break
    case 'part2':
        iterate = 25
        break
    default:
        console.log(`Please specify 'part1' or 'part2', not '${process.argv[2]}'`)
        process.exit(1)
}
for (let i = 0; i < iterate; i++) {
    image = step(step(image, 0), 1)
}
let answer = litPixels(image)
console.log(answer)
