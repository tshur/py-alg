from itertools import repeat
from random import seed, shuffle

from src.dsap.sort import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    sort,
    tree_sort,
    tim_sort,
)


class TestBenchHeap:
    def setup_method(self):
        seed(42)  # So that all benchmarks shuffle the same ways.

    def test_builtin_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(sorted(repeat(0, 10))) == list(repeat(0, 10))
            assert list(sorted(range(10))) == list(range(10))
            assert list(sorted([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_builtin_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(sorted(repeat(0, 800))) == list(repeat(0, 800))
            assert list(sorted(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(sorted(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(sort(range(10))) == list(range(10))
            assert list(sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_bubble_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(bubble_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(bubble_sort(range(10))) == list(range(10))
            assert list(bubble_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_bubble_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(bubble_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(bubble_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(bubble_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_heap_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(heap_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(heap_sort(range(10))) == list(range(10))
            assert list(heap_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_heap_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(heap_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(heap_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(heap_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_insertion_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(insertion_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(insertion_sort(range(10))) == list(range(10))
            assert list(insertion_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(
                range(10)
            )

        benchmark(fn)

    def test_dsap_insertion_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(insertion_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(insertion_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(insertion_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_merge_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(merge_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(merge_sort(range(10))) == list(range(10))
            assert list(merge_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_merge_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(merge_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(merge_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(merge_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_quick_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(quick_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(quick_sort(range(10))) == list(range(10))
            assert list(quick_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_quick_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(quick_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(quick_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(quick_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_selection_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(selection_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(selection_sort(range(10))) == list(range(10))
            assert list(selection_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(
                range(10)
            )

        benchmark(fn)

    def test_dsap_selection_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(selection_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(selection_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(selection_sort(nums)) == list(range(800))

        benchmark(fn)

    def test_dsap_tree_sort_sm(self, benchmark):  # type: ignore
        def fn():
            assert list(tree_sort(repeat(0, 10))) == list(repeat(0, 10))
            assert list(tree_sort(range(10))) == list(range(10))
            assert list(tree_sort([7, 3, 1, 4, 5, 0, 9, 6, 2, 8])) == list(range(10))

        benchmark(fn)

    def test_dsap_tree_sort_lg(self, benchmark):  # type: ignore
        def fn():
            assert list(tree_sort(repeat(0, 800))) == list(repeat(0, 800))
            assert list(tree_sort(range(800))) == list(range(800))

            nums = list(range(800))
            shuffle(nums)
            assert list(tree_sort(nums)) == list(range(800))

        benchmark(fn)
