from dsap.tree import BinarySearchTree


class TestBinarySearchTree:
    def test_init(self) -> None:
        bst = BinarySearchTree[int]()

        assert not bst
        assert len(bst) == 0
        assert str(bst) == ""
        assert list(bst) == []
        assert list(bst.inorder_iterative()) == []
        assert list(bst.inorder_recursive()) == []

    def test_empty_tree(self) -> None:
        bst = BinarySearchTree[int]()

        bst.remove(5)
        bst.remove(0)

        assert 3 not in bst
        assert 0 not in bst

    def test_from_iterable(self) -> None:
        balanced_bst = BinarySearchTree[int].from_iterable([5, 2, 1, 3, 8, 7, 9])
        assert balanced_bst
        assert len(balanced_bst) == 7

        unbalanced_bst = BinarySearchTree[int].from_iterable([1, 2, 3, 4, 5])
        assert unbalanced_bst
        assert len(unbalanced_bst) == 5

    def test_insert(self) -> None:
        bst = BinarySearchTree[int]()

        bst.insert(5)
        assert bst
        assert len(bst) == 1

        bst.insert(3)
        bst.insert(3)
        bst.insert(3)
        assert len(bst) == 4

        bst.insert(8)
        bst.insert(9)
        bst.insert(8)
        bst.insert(9)
        bst.insert(10)
        assert len(bst) == 9
        assert list(bst) == [3, 3, 3, 5, 8, 8, 9, 9, 10]

    def test_near_leaf_remove(self) -> None:
        bst = BinarySearchTree[int].from_iterable([5, 10, 8, 12, 11, 4, 3])

        # Remove nodes that do not exist.
        bst.remove(2)
        bst.remove(13)
        bst.remove(9)
        assert list(bst) == [3, 4, 5, 8, 10, 11, 12]
        assert len(bst) == 7

        bst.remove(4)  # Internal with only left child.
        assert list(bst) == [3, 5, 8, 10, 11, 12]
        bst.remove(3)  # Left leaf node.
        assert list(bst) == [5, 8, 10, 11, 12]

        bst.remove(5)  # Root with only right subtree.
        assert list(bst) == [8, 10, 11, 12]

        bst.remove(12)  # Internal with only left subtree.
        assert list(bst) == [8, 10, 11]

        bst.remove(11)  # Leaf node.
        assert list(bst) == [8, 10]
        bst.remove(10)  # Root with only left subtree.
        assert list(bst) == [8]
        bst.remove(8)  # Root is leaf node.
        assert list(bst) == []
        assert len(bst) == 0

        bst.remove(8)  # Remove from empty tree.
        assert len(bst) == 0

    def test_full_node_remove(self) -> None:
        bst = BinarySearchTree[int].from_iterable(
            [10, 4, 5, 6, 8, 7, 9, 14, 11, 13, 12, 10, 14, 14, 14]
        )
        assert list(bst) == [4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 14, 14, 14]
        assert len(bst) == 15

        bst.remove(8)  # Full node with two leaf children.
        assert list(bst) == [4, 5, 6, 7, 9, 10, 10, 11, 12, 13, 14, 14, 14, 14]
        assert len(bst) == 14

        bst.remove(11)  # Full node with deeper successor.
        assert list(bst) == [4, 5, 6, 7, 9, 10, 10, 12, 13, 14, 14, 14, 14]
        assert len(bst) == 13

        bst.remove(10)  # Root node with full subtrees.
        assert list(bst) == [4, 5, 6, 7, 9, 10, 12, 13, 14, 14, 14, 14]
        assert len(bst) == 12

        bst.remove(14)  # Full node with right chain.
        assert list(bst) == [4, 5, 6, 7, 9, 10, 12, 13, 14, 14, 14]
        assert len(bst) == 11

        # Remove everything else.
        for value in list(bst):
            bst.remove(value)
        assert list(bst) == []
        assert len(bst) == 0

    def test_inorder_iter(self) -> None:
        balanced_bst = BinarySearchTree[int].from_iterable([5, 2, 1, 3, 8, 7, 9])
        assert list(balanced_bst) == [1, 2, 3, 5, 7, 8, 9]
        assert list(balanced_bst.inorder_iterative()) == [1, 2, 3, 5, 7, 8, 9]
        assert list(balanced_bst.inorder_recursive()) == [1, 2, 3, 5, 7, 8, 9]

        ascending_bst = BinarySearchTree[int].from_iterable([1, 2, 3, 4, 5])
        assert list(ascending_bst) == [1, 2, 3, 4, 5]
        assert list(ascending_bst.inorder_iterative()) == [1, 2, 3, 4, 5]
        assert list(ascending_bst.inorder_recursive()) == [1, 2, 3, 4, 5]

        descending_bst = BinarySearchTree[int].from_iterable([5, 4, 3, 2, 1])
        assert list(descending_bst) == [1, 2, 3, 4, 5]
        assert list(descending_bst.inorder_iterative()) == [1, 2, 3, 4, 5]
        assert list(descending_bst.inorder_recursive()) == [1, 2, 3, 4, 5]

        zigzag_bst = BinarySearchTree[int].from_iterable([2, 2, 1, 2, 1, 1, 2, 1, 2, 2])
        assert list(zigzag_bst) == [1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        assert list(zigzag_bst.inorder_iterative()) == [1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        assert list(zigzag_bst.inorder_recursive()) == [1, 1, 1, 1, 2, 2, 2, 2, 2, 2]

    def test_contains(self) -> None:
        bst = BinarySearchTree[int].from_iterable([5, 10, 8, 12, 11])

        assert 5 in bst
        assert 10 in bst
        assert 8 in bst
        assert 12 in bst
        assert 11 in bst

        assert 4 not in bst
        assert 9 not in bst
        assert 7 not in bst
        assert 13 not in bst

    def test_str(self) -> None:
        singleton_bst = BinarySearchTree[int].from_iterable([10])
        assert str(singleton_bst) == "+———10"

        bst = BinarySearchTree[int].from_iterable([5, 10, 8, 12, 11])
        assert (
            str(bst)
            == """\
        +———12
        |   +———11
    +———10
    |   +———8
+———5\
"""
        )

        balanced_bst = BinarySearchTree[int].from_iterable([5, 2, 1, 3, 8, 7, 9])
        assert (
            str(balanced_bst)
            == """\
        +———9
    +———8
    |   +———7
+———5
    |   +———3
    +———2
        +———1\
"""
        )

        right_bst = BinarySearchTree[int].from_iterable([1, 2, 3, 4, 5])
        assert (
            str(right_bst)
            == """\
                +———5
            +———4
        +———3
    +———2
+———1\
"""
        )

        left = BinarySearchTree[int].from_iterable([5, 4, 3, 2, 1])
        assert (
            str(left)
            == """\
+———5
    +———4
        +———3
            +———2
                +———1\
"""
        )

        complicated_bst = BinarySearchTree[int].from_iterable(
            [10, 4, 5, 6, 8, 7, 9, 14, 11, 13, 12, 10, 14, 14, 14]
        )
        assert (
            str(complicated_bst)
            == """\
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
    +———4\
"""
        )
