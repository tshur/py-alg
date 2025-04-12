from dataclasses import dataclass
from typing import Iterable, Optional

from dsa.typing.comparison import Comparable


@dataclass
class Node[CT: Comparable]:
    data: CT
    left: Optional["Node[CT]"] = None
    right: Optional["Node[CT]"] = None


class BinarySearchTree[CT: Comparable]:
    """Binary search tree data structure. Data is sorted order in the tree.

    The primary property of a binary search tree is that for each node, all nodes in the
    left subtree are <= the node's value. All nodes in the right subtree are > the
    node's value. Requires the < comparison operator to be available on the value type.
    Nodes are inserted into the first viable location. The tree is not rebalanced for efficiency.

    Basic operations:
      - insert
      - remove
      - search
    """

    root: Optional[Node[CT]]

    def __init__(self):
        self.root = None

    @staticmethod
    def from_iterable(iterable: Iterable[CT]) -> "BinarySearchTree[CT]":
        """Builds and returns a BinarySearchTree from the given iterable.

        Complexity:
            Time: O(n * logn), due to repeated O(logn) insertions into the tree. At
              worst case, this is O(n**2) if the input is near-sorted, causing an
              severely imbalanced tree.
            Space: O(n), for the output tree

        Args:
            iterable (Iterable[CT]): Given iterable to consume (if a generator) and fill
              the output with values. Nodes are created from values, then inserted in
              the order they are given, and the tree is not rebalanced.

        Returns:
            BinarySearchTree[CT]: The resulting binary search tree after inserting the
              given values from the iterable.
        """
        bst: BinarySearchTree[CT] = BinarySearchTree()
        for value in iterable:
            bst.insert(value)
        return bst

    def insert(self, value: CT) -> None:
        """Insert a new node containing the given value into the tree.

        The new node will be inserted in an available space at the bottom (leaf) of the
        tree. The node will be inserted to maintain sorted order. Multiple copies of a
        value can be inserted into the tree (possibly at non-adjacent locations).

        Complexity:
            Time: O(logn), to traverse to the empty leaf and insert.
            Space: O(1)

        Args:
            value (CT): The value to be added into a new Node and inserted into the
              tree.
        """
        node = Node(value)
        if self.root is None:
            self.root = node
            return

        current = self.root
        while current:  # Loop should not terminate via this condition.
            if value < current.data:
                if current.left is None:
                    current.left = node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    return
                current = current.right

    def remove(self, target: CT):
        """Remove one occurrence of the value in the tree (if it exists).

        Complexity:
            Time: O(logn), to find the node and the new parent to replace it.

        Args:
            target (CT): The target to find and remove. Only the first / one instance of
              the node will be removed.
        """
        # Traverse such that current is the node to delete (or None).
        current = self.root
        while current:
            if target == current.data:
                break
            if target < current.data:
                current = current.left
            else:
                current = current.right
        if current is None:
            return

        successor = None
        if current.right is None:
            successor = current.left
        elif current.left is None:
            successor = current.right
        else:
            successor = self._extract_successor_node(current)
            successor.left = current.left
            successor.right = current.right

    def _extract_successor_node(self, node: Node[CT]) -> Node[CT]:
        return node

    def search(self, target: CT) -> Optional[Node[CT]]:
        """Find the given target in the binary search tree.

        To find a node, we simply traverse the tree downward. At each node, if the
        target is not found, we traverse left or right (depending on comparison).

        Complexity:
            Time: O(logn), by traversing at most the height of the tree. In the worst
              case, this is O(n) if the tree is fully unbalanced.

        Args:
            target (CT): The value to search for in the tree. This method looks for the
              first (highest) Node with a value equal to the target.

        Returns:
            Optional[Node[CT]]: Returns the found node if the target is in the binary
              search tree. If not found, returns None.
        """
        current = self.root
        while current:
            if target == current.data:
                return current
            elif target < current.data:
                current = current.left
            else:
                current = current.right
        return None

    def __str__(self) -> str:
        """_summary_

        Raises:
            NotImplementedError: _description_

        Returns:
            str: _description_
        """
        raise NotImplementedError
