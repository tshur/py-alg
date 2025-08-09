from dsap.iterable import reverse


class TestReverse:
    def test_even_length(self):
        assert reverse([1, 22, 3, 4]) == [4, 3, 22, 1]
        assert reverse([1, 2]) == [2, 1]
        assert reverse([1, 1, 1, 1]) == [1, 1, 1, 1]

    def test_odd_length(self):
        assert reverse([1, 22, 3, 4, 5]) == [5, 4, 3, 22, 1]
        assert reverse([1, 2, 3]) == [3, 2, 1]

    def test_small_input(self):
        assert reverse([1]) == [1]
        assert reverse([]) == []

    def test_reverses_in_place(self):
        array = [1, 2, 3, 4, 5]
        reverse(array)
        assert array == [5, 4, 3, 2, 1]

    def test_reverse_with_start(self):
        assert reverse([1, 2, 3, 4, 5], start=1) == [1, 5, 4, 3, 2]
        assert reverse([1, 2, 3, 4, 5], start=2) == [1, 2, 5, 4, 3]
        assert reverse([1, 2, 3, 4, 5], start=4) == [1, 2, 3, 4, 5]
        assert reverse([1, 2, 3, 4, 5], start=5) == [1, 2, 3, 4, 5]

    def test_reverse_with_end(self):
        assert reverse([1, 2, 3, 4, 5], end=3) == [3, 2, 1, 4, 5]
        assert reverse([1, 2, 3, 4, 5], start=1, end=4) == [1, 4, 3, 2, 5]
        assert reverse([1, 2, 3, 4, 5], start=1, end=10) == [1, 5, 4, 3, 2]
        assert reverse([1, 2, 3, 4, 5], start=3, end=4) == [1, 2, 3, 4, 5]
