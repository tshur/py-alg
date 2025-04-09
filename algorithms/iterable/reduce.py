import operator
from typing import Callable, Iterable, Optional


def reduce[T](
    iterable: Iterable[T],
    function: Callable[[T, T], T] = operator.add,
    *,
    initial: Optional[T] = None,
) -> Optional[T]:
    """Perform a reduction algorithm on the given iterable.

    Similar / related algorithms: functools.reduce, fold (fold_left, fold_right),
    accumulate, aggregate, compress.

    Complexity:
        Time: O(n)
        Space: O(1)

    Args:
        iterable (Iterable[T]): Input values to accumulate. Can be empty.
        function (Callable[[T, T], T], optional): Function to call on each value.
          The first argument will be the accumulator, and the second argument will be
          the new value from the iterable. Defaults to operator.add.
        initial (Optional[T], optional): An initial value for the accumulator. If
          given, the output will start with this value and be one longer than the input
          iterable. Defaults to None.

    Returns
        T: Result of the reduction. If the input is empty, initial is returned (possibly
          None).

    Examples:
        >>> reduce([1, 2, 3, 4, 5])
        15
        >>> reduce([1, 2, 3], operator.mul)
        6
        >>> reduce([1, 1, 1], operator.mul, initial=100)
        100
        >>> reduce([])
    """
    iterator = iter(iterable)
    if initial is not None:
        total = initial
    else:
        try:
            total = next(iterator)
        except StopIteration:
            return initial  # Iterator is empty

    for item in iterator:
        total = function(total, item)
    return total
