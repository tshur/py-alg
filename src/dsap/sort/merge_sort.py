from typing import Iterable

from dsap.type import SupportsRichComparison


def merge_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using merge sort.

    Recursively defined sorting algorithm. We break the input into two partitions. For
    each partition, we merge_sort it. Then, we merge the two sorted arrays into the
    final result.

    Recursive Definition:
        Base cases:
            - len(iterable) <= 1 (it is already sorted)
        Recursive step:
            - merge_sort(left), merge_sort(right)
            - merge(left, right)

    Complexity:
        Time: O(nlogn)
        Space: O(n) extra space needed for merging (and recursive stack memory).

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> merge_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> merge_sort([1])
        [1]
        >>> merge_sort([])
        []
    """

    def merge(left: list[CT], right: list[CT]) -> list[CT]:
        """Helper function to merge two sorted ranges (left, right) within an array."""
        result: list[CT] = []
        left_index, right_index = 0, 0
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        # Move the remaining elements from whichever list wasn't exhausted first.
        if left_index < len(left):
            result.extend(left[left_index:])
        elif right_index < len(right):
            result.extend(right[right_index:])
        return result

    def recursive_helper(array: list[CT]) -> list[CT]:
        """Recursive helper to merge_sort an array within range [start, end)."""
        if len(array) < 2:
            return array  # One or zero element arrays are already sorted.

        mid = len(array) // 2
        return merge(recursive_helper(array[:mid]), recursive_helper(array[mid:]))

    array = list(iterable)
    return recursive_helper(array)
