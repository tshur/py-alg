import pytest

from leetcode.stack.queue_with_stacks import QueueWithStacks


class TestQueueWithStacks:
    def test_empty(self) -> None:
        queue = QueueWithStacks()
        assert len(queue) == 0
        assert queue.is_empty()

        with pytest.raises(IndexError, match="peek called on empty queue"):
            queue.peek()
        with pytest.raises(IndexError, match="remove called on empty queue"):
            queue.remove()

    def test_from_iterable(self) -> None:
        queue = QueueWithStacks.from_iterable([1, 2, 3, 4, 5])

        assert len(queue) == 5
        assert not queue.is_empty()

        assert queue.peek() == 1

    def test_add(self) -> None:
        queue = QueueWithStacks()

        queue.add(1)
        assert len(queue) == 1
        assert queue.peek() == 1

        queue.add(2)
        assert len(queue) == 2
        assert queue.peek() == 1

        queue.add(30)
        assert len(queue) == 3
        assert queue.peek() == 1

    def test_remove(self) -> None:
        queue = QueueWithStacks.from_iterable([10, 20, 30])

        assert len(queue) == 3
        assert queue.peek() == 10
        assert queue.remove() == 10

        assert len(queue) == 2
        assert queue.peek() == 20
        assert queue.remove() == 20

        assert len(queue) == 1
        assert queue.peek() == 30
        assert queue.remove() == 30

    def test_peek(self) -> None:
        queue = QueueWithStacks.from_iterable([1])
        assert queue.peek() == 1

        empty_queue = QueueWithStacks()
        with pytest.raises(IndexError, match="peek called on empty queue"):
            empty_queue.peek()

    def test_alternate_add_remove(self) -> None:
        queue = QueueWithStacks.from_iterable([1, 2, 3])

        assert queue.remove() == 1

        queue.add(4)
        queue.add(5)
        assert queue.remove() == 2
        assert queue.peek() == 3

        queue.add(6)
        assert len(queue) == 4

        assert queue.remove() == 3
        assert queue.remove() == 4
        assert queue.remove() == 5
        assert queue.remove() == 6
        assert len(queue) == 0
