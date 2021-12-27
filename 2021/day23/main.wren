import "/queue" for PriorityQueue

var A = 0
var B = 1
var C = 2
var D = 3
var Door = 4
var Empty = 5

var Cost = [1, 10, 100, 1000]
var Display = ["A", "B", "C", "D", ".", "."]

class State {
    construct new(hall, top, base, gscore) {
        _hall = hall
        _top = top
        _base = base
        _gscore = gscore
    }

    construct initial() {
        _hall = [Empty, Empty, Door, Empty, Door, Empty, Door, Empty, Door, Empty, Empty]
        _top = [D, A, B, C]
        _base = [B, A, D, C]
        _gscore = 0
    }

    hall { _hall }
    top { _top }
    base { _base }
    gscore { _gscore }
    gscore=(new) { _gscore = new }
    toString {
        var hall = _hall.map { |e| Display[e] }.join("")
        var top = _top.map { |e| Display[e] }.toList
        var topStr = "###%(top[0])#%(top[1])#%(top[2])#%(top[3])###"
        var base = _base.map { |e| Display[e] }.toList
        var baseStr = "  #%(base[0])#%(base[1])#%(base[2])#%(base[3])#"
        return "\n#%(hall)#\n%(topStr)\n%(baseStr)\n"
    }

    clone() { State.new(_hall[0..-1], _top[0..-1], _base[0..-1], _gscore) }

    isReceptive(idx) { isBaseReceptive(idx) || isTopReceptive(idx) }
    isTopReceptive(idx) { base[idx] == idx && top[idx] == Empty }
    isBaseReceptive(idx) { base[idx] == Empty }
    // No list equality ಠ_ಠ
    // isDone { top == [A, B, C, D] && base == [A, B, C, D] }
    isDone {
        return top[0] == A && top[1] == B && top[2] == C && top[3] == D &&
            base[0] == A && base[1] == B && base[2] == C && base[3] == D
    }

    fscore { heuristic + _gscore }
    hash { "%(_hall.join(""))%(_top.join(""))%(_base.join(""))" }
    heuristic {
        var total = 0
        for (h in 0..10) {
            if (hall[h] != Empty && hall[h] != Door) {
                var goal = hall[h] * 2 + 2
                total = total + ((h - goal).abs + 1) * Cost[hall[h]]
            }
        }
        for (i in 0..3) {
            if (base[i] != Empty && base[i] != i) {
                total = total + ((base[i] - i).abs * 2 + 3) * Cost[base[i]]
            }
            if (top[i] != Empty && top[i] != i) {
                total = total + ((top[i] - i).abs * 2 + 2) * Cost[top[i]]
            }
        }
        return total
    }

    nextStates() {
        return Fiber.new {
            // We're either moving one of the stacks..
            for (i in 0..3) {
                var top = this.top[i]
                var base = this.base[i]
                var lift = this.clone()
                var steps
                var piece

                // Can lift top
                if (top != Empty) {
                    if (top != i || base != i) {
                        piece = top
                        lift.top[i] = Empty
                        steps = 1
                    } else continue
                } else if (base != Empty && base != i) {
                    piece = base
                    lift.base[i] = Empty
                    steps = 2
                } else continue
                // Place it in the hall UNLESS there's a direct route
                // to the room.
                var hallIdx = 2 + i * 2
                var goalIdx = 2 + piece * 2

                if (isReceptive(piece) && hall[hallIdx..goalIdx].all {|elem| elem == Empty || elem == Door}) {
                    steps = steps + (hallIdx - goalIdx).abs + 1
                    if (isBaseReceptive(piece)) {
                        steps = steps + 1
                        lift.base[piece] = piece
                    } else lift.top[piece] = piece
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
                        if (isBaseReceptive(piece)) {
                            var next = this.clone()
                            next.hall[pieceIdx] = Empty
                            next.base[piece] = piece
                            var dist = (pieceIdx - h).abs + 2
                            next.gscore = next.gscore + dist * Cost[piece]
                            Fiber.yield(next)
                        } else if (isTopReceptive(piece)) {
                            var next = this.clone()
                            next.hall[pieceIdx] = Empty
                            next.top[piece] = piece
                            var dist = (pieceIdx - h).abs + 1
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

var findCost = Fn.new {
    var queue = PriorityQueue.new()
    var state = State.initial()
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

System.print(findCost.call())
