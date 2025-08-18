import pytest

from dsap.hash import Map, MapLinkedList, MapList
from dsap.hash.map import MapBase
from dsap.sort import sort

pytestmark = pytest.mark.parametrize(
    "cls",
    [Map, MapList, MapLinkedList],
)


class TestMap:
    def test_empty_map(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls()

        assert not hm
        assert "a" not in hm
        assert len(hm) == 0
        assert list(hm) == []

    def test_from_items(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert len(hm) == 3
        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert hm["a"] == 1
        assert hm["b"] == 4
        assert hm["c"] == 3

    def test_set_item(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls()

        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        hm["b"] = 4

        assert len(hm) == 3
        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert hm["b"] == 4

    def test_get_item(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert hm["a"] == 1
        assert hm["b"] == 4
        assert hm["c"] == 3

        with pytest.raises(KeyError, match="key not found in map"):
            hm["d"]
        with pytest.raises(KeyError, match="key not found in map"):
            hm["1"]

    def test_del_item(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        del hm["a"]
        del hm["b"]

        assert len(hm) == 1
        with pytest.raises(KeyError, match="key not found in map"):
            hm["a"]
        with pytest.raises(KeyError, match="key not found in map"):
            hm["b"]

    def test_pop(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert hm.pop("a") == 1
        assert hm.pop("b") == 4
        assert len(hm) == 1

        with pytest.raises(KeyError, match="key not found in map"):
            hm["b"]

    def test_iter(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert list(sort(hm)) == ["a", "b", "c"]
        assert list(sort(hm.keys())) == ["a", "b", "c"]
        assert list(sort(hm.values())) == [1, 3, 4]
        assert list(sort(hm.items())) == [("a", 1), ("b", 4), ("c", 3)]

    def test_contains(self, cls: type[MapBase[str, int]]) -> None:
        hm = cls.from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert "d" not in hm
        assert "1" not in hm

    def test_grow(self, cls: type[MapBase[str, int]]) -> None:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        hm = cls(capacity=1)

        for i, ch in enumerate(alphabet):
            hm[ch] = i

        assert len(hm) == 26
        assert list(sort(hm)) == list(alphabet)
        assert list(sort(hm.items())) == [(ch, i) for i, ch in enumerate(alphabet)]
