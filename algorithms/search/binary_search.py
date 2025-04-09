from typing import Optional, Sequence

from algorithms.typing.comparison import Comparable


def binary_search[CT: Comparable](array: Sequence[CT], target: CT) -> Optional[int]:
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
