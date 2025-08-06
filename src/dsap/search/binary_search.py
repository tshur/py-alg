from typing import Optional, Sequence

from dsap.type import SupportsRichComparison


def binary_search[CT: SupportsRichComparison](
    array: Sequence[CT], target: CT
) -> Optional[int]:
    """Uses binary search to find the target value in a sorted sequence.

    The array type and target type must be a Comparable type which supports at least the
    __lt__ (<) operator. Similar / related algorithms: bisect, lower_bound, upper_bound,
    insort, binary search tree.

    Sample:
        [1, 2, 3, 4, 5, 6, 7], target=5
         L        M           H (mid is too low)
                     L  M     H (mid is too high)
                     LM H       (mid == target; found!)

    Complexity:
        Time: O(logn)
        Space: O(1)

    Args:
        array (Sequence[CT]): The input sequence to be searched. This must be in
          (ascending) sorted order.
        target (CT): The target value to find.

    Returns:
        Optional[int]: The index where the target was found in the input array. If the
          target has multiple occurrences, one index will be returned. If the target is
          not found, returns None.

    Examples:
        >>> binary_search([1, 2, 4, 5], 4)
        2
        >>> binary_search([1, 2, 4, 5], 3)
        >>> binary_search([1, 2, 4, 5], 7)
    """
    # Search space is [0, len(array)), with an exclusive end to match slicing.
    low = 0
    high = len(array)

    while low < high:
        mid = (low + high) // 2
        if target == array[mid]:
            return mid

        if array[mid] < target:
            low = mid + 1
        else:
            high = mid
    return None


def lower_bound[CT: SupportsRichComparison](array: Sequence[CT], target: CT) -> int:
    """Uses binary search to find the smallest index where target could be inserted.

    This function has the difference with the core binary_search function in two ways.
    First, if the value is not found in the array, lower_bound will not return None, but
    an index where the target could be inserted while maintaining sorted order. Second,
    if there are multiple copies of the target, this function will return the leftmost
    index.

    Sample: (L=low, M=mid, H=high)
        [1, 3, 3, 3, 5, 6, 7], target=3
         L        M           H (mid is not too low)
         L  M     H             (mid is not too low)
         LM H                   (mid is too low)
           LMH                  (break loop; return L index)

    Complexity:
        Time: O(logn)
        Space: O(1)

    Args:
        array (Sequence[CT]): The input sequence to be searched. This must be in
          (ascending) sorted order.
        target (CT): The target value to find.

    Returns:
        int: The lowest index where the target could be inserted into the input sequence
          while maintaining sorted order. If the target is present in the array, this is
          equal to the leftmost index of the target.

    Examples:
        >>> lower_bound([1, 2, 4, 5], 4)
        2
        >>> lower_bound([1, 2, 4, 5], 3)
        2
        >>> lower_bound([1, 2, 4, 5], 7)
        4
    """
    # Search space is [0, len(array)), with an exclusive end to match slicing.
    low = 0
    high = len(array)

    while low < high:
        mid = (low + high) // 2
        if array[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def upper_bound[CT: SupportsRichComparison](array: Sequence[CT], target: CT) -> int:
    """Uses binary search to find the largest index where target could be inserted.

    This returns the first index in the array with a value greater than the target. If
    no such index exists, returns the length of the array. This is the largest index
    where the target could be inserted into the array while still maintaining sorted
    order.

    Sample: (L=low, M=mid, H=high)
        [1, 3, 3, 3, 5, 6, 7], target=3
         L        M           H (mid is not too high)
                  L     M     H (mid is too high)
                  L  M  H       (mid is too high)
                  LM H          (mid is not too high)
                    LMH         (break loop; return L index)

    Complexity:
        Time: O(logn)
        Space: O(1)

    Args:
        array (Sequence[CT]): The input sequence to be searched. This must be in
          (ascending) sorted order.
        target (CT): The target value to find.

    Returns:
        int: The highest index where the target could be inserted into the input
          sequence while maintaining sorted order. If the target is present in the
          array, this is equal to one after the rightmost index of the target.

    Examples:
        >>> upper_bound([1, 2, 4, 5], 4)
        3
        >>> upper_bound([1, 2, 4, 5], 3)
        2
        >>> upper_bound([1, 2, 4, 5], 7)
        4
    """
    # Search space is [0, len(array)), with an exclusive end to match slicing.
    low = 0
    high = len(array)

    while low < high:
        mid = (low + high) // 2
        if target < array[mid]:
            high = mid
        else:
            low = mid + 1
    return low
