import operator
from typing import Any, Callable, Iterable, Iterator, Optional


def scan(
    iterable: Iterable[Any],
    function: Callable[[Any, Any], Any] = operator.add,
    *,
    initial: Optional[Any] = None,
) -> Iterator[Any]:
    """Generate accumulated values from an iterable (left scan algorithm).

    Optionally takes an accumulator function (in the format of reduce(acc, val)). Can
    take an initial value, which will be yielded first.

    Args:
        iterable (Iterable[Any]): Input values to accumulate. Can be empty.
        function (Callable[[Any, Any], Any], optional): Function to call on each value.
          The first argument will be the accumulator, and the second argument will be
          the new value from the iterable. Defaults to operator.add.
        initial (Optional[Any], optional): An initial value for the accumulator. If
          given, the output will start with this value and be one longer than the input
          iterable. Defaults to None.

    Yields:
        Iterator[Any]: Generated values. If initial is given, the first value generated
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
    total = initial
    if initial is None:
        try:
            total = next(iterator)
        except StopIteration:
            return  # Iterator is empty

    yield total
    for item in iterator:
        total = function(total, item)
        yield total
