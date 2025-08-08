from typing import Iterable, Iterator, Optional, Self

from dsap.iterable import rotate


class Deque[T]:
    """Doubly-ended queue supporting fast push/pop from both ends.

    Implementation uses a circular / ring buffer for space and memory. Other
    implementations exist, such as using a doubly-linked list of block arrays (such as
    used for collections.deque).

    The deque has a fixed capacity, which is increased (doubled) when the capacity is
    exceeded. The doubling requires copying to a new (larger) container, but leads to
    amortized time complexity.

    Common operations:
      - push_front, amortized O(1)
      - push_back, amortized O(1)
      - pop_front, O(1)
      - pop_back, O(1)
      - front, O(1)
      - back, O(1)
      - is_empty, O(1)
    """

    # A ring/circular buffer to internally store the contents of the deque. We use a
    # ring buffer for amortized O(1) push from both sides, and space efficiency. We
    # manage the ring buffer via a _start and _size. The _start may not be at index 0,
    # and the elements may wrap around the end of the ring buffer. To ensure consistent
    # data storage, we perform _normalize(), _grow(), and _index() operations to remap
    # indexing and grow the capacity without invalidating the data.
    _ring_buffer: list[Optional[T]]
    _start: int  # Index representing the head / start of the ring buffer.
    _size: int

    def __init__(self, *, capacity: int = 16):
        self._ring_buffer = [None] * capacity
        self._start = 0
        self._size = 0

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Build a new deque to contain the elements from the given iterable.

        Elements will be inserted from the iterable by repeatedly calling push_back for
        each value in order. Therefore, the first value of the iterable will become the
        front of the deque, and the last value will become the back of the deque.

        Args:
            iterable (Iterable[T]): The values to insert into a new deque.

        Returns:
            Self: The newly constructed deque.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> print(deque)
            [1, 2, 3]
        """
        deque = cls()
        for value in iterable:
            deque.push_back(value)
        return deque

    def push_front(self, value: T) -> None:
        """Append a value at the front of the deque.

        After inserting the element, the element will now be the first element in the
        deque, aka, the front.

        If the deque is at capacity (len(deque) == deque.capacity()), we normalize and
        grow the deque such that the capacity can hold the additional element.

        Implementation detail: Normalization will put the _start element at index 0 of
        the _ring_buffer. Growing the deque will double the capacity and copy elements
        over, such that push time complexity is amortized to O(1).

        Args:
            value (T): The value to be added.

        Examples:
            >>> deque = Deque()
            >>> deque.push_front(1)
            >>> deque.push_front(2)
            >>> deque.push_front(3)
            >>> print(deque)
            [3, 2, 1]
        """
        if self._size >= self.capacity():
            self._grow()
        self._start = self._index(-1)
        self._ring_buffer[self._start] = value
        self._size += 1

    def push_back(self, value: T) -> None:
        """Append a value at the end of the deque.

        After inserting the element, the element will now be the last element in the
        deque, aka, the back.

        If the deque is at capacity (len(deque) == deque.capacity()), we normalize and
        grow the deque such that the capacity can hold the additional element.

        Implementation detail: Normalization will put the _start element at index 0 of
        the _ring_buffer. Growing the deque will double the capacity and copy elements
        over, such that push time complexity is amortized to O(1).

        Args:
            value (T): The value to be added.

        Examples:
            >>> deque = Deque()
            >>> deque.push_back(1)
            >>> deque.push_back(2)
            >>> deque.push_back(3)
            >>> print(deque)
            [1, 2, 3]
        """
        if self._size >= self.capacity():
            self._grow()
        self._ring_buffer[self._index(self._size)] = value
        self._size += 1

    def pop_front(self) -> Optional[T]:
        """Removes and returns the first element of the deque (the front).

        Returns:
            Optional[T]: The removed element at the front of the deque. If the deque is
              empty, returns None.

        Examples:
            >>> deque = Deque.from_iterable([1, 2])
            >>> deque.pop_front()
            1
            >>> deque.pop_front()
            2
            >>> deque.pop_front()
        """
        if len(self) == 0:
            return None
        value = self._ring_buffer[self._start]
        self._ring_buffer[self._start] = None  # We don't *need* to erase the element.
        self._start = self._index(1)
        self._size -= 1
        return value

    def pop_back(self) -> Optional[T]:
        """Removes and returns the last element of the deque (the back).

        Implementation detail: the element is not actually removed or erased from the
        internal container. The start / size are simply updated to exclude it from the
        valid range.

        Returns:
            Optional[T]: The removed element at the end of the deque. If the deque is
              empty, returns None.

        Examples:
            >>> deque = Deque.from_iterable([1, 2])
            >>> deque.pop_back()
            2
            >>> deque.pop_back()
            1
            >>> deque.pop_back()
        """
        if len(self) == 0:
            return None
        self._size -= 1
        value = self._ring_buffer[self._index(self._size)]
        return value

    def front(self) -> Optional[T]:
        """Get the first element of the deque (the front, or leftmost element).

        Returns:
            Optional[T]: The first element of the deque. If the deque is empty, returns
              None.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> deque.front()
            1
        """
        if len(self) == 0:
            return None
        return self._ring_buffer[self._start]

    def back(self) -> Optional[T]:
        """Get the last element of the deque (the back, or rightmost element).

        Returns:
            Optional[T]: The last element of the deque. If the deque is empty, returns
              None.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> deque.back()
            3
        """
        if len(self) == 0:
            return None
        return self._ring_buffer[self._index(self._size - 1)]

    def is_empty(self) -> bool:
        """Returns true if the deque is empty (has no elements).

        Returns:
            bool: Whether or not the deque is empty.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> deque.is_empty()
            False
            >>> empty_deque = Deque()
            >>> empty_deque.is_empty()
            True
        """
        return self._size == 0

    def _index(self, offset: int) -> int:
        """Helper to convert a logical offset (nth element) into a ring buffer index.

        To get this index, we need to modulo the offset by the capacity, to handle cases
        where the offset wraps us beyond the end of the array.

        Args:
            offset (int): The logical offset of the target element. The offset
              corresponds to the "n-th" element (0-based). However, due to the rotating
              nature of the ring buffer, we need to re-map this to a real index.

        Returns:
            int: A re-mapped index that can be used to index the _ring_buffer. This
              index should get the logical element at the given offset.

        Examples:
            >>> deque = Deque(capacity=4)
            >>> deque.push_back(1)
            >>> deque.push_back(2)
            >>> deque.push_back(3)
            >>> deque.pop_front()
            1
            >>> deque._ring_buffer
            [None, 2, 3, None]
            >>> deque._index(0)
            1
        """
        return (self._start + offset) % self.capacity()

    def _normalize(self) -> None:
        """Helper to normalize the ring buffer (such that _start is index 0).

        We can perform normalization by simply rotating the _start index into place at
        index 0. This is important if we need to resize the ring buffer, without making
        it inconsistent.

        Examples:
            >>> deque = Deque(capacity=4)
            >>> deque.push_back(1)
            >>> deque.push_back(2)
            >>> deque.push_back(3)
            >>> deque.pop_front()
            1
            >>> deque._ring_buffer
            [None, 2, 3, None]
            >>> deque._normalize()
            >>> deque._ring_buffer
            [2, 3, None, None]
        """
        rotate(self._ring_buffer, -self._start)
        self._start = 0

    def _grow(self) -> None:
        """Helper to grow (double) the capacity if needed.

        Before growing the capacity, we must normalize the ring buffer to prevent any
        inconsitencies at the end of the ring buffer. Otherwise, the sequence may
        become disjoint, leading to undefined behavior.

        After normalization, the _start will be at the beginning of the ring buffer.

        Examples:
            >>> deque = Deque(capacity=2)
            >>> deque.capacity()
            2
            >>> deque._grow()
            >>> deque.capacity()
            4
        """
        self._normalize()
        self._ring_buffer = self._ring_buffer + [None] * self.capacity()

    def capacity(self) -> int:
        """The current total available capacity of the deque.

        Note: the capacity may grow to fit additional elements (via doubling). The
        current capacity is not necessarily equal to (probably not) the number of
        elements in the deque.

        Returns:
            int: The current capacity (of the internal storage ring buffer).
        """
        return len(self._ring_buffer)

    def __iter__(self) -> Iterator[T]:
        """Returns a generator of values from the deque (in remove / FIFO order).

        The deque remains unchanged from this method.

        Yields:
            Iterator[T]: Values from the deque.
        """
        for i in range(self._size):
            # It is *possible* to encounter None via type system, but due to class
            # invariant, we should never encounter non-T data in the valid index range.
            value = self._ring_buffer[self._index(i)]
            if value is not None:
                yield value

    def __contains__(self, value: T) -> bool:
        """Whether a value is present in the deque.

        Must iterate over the deque, so operates in O(n) time.

        Args:
            value (T): The value to search for in the deque.

        Returns:
            bool: If the value is present in the deque.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> 2 in deque
            True
            >>> 5 in deque
            False
        """
        return value in iter(self)

    def __len__(self) -> int:
        """Returns the number of elements in the deque.

        Returns:
            int: How many elements are present in the deque.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> len(deque)
            3
        """
        return self._size

    def __str__(self) -> str:
        """Return displayable string of elements in deque.

        Ignores implementation details such as ring buffer capacity, and the offset /
        start index. The front is on the left, and the back is to the right.

        Returns:
            str: A printable string representation of the elements in the deque.

        Examples:
            >>> deque = Deque.from_iterable([1, 2, 3])
            >>> str(deque)
            '[1, 2, 3]'
        """
        return str(list(self))
