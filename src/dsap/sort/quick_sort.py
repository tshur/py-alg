from typing import Iterable

from src.dsap.type import SupportsRichComparison


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

    def recursive_helper(array: list[CT]) -> list[CT]:
        if len(array) <= 1:
            return array  # Already sorted.

        pivot = array[0]
        left_partition: list[CT] = []
        right_partition: list[CT] = []
        for item in array[1:]:
            if item < pivot:
                left_partition.append(item)
            else:
                right_partition.append(item)

        return (
            recursive_helper(left_partition)
            + [pivot]
            + recursive_helper(right_partition)
        )

    return recursive_helper(list(iterable))
