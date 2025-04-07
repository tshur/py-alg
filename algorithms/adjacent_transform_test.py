import operator
import unittest

from algorithms.adjacent_transform import pairwise_transform


class PairwiseTransformTest(unittest.TestCase):
    def test_default_pairwise_sum(self):
        self.assertEqual(list(pairwise_transform([1, 2, 3, 4, 5])), [3, 5, 7, 9])
        self.assertEqual(list(pairwise_transform([-5, 5])), [0])
        self.assertEqual(list(pairwise_transform([1, 1, 1, 1, 1])), [2, 2, 2, 2])

    def test_input_too_short(self):
        self.assertEqual(list(pairwise_transform([])), [])
        self.assertEqual(list(pairwise_transform([5])), [])

    def test_subtraction_operator(self):
        self.assertEqual(
            list(pairwise_transform([5, 4, 3, 2, 1], operator.sub)), [1, 1, 1, 1]
        )
        self.assertEqual(list(pairwise_transform([10, 10], operator.sub)), [0])

    def test_moving_average(self):
        def average(a: int, b: int) -> float:
            return (a + b) / 2

        self.assertEqual(list(pairwise_transform([1, 3, -1, 1], average)), [2, 1, 0])
        self.assertEqual(list(pairwise_transform([1, 2, 5], average)), [1.5, 3.5])
