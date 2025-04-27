import operator
from itertools import tee
from typing import Callable, Iterable, Iterator, Tuple

from .skip import skip


def adjacent_transform[T, U](
    iterable: Iterable[T],
    function: Callable[[Tuple[T, ...]], U],
    window_size: int = 2,
) -> Iterator[U]:
    """Applies a function on a sliding window from the input iterable.

    Similar / equivalent algorithms: itertools.pairwise, pairwise_transform, sliding
    window.

    Complexity:
        Time: O(n * k), where k is the window size, due to zipping k iterators
        Space: O(k), due to tee'ing the input iterator k times

    Args:
        iterable (Iterable[T]): Input values, which will be traversed in windows of size
          window_size.
        function (Callable[[Tuple[T, ...]], U]): Function to call on each window of
          values. The function will be called with a tuple of length matching the
          window_size.
        window_size (int, optional): Window size to apply the function. This value
          represents the number of adjacent elements to give to the function. Defaults
          to 2 (pairwise_transform).

    Yields:
        Iterator[U]: Generated values. The length of the output iterator will be
        len(iterable) - (window_size - 1).

    Raises:
        ValueError: If window_size < 0.

    Examples:
        >>> list(adjacent_transform([15, 10, 6, 3, 1], sum))
        [25, 16, 9, 4]
        >>> list(adjacent_transform([15, 10, 6, 3, 1], sum, 3))
        [31, 19, 10]
        >>> list(adjacent_transform([10, 10], sum, 1))
        [10, 10]
        >>> list(adjacent_transform([10, 10], sum, 3))
        []
    """
    iterators = tee(iterable, window_size)
    try:
        # Offset the iterators according to their index to create the window.
        for i, iterator in enumerate(iterators):
            skip(iterator, i)
    except StopIteration:
        return  # Not enough elements to access pairwise.

    for window in zip(*iterators):
        yield function(window)


def pairwise_transform[T, U](
    iterable: Iterable[T], function: Callable[[T, T], U] = operator.add
) -> Iterator[U]:
    """Applies a function on a sliding window of pairs from the input iterable.

    Similar / equivalent algorithms: itertools.pairwise, adjacent_transform, sliding
    window.

    Args:
        iterable (Iterable[T]): Input values, which will be traversed in pairs.
        function (Callable[[T, T], U], optional): Function to call on each pair of
          values. The first and second values will be adjacent in the input iterable
          (i.e., (iterable[i], iterable[i+1])). Defaults to operator.add.

    Yields:
        Iterator[U]: Generated values. The length of the output iterator will be one
        less than the input iterator.

    Examples:
        >>> list(pairwise_transform([15, 10, 6, 3, 1]))
        [25, 16, 9, 4]
        >>> list(pairwise_transform([15, 10, 6, 3, 1], operator.sub))
        [5, 4, 3, 2]
        >>> list(pairwise_transform([10]))
        []
    """

    # We need to adjust the argument shape to use the generic adjacent_transform.
    def tuple_function(values: tuple[T, ...]) -> U:
        return function(*values)

    yield from adjacent_transform(iterable, tuple_function, 2)
