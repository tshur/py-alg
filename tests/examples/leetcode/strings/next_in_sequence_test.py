from typing import Callable

import pytest

from examples.leetcode.strings.next_in_sequence import (
    next_in_sequence_v1,
    next_in_sequence_v2,
)

pytestmark = pytest.mark.parametrize(
    "fn",
    [
        next_in_sequence_v1,
        next_in_sequence_v2,
    ],
)


class TestNextInSequence:
    def test_empty_input(self, fn: Callable[[str], str]):
        assert fn("") == ""

    def test_one_character(self, fn: Callable[[str], str]):
        assert fn("s") == "s"
        assert fn("a") == "a"

    def test_two_character(self, fn: Callable[[str], str]):
        assert fn("ab") == "ba"
        assert fn("ba") == "ab"

    def test_three_character(self, fn: Callable[[str], str]):
        assert fn("abc") == "acb"
        assert fn("acb") == "bac"
        assert fn("bac") == "bca"
        assert fn("bca") == "cab"
        assert fn("cab") == "cba"
        assert fn("cba") == "abc"

    def test_same_character(self, fn: Callable[[str], str]):
        assert fn("aaa") == "aaa"

        assert fn("aab") == "aba"
        assert fn("aba") == "baa"
        assert fn("baa") == "aab"

    def test_four_character(self, fn: Callable[[str], str]):
        assert fn("abcd") == "abdc"
        assert fn("dcba") == "abcd"

    def test_large_input(self, fn: Callable[[str], str]):
        assert fn("abcedda") == "abdacde"
