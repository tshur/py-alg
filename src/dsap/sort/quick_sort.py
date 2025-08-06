from typing import Iterable

from dsap.type import SupportsRichComparison


def quick_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using quick sort method.

    This implementation of quick sort is recursive. At each step, we choose a pivot.
    Then, we partition the array into elements that are smaller than, and larger than,
    the pivot. Finally, we recursively quick sort the two partitions (until finished).

    Selecting the pivot element can be an implementation detail. A bad pivot can lead to
    poor runtime. For simplicity, we will always choose the first element as the pivot.

    Sample: (using ^ to denote the pivot, and | to denote the partition locations)
        [5, 1, 3, 2, 4]
               ^
        [2, 1| 3 |5, 4]
               ^
        [2, 1] 3 [5, 4]
            ^        ^
        [1, 2] 3 [4, 5]
         ^        ^
        [1, 2, 3, 4, 5]

    Complexity:
        Time: O(nlogn), (with balanced pivot selection) due to recursive splitting.
        Space: O(n), for consuming the input into an array.

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> quick_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> quick_sort([1])
        [1]
        >>> quick_sort([])
        []
    """

    def swap(array: list[CT], i: int, j: int):
        """Swap elements at two indicies in an array (assuming they are in-bounds)."""
        array[i], array[j] = array[j], array[i]

    def partition(array: list[CT], start: int, end: int) -> int:
        """Partition the subsequence in [start, end), and return a valid pivot.

        Sample: (using ^ to denote the pivot)
        [2, 5, 3, 1, 4]
         ^
            i
        [2, 5, 3, 1, 4]
               i
        [2, 5, 3, 1, 4]
                  i (swap)
        [2, 1, 3, 5, 4] (swap after pivot)
        [1, 2, 3, 5, 4] (swap with pivot)
            ^
                     i
        """
        pivot = start
        for other in range(start + 1, end):
            if array[pivot] < array[other]:
                continue
            swap(array, pivot + 1, other)
            swap(array, pivot, pivot + 1)
            pivot += 1
        return pivot

    def recursive_helper(array: list[CT], start: int, end: int):
        """Recursively quick sorts the array within inclusive range [start, end)."""
        if end - start < 2:
            return  # Already sorted.

        pivot = partition(array, start, end)
        recursive_helper(array, start, pivot)
        recursive_helper(array, pivot + 1, end)

    array = list(iterable)
    recursive_helper(array, 0, len(array))
    return array
