from dsa.sort import selection_sort


class TestSelectionSort:
    def test_simple_array(self):
        assert selection_sort([5, 1, 3, 2, 4]) == [1, 2, 3, 4, 5]
        assert selection_sort([5, 5, 2, 1, 2, 1, 1]) == [1, 1, 1, 2, 2, 5, 5]
        assert selection_sort([1, 1, 1]) == [1, 1, 1]

    def test_non_numeric_types(self):
        assert selection_sort(["c", "a", "bb", "ba"]) == ["a", "ba", "bb", "c"]

    def test_empty_input(self):
        assert selection_sort([]) == []
