from typing import Iterable, Iterator, Self


class Map[K, V]:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_items(cls, items: Iterable[tuple[K, V]]) -> Self:
        hm = cls()
        for key, value in items:
            hm[key] = value
        return hm

    def pop(self, key: K) -> V:
        raise NotImplementedError

    def __getitem__(self, key: K) -> V:
        raise NotImplementedError

    def __setitem__(self, key: K, value: V) -> None:
        raise NotImplementedError

    def __delitem__(self, key: K) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[K]:
        raise NotImplementedError

    def keys(self) -> Iterator[K]:
        raise NotImplementedError

    def values(self) -> Iterator[V]:
        raise NotImplementedError

    def items(self) -> Iterator[tuple[K, V]]:
        raise NotImplementedError

    def __contains__(self, key: K) -> bool:
        """Return if a given key exists in the map.

        Args:
            key (T): The key to search for in the map.

        Returns:
            bool: True if the key is in the map. False, otherwise.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __bool__(self) -> bool:
        """Returns true if the map has at least one entry.

        Returns:
            bool: True if the map has at least one entry. False, otherwise.
        """
        return len(self) > 0
