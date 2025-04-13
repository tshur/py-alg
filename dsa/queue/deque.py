from typing import Iterable, Optional


class Deque[T]:
    """Doubly-ended queue supporting fast push/pop from both ends.

    Implementation uses a circular / ring buffer for space and memory. Other
    implementations exist, such as using a doubly-linked list of block arrays (such as
    used for collections.deque).

    The deque has a fixed capacity, which is increased (doubled) when the capacity is
    exceeded. The doubling requires copying to a new (larger) container, but leads to
    amortized time complexity.

    Warning: Due to implementation details, the given T value type must not be None! If
    a value is pushed or inserted with a None type, an exception will be raised.

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
    _head: int  # Index representing the head / start of the ring buffer.
    _capacity: int

    def __init__(self, capacity: int = 16):
        self._ring_buffer = [None] * capacity
        self._head = 0
        self._capacity = capacity

    @classmethod
    def from_iterable[U](cls, iterable: Iterable[U]) -> "Deque[U]":
        raise NotImplementedError

    def push_front(self, value: T) -> None:
        raise NotImplementedError

    def push_back(self, value: T) -> None:
        raise NotImplementedError

    def pop_front(self) -> Optional[T]:
        raise NotImplementedError

    def pop_back(self) -> Optional[T]:
        raise NotImplementedError

    def front(self) -> Optional[T]:
        raise NotImplementedError

    def back(self) -> Optional[T]:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def capacity(self) -> int:
        raise NotImplementedError

    def __contains__(self, value: T) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
