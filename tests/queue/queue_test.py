from dsap.queue import Queue


class TestQueue:
    def test_empty_queue(self) -> None:
        queue = Queue[int]()
        assert queue.is_empty()
        assert len(queue) == 0
        assert str(queue) == "[]"

    def test_from_iterable(self) -> None:
        queue = Queue[int].from_iterable([1, 2, 3])
        assert not queue.is_empty()
        assert len(queue) == 3
        assert str(queue) == "[1, 2, 3]"

    def test_enqueue(self) -> None:
        queue = Queue[int]()
        assert str(queue) == "[]"

        queue.enqueue(1)
        assert len(queue) == 1
        assert str(queue) == "[1]"

        queue.enqueue(2)
        assert len(queue) == 2
        assert str(queue) == "[1, 2]"

        queue.enqueue(3)
        assert len(queue) == 3
        assert str(queue) == "[1, 2, 3]"

    def test_dequeue(self) -> None:
        queue = Queue[int].from_iterable([1, 2, 3])

        assert queue.dequeue() == 1
        assert str(queue) == "[2, 3]"
        assert queue.dequeue() == 2
        assert str(queue) == "[3]"
        assert queue.dequeue() == 3
        assert str(queue) == "[]"
        assert queue.dequeue() is None
        assert queue.dequeue() is None
        assert len(queue) == 0
        assert str(queue) == "[]"

    def test_peek(self) -> None:
        queue = Queue[int].from_iterable([1, 2, 3])
        assert queue.peek() == 1
        assert queue.peek() == 1

        empty_queue = Queue[int]()
        assert empty_queue.peek() is None

    def test_iter(self) -> None:
        queue = Queue[int].from_iterable([1, 2, 3])

        assert list(queue) == [1, 2, 3]
        assert len(queue) == 3

        empty_queue = Queue[int]()
        assert list(empty_queue) == []

    def test_contains(self) -> None:
        queue = Queue[int].from_iterable([1, 2, 3])
        assert 1 in queue
        assert 2 in queue
        assert 3 in queue
        assert 4 not in queue
        assert 0 not in queue

        empty_queue = Queue[int | None]()
        assert 1 not in empty_queue
        assert None not in empty_queue
