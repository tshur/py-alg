from typing import Iterable

from dsap.heap import MinHeap
from dsap.type import SupportsRichComparison


def heap_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using heap sort method.

    Uses the ordering property of a heap to sort an iterable. First, we construct a heap
    from a full array (copy of iterable, but can be modified to sort in-place). This
    heapification takes O(n) time. Then, we can pop n elements from the heap. The result
    will be in sorted order.

    Complexity:
        Time: O(nlogn), to heapify in O(n) then pop O(n) elements in O(logn) for each.
        Space: O(n), for building a heap (need to copy input; but can be done in-place).

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> heap_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> heap_sort([1])
        [1]
        >>> heap_sort([])
        []
    """

    heap = MinHeap[CT].from_iterable(iterable)
    return list(heap.consume_all())
