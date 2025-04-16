from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional, Self


class SinglyLinkedList[T]:
    """Singly linked list data structure with head and tail pointer.

    Basic operations:
      - SinglyLinkedList.from_iterable, O(n) (static method)
      - push_head, O(1)
      - push_tail, O(1)
      - remove_head, O(1)
      - remove_tail, O(n) due to singly-linked list
      - __contains__, O(n)
      - __len__, O(1) (pre-computed)
      - __str__, O(n)
    """

    @dataclass
    class _Node[U]:
        data: U
        next: Optional[SinglyLinkedList._Node[U]] = None

    _head: Optional[_Node[T]]
    _tail: Optional[_Node[T]]
    _size: int

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Builds a SinglyLinkedList given an Iterable of values.

        Args:
            iterable (Iterable[T]): Values to insert into a linked list.

        Returns:
            Self: The built linked list from the iterable. Values will be added
              such that linked_list.head.data == iterable[0], and len(linked_list) ==
              len(iterable).


        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> print(linked_list)
            1->2->3->None
        """
        linked_list = cls()
        for value in iterable:
            linked_list.push_tail(value)
        return linked_list

    def push_head(self, value: T) -> None:
        """Insert a new Node(value) into the front/head of the linked list.

        Args:
            value (T): The value to be inserted.

        Examples:
            >>> linked_list = SinglyLinkedList()
            >>> linked_list.push_head(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_head(2)
            >>> print(linked_list)
            2->1->None
        """
        node = SinglyLinkedList._Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head = node
        self._size += 1

    def push_tail(self, value: T) -> None:
        """Insert a new Node(value) into the back/tail of the linked list.

        Args:
            value (T): The value to be inserted.

        Examples:
            >>> linked_list = SinglyLinkedList()
            >>> linked_list.push_tail(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_tail(2)
            >>> print(linked_list)
            1->2->None
        """
        node = SinglyLinkedList._Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def remove_head(self) -> None:
        """Remove a node from the front/head of the linked list (if one exists).

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_head()
            >>> print(linked_list)
            2->3->None
        """
        if self._head is None:
            return
        if self._head == self._tail:
            self._head = self._tail = None
            self._size -= 1
            return
        self._head = self._head.next
        self._size -= 1

    def remove_tail(self) -> None:
        """Remove a node from the back/tail of the linked list (if one exists).

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_tail()
            >>> print(linked_list)
            1->2->None
        """
        if self._head is None:
            return
        if self._head == self._tail:
            self._head = self._tail = None
            self._size -= 1
            return

        current: Optional[SinglyLinkedList._Node[T]] = self._head
        while current and current.next != self._tail:
            current = current.next

        if current is not None:
            current.next = None
        self._tail = current
        self._size -= 1

    def __contains__(self, value: T) -> bool:
        """Check if the SinglyLinkedList contains a node with given value.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value is found. Otherwise, returns False.

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> 2 in linked_list
            True
            >>> 4 in linked_list
            False
        """
        return value in iter(self)

    def __len__(self) -> int:
        """Returns the number of nodes in the SinglyLinkedList (in O(1) time).

        Returns:
            int: The number of nodes.

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> len(linked_list)
            3
        """
        return self._size

    def __str__(self) -> str:
        """Returns a printable string containing all nodes in one line.

        Returns:
            str: A visual representation of the linked list.

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 3])
            >>> str(linked_list)
            '1->2->3->None'
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

    def node_iterator(self) -> Iterator[_Node[T]]:
        """Iterator that yields Nodes in order from the head to the tail.

        Yields:
            Iterator[_Node[T]]: Nodes in the linked list.
        """
        current = self._head
        while current:
            yield current
            current = current.next

    def pairwise_iterator(self) -> Iterator[tuple[Optional[_Node[T]], _Node[T]]]:
        """Iterator that yields (previous, current) pairs in the linked list.

        The return values will be such that previous starts at None and current starts
        at self._head. The pair of returned nodes will remain in lock-step, a single
        node index apart.

        Yields:
            Iterator[tuple[Optional[_Node[T]], _Node[T]]: (previous, current) pairs of
              nodes in the linked list.
        """
        previous = None
        current = self._head
        while current:
            yield previous, current
            previous, current = current, current.next
