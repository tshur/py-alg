from operator import itemgetter
from typing import Iterable, Iterator, Self

from dsa.search import linear_search


class Map[K, V]:
    # We handle hash collisions simply by extending the list at the colliding key.
    _map: list[list[tuple[K, V]]]
    _size: int
    _load_factor = 0.75  # Ratio of size:capacity before we grow the map's capacity.

    def __init__(self, /, capacity: int = 31):
        self._map = [[] for _ in range(capacity)]
        self._size = 0

    @classmethod
    def from_items(cls, items: Iterable[tuple[K, V]]) -> Self:
        hm = cls()
        for key, value in items:
            hm[key] = value
        return hm

    def pop(self, key: K) -> V:
        value = self[key]
        del self[key]
        return value

    def __getitem__(self, key: K) -> V:
        hashes, index = self._get(key)
        return hashes[index][1]

    def __setitem__(self, key: K, value: V) -> None:
        hashes = self._map[self._index(key)]
        index = linear_search(hashes, key, key=itemgetter(0))

        if index is None:
            hashes.append((key, value))
            self._size += 1
            if self._size >= Map._load_factor * self._capacity():
                self._grow()
        else:
            hashes[index] = (key, value)

    def __delitem__(self, key: K) -> None:
        hashes, index = self._get(key)
        hashes.pop(index)
        self._size -= 1

    def __iter__(self) -> Iterator[K]:
        yield from self.keys()

    def keys(self) -> Iterator[K]:
        for hashes in self._map:
            for key, _ in hashes:
                yield key

    def values(self) -> Iterator[V]:
        for hashes in self._map:
            for _, value in hashes:
                yield value

    def items(self) -> Iterator[tuple[K, V]]:
        for hashes in self._map:
            for item in hashes:
                yield item

    def _capacity(self) -> int:
        return len(self._map)

    def _index(self, key: K) -> int:
        return hash(key) % self._capacity()

    def _get(self, key: K) -> tuple[list[tuple[K, V]], int]:
        hashes = self._map[self._index(key)]
        index = linear_search(hashes, key, key=itemgetter(0))
        if index is None:
            raise KeyError("key not found in map")
        return hashes, index

    def _grow(self) -> None:
        items = list(self.items())
        self._map = [[] for _ in range(self._capacity() * 2 + 1)]
        self._size = 0

        for key, value in items:
            self[key] = value

    def __contains__(self, key: K) -> bool:
        """Return if a given key exists in the map.

        Args:
            key (K): The key to search for in the map.

        Returns:
            bool: True if the key is in the map. False, otherwise.
        """
        try:
            self._get(key)
        except KeyError:
            return False
        return True

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        """Returns true if the map has at least one entry.

        Returns:
            bool: True if the map has at least one entry. False, otherwise.
        """
        return len(self) > 0

    def __str__(self) -> str:
        return str(self._map)
