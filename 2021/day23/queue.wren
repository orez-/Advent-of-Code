// Based on Python's heapq module.
// https://github.com/python/cpython/blob/main/Lib/heapq.py
class PriorityQueue is Sequence {
    static cmp_(e1, e2) { e1[1] <= e2[1] }
    construct new() { _heap = [] }

    push(value, priority) {
        _heap.add([value, priority])
        siftDown_(0, _heap.count - 1)
    }

    pop() {
        var lastElem = _heap.removeAt(-1)
        if (!_heap.isEmpty) {
            var returnItem = _heap[0]
            _heap[0] = lastElem
            siftUp_(0)
            return returnItem
        }
        return lastElem
    }

    siftDown_(startpos, pos) {
        var newitem = _heap[pos]
        while (pos > startpos) {
            var parentpos = (pos - 1) >> 1
            var parent = _heap[parentpos]
            if (PriorityQueue.cmp_(newitem, parent)) {
                _heap[pos] = parent
                pos = parentpos
                continue
            }
            break
        }
        _heap[pos] = newitem
    }

    siftUp_(pos) {
        var endpos = _heap.count
        var startpos = pos
        var newitem = _heap[pos]
        // Bubble up the smaller child until hitting a leaf.
        var childpos = 2*pos + 1    // leftmost child position
        while (childpos < endpos) {
            // Set childpos to index of smaller child.
            var rightpos = childpos + 1
            if (rightpos < endpos && !PriorityQueue.cmp_(_heap[childpos], _heap[rightpos])) {
                childpos = rightpos
            }
            // Move the smaller child up.
            _heap[pos] = _heap[childpos]
            pos = childpos
            childpos = 2*pos + 1
        }
        // The leaf at pos is empty now. Put newitem there, and bubble it up
        // to its final resting place (by sifting its parents down).
        _heap[pos] = newitem
        siftDown_(startpos, pos)
    }
}
