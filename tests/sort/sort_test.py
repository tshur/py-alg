from typing import Callable, Iterable
from random import shuffle

import pytest

from dsap.sort import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    sort,
    tim_sort,
    tree_sort,
)
from dsap.type import SupportsRichComparison

pytestmark = pytest.mark.parametrize(
    "sort_algorithm",
    [
        bubble_sort,
        heap_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
        selection_sort,
        sort,
        tim_sort,
        tree_sort,
    ],
)


class TestSortAlgorithms:
    def test_simple_array(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([5, 1, 3, 2, 4]) == [1, 2, 3, 4, 5]
        assert sort_algorithm([5, 5, 2, 1, 2, 1, 1]) == [1, 1, 1, 2, 2, 5, 5]

    def test_near_sorted(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([1, 2, 3, 4, 5])
        assert sort_algorithm([5, 4, 3, 2, 1])
        assert sort_algorithm([1, 3, 2, 4, 5])

    def test_equal_values(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def test_larger_input(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm(
            [10, 4, 12, 11, 9, 13, 2, 6, 19, 0, 17, 3, 8, 18, 14, 16, 7, 15, 5, 1]
        ) == list(range(20))
    
    def test_extra_larger_input(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm(
            [101, 78, 55, 11, 64, 4, 93, 29, 120, 88, 37, 7, 106, 50, 81, 115, 69,
            42, 98, 21, 0, 60, 33, 73, 16, 91, 125, 47, 83, 110, 2, 58, 96, 39,
            118, 67, 13, 86, 25, 103, 53, 76, 31, 113, 9, 62, 99, 44, 80, 123, 19,
            71, 108, 35, 94, 27, 51, 116, 65, 1, 48, 84, 12, 100, 38, 79, 23, 111,
            56, 89, 127, 41, 105, 17, 74, 30, 97, 6, 68, 119, 46, 82, 122, 14, 102,
            3, 61, 92, 28, 77, 126, 52, 114, 36, 85, 20, 66, 10, 95, 49, 121, 5, 72,
            32, 109, 59, 18, 87, 24, 117, 43, 104, 70, 8, 63, 15, 124, 34, 90, 57,
            26, 75, 112, 45, 107, 22, 54, 40]
        ) == list(range(128))

    def test_non_numeric_types(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm(["c", "a", "bb", "ba"]) == ["a", "ba", "bb", "c"]

    def test_empty_input(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([]) == []

    def test_single_value(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([1]) == [1]
