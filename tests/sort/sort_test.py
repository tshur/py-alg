from typing import Callable, Iterable

import pytest

from src.dsap.typing import SupportsRichComparison

from src.dsap.sort import heap_sort, insertion_sort, selection_sort, tree_sort

pytestmark = pytest.mark.parametrize(
    "sort_algorithm",
    [
        heap_sort,
        insertion_sort,
        selection_sort,
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
        assert sort_algorithm([1, 1, 1]) == [1, 1, 1]

    def test_near_sorted(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm([1, 2, 3, 4, 5])
        assert sort_algorithm([5, 4, 3, 2, 1])
        assert sort_algorithm([1, 3, 2, 4, 5])

    def test_larger_input(
        self,
        sort_algorithm: Callable[
            [Iterable[SupportsRichComparison]], list[SupportsRichComparison]
        ],
    ) -> None:
        assert sort_algorithm(
            [10, 4, 12, 11, 9, 13, 2, 6, 19, 0, 17, 3, 8, 18, 14, 16, 7, 15, 5, 1]
        ) == list(range(20))

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
