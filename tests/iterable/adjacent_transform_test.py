import operator

from dsap.iterable import adjacent_transform, pairwise_transform


class TestAdjacentTransform:
    def test_pairwise_transform_sum(self):
        assert list(adjacent_transform([1, 2, 3, 4, 5], sum)) == [3, 5, 7, 9]
        assert list(adjacent_transform([-5, 5], sum)) == [0]
        assert list(adjacent_transform([1, 1, 1, 1, 1], sum)) == [2, 2, 2, 2]

    def test_adjacent_transform_sum(self):
        assert list(adjacent_transform([1, 2, 3, 4, 5], sum, 3)) == [6, 9, 12]
        assert list(adjacent_transform([1, 2, 3, 4, 5], sum, 4)) == [10, 14]
        assert list(adjacent_transform([1, 2, 3, 4, 5], sum, 5)) == [15]

    def test_input_too_short(self):
        assert list(adjacent_transform([], sum)) == []
        assert list(adjacent_transform([5], sum)) == []
        assert list(adjacent_transform([-5, 5], sum, 3)) == []

    def test_small_window_size(self):
        assert list(adjacent_transform([1, 2, 3], sum, 1)) == [1, 2, 3]
        assert list(adjacent_transform([1, 2, 3], sum, 0)) == []

    def test_moving_average(self):
        def average(nums: tuple[int, ...]) -> float:
            return sum(nums) / len(nums)

        assert list(adjacent_transform([1, 3, -1, 1], average)) == [2, 1, 0]
        assert list(adjacent_transform([1, 2, 5], average)) == [1.5, 3.5]


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
