import operator
from typing import Callable, Iterable, Iterator, Optional


def scan[T](
    iterable: Iterable[T],
    function: Callable[[T, T], T] = operator.add,
    *,
    initial: Optional[T] = None,
) -> Iterator[T]:
    """Generate accumulated values from an iterable (left scan algorithm).

    Optionally takes an accumulator function (in the format of reduce(acc, val)). Can
    take an initial value, which will be yielded first.

    Similar / related algorithms: itertools.accumulate, inclusive/exclusive scan, prefix
    sum, cumulative sum, partial sums.

    Complexity:
        Time: O(n)
        Space: O(1)

    Args:
        iterable (Iterable[T]): Input values to accumulate. Can be empty.
        function (Callable[[T | U, T], T | U], optional): Function to call on each value.
          The first argument will be the accumulator, and the second argument will be
          the new value from the iterable. Defaults to operator.add.
        initial (Optional[T | U], optional): An initial value for the accumulator. If
          given, the output will start with this value and be one longer than the input
          iterable. Defaults to None.

    Yields:
        Iterator[T | U]: Generated values. If initial is given, the first value generated
          will be initial and the output will be one longer than the input.

    Examples:
        >>> list(scan([1, 2, 3, 4, 5]))
        [1, 3, 6, 10, 15]
        >>> list(scan([15, 10, 6, 3, 1], operator.sub))
        [15, 5, -1, -4, -5]
        >>> list(scan([1, 2, 3], initial=0))
        [0, 1, 3, 6]
        >>> list(scan([]))
        []
    """
    iterator = iter(iterable)
    if initial is not None:
        total = initial
    else:
        try:
            total = next(iterator)
        except StopIteration:
            return  # Iterator is empty

    yield total
    for item in iterator:
        total = function(total, item)
        yield total
