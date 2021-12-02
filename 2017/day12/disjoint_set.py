class DisjointSet(object):
    def __init__(self):
        self._all_nodes = dict()
        self._representative_nodes = set()

    def add(self, value):
        if value in self._all_nodes:
            return False
        node = _Node(value)
        self._all_nodes[value] = node
        self._representative_nodes.add(node)
        return True

    def _get_or_add(self, value):
        self.add(value)
        return self._all_nodes[value]

    def union(self, value1, value2):
        # https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Union_by_rank
        node1 = self._get_or_add(value1).find_root()
        node2 = self._get_or_add(value2).find_root()
        if node1 is node2:
            return

        if node1.rank < node2.rank:
            node1.parent = node2
            self._representative_nodes.remove(node1)
        elif node1.rank > node2.rank:
            node2.parent = node1
            self._representative_nodes.remove(node2)
        else:
            node2.parent = node1
            node1.rank += 1
            self._representative_nodes.remove(node2)

    def find_group(self, value):
        if value not in self._all_nodes:
            raise KeyError(value)
        return iter(self._all_nodes[value].find_root())

    def __len__(self):
        return len(self._representative_nodes)

    def __iter__(self):
        return (iter(node) for node in self._representative_nodes)

    def __repr__(self):
        return 'DisjointSet({})'.format(', '.join(repr(set(st)) for st in self))


class _Node(object):
    def __init__(self, value):
        self.rank = 0
        self.value = value
        self._parent = self
        self.children = set()

    def find_root(self):
        # https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Path_compression
        if self.parent is not self:
            self.parent.children.discard(self)
            self.parent = self.parent.find_root()
        return self.parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        assert self not in self.parent.children
        assert self is not node
        node.children.add(self)
        self._parent = node

    def __iter__(self):
        yield self.value
        for child in self.children:
            yield from child
