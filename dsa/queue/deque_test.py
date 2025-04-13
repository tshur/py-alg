import pytest

from dsa.queue.deque import Deque


class TestDeque:
    def test_empty_deque(self) -> None:
        deque: Deque[int] = Deque()
        assert deque.is_empty()
        assert len(deque) == 0
        assert str(deque) == "[]"

    def test_from_iterable(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])
        assert not deque.is_empty()
        assert len(deque) == 3
        assert str(deque) == "[1, 2, 3]"

    def test_push_front(self) -> None:
        deque: Deque[int] = Deque()

        deque.push_front(1)
        assert len(deque) == 1
        assert str(deque) == "[1]"

        deque.push_front(2)
        assert len(deque) == 2
        assert str(deque) == "[2, 1]"

        deque.push_front(3)
        assert len(deque) == 3
        assert str(deque) == "[3, 2, 1]"

    def test_push_back(self) -> None:
        deque: Deque[int] = Deque()

        deque.push_back(1)
        assert len(deque) == 1
        assert str(deque) == "[1]"

        deque.push_back(2)
        assert len(deque) == 2
        assert str(deque) == "[1, 2]"

        deque.push_back(3)
        assert len(deque) == 3
        assert str(deque) == "[1, 2, 3]"

    def test_pop_front(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])

        assert deque.pop_front() == 1
        assert deque.pop_front() == 2
        assert deque.pop_front() == 3
        assert deque.pop_front() is None
        assert deque.pop_front() is None
        assert len(deque) == 0

    def test_pop_back(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])

        assert deque.pop_back() == 3
        assert deque.pop_back() == 2
        assert deque.pop_back() == 1
        assert deque.pop_back() is None
        assert deque.pop_back() is None
        assert len(deque) == 0

    def test_front(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])
        assert deque.front() == 1
        assert deque.front() == 1

        empty_deque: Deque[int] = Deque()
        assert empty_deque.front() is None

    def test_back(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])
        assert deque.back() == 3
        assert deque.back() == 3

        empty_deque: Deque[int] = Deque()
        assert empty_deque.back() is None

    def test_contains(self) -> None:
        deque = Deque.from_iterable([1, 2, 3])
        assert 1 in deque
        assert 2 in deque
        assert 3 in deque
        assert 4 not in deque
        assert 0 not in deque

        empty_deque: Deque[int | None] = Deque()
        assert 1 not in empty_deque
        assert None not in empty_deque

    def test_capacity_doubles(self) -> None:
        deque: Deque[int] = Deque(capacity=1)
        assert deque.capacity() == 1

        deque.push_back(1)
        assert len(deque) == 1
        assert deque.capacity() == 1

        deque.push_back(2)
        assert len(deque) == 2
        assert deque.capacity() == 2

        deque.push_back(3)
        assert len(deque) == 3
        assert deque.capacity() == 4

        deque.push_back(4)
        deque.push_back(5)
        assert len(deque) == 5
        assert deque.capacity() == 8

    def test_none_type(self) -> None:
        deque: Deque[int | None] = Deque()

        with pytest.raises(TypeError):
            deque.push_back(None)
        with pytest.raises(TypeError):
            deque.push_front(None)
        with pytest.raises(TypeError):
            deque = Deque.from_iterable([1, None, 3])
