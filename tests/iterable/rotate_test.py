from dsap.iterable import rotate


class TestRotate:
    def test_rotate_forward(self):
        assert rotate([1, 2, 3, 4, 5], 1) == [5, 1, 2, 3, 4]
        assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
        assert rotate([1, 2, 3, 4, 5], 3) == [3, 4, 5, 1, 2]
        assert rotate([1, 2, 3, 4, 5], 4) == [2, 3, 4, 5, 1]
        assert rotate([1, 2, 3, 4, 5], 0) == [1, 2, 3, 4, 5]

    def test_rotate_backward(self):
        assert rotate([1, 2, 3, 4, 5], -1) == [2, 3, 4, 5, 1]
        assert rotate([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]
        assert rotate([1, 2, 3, 4, 5], -3) == [4, 5, 1, 2, 3]
        assert rotate([1, 2, 3, 4, 5], -4) == [5, 1, 2, 3, 4]

    def test_rotate_multiple_cycles(self):
        assert rotate([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]
        assert rotate([1, 2, 3, 4, 5], 15) == [1, 2, 3, 4, 5]
        assert rotate([1, 2, 3, 4, 5], 17) == [4, 5, 1, 2, 3]

    def test_rotate_small_input(self):
        assert rotate([], 3) == []
        assert rotate([1], 3) == [1]

    def test_equivalence(self):
        # Two rotates are equivalent if their modulo the array length is equal.
        assert rotate([1, 2, 3, 4, 5], 2) == rotate([1, 2, 3, 4, 5], -3)
        assert rotate([1, 2, 3, 4, 5], 2) == rotate([1, 2, 3, 4, 5], 7)
