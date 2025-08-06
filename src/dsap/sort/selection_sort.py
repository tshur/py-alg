from typing import Iterable

from dsap.type import SupportsRichComparison


def selection_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using selection sort method.

    Selection sort uses a partition to separate the sorted area (left of the partition)
    from the unsorted area (right of the partition). At each index, we move the
    partition to the right by "selecting" the next smallest element to be moved
    (swapped) to the left of the partition.

    Sample: (using | to denote the partition location)
        [|5, 1, 3, 2, 4]
        [1, |5, 3, 2, 4]
        [1, 2, |3, 5, 4]
        [1, 2, 3, |5, 4]
        [1, 2, 3, 4, 5] (do not need to check the last element).

    Complexity:
        Time: O(n**2)
        Space: O(n)

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> selection_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> selection_sort([1])
        [1]
        >>> selection_sort([])
        []
    """

    def get_index_of_minimum(array: list[CT], start: int) -> int:
        min_index = start
        for i in range(start + 1, len(array)):
            if array[i] < array[min_index]:
                min_index = i
        return min_index

    array = list(iterable)
    for i in range(len(array) - 1):
        min_index = get_index_of_minimum(array, start=i)
        array[i], array[min_index] = array[min_index], array[i]
    return array
