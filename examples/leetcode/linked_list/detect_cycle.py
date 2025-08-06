from dsap.hash import Set
from dsap.iterable import skip
from dsap.linked_list import SinglyLinkedList


class DetectCycle(SinglyLinkedList[int]):
    def create_cycle(self, index: int):
        if index >= len(self) or not self._tail:
            raise IndexError("index out of bounds")

        iterator = skip(self.node_iterator(), index)
        self._tail.next = next(iterator)

    def hash_set(self) -> bool:
        seen = Set[SinglyLinkedList._Node[int]]()
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
