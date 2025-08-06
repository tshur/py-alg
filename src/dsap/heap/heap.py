from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Optional, Self

from dsap.type import SupportsRichComparison


class _Heap[CT: SupportsRichComparison](ABC):
    """Abstract heap data structure implementation using a list with custom comparator.

    The heap is organized such that the highest priority element is always at the
    front / root of the heap (index 0). After push/pop operations, we need to re-heapify
    (sift_up or sift_down) to maintain the heap invariant.

    We use a list because the heap will always be a complete binary tree. We can
    traverse to parent/child "nodes" via index manipulation. Left and right children are
    at 2i+1 and 2i+2, respectively. The parent node is at (i-2)//2.

    Values must support a Comparable type (at least support __lt__ operation). For
    MinHeap, the highest priority element is the "smallest"; for MaxHeap it is the
    "largest".

    Supports the following core algorithms:
     - from_iterable in O(n) time
     - push in O(logn) time
     - pop in O(logn) time
     - peek in O(1) time
     - consume_all in O(nlogn) time (n pop operations)
     - private methods to sift_up, sift_down, and heapify
    """

    _heap: list[CT]

    def __init__(self):
        """Create an empty heap."""
        self._heap = []

    @classmethod
    def from_iterable(cls, iterable: Iterable[CT]) -> Self:
        """Create a heap from an existing iterable in O(n) time.

        We can achieve O(n) time by first using the iterable as the heap, then
        performing the O(n) heapify algorithm in-place. If we did n push'es, it would be
        O(nlogn) instead.

        Complexity:
            Time: O(n) due to heapify.
            Space: O(n) due to copying input iterable into heap memory.

        Args:
            iterable (Iterable[CT]): The iterable to fill the heap with. The iterable
              will be copied into the heap, and not mutated in-place.

        Returns:
            Self: The newly constructed heap.

        Examples:
            >>> heap = MinHeap.from_iterable([5, 1, 3, 2, 4])
            >>> list(heap.consume_all())
            [1, 2, 3, 4, 5]
        """
        heap = cls()
        heap._heap = list(iterable)
        heap._heapify()
        return heap

    def push(self, value: CT) -> None:
        """Push a value into the heap.

        The value is inserted at the end of the heap. Then, we repeatedly call _sift_up
        until the heap invariant is restored.

        Complexity:
            Time: O(logn) to re-heapify.

        Args:
            value (CT): The value to add into the heap.

        Examples:
            >>> heap = MinHeap()
            >>> heap.push(3)
            >>> heap.push(1)
            >>> heap.push(2)
            >>> heap.peek()
            1
        """
        self._heap.append(value)
        self._sift_up(len(self) - 1)

    def pop(self) -> Optional[CT]:
        """Pop (and return) the highest priority item from the top of the heap.

        Popping the element could occur in O(1) time (like the peek operation). However,
        we need to maintain the heap invariant by swapping with the last value and then
        calling _sift_down.

        Complexity:
            Time: O(logn) to reheapify.

        Returns:
            Optional[CT]: The popped / removed value. If the heap is empty, return None.

        Examples:
            >>> heap = MinHeap.from_iterable([3, 1, 2])
            >>> heap.pop()
            1
            >>> heap.pop()
            2
            >>> heap.pop()
            3
            >>> heap.pop()
        """
        if self.is_empty():
            return None
        if len(self) == 1:
            return self._heap.pop()

        value = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return value

    def peek(self) -> Optional[CT]:
        """Return the highest priority value in the heap (the front).

        Complexity:
            Time: O(1)

        Returns:
            Optional[CT]: The highest priority value / root of the heap. If the heap is
              empty, returns None.

        Examples:
            >>> heap = MinHeap.from_iterable([3, 1, 2])
            >>> heap.peek()
            1
            >>> heap = MinHeap()
            >>> heap.peek()
        """
        return self._heap[0] if not self.is_empty() else None

    def is_empty(self) -> bool:
        """Returns True if the heap is empty (no elements). Otherwise, returns False.

        Returns:
            bool: True if the heap is empty. Otherwise, returns False.

        Examples:
            >>> heap = MinHeap.from_iterable([3, 1, 2])
            >>> heap.is_empty()
            False
            >>> heap = MinHeap()
            >>> heap.is_empty()
            True
        """
        return not self._heap

    def consume_all(self) -> Iterator[CT]:
        """Pop (and yield) values from the heap until the heap is empty.

        Repeatedly calls pop to get the highest priority value from the heap until the
        heap is empty. After this, the heap will be empty and is mutated by this
        function. The returned values will be in sorted order due to the heap invariant.

        Caution: If this iterator is not consumed, then the heap will still have values
        that could later be removed via the pop()s of this iterator.

        Complexity:
            Time: O(nlogn) due to O(n) pop operations of O(logn) each.

        Yields:
            Iterator[CT]: An iterator over values in the heap.

        Examples:
            >>> heap = MinHeap.from_iterable([5, 1, 3, 2, 4])
            >>> list(heap.consume_all())
            [1, 2, 3, 4, 5]
        """
        while (value := self.pop()) is not None:
            yield value

    def __contains__(self, value: CT) -> bool:
        """Check if a given value exists in the heap.

        Args:
            value (CT): The value to search for in the heap.

        Returns:
            bool: Whether or not the value is present in the heap.

        Examples:
            >>> heap = MinHeap.from_iterable([5, 1, 3, 2, 4])
            >>> 2 in heap
            True
            >>> 6 in heap
            False
        """
        # No need to iterate in heap ordering. We cannot really benefit from binary
        # search with loose heap structure. Minor optimizations exist with stopping
        # early in search.
        return value in self._heap

    def __len__(self) -> int:
        """Return the length of the heap (number of elements).

        Returns:
            int: The number of elements present in the heap.

        Examples:
            >>> heap = MinHeap.from_iterable([5, 1, 3, 2, 4])
            >>> len(heap)
            5
        """
        return len(self._heap)

    @abstractmethod
    def _compare(self, value1: CT, value2: CT) -> bool: ...

    def _priority_child(self, i: int) -> Optional[int]:
        """Returns the index of the (highest) priority child for the given node index.

        Args:
            i (int): The current node to find the (higher) priority child of.

        Returns:
            Optional[int]: The index of the child node with higher priority. There is no
              guarantee that the returned child has a higher priority than the current
              node. If no such child exists (e.g., leaf node), then None is returned.
        """
        left, right = _Heap._left_child(i), _Heap._right_child(i)
        if left >= len(self):
            return None
        elif right >= len(self):
            return left

        if self._compare(self._heap[left], self._heap[right]):
            return left
        return right

    def _sift_up(self, i: int) -> None:
        """Sift/heapify nodes upwards until the heap invariant is restored.

        Only checks the heap invariant for the current node (i.e., stops when a node is
        encountered with higher priority). Sifting means swapping the node with its
        parent until the parent is higher priority.

        Complexity:
            Time: O(logn) due to repeated swaps possibly the height of the heap.

        Args:
            i (int): The current index of the node to sift upwards.
        """
        while i > 0:
            parent = _Heap._parent(i)
            if self._compare(self._heap[parent], self._heap[i]):
                return

            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:
        """Sift/heapify nodes downwards until the heap invariant is restored.

        Only checks the heap invariant for the current node (i.e., stops when a node is
        encountered with lower priority). Sifting means swapping the node with the
        higher priority of its two children (if that value is higher priority than
        current).

        Complexity:
            Time: O(logn) due to repeated swaps possibly the height of the heap.

        Args:
            i (int): The current index of the node to sift downwards.
        """
        while i < len(self):
            child = self._priority_child(i)
            if not child or self._compare(self._heap[i], self._heap[child]):
                return

            self._swap(i, child)
            i = child

    def _heapify(self) -> None:
        """Heapify the entire heap array in-place.

        Typically called from an unstructured input (e.g., from an iterable). Repeatedly
        calls sift_down from the end of the array. This is more efficient than calling
        sift_up.

        Complexity:
            Time: O(n)
        """
        for i in range(len(self) - 1, -1, -1):
            self._sift_down(i)

    def _swap(self, i: int, j: int) -> None:
        """Swaps the positions of two indices in the heap.

        Args:
            i (int): The first node index to swap.
            j (int): The second node index to swap.
        """
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    @staticmethod
    def _parent(i: int) -> int:
        """Return the index of the parent node of i.

        Since the values are stored in a flat array, we use index manipulation to find
        the parent/children of a given node.

        Args:
            i (int): The index of the value to find the parent of.

        Returns:
            int: The index of the parent of the given node index. If 0 is given (root),
              then an index of -1 will be returned (representing no parent).

        Examples:
            >>> _Heap._parent(5)
            2
            >>> _Heap._parent(2)
            0
            >>> _Heap._parent(0)
            -1
        """
        return (i - 1) // 2

    @staticmethod
    def _left_child(i: int) -> int:
        """Return the index of the left child node of i.

        Since the values are stored in a flat array, we use index manipulation to find
        the parent/children of a given node.

        Args:
            i (int): The index of the value to find the left child of.

        Returns:
            int: The index of the left child of the given node index. Possibly returns
              values beyond the length of the heap, if the requested child does not
              exist (e.g., leaf node).

        Examples:
            >>> _Heap._left_child(0)
            1
            >>> _Heap._left_child(1)
            3
            >>> _Heap._left_child(2)
            5
        """
        return i * 2 + 1

    @staticmethod
    def _right_child(i: int) -> int:
        """Return the index of the right child node of i.

        Since the values are stored in a flat array, we use index manipulation to find
        the parent/children of a given node.

        Args:
            i (int): The index of the value to find the right child of.

        Returns:
            int: The index of the right child of the given node index. Possibly returns
              values beyond the length of the heap, if the requested child does not
              exist (e.g., leaf node).

        Examples:
            >>> _Heap._right_child(0)
            2
            >>> _Heap._right_child(1)
            4
            >>> _Heap._right_child(2)
            6
        """
        return i * 2 + 2


class MinHeap[CT: SupportsRichComparison](_Heap[CT]):
    """MinHeap, where the smallest item is always at the front.

    Examples:
        >>> min_heap = MinHeap[int].from_iterable([5, 1, 4, 3, 2])
        >>> min_heap.peek()
        1
        >>> list(min_heap.consume_all())
        [1, 2, 3, 4, 5]
    """

    def _compare(self, value1: CT, value2: CT) -> bool:
        """Use __lt__ ordering to construct a min-heap."""
        return value1 < value2


class MaxHeap[CT: SupportsRichComparison](_Heap[CT]):
    """MaxHeap, where the largest item is always at the front.

    Examples:
        >>> max_heap = MaxHeap[int].from_iterable([5, 1, 4, 3, 2])
        >>> max_heap.peek()
        5
        >>> list(max_heap.consume_all())
        [5, 4, 3, 2, 1]
    """

    def _compare(self, value1: CT, value2: CT) -> bool:
        """Use __gt__ ordering to construct a min-heap."""
        return value1 > value2
