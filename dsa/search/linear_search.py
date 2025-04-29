from typing import Callable, Iterable, Optional


def linear_search[T, U](
    iterable: Iterable[T], target: U, /, key: Optional[Callable[[T], U]] = None
) -> Optional[int]:
    """Uses linear search to find the target value in an iterable.

    Complexity:
        Time: O(n)
        Space: O(1)

    Args:
        iterable (Iterable[T]): The input sequence to be searched.
        target (T): The target value to find.
        key (Optional[Callable[[T], U]], optional): A key function to transform values
          in the iterable before testing. Defaults to None.

    Returns:
        Optional[int]: The index where the target was found in the input iterable. If
          the target has multiple occurrences, the first index will be returned. If the
          target is not present in the iterable, returns None.

    Examples:
        >>> linear_search([5, 2, 1, 4], 1)
        2
        >>> linear_search([5, 2, 1, 4], 3)
        >>> linear_search([5, 2, 1, 4], 7)
    """

    if key is None:
        for i, value in enumerate(iterable):
            if value == target:
                return i
    else:
        for i, value in enumerate(iterable):
            if key(value) == target:
                return i
    return None
