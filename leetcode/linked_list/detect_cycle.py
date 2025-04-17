from dsa.linked_list import SinglyLinkedList


class DetectCycle(SinglyLinkedList[int]):
    def create_cycle(self, index: int):
        if index >= len(self) or not self._tail:
            raise IndexError("index out of bounds")

        # TODO: Replace this with a skip(iterator, n) algorithm.
        iterator = self.node_iterator()
        for _ in range(index):
            next(iterator)
        self._tail.next = next(iterator)

    def hash_set(self) -> bool:
        seen = set[SinglyLinkedList._Node[int]]()
        for node in self.node_iterator():
            if node in seen:
                return True
            seen.add(node)
        return False

    def fast_slow(self) -> bool:
        fast_iterator = self.node_iterator()
        slow_iterator = self.node_iterator()
        while True:
            try:
                next(fast_iterator)
                fast = next(fast_iterator)
                slow = next(slow_iterator)
            except StopIteration:
                return False

            if fast == slow:
                return True
