from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Self


@dataclass
class _Node[T]:
    data: T
    prev: Optional[_Node[T]] = None
    next: Optional[_Node[T]] = None


class DoublyLinkedList[T]:
    """Doubly linked list data structure with head and tail pointer.

    Basic operations:
      - DoublyLinkedList.from_iterable, O(n) (static method)
      - push_head, O(1)
      - push_tail, O(1)
      - remove_head, O(1)
      - remove_tail, O(1)
      - __contains__, O(n)
      - __len__, O(1) (pre-computed)
      - __str__, O(n)
    """

    _head: Optional[_Node[T]]
    _tail: Optional[_Node[T]]
    _size: int

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Builds a DoublyLinkedList given an Iterable of values.

        Args:
            iterable (Iterable[T]): Values to insert into a linked list.

        Returns:
            Self: The built linked list from the iterable. Values will be added
              such that linked_list.head.data == iterable[0], and len(linked_list) ==
              len(iterable).


        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
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
            >>> linked_list = DoublyLinkedList()
            >>> linked_list.push_head(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_head(2)
            >>> print(linked_list)
            2->1->None
        """
        node = _Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def push_tail(self, value: T) -> None:
        """Insert a new Node(value) into the back/tail of the linked list.

        Args:
            value (T): The value to be inserted.

        Examples:
            >>> linked_list = DoublyLinkedList()
            >>> linked_list.push_tail(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_tail(2)
            >>> print(linked_list)
            1->2->None
        """
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def remove_head(self) -> None:
        """Remove a node from the front/head of the linked list (if one exists).

        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
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
        if self._head is not None:
            self._head.prev = None
        self._size -= 1

    def remove_tail(self) -> None:
        """Remove a node from the back/tail of the linked list (if one exists).

        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_tail()
            >>> print(linked_list)
            1->2->None
        """
        if self._tail is None:
            return
        if self._head == self._tail:
            self._head = self._tail = None
            self._size -= 1
            return

        self._tail = self._tail.prev
        if self._tail is not None:
            self._tail.next = None
        self._size -= 1

    def __contains__(self, value: T) -> bool:
        """Check if the DoublyLinkedList contains a node with given value.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value is found. Otherwise, returns False.

        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
            >>> 2 in linked_list
            True
            >>> 4 in linked_list
            False
        """
        current = self._head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def __len__(self) -> int:
        """Returns the number of nodes in the DoublyLinkedList (in O(1) time).

        Returns:
            int: The number of nodes.

        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
            >>> len(linked_list)
            3
        """
        return self._size

    def __str__(self) -> str:
        """Returns a printable string containing all nodes in one line.

        Returns:
            str: A visual representation of the linked list.

        Examples:
            >>> linked_list = DoublyLinkedList.from_iterable([1, 2, 3])
            >>> str(linked_list)
            '1->2->3->None'
        """
        nodes: list[str] = []

        current = self._head
        while current:
            nodes.append(str(current.data))
            current = current.next
        nodes.append("None")

        return "->".join(nodes)
