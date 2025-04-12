from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node[T]:
    data: T
    next: Optional["Node[T]"] = None


class LinkedList[T]:
    """Singly linked list data structure with head and tail pointer.

    Basic operations:
      - LinkedList.from_iterable, O(n) (static method)
      - push_front, O(1)
      - push_back, O(1)
      - remove_front, O(1)
      - remove_back, O(n)
      - __contains__, O(n)
      - __len__, O(n) (computed)
      - __str__, O(n)
    """

    head: Optional[Node[T]]
    tail: Optional[Node[T]]

    def __init__(self):
        self.head = None
        self.tail = None

    @staticmethod
    def from_iterable[U](iterable: Iterable[U]) -> "LinkedList[U]":
        """Builds a LinkedList given an Iterable of values.

        Args:
            iterable (Iterable[U]): Values to insert into a linked list.

        Returns:
            LinkedList[U]: The built linked list from the iterable. Values will be added
              such that linked_list.head.data == iterable[0], and len(linked_list) ==
              len(iterable).


        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> print(linked_list)
            1->2->3->None
        """
        ll: LinkedList[U] = LinkedList()
        for value in iterable:
            ll.push_back(value)
        return ll

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
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node

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
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def remove_front(self) -> None:
        """Remove a node from the front/head of the linked list (if one exists).

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> linked_list.remove_front()
            >>> print(linked_list)
            2->3->None
        """
        if self.head is None:
            return
        self.head = self.head.next

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
        if self.head is None:
            return
        if self.head == self.tail:
            self.head = self.tail = None
            return

        current: Optional[Node[T]] = self.head
        while current and current.next != self.tail:
            current = current.next

        if current is not None:
            current.next = None
        self.tail = current

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
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def __len__(self) -> int:
        """Returns the number of nodes in the LinkedList (in O(n) time).

        Returns:
            int: The number of nodes.

        Examples:
            >>> linked_list = LinkedList.from_iterable([1, 2, 3])
            >>> len(linked_list)
            3
        """
        size = 0
        current = self.head
        while current:
            size += 1
            current = current.next
        return size

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

        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        nodes.append("None")

        return "->".join(nodes)
