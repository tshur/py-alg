from typing import Optional, Sequence

from algorithms.typing.comparison import Comparable


def binary_search[CT: Comparable](array: Sequence[CT], target: CT) -> Optional[int]:
    """Uses binary search to find the target value in a sorted sequence.

    The array type and target type must be a Comparable type which supports at least the
    __lt__ (<) operator.

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
    """
    # Define the search space as [0, len(array)), with an exclusive end bounds to match
    # how slicing does it.
    lo = 0
    hi = len(array)

    while lo < hi:
        mid = (lo + hi) // 2
        if target == array[mid]:
            return mid

        if array[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return None
