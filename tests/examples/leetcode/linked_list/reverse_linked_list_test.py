from typing import Callable

import pytest

from examples.leetcode.linked_list.reverse_linked_list import ReverseLinkedList

pytestmark = pytest.mark.parametrize(
    "reverse_algorithm",
    [
        ReverseLinkedList.reverse_iterative,
        ReverseLinkedList.reverse_recursive,
    ],
)


class TestReverseLinkedList:
    def test_empty_list(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([])

        reverse_algorithm(linked_list)

        assert len(linked_list) == 0
        assert str(linked_list) == "None"

    def test_single_element(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([1])

        reverse_algorithm(linked_list)

        assert len(linked_list) == 1
        assert str(linked_list) == "1->None"

    def test_two_element(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([1, 2])

        reverse_algorithm(linked_list)

        assert len(linked_list) == 2
        assert str(linked_list) == "2->1->None"

    def test_full_list(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(linked_list)

        assert len(linked_list) == 5
        assert str(linked_list) == "5->4->3->2->1->None"

    def test_two_reverses(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(linked_list)
        reverse_algorithm(linked_list)

        assert len(linked_list) == 5
        assert str(linked_list) == "1->2->3->4->5->None"

    def test_valid_head_and_tail(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        linked_list = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(linked_list)

        assert len(linked_list) == 5
        assert str(linked_list) == "5->4->3->2->1->None"

        linked_list.push_head(6)
        linked_list.push_tail(0)
        assert len(linked_list) == 7
        assert str(linked_list) == "6->5->4->3->2->1->0->None"
