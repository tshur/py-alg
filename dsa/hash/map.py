from operator import itemgetter
from typing import Iterable, Iterator, Self

from dsa.search import linear_search


class Map[K, V]:
    """HashMap data structure implemented using a list per bucket for collisions.

    Instead of probing for collisions, we simply aggregate values into a list. We could
    change the internal data structure from list to linked list or binary search tree
    for potential efficiency improvements.

    Basic operations:
     - __setitem__, in ~O(1), but really O(k) where k is the length of collided values.
         Worst case, this is O(n) due to rehashing, but this is amortized.
     - __getitem__, in ~O(1), but really O(k) where k is the length of collided values.
     - pop, in ~O(1), but really O(k) where k is the length of collided values.
     - __iter__ (and variants), in ~O(n).
    """

    # We handle hash collisions simply by extending the list at the colliding key.
    _buckets: list[list[tuple[K, V]]]
    _size: int
    _load_factor = 0.75  # Ratio of size:capacity before we grow the map's capacity.

    def __init__(self, /, capacity: int = 31):
        """Create a new (empty) map.

        Args:
            capacity (int, optional): Give a custom capacity to initialize the map. This
              value should be prime to maximize performance. Defaults to 31.
        """
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    @classmethod
    def from_items(cls, items: Iterable[tuple[K, V]]) -> Self:
        """Create (and return) a new hash map from an iterable of (key, value) pairs.

        Args:
            items (Iterable[tuple[K, V]]): An iterable of (key, value) pairs to add into
              the newly created map.

        Returns:
            Self: The newly created object.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> list(sorted(hm.items()))
            [('a', 1), ('b', 2), ('c', 3)]
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

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> hm.pop('b')
            2
            >>> 'b' in hm
            False
        """
        value = self[key]
        del self[key]
        return value

    def __getitem__(self, key: K) -> V:
        """Return the value at self[key] without modifying the map.

        Args:
            key (K): The key of the desired item to get.

        Raises:
            KeyError: If the key is not found in the map.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> hm['a']
            1
            >>> hm['b']
            2
        """
        bucket, index = self._get(key)
        return bucket[index][1]

    def __setitem__(self, key: K, value: V) -> None:
        """Sets self[key] to value.

        Adds a new (key, value) entry if the key does not exist. If the key does exist,
        the value will be updated (and the old value discarded).

        Args:
            key (K): The key to add/set.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> hm['a'] = 4
            >>> hm['a']
            4
            >>> hm['d'] = 5
            >>> hm['d']
            5
        """
        bucket = self._buckets[self._hash(key)]
        index = linear_search(bucket, key, key=itemgetter(0))

        if index is None:
            bucket.append((key, value))
            self._size += 1
            if self._size >= Map._load_factor * self._capacity():
                self._grow()
        else:
            bucket[index] = (key, value)

    def __delitem__(self, key: K) -> None:
        """Delete the entry at self[key].

        Args:
            key (K): The key to find and delete.

        Raises:
            KeyError: If the key is not found in the map.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> del hm['a']
            >>> 'a' in hm
            False
        """
        bucket, index = self._get(key)
        bucket.pop(index)
        self._size -= 1

    def __iter__(self) -> Iterator[K]:
        """Yields keys stored in the map (in an arbitrary order).

        Equivalent to self.keys().

        Yields:
            Iterator[K]: Keys in the map.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> list(sorted(hm.keys()))
            ['a', 'b', 'c']
        """
        yield from self.keys()

    def keys(self) -> Iterator[K]:
        """Yields keys stored in the map (in an arbitrary order).

        Yields:
            Iterator[K]: Keys in the map.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> list(sorted(hm.keys()))
            ['a', 'b', 'c']
        """
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def values(self) -> Iterator[V]:
        """Yields values stored in the map (in an arbitrary order).

        Yields:
            Iterator[V]: Values in the map.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> list(sorted(hm.values()))
            [1, 2, 3]
        """
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def items(self) -> Iterator[tuple[K, V]]:
        """Yields (key, value) items stored in the map (in an arbitrary order).

        Yields:
            Iterator[tuple[K, V]]: Entries as (key, value) pairs.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> list(sorted(hm.items()))
            [('a', 1), ('b', 2), ('c', 3)]
        """
        for bucket in self._buckets:
            for item in bucket:
                yield item

    def _capacity(self) -> int:
        """The total capacity of the hash map (i.e., the number of hashable buckets)."""
        return len(self._buckets)

    def _hash(self, key: K) -> int:
        """The bucket index of the keyed item, based on its hash."""
        return hash(key) % self._capacity()

    def _get(self, key: K) -> tuple[list[tuple[K, V]], int]:
        """Get the (bucket, index) of the item at the given key.

        To get the item, we must find the correct bucket via hashed key. Then, we need
        to iterate through the collisions in the bucket to match the key exactly.

        Args:
            key (K): The key to search for.

        Raises:
            KeyError: If the key is not found in the map.

        Returns:
            tuple[list[tuple[K, V]], int]: (bucket, index) tuple representing the found
              entry. The entry is at bucket[index].
        """
        bucket = self._buckets[self._hash(key)]
        index = linear_search(bucket, key, key=itemgetter(0))
        if index is None:
            raise KeyError("key not found in map")
        return bucket, index

    def _grow(self) -> None:
        """Grow the capacity of the map to be roughly double. All items are rehashed.

        When growing the hashmap, we ideally would like the new capacity to be prime.
        This would prevent cycles and improve the effective capacity of the hashmap.

        However, we do a naive algorithm to double and add one. We start (default) with
        the prime 31, so we will always be one less than a power of 2. This gives us a
        chance to use mersenne primes (but at least odd values).

        Complexity:
            Time: O(n) to get, then rehash all items into the bigger bucket.
            Space: O(n) due to storing a copy of items before rehashing.
        """
        items = list(self.items())
        self._buckets = [[] for _ in range(self._capacity() * 2 + 1)]
        self._size = 0

        for key, value in items:
            self[key] = value

    def __contains__(self, key: K) -> bool:
        """Return if a given key exists in the map.

        Args:
            key (K): The key to search for in the map.

        Returns:
            bool: True if the key is in the map. False, otherwise.

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> 'b' in hm
            True
            >>> 'd' in hm
            False
        """
        try:
            self._get(key)
        except KeyError:
            return False
        return True

    def __len__(self) -> int:
        """Return the number of entries in the map.

        Returns:
            int: The number of entries in the map (size, not capacity).

        Examples:
            >>> hm = Map.from_items([('a', 1), ('b', 2), ('c', 3)])
            >>> len(hm)
            3
        """
        return self._size

    def __bool__(self) -> bool:
        """Returns true if the map has at least one entry.

        Returns:
            bool: True if the map has at least one entry. False, otherwise.

        Examples:
            >>> bool(Map.from_items([('a', 1), ('b', 2), ('c', 3)]))
            True
            >>> bool(Map())
            False
        """
        return len(self) > 0
