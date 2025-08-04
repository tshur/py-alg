from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Self


class MapBase[K, V](ABC):
    """Abstract HashMap data structure."""

    _size: int
    _load_factor = 0.75  # Ratio of size:capacity before we grow the map's capacity.

    @abstractmethod
    def __init__(self, /, capacity: int = 31): ...

    @classmethod
    def from_items(cls, items: Iterable[tuple[K, V]]) -> Self:
        """Create (and return) a new hash map from an iterable of (key, value) pairs.

        Args:
            items (Iterable[tuple[K, V]]): An iterable of (key, value) pairs to add into
              the newly created map.

        Returns:
            Self: The newly created object.
        """
        hm = cls()
        for key, value in items:
            hm[key] = value
        return hm

    def pop(self, key: K) -> V:
        """Delete (and return) the entry at self[key].

        Args:
            key (K): The key of the desired item to pop.

        Raises:
            KeyError: If the key is not found in the map.
        """
        value = self[key]
        del self[key]
        return value

    @abstractmethod
    def __getitem__(self, key: K) -> V: ...

    @abstractmethod
    def __setitem__(self, key: K, value: V) -> None: ...

    @abstractmethod
    def __delitem__(self, key: K) -> None: ...

    def __iter__(self) -> Iterator[K]:
        """Yields keys stored in the map (in an arbitrary order).

        Equivalent to self.keys().

        Yields:
            Iterator[K]: Keys in the map.
        """
        yield from self.keys()

    @abstractmethod
    def keys(self) -> Iterator[K]: ...

    @abstractmethod
    def values(self) -> Iterator[V]: ...

    @abstractmethod
    def items(self) -> Iterator[tuple[K, V]]: ...

    @abstractmethod
    def _capacity(self) -> int: ...

    @abstractmethod
    def _grow(self) -> None: ...

    def _hash(self, key: K) -> int:
        """The bucket index of the keyed item, based on its hash."""
        return hash(key) % self._capacity()

    def __contains__(self, key: K) -> bool:
        """Return if a given key exists in the map.

        Args:
            key (K): The key to search for in the map.

        Returns:
            bool: True if the key is in the map. False, otherwise.
        """
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __len__(self) -> int:
        """Return the number of entries in the map.

        Returns:
            int: The number of entries in the map (size, not capacity).
        """
        return self._size

    def __bool__(self) -> bool:
        """Returns true if the map has at least one entry.

        Returns:
            bool: True if the map has at least one entry. False, otherwise.
        """
        return len(self) > 0
