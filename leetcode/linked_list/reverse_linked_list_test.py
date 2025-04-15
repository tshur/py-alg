from typing import Callable

import pytest

from leetcode.linked_list.reverse_linked_list import ReverseLinkedList

pytestmark = pytest.mark.parametrize(
    "algorithm",
    [
        ReverseLinkedList.reverse_iterative,
        ReverseLinkedList.reverse_recursive,
    ],
)


class TestReverseLinkedList:
    def test_empty_list(
        self, algorithm: Callable[[ReverseLinkedList], None]
    ) -> None: ...
