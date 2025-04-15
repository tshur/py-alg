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
        stack = ReverseLinkedList.from_iterable([1, 2, 3])

        reverse_algorithm(stack)
