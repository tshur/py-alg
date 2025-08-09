import pytest

from dsap.hash import Set
from dsap.sort import sort


class TestSet:
    def test_empty_set(self) -> None:
        s = Set[int]()

        assert not s
        assert 1 not in s
        assert len(s) == 0
        assert list(s) == []

    def test_from_iterable(self) -> None:
        s = Set[int].from_iterable([1, 2, 3])

        assert len(s) == 3
        assert 1 in s
        assert 2 in s
        assert 3 in s

    def test_add(self) -> None:
        s = Set[int]()

        s.add(1)
        s.add(2)
        s.add(3)
        s.add(4)
        s.add(1)
        s.add(1)

        assert len(s) == 4
        assert 1 in s
        assert 2 in s
        assert 3 in s
        assert 4 in s

    def test_remove(self) -> None:
        s = Set[int].from_iterable([1, 2, 3, 4])

        s.remove(1)
        s.remove(4)
        assert len(s) == 2

        with pytest.raises(KeyError, match="key not found in map"):
            s.remove(4)
        with pytest.raises(KeyError, match="key not found in map"):
            s.remove(5)

    def test_iter(self) -> None:
        s = Set[int].from_iterable([1, 4, 2, 3, 4])

        assert list(sort(s)) == [1, 2, 3, 4]

    def test_contains(self) -> None:
        s = Set[int].from_iterable([1, 2, 3, 4])

        assert 1 in s
        assert 2 in s
        assert 3 in s
        assert 4 in s
        assert 0 not in s
        assert 5 not in s

    def test_duplicates(self) -> None:
        s = Set[int].from_iterable([1, 2, 3, 4, 1, 3, 2, 1, 2, 2, 1, 1])

        assert len(s) == 4
        assert list(sort(s)) == [1, 2, 3, 4]
