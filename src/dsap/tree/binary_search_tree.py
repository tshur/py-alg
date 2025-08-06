from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

from dsap.stack import Stack
from dsap.type import SupportsRichComparison


@dataclass
class _Node[CT: SupportsRichComparison]:
    data: CT
    left: Optional[_Node[CT]] = None
    right: Optional[_Node[CT]] = None


class BinarySearchTree[CT: SupportsRichComparison]:
    """Binary search tree data structure. Data is sorted order in the tree.

    The primary property of a binary search tree is that for each node, all nodes in the
    left subtree are <= the node's value. All nodes in the right subtree are > the
    node's value. Requires the < comparison operator to be available on the value type.
    Nodes are inserted into the first viable location. The tree is not rebalanced for
    efficiency.

    Basic operations:
      - insert, O(logn) average case, O(n) worst case (unbalanced tree).
      - remove, O(logn) average case, O(n) worst case (unbalanced tree).
      - __contains__, O(logn) average case, O(n) worst case (unbalanced tree).
      - __iter__, in-order traversal of the tree in O(n) time and O(h) space.
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

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 12, 11])
            >>> print(bst)
                    +———12
                    |   +———11
                +———10
                |   +———8
            +———5
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
            Time: O(logn), to traverse to the empty leaf and insert. Assumes the tree is
              reasonably balanced, otherwise will take worst-case O(n) time complexity.
            Space: O(1)

        Args:
            value (CT): The value to be added into a new Node and inserted into the
              tree.

        Examples:
            >>> bst = BinarySearchTree()
            >>> bst.insert(5)
            >>> bst.insert(3)
            >>> bst.insert(5)
            >>> print(bst)
                +———5
            +———5
                +———3
        """
        parent = None
        current = self._root
        while current:
            parent = current
            if value < current.data:
                current = current.left
            else:
                current = current.right

        node = _Node(value)
        if parent is None:
            self._root = node
        elif value < parent.data:
            parent.left = node
        else:
            parent.right = node
        self._size += 1

    def remove(self, value: CT) -> None:
        """Remove one occurrence of the value in the tree (if it exists).

        The method to delete a node can be reduced to a few cases.

        Node to delete has zero or one children:
            To delete this node, we can simply replace it with its non-None child. If
            both children are None, we can just remove the node.
                  +———10
                  |   +———8
              +———5
                  ^ to_delete
            becomes
              +———10
                  +———8

        Node to delete has two children (harder case):
            To delete this node, we will replace (swap) it with its in-order successor.
            The successor is the next-largest node (i.e., the smallest node in the right
            subtree). This is to preserve the "sorted" structure of the BST.
                  +———10     <- successor_parent
                  |   +———8  <- successor
              +———5          <- to_delete
                  +———3
            becomes
                  +———10
                  |   +———X  <- new to_delete
              +———8
                  +———3
            After swapping, we still need to delete the old successor node. By
            definition, this should have at most one child. We can delete this using the
            same removal algorithm (but this time the simple case).
                  +———10
              +———8
                  +———3

        Complexity:
            Time: O(logn), to find the node and the new parent to replace it. If the
              tree is severely unbalanced, this is worst-case O(n) time.

        Args:
            value (CT): The target to find and remove. Only the first / one instance of
              the node will be removed.

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 3])
            >>> print(bst)
                +———10
                |   +———8
            +———5
                +———3
            >>> bst.remove(5)
            >>> print(bst)
                +———10
            +———8
                +———3
            >>> bst.remove(10)
            >>> print(bst)
            +———8
                +———3
            >>> bst.remove(8)
            >>> print(bst)
            +———3
        """
        to_delete_parent, to_delete = self._find_parent(value)
        if to_delete is None:
            return

        if to_delete.left is None or to_delete.right is None:
            self._delete_near_leaf(to_delete_parent, to_delete)
        else:
            successor_parent, successor = self._find_successor(to_delete)
            if successor:
                to_delete.data = successor.data
                self._delete_near_leaf(successor_parent, successor)
        self._size -= 1

    def _delete_near_leaf(self, parent: Optional[_Node[CT]], node: _Node[CT]):
        """Delete the only child of parent (if one exists).

        Assumes that given node does not have two children (i.e., near-leaf node).
        Otherwise, this function has undefined behavior.

        Args:
            parent (Optional[_Node[CT]]): The parent of the node to delete. None
              represents that the node is the root of the tree.
            node (_Node[CT]): The node to delete. This node must have at most one child.
        """
        if node.left is None:
            new_node = node.right
        else:
            new_node = node.left

        if parent is None:
            self._root = new_node
        elif parent.left == node:
            parent.left = new_node
        else:
            parent.right = new_node

    def _find_successor(self, node: _Node[CT]) -> tuple[_Node[CT], Optional[_Node[CT]]]:
        """Find the in-order successor for node and its parent.

        Runs in O(logn) time. Worst-case, O(n) time if the tree is severely unbalanced.

        Sample: (using simplified tree section)
                    v parent of in-order successor of node
                +———10
                |   +———8
            +———5       ^ in-order successor of node
                ^ node

        Args:
            node (_Node[CT]): Target node to find the successor of.

        Returns:
            tuple[_Node[CT], Optional[_Node[CT]]]: A (previous, current) pair such that
              current is the next in-order successor to node. That is, current is the
              smallest node in the right subtree of node. By definition, this means that
              the successor does not have two children. Also, return its parent.
        """
        previous = node
        current = node.right
        while current and current.left:
            previous, current = current, current.left
        return previous, current

    def _find_parent(
        self, value: CT
    ) -> tuple[Optional[_Node[CT]], Optional[_Node[CT]]]:
        """Find (previous, current) such that current has the target value (or None).

        Runs in O(logn) time. Worst-case, O(n) time if the tree is severely unbalanced.

        Args:
            value (CT): Target value to search for.

        Returns:
            tuple[Optional[_Node[CT]], Optional[_Node[CT]]]: A (previous, current) pair
              where current.data == value (or current is None, if value not found). The
              previous node is the parent of current (or None, if the root / no parent).
        """
        previous = None
        current = self._root
        while current:
            if value == current.data:
                return previous, current

            previous = current
            if value < current.data:
                current = current.left
            else:
                current = current.right
        return previous, current

    def _find(self, value: CT) -> Optional[_Node[CT]]:
        """Find a node with target value in the BST (or None if not found).

        Runs in O(logn) time. Worst-case, O(n) time if the tree is severely unbalanced.

        Args:
            value (CT): Target value to search for.

        Returns:
            Optional[_Node[CT]]: The first node containing the target value. If no such
              node exists, return None.
        """
        _, current = self._find_parent(value)
        return current

    def __iter__(self) -> Iterator[CT]:
        """In-order traversal of the binary search tree.

        Traversal should yield left subtree, then root node, then right subtree. The
        order should be such that values are yielded in sorted order (due to BST
        ordering).

        Yields:
            Iterator[CT]: Values in-order from the tree.

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 12, 11])
            >>> list(bst)
            [5, 8, 10, 11, 12]
        """
        yield from self.inorder_recursive()

    def inorder_recursive(self) -> Iterator[CT]:
        """Recursive implementation of in-order traversal from the tree.

        Yields:
            Iterator[CT]: Values in-order from the tree.

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 12, 11])
            >>> list(bst.inorder_recursive())
            [5, 8, 10, 11, 12]
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

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 12, 11])
            >>> list(bst.inorder_iterative())
            [5, 8, 10, 11, 12]
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

        Examples:
            >>> bst = BinarySearchTree.from_iterable([5, 10, 8, 12, 11])
            >>> 8 in bst
            True
            >>> 9 in bst
            False
        """
        return self._find(value) is not None

    def __bool__(self) -> bool:
        """Get the truthy-ness of the tree (whether non-empty).

        Returns:
            bool: True if the tree at least one element/node. Otherwise, returns false.

        Examples:
            >>> bool(BinarySearchTree.from_iterable([5, 10, 8]))
            True
            >>> bool(BinarySearchTree())
            False
        """
        return len(self) != 0

    def __len__(self) -> int:
        """Returns the number of nodes in the tree.

        Returns:
            int: The number of nodes in the tree.

        Examples:
            >>> len(BinarySearchTree.from_iterable([5, 10, 8]))
            3
            >>> len(BinarySearchTree())
            0
        """
        return self._size

    def __str__(self) -> str:
        """Get a printable representation of the binary search tree.

        Prints a binary tree horizontally, so there is enough space to print a full node
        string for each node. Prints reverse-in-order, aka right subtree first.

        This is a recursive function which prints the right subtree, then the root, then
        the left subtree. We carry around a final prefix for printing, and a short
        prefix segment to handle branching left/right.

        Each time we descend down the recursive stack, we extend our prefix. Whenever we
        switch directions, we add a bar (|) to the prefix string. We keep track of the
        additive segments (and invert them), based on which direction we are going.

        From https://stackoverflow.com/questions/64660540/how-can-i-print-a-binary-tree.

        Returns:
            str: String displaying the tree structure and data.

        Examples:
            >>> bst = BinarySearchTree[int].from_iterable([5, 10, 8])
            >>> print(bst)
                +———10
                |   +———8
            +———5
            >>> bst = BinarySearchTree[int].from_iterable(
            ...     [10, 4, 5, 6, 8, 7, 9, 14, 11, 13, 12, 10, 14, 14, 14]
            ... )
            >>> print(bst)
                            +———14
                        +———14
                    +———14
                +———14
                |   |   +———13
                |   |   |   +———12
                |   +———11
                |       +———10
            +———10
                |               +———9
                |           +———8
                |           |   +———7
                |       +———6
                |   +———5
                +———4
        """

        def helper(
            root: Optional[_Node[CT]],
            prefix: str,
            right_prefix: str,
            left_prefix: str,
        ) -> list[str]:
            """Recursive helper function for printing the binary tree.

            Args:
                root (Optional[_Node[CT]]): The root of the current (recursive) subtree.
                prefix (str): The current prefix to prepend any root printing at this
                  level.
                right_prefix (str): The prefix segment to append if we branch to the
                  right. Note: right comes before left in arguments order to mimic the
                  reverse-in-order nature of the printing.
                left_prefix (str): The prefix segment to append if we branch to the
                  left.

            Returns:
                list[str]: A list of built strings / nodes that can be joined later.
            """
            if not root:
                return []

            root_str = f"{prefix}+———{root.data}"
            return (
                helper(
                    root.right,
                    prefix + right_prefix,
                    right_prefix="    ",
                    left_prefix="|   ",
                )
                + [root_str]
                + helper(
                    root.left,
                    prefix + left_prefix,
                    right_prefix="|   ",
                    left_prefix="    ",
                )
            )

        # At the top-level, we don't need to add | bars to either direction. We will
        # start this process for subtrees.
        return "\n".join(helper(self._root, "", "    ", "    "))
