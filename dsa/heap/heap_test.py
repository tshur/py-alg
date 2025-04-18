from .heap import Heap


class TestHeap:
    def test_empty_heap(self) -> None:
        heap = Heap[int]()

        assert heap.is_empty()
        assert len(heap) == 0

    def test_from_iterable(self) -> None:
        heap = Heap[int].from_iterable([7, 5, 1, 3, 9, 0, 4, 2, 8])

        heap_sorted = [heap.pop() for _ in range(len(heap))]

        assert heap_sorted == list(range(10))

    def test_push(self) -> None:
        heap = Heap[int]()

        # Push ascending values.
        heap.push(4)
        heap.push(6)
        heap.push(8)
        assert len(heap) == 3

        # Push at head.
        heap.push(2)
        heap.push(1)
        heap.push(0)
        assert len(heap) == 6

        # Push middle nodes.
        heap.push(5)
        heap.push(7)
        heap.push(9)
        heap.push(3)
        assert len(heap) == 10

        # Push repeated elements.
        heap.push(3)
        heap.push(3)
        heap.push(3)
        assert len(heap) == 13

        # Verify pop order.
        heap_sorted = [heap.pop() for _ in range(len(heap))]
        assert heap_sorted == [0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9]

    def test_pop(self) -> None:
        heap = Heap[int].from_iterable([0, 4, 5, 1, -2, 12, -1, 9, -1, -1])

        heap_sorted = [heap.pop() for _ in range(len(heap))]
        assert heap_sorted == [-2, -1, -1, -1, 0, 1, 4, 5, 9, 12]

    def test_peek(self) -> None:
        assert Heap[int].from_iterable([5, 1, 3, 2, 4]).peek() == 1
        assert Heap[int].from_iterable([5]).peek() == 5
        assert Heap[int].from_iterable([0, 4, 5, 1, -2, 12, -1, 9]).peek() == -2

    def test_pop_peek_on_empty(self) -> None:
        heap = Heap[int]()

        assert heap.peek() is None
        assert heap.pop() is None

    def test_full_push_pop(self) -> None:
        heap = Heap[int]()

        for value in [7, 5, 1, 3, 9, 0, 4, 2, 8]:
            heap.push(value)
        heap_sorted = [heap.pop() for _ in range(len(heap))]

        assert heap_sorted == list(range(10))
