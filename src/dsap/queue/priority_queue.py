from typing import Iterable, Iterator, Optional, Self

from dsap.heap import MaxHeap
from dsap.type import SupportsRichComparison

from .queue import Queue


class PriorityQueue[CT: SupportsRichComparison](Queue[CT]):
    """Queue elements with the highest priority in front (basically a MaxHeap)."""

    _priority_queue: MaxHeap[CT]

    def __init__(self):
        self._priority_queue = MaxHeap()

    @classmethod
    def from_iterable(cls, iterable: Iterable[CT]) -> Self:
        """Build a new priority queue to contain the elements from the given iterable.

        Elements will be inserted from the iterable by repeatedly calling enqueue for
        each value in order. Elements are inserted according to their comparison
        ordering, such that the largest item (i.e., highest priority) is always first.

        Args:
            iterable (Iterable[CT]): The values to insert into a new priority queue.

        Returns:
            Self: The newly constructed priority queue.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> print(priority_queue)
            [3, 2, 1]
        """
        priority_queue = cls()
        priority_queue._priority_queue = MaxHeap[CT].from_iterable(iterable)
        return priority_queue

    def enqueue(self, value: CT) -> None:
        """Insert a value into the queue (in priority order).

        After inserting the element, the priority queue will maintain sorted ordering,
        such that the highest priority item is always at the front.

        Args:
            value (CT): The value to be added.

        Examples:
            >>> priority_queue = PriorityQueue()
            >>> priority_queue.enqueue(1)
            >>> priority_queue.enqueue(3)
            >>> priority_queue.enqueue(2)
            >>> print(priority_queue)
            [3, 2, 1]
        """
        self._priority_queue.push(value)

    def dequeue(self) -> Optional[CT]:
        """Removes and returns the highest priority element of the queue (the front).

        Returns:
            Optional[CT]: The removed element at the front of the priority queue. If the
              queue is empty, returns None.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> priority_queue.dequeue()
            3
            >>> priority_queue.dequeue()
            2
            >>> priority_queue.dequeue()
            1
            >>> priority_queue.dequeue()
        """
        return self._priority_queue.pop()

    def peek(self) -> Optional[CT]:
        """Get the first element of the queue (the front, or leftmost element).

        Returns:
            Optional[CT]: The first element of the queue. If the queue is empty, returns
              None.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> priority_queue.peek()
            3
        """
        return self._priority_queue.peek()

    def is_empty(self) -> bool:
        """Returns true if the priority queue is empty (has no elements).

        Returns:
            bool: Whether or not the priority queue is empty.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> priority_queue.is_empty()
            False
            >>> empty_priority_queue = PriorityQueue()
            >>> empty_priority_queue.is_empty()
            True
        """
        return self._priority_queue.is_empty()

    def __iter__(self) -> Iterator[CT]:
        """Returns a generator of values from the priority queue (in priority order).

        The priority queue remains unchanged from this method. Uses O(n) auxiliary space
        to store the ordered heap elements for iteration.

        Yields:
            Iterator[CT]: Values from the priority queue.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> list(priority_queue)
            [3, 2, 1]
        """
        # Must consume and rebuild to get ordering (or sort internal data).
        items = list(self._priority_queue.consume_all())
        self._priority_queue = MaxHeap[CT].from_iterable(items)
        return iter(items)

    def __contains__(self, value: CT) -> bool:
        """Whether a value is present in the priority queue.

        Must iterate over the priority queue, so operates in O(n) time (non-ordered).

        Args:
            value (CT): The value to search for in the priority queue.

        Returns:
            bool: If the value is present in the priority queue.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> 2 in priority_queue
            True
            >>> 5 in priority_queue
            False
        """
        return value in self._priority_queue

    def __len__(self) -> int:
        """Returns the number of elements in the priority queue.

        Returns:
            int: How many elements are present in the priority queue.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> len(priority_queue)
            3
        """
        return len(self._priority_queue)

    def __str__(self) -> str:
        """Return displayable string of elements in the priority queue.

        The front (highest priority) is on the left, and the back (lowest priority) is
        to the right.

        Returns:
            str: A printable representation of the elements in the priority queue.

        Examples:
            >>> priority_queue = PriorityQueue.from_iterable([1, 3, 2])
            >>> str(priority_queue)
            '[3, 2, 1]'
        """
        return str(list(self))
