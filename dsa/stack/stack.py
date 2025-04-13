from typing import Iterable, Optional


class Stack[T]:
    _buffer: list[T]
    _size: int

    def __init__(self):
        self._buffer = []
        self._size = 0

    @classmethod
    def from_iterable[U](cls, iterable: Iterable[U]) -> "Stack[U]":
        stack: Stack[U] = Stack()
        for value in iterable:
            stack.push(value)
        return stack

    def push(self, value: T) -> None:
        self._buffer.append(value)
        self._size += 1

    def pop(self) -> Optional[T]:
        if len(self) == 0:
            return None
        self._size -= 1
        return self._buffer.pop()

    def peek(self) -> Optional[T]:
        if len(self) == 0:
            return None
        return self._buffer[-1]

    def __contains__(self, value: T) -> bool:
        return value in self._buffer

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self._buffer)
