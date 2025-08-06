from typing import Iterable

from dsap.tree import BinarySearchTree
from dsap.type import SupportsRichComparison


def tree_sort[CT: SupportsRichComparison](iterable: Iterable[CT]) -> list[CT]:
    """Returns a sorted copy of the input iterable using binary search tree sort method.

    Complexity:
        Time: O(nlogn) to make n insertions each in O(logn) time (average case), then
          traverse the tree in-order in O(n) time. For nearly sorted input, the tree
          degenerates, and the worst case runtime is O(n**2).
        Space: O(n) to store the bst.

    Args:
        iterable (Iterable[CT]): The input iterable to sort. By the CT template, this
          iterable must consist of elements that support basic __lt__ comparison.

    Returns:
        list[CT]: Sorted list. Sorts in ascending order.

    Examples:
        >>> tree_sort([5, 1, 3, 2, 4])
        [1, 2, 3, 4, 5]
        >>> tree_sort([1])
        [1]
        >>> tree_sort([])
        []
    """

    bst = BinarySearchTree[CT].from_iterable(iterable)
    return list(bst.inorder_iterative())
