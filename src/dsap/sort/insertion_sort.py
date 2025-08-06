from typing import Iterable

from dsap.type import SupportsRichComparison


def insertion_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using insertion sort method.

    Insertion sort uses a partition to separate the sorted area (left of the partition)
    from the unsorted area (right of the partition). At each index, we move the
    partition to the right by "inserting" the first unsorted element into its correct
    location in the sorted part of the array. To do so, we swap the element left until
    it is in the correct position.

    Sample: (using | to denote the partition location)
        [5, |1, 3, 2, 4] (do not need to check the first element)
        [1, 5, |3, 2, 4]
        [1, 3, 5, |2, 4]
        [1, 2, 3, 5, |4]
        [1, 2, 3, 4, 5|]

    Complexity:
        Time: O(n**2), for inserting n elements into sorted partition of size n.
        Space: O(n), for copying the input

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> insertion_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> insertion_sort([1])
        [1]
        >>> insertion_sort([])
        []
    """

    array = list(iterable)
    for partition_index in range(1, len(array)):
        for swap_index in range(partition_index, 0, -1):
            left, right = array[swap_index - 1], array[swap_index]
            if left > right:
                array[swap_index - 1], array[swap_index] = right, left

    return array
