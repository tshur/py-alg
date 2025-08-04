import pytest

from examples.leetcode.stack.queue_with_stacks import QueueWithStacks


class TestQueueWithStacks:
    def test_empty(self) -> None:
        queue = QueueWithStacks()
        assert len(queue) == 0
        assert queue.is_empty()

        with pytest.raises(IndexError, match="peek called on empty queue"):
            queue.peek()
        with pytest.raises(IndexError, match="remove called on empty queue"):
            queue.dequeue()

    def test_from_iterable(self) -> None:
        queue = QueueWithStacks.from_iterable([1, 2, 3, 4, 5])

        assert len(queue) == 5
        assert not queue.is_empty()

        assert queue.peek() == 1

    def test_add(self) -> None:
        queue = QueueWithStacks()

        queue.enqueue(1)
        assert len(queue) == 1
        assert queue.peek() == 1

        queue.enqueue(2)
        assert len(queue) == 2
        assert queue.peek() == 1

        queue.enqueue(30)
        assert len(queue) == 3
        assert queue.peek() == 1

    def test_remove(self) -> None:
        queue = QueueWithStacks.from_iterable([10, 20, 30])

        assert len(queue) == 3
        assert queue.peek() == 10
        assert queue.dequeue() == 10

        assert len(queue) == 2
        assert queue.peek() == 20
        assert queue.dequeue() == 20

        assert len(queue) == 1
        assert queue.peek() == 30
        assert queue.dequeue() == 30

    def test_peek(self) -> None:
        queue = QueueWithStacks.from_iterable([1])
        assert queue.peek() == 1

        empty_queue = QueueWithStacks()
        with pytest.raises(IndexError, match="peek called on empty queue"):
            empty_queue.peek()

    def test_alternate_add_remove(self) -> None:
        queue = QueueWithStacks.from_iterable([1, 2, 3])

        assert queue.dequeue() == 1

        queue.enqueue(4)
        queue.enqueue(5)
        assert queue.dequeue() == 2
        assert queue.peek() == 3

        queue.enqueue(6)
        assert len(queue) == 4

        assert queue.dequeue() == 3
        assert queue.dequeue() == 4
        assert queue.dequeue() == 5
        assert queue.dequeue() == 6
        assert len(queue) == 0
