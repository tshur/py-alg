from typing import Iterable

from dsap.type import SupportsRichComparison


def bubble_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using bubble sort method.

    Repeatedly swap adjacent pairs of elements (if not ordered) until the whole array is
    sorted. We need to pass through the array until no more swaps are made.

    Sample: (using ^--^ to denote the pair of viewed elements)
        [5, 1, 3, 2, 4]
         ^--^ (swap)
        [1, 5, 3, 2, 4]
            ^--^ (swap)
        [1, 3, 5, 2, 4]
               ^--^ (swap)
        [1, 3, 2, 5, 4]
                  ^--^ (swap)
        [1, 3, 2, 4, 5]
         ^--^
        [1, 3, 2, 4, 5]
            ^--^ (swap)
        [1, 2, 3, 4, 5]  (after one more pass, we will know there were no more swaps)

    Complexity:
        Time: O(n**2), worst case we bubble the last element into the first position.
        Space: O(n), for consuming the input into an array.

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> bubble_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> bubble_sort([1])
        [1]
        >>> bubble_sort([])
        []
    """

    array = list(iterable)

    while True:
        swapped = False
        for i in range(0, len(array) - 1):
            if array[i + 1] < array[i]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True

        if not swapped:
            return array
