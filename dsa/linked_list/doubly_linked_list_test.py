from typing import Any

from .doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList:
    def test_empty_list(self) -> None:
        linked_list = DoublyLinkedList[int]()
        assert len(linked_list) == 0
        assert str(linked_list) == "None"

    def test_from_iterable(self) -> None:
        linked_list1 = DoublyLinkedList[int].from_iterable([1, 2, 3])
        assert len(linked_list1) == 3
        assert str(linked_list1) == "1->2->3->None"

        linked_list2 = DoublyLinkedList[int].from_iterable([])
        assert len(linked_list2) == 0
        assert str(linked_list2) == "None"

    def test_push_head(self) -> None:
        linked_list = DoublyLinkedList[int]()

        linked_list.push_head(3)
        linked_list.push_head(2)
        linked_list.push_head(1)
        assert len(linked_list) == 3
        assert str(linked_list) == "1->2->3->None"

    def test_push_tail(self) -> None:
        linked_list = DoublyLinkedList[int]()

        linked_list.push_tail(1)
        linked_list.push_tail(2)
        linked_list.push_tail(3)
        assert len(linked_list) == 3
        assert str(linked_list) == "1->2->3->None"

    def test_remove_head(self) -> None:
        linked_list = DoublyLinkedList[int].from_iterable([1, 2, 3])

        linked_list.remove_head()
        assert str(linked_list) == "2->3->None"

        linked_list.remove_head()
        assert str(linked_list) == "3->None"

        linked_list.remove_head()
        assert str(linked_list) == "None"

        linked_list.remove_head()
        assert str(linked_list) == "None"

    def test_remove_tail(self) -> None:
        linked_list = DoublyLinkedList[int].from_iterable([1, 2, 3])

        linked_list.remove_tail()
        assert str(linked_list) == "1->2->None"

        linked_list.remove_tail()
        assert str(linked_list) == "1->None"

        linked_list.remove_tail()
        assert str(linked_list) == "None"

        linked_list.remove_tail()
        assert len(linked_list) == 0
        assert str(linked_list) == "None"

    def test_contains(self) -> None:
        linked_list = DoublyLinkedList[int].from_iterable([1, 2, 3])

        assert 1 in linked_list
        assert 2 in linked_list
        assert 3 in linked_list
        assert 0 not in linked_list
        assert 4 not in linked_list

    def test_other_types(self) -> None:
        linked_list1 = DoublyLinkedList[str].from_iterable(
            ["apple", "banana", "cheese"]
        )
        assert str(linked_list1) == "apple->banana->cheese->None"

        linked_list2 = DoublyLinkedList[None].from_iterable([None])
        assert str(linked_list2) == "None->None"

        linked_list3 = DoublyLinkedList[Any].from_iterable([[1, 2], ["a", "b"]])
        assert str(linked_list3) == "[1, 2]->['a', 'b']->None"

    def test_single_node(self) -> None:
        linked_list = DoublyLinkedList[int].from_iterable([1])

        linked_list.remove_head()
        assert str(linked_list) == "None"
        linked_list.push_tail(1)
        assert str(linked_list) == "1->None"

        linked_list.remove_tail()
        assert str(linked_list) == "None"
        linked_list.push_head(1)
        assert str(linked_list) == "1->None"

    def test_iter(self) -> None:
        linked_list = DoublyLinkedList[int].from_iterable([1, 2, 3])
        empty_list = DoublyLinkedList[int]()

        assert list(linked_list) == [1, 2, 3]
        assert list(empty_list) == []

        assert [node.data for node in linked_list.node_iterator()] == [1, 2, 3]
        assert list(empty_list.node_iterator()) == []
