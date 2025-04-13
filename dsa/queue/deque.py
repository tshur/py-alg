from typing import Iterable, Optional

from dsa.iterable import rotate


class Deque[T]:
    """Doubly-ended queue supporting fast push/pop from both ends.

    Implementation uses a circular / ring buffer for space and memory. Other
    implementations exist, such as using a doubly-linked list of block arrays (such as
    used for collections.deque).

    The deque has a fixed capacity, which is increased (doubled) when the capacity is
    exceeded. The doubling requires copying to a new (larger) container, but leads to
    amortized time complexity.

    Common operations:
      - push_front, amortized O(1)
      - push_back, amortized O(1)
      - pop_front, O(1)
      - pop_back, O(1)
      - front, O(1)
      - back, O(1)
      - is_empty, O(1)
    """

    _ring_buffer: list[Optional[T]]
    _start: int  # Index representing the head / start of the ring buffer.
    _size: int

    def __init__(self, *, capacity: int = 16):
        self._ring_buffer = [None] * capacity
        self._start = 0
        self._size = 0

    @classmethod
    def from_iterable[U](cls, iterable: Iterable[U]) -> "Deque[U]":
        deque: Deque[U] = Deque()
        for value in iterable:
            deque.push_back(value)
        return deque

    def push_front(self, value: T) -> None:
        if self._size >= self.capacity():
            self._grow()
        self._start = self._index(-1)
        self._ring_buffer[self._start] = value
        self._size += 1

    def push_back(self, value: T) -> None:
        if self._size >= self.capacity():
            self._grow()
        self._ring_buffer[self._index(self._size)] = value
        self._size += 1

    def pop_front(self) -> Optional[T]:
        if len(self) == 0:
            return None
        value = self._ring_buffer[self._start]
        self._start = self._index(1)
        self._size -= 1
        return value

    def pop_back(self) -> Optional[T]:
        if len(self) == 0:
            return None
        self._size -= 1
        value = self._ring_buffer[self._index(self._size)]
        return value

    def front(self) -> Optional[T]:
        if len(self) == 0:
            return None
        return self._ring_buffer[self._start]

    def back(self) -> Optional[T]:
        if len(self) == 0:
            return None
        return self._ring_buffer[self._index(self._size - 1)]

    def is_empty(self) -> bool:
        return self._size == 0

    def _index(self, offset: int) -> int:
        return (self._start + offset) % self.capacity()

    def _normalize(self) -> None:
        rotate(self._ring_buffer, -self._start)

    def _grow(self) -> None:
        self._normalize()
        self._ring_buffer = self._ring_buffer + [None] * self.capacity()

    def capacity(self) -> int:
        return len(self._ring_buffer)

    def __contains__(self, value: T) -> bool:
        for i in range(self._size):
            if self._ring_buffer[self._index(i)] == value:
                return True
        return False

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        elements = [self._ring_buffer[self._index(i)] for i in range(self._size)]
        return str(elements)
