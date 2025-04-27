import pytest

from .map import Map


class TestMap:
    def test_empty_map(self) -> None:
        hm = Map[str, int]()

        assert not hm
        assert "a" not in hm
        assert len(hm) == 0
        assert str(hm) == ""
        assert list(hm) == []

    def test_from_items(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert len(hm) == 3
        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert hm["a"] == 1
        assert hm["b"] == 4
        assert hm["c"] == 3

    def test_set_item(self) -> None:
        hm = Map[str, int]()

        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        hm["b"] = 4

        assert len(hm) == 3
        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert hm["b"] == 4

    def test_get_item(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert hm["a"] == 1
        assert hm["b"] == 4
        assert hm["c"] == 3

        with pytest.raises(KeyError, match="key not found in map"):
            hm["d"]
        with pytest.raises(KeyError, match="key not found in map"):
            hm["1"]

    def test_del_item(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        del hm["a"]
        del hm["b"]

        assert len(hm) == 1
        with pytest.raises(KeyError, match="key not found in map"):
            hm["a"]
        with pytest.raises(KeyError, match="key not found in map"):
            hm["b"]

    def test_pop(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert hm.pop("a") == 1
        assert hm.pop("b") == 4
        assert len(hm) == 1

        with pytest.raises(KeyError, match="key not found in map"):
            hm["b"]

    def test_iter(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert list(sorted(hm)) == ["a", "b", "c"]
        assert list(sorted(hm.keys())) == ["a", "b", "c"]
        assert list(sorted(hm.values())) == [1, 3, 4]
        assert list(sorted(hm.items())) == [("a", 1), ("b", 4), ("c", 3)]

    def test_contains(self) -> None:
        hm = Map[str, int].from_items([("a", 1), ("b", 2), ("c", 3), ("b", 4)])

        assert "a" in hm
        assert "b" in hm
        assert "c" in hm
        assert "d" not in hm
        assert "1" not in hm
