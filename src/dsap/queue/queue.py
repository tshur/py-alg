from typing import Iterable, Iterator, Optional, Self

from .deque import Deque


class Queue[T]:
    _queue: Deque[T]

    def __init__(self):
        self._queue = Deque()

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Build a new queue to contain the elements from the given iterable.

        Elements will be inserted from the iterable by repeatedly calling enqueue for
        each value in order. Therefore, the first value of the iterable will become the
        front of the queue, and the last value will become the back of the queue.

        Args:
            iterable (Iterable[T]): The values to insert into a new queue.

        Returns:
            Self: The newly constructed queue.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> print(queue)
            [1, 2, 3]
        """
        queue = cls()
        for value in iterable:
            queue.enqueue(value)
        return queue

    def enqueue(self, value: T) -> None:
        """Append a value at the end of the queue.

        After inserting the element, the element will now be the last element in the
        queue, aka, the back.

        Args:
            value (T): The value to be added.

        Examples:
            >>> queue = Queue()
            >>> queue.enqueue(1)
            >>> queue.enqueue(2)
            >>> queue.enqueue(3)
            >>> print(queue)
            [1, 2, 3]
        """
        self._queue.push_back(value)

    def dequeue(self) -> Optional[T]:
        """Removes and returns the first element of the queue (the front).

        Returns:
            Optional[T]: The removed element at the front of the queue. If the queue is
              empty, returns None.

        Examples:
            >>> queue = Queue.from_iterable([1, 2])
            >>> queue.dequeue()
            1
            >>> queue.dequeue()
            2
            >>> queue.dequeue()
        """
        return self._queue.pop_front()

    def peek(self) -> Optional[T]:
        """Get the first element of the queue (the front, or leftmost element).

        Returns:
            Optional[T]: The first element of the queue. If the queue is empty, returns
              None.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> queue.peek()
            1
        """
        return self._queue.front()

    def is_empty(self) -> bool:
        """Returns true if the queue is empty (has no elements).

        Returns:
            bool: Whether or not the queue is empty.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> queue.is_empty()
            False
            >>> empty_queue = Queue()
            >>> empty_queue.is_empty()
            True
        """
        return self._queue.is_empty()

    def __iter__(self) -> Iterator[T]:
        """Returns a generator of values from the queue (in remove / FIFO order).

        The queue remains unchanged from this method.

        Yields:
            Iterator[T]: Values from the queue.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> list(queue)
            [1, 2, 3]
        """
        return iter(self._queue)

    def __contains__(self, value: T) -> bool:
        """Whether a value is present in the queue.

        Must iterate over the queue, so operates in O(n) time.

        Args:
            value (T): The value to search for in the queue.

        Returns:
            bool: If the value is present in the queue.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> 2 in queue
            True
            >>> 5 in queue
            False
        """
        return value in self._queue

    def __len__(self) -> int:
        """Returns the number of elements in the queue.

        Returns:
            int: How many elements are present in the queue.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> len(queue)
            3
        """
        return len(self._queue)

    def __str__(self) -> str:
        """Return displayable string of elements in the queue.

        The front is on the left, and the back is to the right.

        Returns:
            str: A printable string representation of the elements in the queue.

        Examples:
            >>> queue = Queue.from_iterable([1, 2, 3])
            >>> str(queue)
            '[1, 2, 3]'
        """
        return str(self._queue)
