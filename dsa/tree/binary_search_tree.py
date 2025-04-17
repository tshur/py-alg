from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

from dsa.stack import Stack
from dsa.typing.comparison import Comparable


@dataclass
class _Node[CT: Comparable]:
    data: CT
    left: Optional[_Node[CT]] = None
    right: Optional[_Node[CT]] = None


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

    _root: Optional[_Node[CT]]
    _size: int

    def __init__(self):
        self._root = None
        self._size = 0

    @staticmethod
    def from_iterable(iterable: Iterable[CT]) -> BinarySearchTree[CT]:
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
        bst = BinarySearchTree[CT]()
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
        node = _Node(value)
        if self._root is None:
            self._root = node
            self._size += 1
            return

        current = self._root
        while current:  # Loop should not terminate via this condition.
            if value < current.data:
                if current.left is None:
                    current.left = node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    break
                current = current.right
        self._size += 1

    def remove(self, value: CT) -> None:
        """Remove one occurrence of the value in the tree (if it exists).

        Complexity:
            Time: O(logn), to find the node and the new parent to replace it.

        Args:
            target (CT): The target to find and remove. Only the first / one instance of
              the node will be removed.
        """
        # Traverse such that current is the node to delete (or None).
        to_delete = self._search(value)
        if to_delete is None:
            return

        successor = None
        if to_delete.right is None:
            successor = to_delete.left
        elif to_delete.left is None:
            successor = to_delete.right
        else:
            successor = self._extract_successor_node(to_delete)
            successor.left = to_delete.left
            successor.right = to_delete.right
        self._size -= 1

    def _extract_successor_node(self, node: _Node[CT]) -> _Node[CT]:
        return node

    def _search(self, value: CT) -> Optional[_Node[CT]]:
        """Find a node with target value in the BST (or None if not found).

        Runs in O(logn) time. Worst-case, O(n) time if the tree is severely unbalanced.

        Args:
            value (CT): Target value to search for.

        Returns:
            Optional[_Node[CT]]: The first node containing the target value. If no such
              node exists, return None.
        """
        current = self._root
        while current:
            if value == current.data:
                return current
            elif value < current.data:
                current = current.left
            else:
                current = current.right
        return None

    def __iter__(self) -> Iterator[CT]:
        """In-order traversal of the binary search tree.

        Traversal should yield left subtree, then root node, then right subtree. The
        order should be such that values are yielded in sorted order (due to BST
        ordering).

        Yields:
            Iterator[CT]: Values in-order from the tree.
        """
        yield from self.inorder_recursive()

    def inorder_recursive(self) -> Iterator[CT]:
        """Recursive implementation of in-order traversal from the tree.

        Yields:
            Iterator[CT]: Values in-order from the tree.
        """

        def helper(root: Optional[_Node[CT]]) -> Iterator[CT]:
            if not root:
                return

            yield from helper(root.left)
            yield root.data
            yield from helper(root.right)

        yield from helper(self._root)

    def inorder_iterative(self) -> Iterator[CT]:
        """Iterative implementation of in-order traversal from the tree.

        The iterative implementation is trickier than recursion. We maintain a stack,
        which represents roots of subtrees for traversal. When have a current node, we
        visit its left subtree always. When we have no current node, take one from the
        stack. Its left subtree should already be visited, so move right one node.
        Repeat this process.

        Yields:
            Iterator[CT]: Values in-order from the tree.
        """
        if self._root is None:
            return

        stack = Stack[_Node[CT]]()
        current: Optional[_Node[CT]] = self._root
        while True:
            if current:
                # Whenever we have a current node, traverse down its left subtree. Add
                # all nodes to the stack for later traversing their right subtrees.
                stack.push(current)
                current = current.left
            else:
                # If we do not have a current node, take one from the stack. Its left
                # subtree should already be visited. Yield the root, then move on to
                # its right subtree.
                current = stack.pop()
                if not current:
                    return  # Stack is empty, done with traversal.
                yield current.data
                current = current.right

    def __contains__(self, value: CT) -> bool:
        """Return true if the value exists in the binary search tree.

        To find a node, we simply traverse the tree downward. At each node, if the
        target is not found, we traverse left or right (depending on comparison).

        Complexity:
            Time: O(logn), by traversing at most the height of the tree. In the worst
              case, this is O(n) if the tree is fully unbalanced.

        Args:
            value (CT): The value to search for in the tree.

        Returns:
            bool: Whether the value is in the binary search tree.
        """
        return self._search(value) is not None

    def __bool__(self) -> bool:
        """Get the truthy-ness of the tree (whether non-empty).

        Returns:
            bool: True if the tree at least one element/node. Otherwise, returns false.
        """
        return len(self) != 0

    def __len__(self) -> int:
        """Returns the number of nodes in the tree.

        Returns:
            int: The number of nodes in the tree.
        """
        return self._size

    def __str__(self) -> str:
        """Get a printable representation of the binary search tree.

        Returns:
            str: String displaying the tree structure and data.
        """
        if not self:
            return ""
        raise NotImplementedError
