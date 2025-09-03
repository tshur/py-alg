import heapq

from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from dsap.heap import MinHeap


class TestBenchHeap:
    def test_builtin_heap(self, benchmark: BenchmarkFixture):
        def fn():
            heap = [7, 5, 1, 3, 9, 0, 4, 6, 2, 8]
            heapq.heapify(heap)
            consumed = [heapq.heappop(heap) for _ in range(len(heap))]

            assert consumed == list(range(10))

        benchmark(fn)

    def test_dsap_heap(self, benchmark: BenchmarkFixture):
        def fn():
            heap = MinHeap[int]().from_iterable([7, 5, 1, 3, 9, 0, 4, 6, 2, 8])

            assert list(heap.consume_all()) == list(range(10))

        benchmark(fn)
