"""Find the next sequence arrangement in lexicographical order.

https://bytebytego.com/exercises/coding-patterns/two-pointers/next-lexicographical-sequence
"""

from itertools import permutations
from typing import Optional

from dsap.iterable import reverse
from dsap.sort import sort


def next_in_sequence_v1(s: str) -> str:
    """Brute force method: Generate all unique permutations and sort them.

    Method: next_in_sequence('aab')?
        1. Find all permutations (`''.join(...)` into string format).
        2. Unique-ify the permutations.
        3. Sort the unique permutations.
        4. Find the index of our given input `s`.
        5. Return the immediate next element after `s`.

    Runtime: (suppose n is the length of the input string)
        Time: O(n!log(n!))
        Space: O(n!)

    Args:
        s (str): Input sequence as a string.

    Returns:
        str: Next sequence arrangement in lexicographical order.
    """

    unique_permutations = set("".join(perm) for perm in permutations(s))
    ordered_perms = sort(unique_permutations)

    i = ordered_perms.index(s)
    return ordered_perms[(i + 1) % len(ordered_perms)]


def next_in_sequence_v2(s: str) -> str:
    """Two-pointer approach: Find the characters to manipulate to get the next string.

    Insights:
        - We don't want to generate all permutations
        - How does itertools.permutations(...) work / what sequencing?
        - We always want to progress to a slightly larger string than before
            - Idea: What if we move a large character to the left (minimally)
            - Moving a small character to the left probably makes it smaller
        - If string is sorted in reverse order, return sorted string
        - *We can find the target substring to edit "easily"
            - As long as the string (from the right) is sorted non-increasing, it is the
              biggest ordering possible
            - When we find one character that is not ordered, we can do something to
              make that substring bigger

    Method: next_in_sequence('abcd')?
        1. Move left, while the sequence is not decreasing.
        2. When we find a smaller letter, mark that as the left bound
        3. Update the substring [left, end] to be slightly larger
            a. How? Let's try rotating it

    Runtime: (suppose n is the length of the input string)
        Time: O(n)
        Space: O(n)

    Args:
        s (str): Input sequence as a string.

    Returns:
        str: Next sequence arrangement in lexicographical order.
    """

    def get_left_bound(s: str) -> Optional[int]:
        current = s[-1]
        for left in range(len(s) - 1, -1, -1):
            if s[left] < current:
                return left
            current = s[left]
        return None

    def find_next_sequence(s: list[str], left: int) -> list[str]:
        for right in range(len(s) - 1, left, -1):
            if s[right] > s[left]:
                s[left], s[right] = s[right], s[left]
                break

        reverse(s, left + 1)
        return s

    if not s:
        return s

    left = get_left_bound(s)
    if left is None:
        return s[::-1]

    return "".join(find_next_sequence(list(s), left))
