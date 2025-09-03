from itertools import repeat
from random import seed, shuffle

import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from dsap.sort import (
    SortAlgorithm,
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    tim_sort,
    tree_sort,
)

pytestmark = pytest.mark.parametrize(
    "sort_algorithm",
    [
        bubble_sort,
        heap_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
        selection_sort,
        tim_sort,
        tree_sort,
        sorted,
    ],
)


class TestBenchSort:
    def setup_method(self):
        seed(42)  # So that all benchmarks shuffle the same ways.

    @pytest.mark.benchmark(group="sort_sm")
    def test_sort_sm(self, benchmark: BenchmarkFixture, sort_algorithm: SortAlgorithm):
        def fn():
            assert list(sort_algorithm(repeat(0, 10))) == list(repeat(0, 10))
            assert list(sort_algorithm(range(10))) == list(range(10))
            assert list(sort_algorithm([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(
                range(10)
            )

        benchmark(fn)

    @pytest.mark.benchmark(group="sort_lg")
    def test_sort_lg(self, benchmark: BenchmarkFixture, sort_algorithm: SortAlgorithm):
        def fn():
            assert list(sort_algorithm(repeat(0, 800))) == list(repeat(0, 800))
            assert list(sort_algorithm(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(sort_algorithm(nums)) == list(range(800))

        benchmark(fn)
