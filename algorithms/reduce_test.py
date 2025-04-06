import operator
import unittest

from algorithms import reduce


class ReduceTest(unittest.TestCase):
    def test_default_operation_add(self):
        self.assertEqual(reduce.reduce([1, 2, 3, 4, 5]), 15)
        self.assertEqual(reduce.reduce([-1, 5]), 4)
        self.assertEqual(reduce.reduce([0, 0, 0, 0]), 0)

    def test_operation_sub(self):
        self.assertEqual(reduce.reduce([1, 2, 3, 4, 5], operator.sub), -13)
        self.assertEqual(reduce.reduce([5, 1, 1, 1, 1], operator.sub), 1)

    def test_initial_value(self):
        self.assertEqual(reduce.reduce([1, 2, 3, 4, 5], initial=0), 15)
        self.assertEqual(reduce.reduce([-1, 5], initial=1), 5)
        self.assertEqual(reduce.reduce([0], initial=100), 100)
        self.assertEqual(reduce.reduce([], initial=100), 100)

    def test_empty_input_iterator(self):
        self.assertEqual(reduce.reduce([]), None)
        self.assertEqual(reduce.reduce([], operator.mul), None)
        self.assertEqual(reduce.reduce([], initial=100), 100)

    def test_count_ones(self):
        def count_if_even(total: int, item: int) -> int:
            if item % 2 == 0:
                total += 1
            return total

        self.assertEqual(
            reduce.reduce([0, 1, 2, 3, 4], count_if_even, initial=0),
            3,
        )
        self.assertEqual(
            reduce.reduce([-1, -4, 0, 2], count_if_even, initial=0),
            3,
        )


if __name__ == "__main__":
    unittest.main()
