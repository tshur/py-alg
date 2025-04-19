from typing import Iterable, Iterator, Optional, Self

from dsa.typing.comparison import Comparable


class Heap[CT: Comparable]:
    _heap: list[CT]

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

        value = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return value

    def peek(self) -> Optional[CT]:
        return self._heap[0] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return not self._heap

    def consume_all(self) -> Iterator[CT]:
        while (value := self.pop()) is not None:
            yield value

    def __len__(self) -> int:
        return len(self._heap)

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return i * 2 + 1

    def _right_child(self, i: int) -> int:
        return i * 2 + 2

    def _smaller_child(self, i: int) -> Optional[int]:
        left, right = self._left_child(i), self._right_child(i)
        if left >= len(self):
            return None
        elif right >= len(self):
            return left

        if self._heap[left] < self._heap[right]:
            return left
        return right

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = self._parent(i)
            if self._heap[parent] < self._heap[i]:
                return  # Satisfies heap ordering.

            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:
        while i < len(self):
            child = self._smaller_child(i)
            if not child or self._heap[i] < self._heap[child]:
                return  # Satisfies heap ordering.

            self._swap(i, child)
            i = child

    def _heapify(self) -> None:
        for i in range(len(self) - 1, -1, -1):
            self._sift_down(i)

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
