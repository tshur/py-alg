from dsap.queue import Deque


class TestDeque:
    def test_empty_deque(self) -> None:
        deque = Deque[int]()
        assert deque.is_empty()
        assert len(deque) == 0
        assert str(deque) == "[]"

    def test_from_iterable(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])
        assert not deque.is_empty()
        assert len(deque) == 3
        assert str(deque) == "[1, 2, 3]"

    def test_push_front(self) -> None:
        deque = Deque[int]()

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
        deque = Deque[int]()
        assert str(deque) == "[]"

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
        deque = Deque[int].from_iterable([1, 2, 3])

        assert deque.pop_front() == 1
        assert str(deque) == "[2, 3]"
        assert deque.pop_front() == 2
        assert str(deque) == "[3]"
        assert deque.pop_front() == 3
        assert str(deque) == "[]"
        assert deque.pop_front() is None
        assert deque.pop_front() is None
        assert len(deque) == 0
        assert str(deque) == "[]"

    def test_pop_back(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])

        assert deque.pop_back() == 3
        assert str(deque) == "[1, 2]"
        assert deque.pop_back() == 2
        assert str(deque) == "[1]"
        assert deque.pop_back() == 1
        assert str(deque) == "[]"
        assert deque.pop_back() is None
        assert deque.pop_back() is None
        assert len(deque) == 0
        assert str(deque) == "[]"

    def test_front(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])
        assert deque.front() == 1
        assert deque.front() == 1

        empty_deque = Deque[int]()
        assert empty_deque.front() is None

    def test_back(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])
        assert deque.back() == 3
        assert deque.back() == 3

        empty_deque = Deque[int]()
        assert empty_deque.back() is None

    def test_iter(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])

        assert list(deque) == [1, 2, 3]
        assert len(deque) == 3

        empty_deque = Deque[int]()
        assert list(empty_deque) == []

    def test_contains(self) -> None:
        deque = Deque[int].from_iterable([1, 2, 3])
        assert 1 in deque
        assert 2 in deque
        assert 3 in deque
        assert 4 not in deque
        assert 0 not in deque

        empty_deque = Deque[int | None]()
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

        deque.push_front(3)
        assert len(deque) == 3
        assert deque.capacity() == 4

        deque.push_front(4)
        deque.push_back(5)
        assert len(deque) == 5
        assert deque.capacity() == 8

    def test_reinserts(self) -> None:
        deque = Deque[int | None](capacity=3)
        for value in [1, 2, 3]:
            deque.push_back(value)
        assert len(deque) == 3
        assert deque.capacity() == 3
        assert str(deque) == "[1, 2, 3]"

        # Test re-inserting the same element.
        for _ in range(10):
            deque.push_back(deque.pop_back())
        for _ in range(10):
            deque.push_front(deque.pop_front())
        assert len(deque) == 3
        assert deque.capacity() == 3
        assert str(deque) == "[1, 2, 3]"
        assert list(deque) == [1, 2, 3]

        # Test rotating right.
        for _ in range(8):
            deque.push_front(deque.pop_back())
        assert len(deque) == 3
        assert deque.capacity() == 3

        # Test rotating left.
        for _ in range(16):
            deque.push_back(deque.pop_front())
        assert len(deque) == 3
        assert deque.capacity() == 3
