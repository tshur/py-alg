import operator
import unittest

from algorithms import scan


class ScanTest(unittest.TestCase):
    def test_default_operation_add(self):
        self.assertEqual(list(scan.scan([1, 2, 3, 4, 5])), [1, 3, 6, 10, 15])
        self.assertEqual(list(scan.scan([-1, 5])), [-1, 4])
        self.assertEqual(list(scan.scan([0, 0, 0, 0])), [0, 0, 0, 0])

    def test_operation_sub(self):
        self.assertEqual(
            list(scan.scan([1, 2, 3, 4, 5], operator.sub)), [1, -1, -4, -8, -13]
        )
        self.assertEqual(
            list(scan.scan([5, 1, 1, 1, 1], operator.sub)), [5, 4, 3, 2, 1]
        )

    def test_initial_value(self):
        self.assertEqual(
            list(scan.scan([1, 2, 3, 4, 5], initial=0)), [0, 1, 3, 6, 10, 15]
        )
        self.assertEqual(list(scan.scan([-1, 5], initial=1)), [1, 0, 5])
        self.assertEqual(list(scan.scan([0], initial=100)), [100, 100])
        self.assertEqual(list(scan.scan([], initial=100)), [100])

    def test_empty_input_iterator(self):
        self.assertEqual(list(*scan.scan([])), [])
        self.assertEqual(list(*scan.scan([], operator.mul)), [])

    def test_count_ones(self):
        def count_if_even(total: int, item: int) -> int:
            if item % 2 == 0:
                total += 1
            return total

        self.assertEqual(
            list(scan.scan([0, 1, 2, 3, 4], count_if_even, initial=0)),
            [0, 1, 1, 2, 2, 3],
        )
        self.assertEqual(
            list(scan.scan([-1, -4, 0, 2], count_if_even, initial=0)), [0, 0, 1, 2, 3]
        )


if __name__ == "__main__":
    unittest.main()
