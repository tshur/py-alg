from collections import deque

from src.dsap.queue import Deque


class TestBenchHeap:
    def test_builtin_deque(self, benchmark):  # type: ignore
        def fn():
            dq = deque[int]()

            for i in range(100):
                dq.appendleft(i)
            consumed = [dq.pop() for _ in range(len(dq))]

            assert consumed == list(range(100))

        benchmark(fn)

    def test_dsap_deque(self, benchmark):  # type: ignore
        def fn():
            dq = Deque[int]()

            for i in range(100):
                dq.push_front(i)
            consumed = [dq.pop_back() for _ in range(len(dq))]

            assert consumed == list(range(100))

        benchmark(fn)
