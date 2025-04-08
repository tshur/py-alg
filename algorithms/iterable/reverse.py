from typing import MutableSequence, Optional


def reverse[T](
    array: MutableSequence[T], start: int = 0, end: Optional[int] = None
) -> MutableSequence[T]:
    """Reverses an array in the inclusive window [start, end].

    If no start and/or end are given, the default behavior is to reverse the entire
    input array. This function mutates the input argument, and returns it as well.

    Args:
        array (MutableSequence[T]): Input sequence to reverse. The input array will be
          modified (reversed in-place).
        start (int): The (inclusive) start of the range to reverse. Defaults to 0.
        end (Optional[int]): The (inclusive) end of the range to reverse. If not set,
          or beyond the end of the array, then the last element will be used. Defaults
          to None.

    Returns:
        MutableSequence[T]: The reversed input sequence. The input will be mutated
          in-place. The return value is provided for convenience and method chaining.

    Examples:
        >>> reverse([1, 2, 3, 4, 5])
        [5, 4, 3, 2, 1]
        >>> reverse([1, 2, 3, 4, 5], start=1)
        [1, 5, 4, 3, 2]
        >>> reverse([1, 2, 3, 4, 5], start=1, end=3)
        [1, 4, 3, 2, 5]
        >>> reverse([])
        []
    """
    if end is None or end >= len(array):
        end = len(array) - 1

    while start <= end:
        array[start], array[end] = array[end], array[start]
        start += 1
        end -= 1
    return array
