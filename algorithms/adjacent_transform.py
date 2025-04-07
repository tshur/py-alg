import operator
from itertools import tee
from typing import Callable, Iterable, Iterator


def pairwise_transform[T](
    iterable: Iterable[T], function: Callable[[T, T], T] = operator.add
) -> Iterator[T]:
    """Applies a function on a sliding window of pairs from the input iterable.

    Similar / equivalent algorithms: itertools.pairwise, adjacent_transform, sliding
    window.

    Args:
        iterable (Iterable[T]): Input values, which will be traversed in pairs.
        function (Callable[[T, T], T], optional): Function to call on each pair of
          values. The first and second values will be adjacent in the input iterable
          (i.e., (iterable[i], iterable[i+1])). Defaults to operator.add.

    Yields:
        Iterator[T]: Generated values. The length of the output iterate will be one less
        than the input iterator.

    Examples:
        >>> list(pairwise_transform([15, 10, 6, 3, 1]))
        [25, 16, 9, 4]
        >>> list(pairwise_transform([15, 10, 6, 3, 1], operator.sub))
        [5, 4, 3, 2]
        >>> list(pairwise_transform([10]))
        []
    """
    first_iterator, second_iterator = tee(iterable, 2)
    try:
        next(second_iterator)
    except StopIteration:
        return  # Not enough elements to access pairwise.

    for first, second in zip(first_iterator, second_iterator):
        yield function(first, second)
