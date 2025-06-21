'''Find the next sequence arrangement in lexicographical order.

https://bytebytego.com/exercises/coding-patterns/two-pointers/next-lexicographical-sequence
'''

from itertools import permutations

def next_in_sequence(s: str) -> str:
    '''Brute force method: Generate all unique permutations and sort them.

    Method: next_in_sequence('aab')?
        1. Find all permutations (`''.join(...)` into string format).
        2. Unique-ify the permutations.
        3. Sort the unique permutations.
        4. Find the index of our given input `s`.
        5. Return the immediate next element after `s`.

    Args:
        s (str): Input sequence as a string.

    Returns:
        str: Next sequence arrangement in lexicographical order.
    '''

    unique_permutations = set(''.join(perm) for perm in permutations(s))
    ordered_perms = list(sorted(unique_permutations))
    
    i = ordered_perms.index(s)
    return ordered_perms[(i + 1) % len(ordered_perms)]
