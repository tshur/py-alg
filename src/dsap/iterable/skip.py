from typing import Iterator


def skip[T](iterator: Iterator[T], n: int = 1) -> Iterator[T]:
    """Advance (and return) an iterator by n elements.

    Args:
        iterator (Iterator[T]): The iterator to advance.
        n (int, optional): Consume this many elements from the iterator. If 0 or less,
          the input iterator will remain unchanged. Defaults to 1.

    Raises:
        ValueError: If n is negative.
        StopIteration: If the number of elements to skip exceeds the length of the
          iterator.

    Examples:
        >>> iterator = iter(range(10))
        >>> _ = skip(iterator)
        >>> next(iterator)
        1
        >>> _ = skip(iterator, n=5)
        >>> next(iterator)
        7
    """
    if n < 0:
        raise ValueError("cannot skip iterator negative elements")

    for _ in range(n):
        next(iterator)
    return iterator
