import operator

from algorithms import reduce


class TestReduce:
    def test_default_operation_add(self):
        assert reduce.reduce([1, 2, 3, 4, 5]) == 15
        assert reduce.reduce([-1, 5]) == 4
        assert reduce.reduce([0, 0, 0, 0]) == 0

    def test_operation_sub(self):
        assert reduce.reduce([1, 2, 3, 4, 5], operator.sub) == -13
        assert reduce.reduce([5, 1, 1, 1, 1], operator.sub) == 1

    def test_initial_value(self):
        assert reduce.reduce([1, 2, 3, 4, 5], initial=0) == 15
        assert reduce.reduce([-1, 5], initial=1) == 5
        assert reduce.reduce([0], initial=100) == 100
        assert reduce.reduce([], initial=100) == 100

    def test_empty_input_iterator(self):
        assert reduce.reduce([]) is None
        assert reduce.reduce([], operator.mul) is None
        assert reduce.reduce([], initial=100) == 100

    def test_count_ones(self):
        def count_if_even(total: int, item: int) -> int:
            if item % 2 == 0:
                total += 1
            return total

        assert reduce.reduce([0, 1, 2, 3, 4], count_if_even, initial=0) == 3
        assert reduce.reduce([-1, -4, 0, 2], count_if_even, initial=0) == 3
