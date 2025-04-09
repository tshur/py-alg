from dataclasses import dataclass
from typing import Iterable, Optional

from dsa.typing.comparison import Comparable


@dataclass
class Node[CT: Comparable]:
    value: CT
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
    size: int

    def __init__(self):
        self.root = None
        self.size = 0

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

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        """_summary_

        Raises:
            NotImplementedError: _description_

        Returns:
            str: _description_
        """
        raise NotImplementedError

    def insert(self, value: CT) -> Node[CT]:
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
        parent = self._find_new_parent(value)
        return self._insert_under_parent(parent, value)

    def _find_new_parent(self, value: CT) -> Optional[Node[CT]]:
        """Returns a parent node such that there is an empty child slot for value.

        Args:
            value (CT): The value to find an empty space for. This method will find a
              parent such that the parent has an empty child slot in the direction to
              insert a new Node(value) into.

        Returns:
            Optional[Node[CT]]: The parent node with an empty slot to insert a new
              Node(value). Returns None if the tree is empty (insert at root).
        """
        previous = None
        current = self.root
        while current:
            previous = current
            if value > current.value:
                current = current.right
            else:
                current = current.left
        return previous

    def _insert_under_parent(self, parent: Optional[Node[CT]], value: CT) -> Node[CT]:
        """Insert a new Node(value) as a direct child of parent.

        Assumes that there is an empty slot under the parent for the Node(value) to be
        inserted into.

        Raises:
            ValueError: If the parent does not have an empty (None) child slot to insert
              the new Node(value) into.

        Args:
            parent (Optional[Node[CT]]): The parent, with an empty child slot, for the
              target value to be inserted into.
            value (CT): The value to insert, which will be added into a new Node(value).

        Returns:
            Node[CT]: The new node that was inserted.
        """
        node = Node(value)
        if parent is None:
            self.root = node
        elif value > parent.value:
            if parent.right is not None:
                raise ValueError("insert: trying to overwrite existing node")
            parent.right = node
        else:
            if parent.left is not None:
                raise ValueError("insert: trying to overwrite existing node")
            parent.left = node
        self.size += 1
        return node

    def remove(self, value: CT) -> Optional[Node[CT]]:
        """Remove (and return) one occurrence of the value in the tree.

        Args:
            value (CT): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            Optional[Node[CT]]: _description_
        """
        raise NotImplementedError

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
            if target == current.value:
                return current
            elif target < current.value:
                current = current.left
            else:
                current = current.right
        return None
