import "os" for Process
import "/queue" for PriorityQueue

var A = 0
var B = 1
var C = 2
var D = 3
var Door = 4
var Empty = 5

var Cost = [1, 10, 100, 1000]
var Display = ["A", "B", "C", "D", ".", "."]

var Get = Fn.new {|list, idx|
    if (list.count > idx) return list[idx]
    return 4
}

class State {
    construct new(hall, rooms, gscore, depth) {
        _hall = hall
        _rooms = rooms
        _gscore = gscore
        _depth = depth
    }

    construct part1() {
        _hall = [Empty, Empty, Door, Empty, Door, Empty, Door, Empty, Door, Empty, Empty]
        _rooms = [
            [B, D],
            [A, A],
            [D, B],
            [C, C],
        ]
        _gscore = 0
        _depth = 2
    }

    construct part2() {
        _hall = [Empty, Empty, Door, Empty, Door, Empty, Door, Empty, Door, Empty, Empty]
        _rooms = [
            [B, D, D, D],
            [A, B, C, A],
            [D, A, B, B],
            [C, C, A, C],
        ]
        _gscore = 0
        _depth = 4
    }

    hall { _hall }
    rooms { _rooms }
    gscore { _gscore }
    gscore=(new) { _gscore = new }
    isReceptive(idx) { rooms[idx].count < _depth && rooms[idx].all {|e| e == idx} }
    toString {
        var hallStr = _hall.map { |e| Display[e] }.join("")
        hallStr = "#%(hallStr)#"
        for (y in (_depth - 1)..0) {
            var chrs = (0..3).map {|x| Display[Get.call(rooms[x], y)]}.toList
            hallStr = "%(hallStr)\n  #%(chrs[0])#%(chrs[1])#%(chrs[2])#%(chrs[3])#"
        }
        return hallStr
    }

    clone() { State.new(_hall[0..-1], rooms.map {|e| e[0..-1]}.toList, _gscore, _depth) }

    isDone {
        return (0..3).all {|piece|
            return rooms[piece].count == _depth && rooms[piece].all {|e| e == piece}
        }
    }

    fscore { heuristic + _gscore }
    hash { toString }
    heuristic {
        var total = 0
        for (h in 0..10) {
            if (hall[h] != Empty && hall[h] != Door) {
                var goal = hall[h] * 2 + 2
                total = total + ((h - goal).abs + 1) * Cost[hall[h]]
            }
        }
        for (x in 0..3) {
            for (y in 0...rooms[x].count) {
                var piece = rooms[x][y]
                if (piece != x) {
                    var steps = (piece - x).abs * 2 + (_depth + 1 - y)
                    total = total + steps * Cost[piece]
                }
            }
        }
        return total
    }

    nextStates() {
        return Fiber.new {
            // We're either moving one of the stacks..
            for (i in 0..3) {
                if (rooms[i].isEmpty) continue
                if (rooms[i].all {|e| e == i}) continue
                var steps = _depth + 1 - rooms[i].count
                var lift = this.clone()
                var piece = lift.rooms[i].removeAt(-1)

                // Place it in the hall UNLESS there's a direct route
                // to the room.
                var hallIdx = 2 + i * 2
                var goalIdx = 2 + piece * 2

                if (isReceptive(piece) && hall[hallIdx..goalIdx].all {|elem| elem == Empty || elem == Door}) {
                    steps = steps + (hallIdx - goalIdx).abs + (_depth - rooms[piece].count)
                    lift.rooms[piece].add(piece)
                    lift.gscore = lift.gscore + steps * Cost[piece]
                    Fiber.yield(lift)
                    continue
                }
                for (range in [hallIdx..0, hallIdx..10]) {
                    for (h in range) {
                        if (lift.hall[h] == Empty) {
                            var dist = (hallIdx - h).abs + steps
                            var next = lift.clone()
                            next.hall[h] = piece
                            next.gscore = next.gscore + dist * Cost[piece]
                            Fiber.yield(next)
                        } else if (lift.hall[h] != Door) break
                    }
                }
            }
            // ..or one from the hall.
            for (range in [0..8, 10..2]) {
                var pieceIdx = null
                var piece = null
                for (h in range) {
                    if (hall[h] != Empty && hall[h] != Door) {
                        pieceIdx = h
                        piece = hall[h]
                    }
                    if (h / 2 - 1 == piece) {
                        if (isReceptive(piece)) {
                            var next = this.clone()
                            var dist = (pieceIdx - h).abs + (_depth - rooms[piece].count)
                            next.hall[pieceIdx] = Empty
                            next.rooms[piece].add(piece)
                            next.gscore = next.gscore + dist * Cost[piece]
                            Fiber.yield(next)
                        }
                        pieceIdx = null
                        piece = null
                    }
                }
            }
        }
    }
}

var findCost = Fn.new {|state|
    var queue = PriorityQueue.new()
    var seen = {state.hash: 1}
    queue.push(state, state.heuristic)
    while (true) {
        var t = queue.pop()
        state = t[0]
        var fscore = t[1]
        if (state.isDone) {
            return fscore
        }
        var states = state.nextStates()
        var next = true
        while (next = states.call()) {
            if (!seen[next.hash]) {
                seen[next.hash] = 1
                queue.push(next, next.gscore + next.heuristic)
            }
        }
    }
}

var main = Fn.new {
    var arg = Process.arguments[0]
    var initial
    if (arg == "part1") {
        initial = State.part1()
    } else if (arg == "part2") {
        initial = State.part2()
    } else {
        System.print("Please specify 'part1' or 'part2', not '%(arg)'")
        return
    }
    System.print(findCost.call(initial))
}

main.call()
