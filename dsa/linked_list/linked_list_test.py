from dsa.linked_list.linked_list import LinkedList


class TestLinkedList:
    def test_empty_list(self) -> None:
        linked_list: LinkedList[int] = LinkedList()
        assert len(linked_list) == 0
        assert str(linked_list) == "None"

    def test_from_iterable(self) -> None:
        linked_list1 = LinkedList.from_iterable([1, 2, 3])
        assert len(linked_list1) == 3
        assert str(linked_list1) == "1->2->3->None"

        linked_list2: LinkedList[int] = LinkedList.from_iterable([])
        assert len(linked_list2) == 0
        assert str(linked_list2) == "None"

    def test_push_front(self) -> None:
        linked_list: LinkedList[int] = LinkedList()

        linked_list.push_front(3)
        linked_list.push_front(2)
        linked_list.push_front(1)
        assert len(linked_list) == 3
        assert str(linked_list) == "1->2->3->None"

    def test_push_back(self) -> None:
        linked_list: LinkedList[int] = LinkedList()

        linked_list.push_back(1)
        linked_list.push_back(2)
        linked_list.push_back(3)
        assert len(linked_list) == 3
        assert str(linked_list) == "1->2->3->None"

    def test_remove_front(self) -> None:
        linked_list = LinkedList.from_iterable([1, 2, 3])

        linked_list.remove_front()
        assert str(linked_list) == "2->3->None"

        linked_list.remove_front()
        assert str(linked_list) == "3->None"

        linked_list.remove_front()
        assert str(linked_list) == "None"

        linked_list.remove_front()
        assert str(linked_list) == "None"

    def test_remove_back(self) -> None:
        linked_list = LinkedList.from_iterable([1, 2, 3])

        linked_list.remove_back()
        assert str(linked_list) == "1->2->None"

        linked_list.remove_back()
        assert str(linked_list) == "1->None"

        linked_list.remove_back()
        assert str(linked_list) == "None"

        linked_list.remove_back()
        assert len(linked_list) == 0
        assert str(linked_list) == "None"

    def test_contains(self) -> None:
        linked_list = LinkedList.from_iterable([1, 2, 3])

        assert 1 in linked_list
        assert 2 in linked_list
        assert 3 in linked_list
        assert 0 not in linked_list
        assert 4 not in linked_list

    def test_other_types(self) -> None:
        linked_list1 = LinkedList.from_iterable(["apple", "banana", "cheese"])
        assert str(linked_list1) == "apple->banana->cheese->None"

        linked_list2 = LinkedList.from_iterable([None])
        assert str(linked_list2) == "None->None"

        linked_list3 = LinkedList.from_iterable([[1, 2], ["a", "b"]])
        assert str(linked_list3) == '[1, 2]->["a", "b"]->None'
