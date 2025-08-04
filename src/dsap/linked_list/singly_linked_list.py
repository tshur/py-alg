from __future__ import annotations

from typing import Iterator, Optional

from .linked_list import LinkedListBase


class SinglyLinkedList[T](LinkedListBase[T]):
    """Singly linked list data structure with head and tail pointer.

    Basic operations:
      - SinglyLinkedList.from_iterable, O(n) (static method)
      - push_head, O(1)
      - push_tail, O(1)
      - remove_head, O(1)
      - remove_tail, O(n) due to singly-linked list
      - remove, O(n)
      - __contains__, O(n)
      - __len__, O(1) (pre-computed)
      - __str__, O(n)
    """

    class _Node[U](LinkedListBase.NodeBase[U]):
        data: U
        next: Optional[SinglyLinkedList._Node[U]] = None

        def __init__(self, data: U):
            self.data = data

    _head: Optional[_Node[T]]
    _tail: Optional[_Node[T]]
    _size: int

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

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

        for previous, current in self.pairwise_iterator():
            if current == self._tail:
                if previous is not None:
                    previous.next = None
                self._tail = previous
                self._size -= 1
                return

    def remove(self, value: T) -> None:
        """Remove the first occurrence of a node with value in the linked list.

        If no node matches the given value, then the linked list will be unchanged.

        Args:
            value (T): The value to search for in the linked list. If a node contains
              data equal to this value, the first such node will be removed.

        Examples:
            >>> linked_list = SinglyLinkedList.from_iterable([1, 2, 1, 3])
            >>> linked_list.remove(1)
            >>> print(linked_list)
            2->1->3->None
        """
        for previous, current in self.pairwise_iterator():
            if current.data != value:
                continue

            if current == self._head:
                self.remove_head()
            elif current == self._tail:
                self.remove_tail()
            else:
                if previous:
                    previous.next = current.next
                self._size -= 1
            return

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
