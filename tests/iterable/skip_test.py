import pytest

from dsap.iterable import skip


class TestSkip:
    def test_default_skip_one_element(self):
        iterator = iter(range(10))

        skip(iterator)
        assert next(iterator) == 1
        skip(iterator)
        assert next(iterator) == 3
        skip(iterator)
        assert next(iterator) == 5

    def test_skip_multiple(self):
        iterator = iter(range(10))

        skip(iterator, 5)
        assert next(iterator) == 5
        skip(iterator, 2)
        assert next(iterator) == 8

    def test_skip_zero_elements(self):
        iterator = iter(range(10))

        skip(iterator, n=0)
        assert next(iterator) == 0

        skip(iterator, n=0)
        skip(iterator, n=0)
        skip(iterator, n=0)
        assert next(iterator) == 1

    def test_skip_beyond_length(self):
        with pytest.raises(StopIteration):
            skip(iter(range(2)), 3)
        with pytest.raises(StopIteration):
            skip(iter(range(10)), 20)
        with pytest.raises(StopIteration):
            skip(iter(range(0)))

    def test_skip_negative(self):
        with pytest.raises(ValueError, match="cannot skip iterator negative elements"):
            skip(iter(range(10)), -2)
