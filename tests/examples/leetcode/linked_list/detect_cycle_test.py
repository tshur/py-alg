from typing import Callable

import pytest

from examples.leetcode.linked_list.detect_cycle import DetectCycle

pytestmark = pytest.mark.parametrize(
    "has_cycle_algorithm",
    [
        DetectCycle.hash_set,
        DetectCycle.fast_slow,
    ],
)


class TestDetectCycle:
    def test_empty_list(
        self, has_cycle_algorithm: Callable[[DetectCycle], bool]
    ) -> None:
        linked_list = DetectCycle.from_iterable([])

        assert not has_cycle_algorithm(linked_list)
        with pytest.raises(IndexError, match="index out of bounds"):
            linked_list.create_cycle(0)
        with pytest.raises(IndexError, match="index out of bounds"):
            linked_list.create_cycle(4)

    def test_single_element(
        self, has_cycle_algorithm: Callable[[DetectCycle], bool]
    ) -> None:
        linked_list = DetectCycle.from_iterable([1])

        assert not has_cycle_algorithm(linked_list)
        linked_list.create_cycle(0)
        assert has_cycle_algorithm(linked_list)

    def test_two_element(
        self, has_cycle_algorithm: Callable[[DetectCycle], bool]
    ) -> None:
        linked_list = DetectCycle.from_iterable([1, 2])

        assert not has_cycle_algorithm(linked_list)
        linked_list.create_cycle(0)
        assert has_cycle_algorithm(linked_list)
        linked_list.create_cycle(1)
        assert has_cycle_algorithm(linked_list)

    def test_full_list(
        self, has_cycle_algorithm: Callable[[DetectCycle], bool]
    ) -> None:
        linked_list = DetectCycle.from_iterable([1, 2, 3, 4, 5])

        assert not has_cycle_algorithm(linked_list)
        linked_list.create_cycle(0)
        assert has_cycle_algorithm(linked_list)
        linked_list.create_cycle(1)
        assert has_cycle_algorithm(linked_list)
        linked_list.create_cycle(2)
        assert has_cycle_algorithm(linked_list)
        linked_list.create_cycle(3)
        assert has_cycle_algorithm(linked_list)
        linked_list.create_cycle(4)
        assert has_cycle_algorithm(linked_list)
