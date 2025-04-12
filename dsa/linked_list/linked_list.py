from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node[T]:
    data: T
    next: Optional["Node[T]"]


class LinkedList[T]:
    head: Optional[Node[T]]
    tail: Optional[Node[T]]

    def __init__(self):
        self.head = None
        self.tail = None

    @staticmethod
    def from_iterable[U](iterable: Iterable[U]) -> "LinkedList[U]":
        ll: LinkedList[U] = LinkedList()
        for value in iterable:
            ll.push_back(value)
        return ll

    def push_front(self, value: T) -> None:
        raise NotImplementedError

    def push_back(self, value: T) -> None:
        raise NotImplementedError

    def remove_front(self) -> None:
        raise NotImplementedError

    def remove_back(self) -> None:
        raise NotImplementedError

    def __contains__(self, value: T) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
