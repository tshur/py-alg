import operator

from algorithms.adjacent_transform import pairwise_transform


class TestPairwiseTransform:
    def test_default_pairwise_sum(self):
        assert list(pairwise_transform([1, 2, 3, 4, 5])) == [3, 5, 7, 9]
        assert list(pairwise_transform([-5, 5])) == [0]
        assert list(pairwise_transform([1, 1, 1, 1, 1])) == [2, 2, 2, 2]

    def test_input_too_short(self):
        assert list(pairwise_transform([])) == []
        assert list(pairwise_transform([5])) == []

    def test_subtraction_operator(self):
        assert list(pairwise_transform([5, 4, 3, 2, 1], operator.sub)) == [1, 1, 1, 1]
        assert list(pairwise_transform([10, 10], operator.sub)) == [0]

    def test_moving_average(self):
        def average(a: int, b: int) -> float:
            return (a + b) / 2

        assert list(pairwise_transform([1, 3, -1, 1], average)) == [2, 1, 0]
        assert list(pairwise_transform([1, 2, 5], average)) == [1.5, 3.5]
