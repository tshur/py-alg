from typing import Callable

import pytest

from leetcode.linked_list.reverse_linked_list import ReverseLinkedList

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
        stack = ReverseLinkedList.from_iterable([])

        reverse_algorithm(stack)

        assert len(stack) == 0
        assert str(stack) == "None"

    def test_single_element(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        stack = ReverseLinkedList.from_iterable([1])

        reverse_algorithm(stack)

        assert len(stack) == 1
        assert str(stack) == "1->None"

    def test_two_element(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        stack = ReverseLinkedList.from_iterable([1, 2])

        reverse_algorithm(stack)

        assert len(stack) == 2
        assert str(stack) == "2->1->None"

    def test_full_list(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        stack = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(stack)

        assert len(stack) == 5
        assert str(stack) == "5->4->3->2->1->None"

    def test_two_reverses(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        stack = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(stack)
        reverse_algorithm(stack)

        assert len(stack) == 5
        assert str(stack) == "1->2->3->4->5->None"

    def test_valid_head_and_tail(
        self, reverse_algorithm: Callable[[ReverseLinkedList], None]
    ) -> None:
        stack = ReverseLinkedList.from_iterable([1, 2, 3, 4, 5])

        reverse_algorithm(stack)

        assert len(stack) == 5
        assert str(stack) == "5->4->3->2->1->None"

        stack.push_head(6)
        stack.push_tail(0)
        assert len(stack) == 7
        assert str(stack) == "6->5->4->3->2->1->0->None"
