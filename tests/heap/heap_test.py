from dsap.heap import MaxHeap, MinHeap


class TestMinHeap:
    def test_empty_heap(self) -> None:
        heap = MinHeap[int]()

        assert heap.is_empty()
        assert len(heap) == 0

    def test_from_iterable(self) -> None:
        heap = MinHeap[int].from_iterable([7, 5, 1, 3, 9, 0, 4, 6, 2, 8])

        assert list(heap.consume_all()) == list(range(10))

    def test_push(self) -> None:
        heap = MinHeap[int]()

        # Push ascending values.
        heap.push(4)
        heap.push(6)
        heap.push(8)
        assert heap.peek() == 4
        assert len(heap) == 3

        # Push at head.
        heap.push(2)
        assert heap.peek() == 2
        heap.push(1)
        assert heap.peek() == 1
        heap.push(0)
        assert heap.peek() == 0
        assert len(heap) == 6

        # Push middle nodes.
        heap.push(5)
        heap.push(7)
        heap.push(9)
        heap.push(3)
        assert heap.peek() == 0
        assert len(heap) == 10

        # Push repeated elements.
        heap.push(3)
        heap.push(3)
        heap.push(3)
        assert heap.peek() == 0
        assert len(heap) == 13

        # Verify pop order.
        assert list(heap.consume_all()) == [0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9]

    def test_pop(self) -> None:
        heap = MinHeap[int].from_iterable([0, 4, 5, 1, -2, 12, -1, 9, -1, -1])

        assert list(heap.consume_all()) == [-2, -1, -1, -1, 0, 1, 4, 5, 9, 12]

    def test_peek(self) -> None:
        assert MinHeap[int].from_iterable([5, 1, 3, 2, 4]).peek() == 1
        assert MinHeap[int].from_iterable([5]).peek() == 5
        assert MinHeap[int].from_iterable([0, 4, 5, 1, -2, 12, -1, 9]).peek() == -2

    def test_contains(self) -> None:
        heap = MinHeap[int].from_iterable([5, 1, 3, 2, 4])

        assert 1 in heap
        assert 2 in heap
        assert 3 in heap
        assert 4 in heap
        assert 5 in heap

        assert 0 not in heap
        assert 6 not in heap
        assert 10 not in heap

    def test_remove_on_empty(self) -> None:
        heap = MinHeap[int]()

        assert heap.peek() is None
        assert heap.pop() is None
        assert list(heap.consume_all()) == []

    def test_full_push_pop(self) -> None:
        heap = MinHeap[int]()

        for value in [7, 5, 1, 3, 9, 0, 4, 6, 2, 8]:
            heap.push(value)

        assert list(heap.consume_all()) == list(range(10))

    def test_large_heap(self) -> None:
        heap1 = MinHeap[int].from_iterable(range(100))
        assert list(heap1.consume_all()) == list(range(100))

        heap2 = MinHeap[int]()
        for value in range(100):
            heap2.push(value)
        assert list(heap2.consume_all()) == list(range(100))


class TestMaxHeap:
    def test_empty_heap(self) -> None:
        heap = MaxHeap[int]()

        assert heap.is_empty()
        assert len(heap) == 0

    def test_from_iterable(self) -> None:
        heap = MaxHeap[int].from_iterable([7, 5, 1, 3, 9, 0, 4, 6, 2, 8])

        assert list(heap.consume_all()) == list(reversed(range(10)))

    def test_full_push_pop(self) -> None:
        heap = MaxHeap[int]()

        for value in [7, 5, 1, 3, 9, 0, 4, 6, 2, 8]:
            heap.push(value)

        assert list(heap.consume_all()) == list(reversed(range(10)))

    def test_large_heap(self) -> None:
        heap1 = MaxHeap[int].from_iterable(range(100))
        assert list(heap1.consume_all()) == list(reversed(range(100)))

        heap2 = MaxHeap[int]()
        for value in range(100):
            heap2.push(value)
        assert list(heap2.consume_all()) == list(reversed(range(100)))
