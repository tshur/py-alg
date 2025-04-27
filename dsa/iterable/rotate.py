from typing import MutableSequence

from .reverse import reverse


def rotate[T](array: MutableSequence[T], k: int) -> MutableSequence[T]:
    """Rotates the given sequence in-place by k steps.

    Uses three reverses as the algorithm to rotate in-place. Similar / related
    algorithms: deque.rotate.

    Sample:
        [1, 2, 3, 4, 5, 6, 7], k=-2, len=7 -> k=5, len=7
        [2, 1, 3, 4, 5, 6, 7] (reverse range(0, 7-5))
        [2, 1, 7, 6, 5, 4, 3] (reverse range(7-5, 7))
        [3, 4, 5, 6, 7, 1, 2] (reverse range(0, 7))


    Complexity:
        Time: O(n) (performs O(n) reverse algorithm 3 times)
        Space: O(1)

    Args:
        array (MutableSequence[T]): The input sequence to rotate. This algorithm mutates
          the original input.
        k (int): The number of positions to rotate. For positive k, rotate clockwise (to
          the right or forward). For negative k rotate counter-clockwise (to the left
          or backward). If k is negative (and magnitude less then array length), then
          the element at index -k will become the first element after rotation.

    Returns:
        MutableSequence[T]: The rotated sequence. The original sequence will be mutated,
          but is also returned as a convenience.

    Example:
        >>> rotate([1, 2, 3, 4], 1)
        [4, 1, 2, 3]
        >>> rotate([1, 2, 3, 4], -1)
        [2, 3, 4, 1]
        >>> rotate([1, 2, 3, 4], -5)
        [2, 3, 4, 1]
    """
    if not array:
        return array

    k = k % len(array)
    partition = len(array) - k
    reverse(array, end=partition)
    reverse(array, start=partition)
    reverse(array)
    return array
