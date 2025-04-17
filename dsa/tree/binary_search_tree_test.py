from .binary_search_tree import BinarySearchTree


class TestBinarySearchTree:
    def test_init(self) -> None:
        bst = BinarySearchTree[int]()

        assert not bst
        assert len(bst) == 0
        assert str(bst) == ""
        assert list(bst) == []

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

    def test_basic_remove(self) -> None:
        bst = BinarySearchTree[int].from_iterable([5, 10, 8, 12, 11, 11])

        assert list(bst) == [5, 8, 10, 11, 11, 12]
        bst.remove(11)
        assert list(bst) == [5, 8, 10, 11, 12]
        bst.remove(11)
        assert list(bst) == [5, 8, 10, 12]
        bst.remove(5)
        assert list(bst) == [8, 10, 12]
        bst.remove(10)
        assert list(bst) == [8, 12]
        bst.remove(12)
        assert list(bst) == [8]
        bst.remove(8)
        assert len(bst) == 0
        assert list(bst) == []

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
        assert str(singleton_bst) == "+—10"

        bst = BinarySearchTree[int].from_iterable([5, 10, 8, 12, 11])
        assert (
            str(bst)
            == """
                +—12
                | +—11
              +—10
              | +—8
            +—5
            """
        )

        balanced_bst = BinarySearchTree[int].from_iterable([5, 2, 1, 3, 8, 7, 9])
        assert (
            str(balanced_bst)
            == """
    +—9
  +—8
  | +—7
+—5
  | +—3
  +—2
    +—1
"""
        )

        unbalanced_bst = BinarySearchTree[int].from_iterable([1, 2, 3, 4, 5])
        assert (
            str(unbalanced_bst)
            == """
        +—5
      +—4
    +—3
  +—2
+—1
"""
        )
