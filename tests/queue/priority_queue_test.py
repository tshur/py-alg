from dsap.queue import PriorityQueue


class TestPriorityQueue:
    def test_empty_priority_queue(self) -> None:
        priority_queue = PriorityQueue[int]()

        assert priority_queue.is_empty()
        assert len(priority_queue) == 0

    def test_from_iterable(self) -> None:
        priority_queue = PriorityQueue[int].from_iterable(
            [7, 5, 1, 3, 9, 0, 4, 6, 2, 8]
        )

        assert list(priority_queue) == list(reversed(range(10)))

    def test_enqueue(self) -> None:
        priority_queue = PriorityQueue[int]()

        priority_queue.enqueue(4)
        assert priority_queue.peek() == 4
        priority_queue.enqueue(6)
        assert priority_queue.peek() == 6
        priority_queue.enqueue(8)
        assert priority_queue.peek() == 8
        assert len(priority_queue) == 3

        priority_queue.enqueue(2)
        priority_queue.enqueue(1)
        priority_queue.enqueue(0)
        assert priority_queue.peek() == 8
        assert len(priority_queue) == 6

        priority_queue.enqueue(5)
        priority_queue.enqueue(7)
        priority_queue.enqueue(9)
        priority_queue.enqueue(3)
        assert priority_queue.peek() == 9
        assert len(priority_queue) == 10

        priority_queue.enqueue(3)
        priority_queue.enqueue(3)
        priority_queue.enqueue(3)
        assert priority_queue.peek() == 9
        assert len(priority_queue) == 13

        # Verify priority queue order.
        assert list(priority_queue) == [
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            3,
            3,
            3,
            2,
            1,
            0,
        ]

    def test_dequeue(self) -> None:
        priority_queue = PriorityQueue[int].from_iterable(
            [0, 4, 5, 1, -2, 12, -1, 9, -1, -1]
        )

        assert priority_queue.dequeue() == 12
        assert priority_queue.dequeue() == 9
        assert priority_queue.dequeue() == 5
        assert priority_queue.dequeue() == 4
        assert priority_queue.dequeue() == 1
        assert priority_queue.dequeue() == 0
        assert priority_queue.dequeue() == -1
        assert priority_queue.dequeue() == -1
        assert priority_queue.dequeue() == -1
        assert priority_queue.dequeue() == -2

    def test_peek(self) -> None:
        assert PriorityQueue[int].from_iterable([5, 1, 3, 2, 4]).peek() == 5
        assert PriorityQueue[int].from_iterable([5]).peek() == 5
        assert (
            PriorityQueue[int].from_iterable([0, 4, 5, 1, -2, 12, -1, 9]).peek() == 12
        )

    def test_contains(self) -> None:
        priority_queue = PriorityQueue[int].from_iterable([5, 1, 3, 2, 4])

        assert 1 in priority_queue
        assert 2 in priority_queue
        assert 3 in priority_queue
        assert 4 in priority_queue
        assert 5 in priority_queue

        assert 0 not in priority_queue
        assert 6 not in priority_queue
        assert 10 not in priority_queue

    def test_dequeue_on_empty(self) -> None:
        priority_queue = PriorityQueue[int]()

        assert priority_queue.peek() is None
        assert priority_queue.dequeue() is None
        assert list(priority_queue) == []

    def test_full_enqueue_dequeue(self) -> None:
        priority_queue = PriorityQueue[int]()

        for value in [7, 5, 1, 3, 9, 0, 4, 6, 2, 8]:
            priority_queue.enqueue(value)

        assert [priority_queue.dequeue() for _ in range(10)] == list(
            reversed(range(10))
        )

    def test_large_priority_queue(self) -> None:
        priority_queue1 = PriorityQueue[int].from_iterable(range(100))
        assert list(priority_queue1) == list(reversed(range(100)))

        priority_queue2 = PriorityQueue[int]()
        for value in range(100):
            priority_queue2.enqueue(value)
        assert list(priority_queue2) == list(reversed(range(100)))

    def test_str(self) -> None:
        priority_queue = PriorityQueue[int].from_iterable([5, 1, 3, 2, 4])

        assert str(priority_queue) == "[5, 4, 3, 2, 1]"
