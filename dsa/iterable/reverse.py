from typing import MutableSequence, Optional


def reverse[T](
    array: MutableSequence[T], start: int = 0, end: Optional[int] = None
) -> MutableSequence[T]:
    """Reverses an array in the window [start, end).

    If no start and/or end are given, the default behavior is to reverse the entire
    input array. This function mutates the input argument, and returns it as well.
    Similar/related algorithms: list.reverse, reversed, list[::-1].

    Complexity:
        Time: O(n), n/2 total swaps, where n = end - start
        Space: O(1), in-place algorithm

    Args:
        array (MutableSequence[T]): Input sequence to reverse. The input array will be
          modified (reversed in-place).
        start (int): The (inclusive) start of the range to reverse. Defaults to 0.
        end (Optional[int]): The (exclusive) end of the range to reverse. If not set,
          or beyond the end of the array, then the array length will be used. Defaults
          to None.

    Returns:
        MutableSequence[T]: The reversed input sequence. The input will be mutated
          in-place. The return value is provided for convenience and method chaining.

    Examples:
        >>> reverse([1, 2, 3, 4, 5])
        [5, 4, 3, 2, 1]
        >>> reverse([1, 2, 3, 4, 5], start=1)
        [1, 5, 4, 3, 2]
        >>> reverse([1, 2, 3, 4, 5], start=1, end=4)
        [1, 4, 3, 2, 5]
        >>> reverse([])
        []
    """
    if end is None or end > len(array):
        end = len(array)

    for i in range((end - start) // 2):
        array[start + i], array[end - i - 1] = array[end - i - 1], array[start + i]
    return array
