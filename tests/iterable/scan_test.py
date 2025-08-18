import operator

from dsap.iterable import scan


class TestScan:
    def test_default_operation_add(self):
        assert list(scan([1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]
        assert list(scan([-1, 5])) == [-1, 4]
        assert list(scan([0, 0, 0, 0])) == [0, 0, 0, 0]

    def test_operation_sub(self):
        assert list(scan([1, 2, 3, 4, 5], operator.sub)) == [1, -1, -4, -8, -13]
        assert list(scan([5, 1, 1, 1, 1], operator.sub)) == [5, 4, 3, 2, 1]

    def test_initial_value(self):
        assert list(scan([1, 2, 3, 4, 5], initial=0)) == [0, 1, 3, 6, 10, 15]
        assert list(scan([-1, 5], initial=1)) == [1, 0, 5]
        assert list(scan([0], initial=100)) == [100, 100]
        assert list(scan([], initial=100)) == [100]

    def test_empty_input_iterator(self):
        assert list(scan([])) == []
        assert list(scan([], operator.mul)) == []

    def test_count_ones(self):
        def count_if_even(total: int, item: int) -> int:
            if item % 2 == 0:
                total += 1
            return total

        assert list(scan([0, 1, 2, 3, 4], count_if_even, initial=0)) == [
            0,
            1,
            1,
            2,
            2,
            3,
        ]
        assert list(scan([-1, -4, 0, 2], count_if_even, initial=0)) == [
            0,
            0,
            1,
            2,
            3,
        ]
