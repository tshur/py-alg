from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Optional, Self


class NodeBase[T]:
    data: T


class LinkedListBase[T](ABC):
    _size: int

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Builds a LinkedList given an Iterable of values.

        Args:
            iterable (Iterable[T]): Values to insert into a linked list.

        Returns:
            Self: The built linked list from the iterable. Values will be added
              such that linked_list.head.data == iterable[0], and len(linked_list) ==
              len(iterable).
        """
        linked_list = cls()
        for value in iterable:
            linked_list.push_tail(value)
        return linked_list

    @abstractmethod
    def push_head(self, value: T) -> None: ...

    @abstractmethod
    def push_tail(self, value: T) -> None: ...

    @abstractmethod
    def remove_head(self) -> None: ...

    @abstractmethod
    def remove_tail(self) -> None: ...

    def __contains__(self, value: T) -> bool:
        """Check if the LinkedList contains a node with given value.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value is found. Otherwise, returns False.
        """
        return value in iter(self)

    def __len__(self) -> int:
        """Returns the number of nodes in the DoublyLinkedList (in O(1) time).

        Returns:
            int: The number of nodes.
        """
        return self._size

    def __str__(self) -> str:
        """Returns a printable string containing all nodes in one line.

        Returns:
            str: A visual representation of the linked list.
        """
        nodes = [str(value) for value in self]
        nodes.append("None")

        return "->".join(nodes)

    def __iter__(self) -> Iterator[T]:
        """Iterator that yields values in order from the head to the tail.

        Yields:
            Iterator[T]: Values of nodes in the linked list.
        """
        for node in self.node_iterator():
            yield node.data

    @abstractmethod
    def node_iterator(self) -> Iterator[NodeBase[T]]: ...

    @abstractmethod
    def pairwise_iterator(
        self,
    ) -> Iterator[tuple[Optional[NodeBase[T]], NodeBase[T]]]: ...
