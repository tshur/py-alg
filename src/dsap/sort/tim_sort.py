from typing import Iterable

from dsap.type import SupportsRichComparison


def tim_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using tim sort method.

    Timsort is a hybrid sorting algorithm derived from merge sort and insertion sort.
    The algorithm finds natural, already sorted subsequences called "runs," then
    efficiently merges them together. Insertion sort is used to sort small runs for
    optimal performance (e.g., chunks of 32).

    Sample: (using | to denote the sub run locations; insertion sort runs of size 2)
        [5, 1|, 3, 2|, 4]
        [1, 5|, 2, 3|, 4] first insert sort
        [1, 2, 3, 5|, 4] first merge sort
        [1, 2, 3, 4, 5] second merge sort

    Complexity:
        Time: O(nlogn), worst case when we have no existing ascending trend in the input
          array for optimization.
        Space: O(n), for consuming the input into an array.

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> tim_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> tim_sort([1])
        [1]
        >>> tim_sort([])
        []
    """

    def calc_minrun(n: int) -> int:
        """Calculates the minimum run size for Timsort.

        Returns the smallest power of 2 that is less than or equal to n.
        """
        # Insertion sort length can be changed to 64 if list longer than 2^10.
        INSERTION_SORT_LENGTH = 32
        r = 0
        while n >= INSERTION_SORT_LENGTH:
            r |= n & 1
            n >>= 1
        return n + r

    def insertion_sort(array: list[CT], left: int, right: int) -> None:
        """Sorts a slice of an array using insertion sort.

        This is used for sorting small runs.
        """
        for i in range(left + 1, right + 1):
            key_item = array[i]
            j = i - 1
            while j >= left and array[j] > key_item:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key_item

    def merge(array: list[CT], lft: int, mid: int, rgt: int) -> None:
        """Merges two sorted subarrays arr[lft..mid] and arr[mid+1..rgt]."""
        left, right = array[lft : mid + 1], array[mid + 1 : rgt + 1]
        len1, len2 = len(left), len(right)

        i = j = 0
        k = lft
        # Merge
        while i < len1 and j < len2:
            if right[j] < left[i]:
                array[k] = right[j]
                j += 1
            else:
                array[k] = left[i]
                i += 1
            k += 1

        # Remaining elements of left[].
        while i < len1:
            array[k] = left[i]
            k += 1
            i += 1

        # Remaining elements of right[].
        while j < len2:
            array[k] = right[j]
            k += 1
            j += 1

    array = list(iterable)
    n = len(array)

    if n < 2:
        return array

    minrun = calc_minrun(n)

    # Sort initial runs.
    for start in range(0, n, minrun):
        end = min(start + minrun - 1, n - 1)
        insertion_sort(array, start, end)

    # Merge runs together, bottom-up.
    size = minrun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:  # Spot optimized location for merge.
                merge(array, left, mid, right)

        size *= 2

    return array
