from typing import Iterable, Iterator, Optional, Self

from dsa.typing.comparison import Comparable


class Heap[CT: Comparable]:
    _heap: list[CT]

    class _Node[T]:
        index: int
        value: T

        def __init__(self, index: int, value: T):
            self.index = index
            self.value = value

    def __init__(self):
        self._heap = []

    @classmethod
    def from_iterable(cls, iterable: Iterable[CT]) -> Self:
        heap = cls()
        heap._heap = list(iterable)
        heap._heapify()
        return heap

    def push(self, value: CT) -> None:
        self._heap.append(value)
        self._sift_up(len(self) - 1)

    def pop(self) -> Optional[CT]:
        if self.is_empty():
            return None
        if len(self) == 1:
            return self._heap.pop()

        removed = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return removed

    def peek(self) -> Optional[CT]:
        if self.is_empty():
            return None
        return self._heap[0]

    def is_empty(self) -> bool:
        return len(self) == 0

    def consume_all(self) -> Iterator[CT]:
        while True:
            value = self.pop()
            if value is None:
                break
            yield value

    def __len__(self) -> int:
        return len(self._heap)

    def _parent(self, index: int) -> Optional[_Node[CT]]:
        parent_index = (index - 1) // 2
        if parent_index < 0:
            return None
        return Heap._Node(parent_index, self._heap[parent_index])

    def _left_child(self, index: int) -> Optional[_Node[CT]]:
        child_index = index * 2 + 1
        if child_index >= len(self):
            return None
        return Heap._Node(child_index, self._heap[child_index])

    def _right_child(self, index: int) -> Optional[_Node[CT]]:
        child_index = index * 2 + 2
        if child_index >= len(self):
            return None
        return Heap._Node(child_index, self._heap[child_index])

    def _smaller_child(self, index: int) -> Optional[_Node[CT]]:
        left, right = self._left_child(index), self._right_child(index)
        if not left or not right:
            return left

        if left.value < right.value:
            return left
        return right

    def _sift_up(self, index: int) -> None:
        while index >= 0:
            current = self._heap[index]
            parent = self._parent(index)
            if not parent or parent.value < current:
                return  # Satisfies heap ordering.

            self._heap[parent.index], self._heap[index] = current, parent.value
            index = parent.index

    def _sift_down(self, index: int) -> None:
        while index < len(self):
            current = self._heap[index]
            child = self._smaller_child(index)
            if not child or current < child.value:
                return  # Satisfies heap ordering.

            self._heap[index], self._heap[child.index] = child.value, current
            index = child.index

    def _heapify(self) -> None:
        for i in range(len(self) - 1, -1, -1):
            self._sift_down(i)
