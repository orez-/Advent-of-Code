import kotlin.math.*

val WIDTH = 10
val HEIGHT = 10

data class Octos(var board: ArrayList<Int>) {
    fun step(): Int {
        var total = 0
        var queue: ArrayDeque<Int> = ArrayDeque()
        queue.addAll((0..99).toList())
        while (!queue.isEmpty()) {
            val idx = queue.removeFirst()
            board[idx] += 1
            if (board[idx] == 10) {
                total += 1
                queue.addAll(surrounding(idx))
            }
        }
        for (idx in board.indices) {
            if (board[idx] > 9) board[idx] = 0
        }
        return total
    }

    fun fullFlash() = board.all { it == 0 }
}

fun surrounding(idx: Int) = sequence {
    val x = idx % WIDTH
    val y = idx / WIDTH
    val left = max(x-1, 0)
    val top = max(y-1, 0)
    val right = min(x+1, 9)
    val bottom = min(y+1, 9)
    for (nx in left..right) {
        for (ny in top..bottom) {
            if (!(nx == x && ny == y)) {
                yield(ny * WIDTH + nx)
            }
        }
    }
}

fun readBoard(): Octos {
    var board: ArrayList<Int> = ArrayList()
    var line: String?
    do {
        line = readLine()
        if (line != null) board.addAll(line.map(Character::getNumericValue))
    } while (line != null)
    return Octos(board)
}

fun part1() {
    var board = readBoard()
    var total = 0
    for (i in 1..100) {
        total += board.step()
    }
    println(total)
}

fun part2() {
    var board = readBoard()
    var total = 0
    while (!board.fullFlash()) {
        board.step()
        total += 1
    }
    println(total)
}

fun main(args: Array<String>) {
    when (args[0]) {
        "part1" -> part1()
        "part2" -> part2()
        else -> println("Please specify 'part1' or 'part2', not '${args[0]}'")
    }
}
