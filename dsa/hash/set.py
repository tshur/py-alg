from typing import Iterable, Iterator, Self

from .map_list import MapList

Map = MapList


class Set[T]:
    """HashSet data structure implemented using a Map[T, None].

    Basic operations:
     - add, in ~O(1), but really O(k) where k is the length of collided values. Worst
         case, this is O(n) due to rehashing, but this is amortized.
     - remove, in ~O(1), but really O(k) where k is the length of collided values.
     - __contains__, in ~O(1), but really O(k) where k is the length of collided values.
     - __iter__, in ~O(n).
    """

    _hm: Map[T, None]

    def __init__(self):
        """Create a new (empty) set."""
        self._hm = Map()

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Self:
        """Create (and return) a new hash set from an iterable of values.

        Args:
            iterable (Iterable[T]): An iterable of values to add into the new set.

        Returns:
            Self: The newly created set.

        Examples:
            >>> s = Set.from_iterable([1, 2, 2, 3, 2])
            >>> list(sorted(s))
            [1, 2, 3]
        """
        s = cls()
        for value in iterable:
            s.add(value)
        return s

    def add(self, value: T) -> None:
        """Adds a value into the set. Has no effect if the value already exists.

        Args:
            value (T): The value to add.

        Examples:
            >>> s = Set()
            >>> s.add(1)
            >>> s.add(2)
            >>> s.add(2)
            >>> list(sorted(s))
            [1, 2]
        """
        self._hm[value] = None

    def remove(self, value: T) -> None:
        """Delete the value from the set.

        Args:
            value (T): The value to find and delete.

        Raises:
            KeyError: If the value is not in the set.

        Examples:
            >>> s = Set.from_iterable([1, 2, 3])
            >>> s.remove(3)
            >>> 3 in s
            False
        """
        del self._hm[value]

    def __iter__(self) -> Iterator[T]:
        """Yields values stored in the set (in an arbitrary order).

        Yields:
            Iterator[T]: Values in the set.

        Examples:
            >>> s = Set.from_iterable([1, 2, 2, 3, 2])
            >>> list(sorted(s))
            [1, 2, 3]
        """
        yield from self._hm.keys()

    def __contains__(self, value: T) -> bool:
        """Return if a given value exists in the set.

        Args:
            value (T): The value to search for in the set.

        Returns:
            bool: True if the value is in the set. False, otherwise.

        Examples:
            >>> s = Set.from_iterable([1, 2, 2, 3, 2])
            >>> 2 in s
            True
            >>> 4 in s
            False
        """
        return value in self._hm

    def __len__(self) -> int:
        """Return the number of values in the set.

        Returns:
            int: The number of values in the set.

        Examples:
            >>> s = Set.from_iterable([1, 2, 2, 3, 2])
            >>> len(s)
            3
        """
        return len(self._hm)

    def __bool__(self) -> bool:
        """Returns true if the set has at least one value.

        Returns:
            bool: True if the set has at least one value. False, otherwise.

        Examples:
            >>> bool(Set.from_iterable([1, 2, 2, 3, 2]))
            True
            >>> bool(Set())
            False
        """
        return bool(self._hm)
