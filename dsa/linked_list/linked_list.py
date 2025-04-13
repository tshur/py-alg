from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class _Node[T]:
    data: T
    next: Optional["_Node[T]"] = None


class LinkedList[T]:
    """Singly linked list data structure with head and tail pointer.

    Basic operations:
      - LinkedList.from_iterable, O(n) (static method)
      - push_front, O(1)
      - push_back, O(1)
      - remove_front, O(1)
      - remove_back, O(n)
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
    def from_iterable(cls, iterable: Iterable[T]) -> "LinkedList[T]":
        """Builds a LinkedList given an Iterable of values.

        Args:
            iterable (Iterable[T]): Values to insert into a linked list.

        Returns:
            LinkedList[T]: The built linked list from the iterable. Values will be added
              such that linked_list.head.data == iterable[0], and len(linked_list) ==
              len(iterable).


        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> print(linked_list)
            1->2->3->None
        """
        linked_list = cls()
        for value in iterable:
            linked_list.push_back(value)
        return linked_list

    def push_front(self, value: T) -> None:
        """Insert a new Node(value) into the front/head of the linked list.

        Args:
            value (T): The value to be inserted.

        Examples:
            >>> linked_list = LinkedList()
            >>> linked_list.push_front(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_front(2)
            >>> print(linked_list)
            2->1->None
        """
        node = _Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head = node
        self._size += 1

    def push_back(self, value: T) -> None:
        """Insert a new Node(value) into the back/tail of the linked list.

        Args:
            value (T): The value to be inserted.

        Examples:
            >>> linked_list = LinkedList()
            >>> linked_list.push_back(1)
            >>> print(linked_list)
            1->None
            >>> linked_list.push_back(2)
            >>> print(linked_list)
            1->2->None
        """
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def remove_front(self) -> None:
        """Remove a node from the front/head of the linked list (if one exists).

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_front()
            >>> print(linked_list)
            2->3->None
        """
        if self._head is None:
            return
        self._head = self._head.next
        self._size -= 1

    def remove_back(self) -> None:
        """Remove a node from the back/tail of the linked list (if one exists).

        Raises:
            ValueError: If self.tail does not exist in the linked list. This is an
              invariant, so should not happen unless private variables are manipulated
              outside the object methods.

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_back()
            >>> print(linked_list)
            1->2->None
        """
        if self._head is None:
            return
        if self._head == self._tail:
            self._head = self._tail = None
            self._size -= 1
            return

        current: Optional[_Node[T]] = self._head
        while current and current.next != self._tail:
            current = current.next

        if current is not None:
            current.next = None
        self._tail = current
        self._size -= 1

    def __contains__(self, value: T) -> bool:
        """Check if the LinkedList contains a node with given value.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value is found. Otherwise, returns False.

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
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
        """Returns the number of nodes in the LinkedList (in O(1) time).

        Returns:
            int: The number of nodes.

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> len(linked_list)
            3
        """
        return self._size

    def __str__(self) -> str:
        """Returns a printable string containing all nodes in one line.

        Returns:
            str: A visual representation of the linked list.

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
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
