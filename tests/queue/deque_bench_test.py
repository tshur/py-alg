from collections import deque

from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from dsap.queue import Deque


class TestBenchHeap:
    def test_builtin_deque(self, benchmark: BenchmarkFixture):
        def fn():
            dq = deque[int]()

            for i in range(100):
                dq.appendleft(i)
            consumed = [dq.pop() for _ in range(len(dq))]

            assert consumed == list(range(100))

        benchmark(fn)

    def test_dsap_deque(self, benchmark: BenchmarkFixture):
        def fn():
            dq = Deque[int]()

            for i in range(100):
                dq.push_front(i)
            consumed = [dq.pop_back() for _ in range(len(dq))]

            assert consumed == list(range(100))

        benchmark(fn)
