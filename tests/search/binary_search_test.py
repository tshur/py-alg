from dsap.search import binary_search
from dsap.search.binary_search import lower_bound, upper_bound


class TestBinarySearch:
    def test_element_exists(self):
        assert binary_search([1, 2, 3, 4, 5], 3) == 2
        assert binary_search([1, 2, 3, 4, 5], 2) == 1
        assert binary_search([1, 2, 3, 4, 5], 4) == 3

    def test_element_not_found(self):
        assert binary_search([1, 2, 3, 4, 5], 0) is None
        assert binary_search([1, 2, 3, 4, 5], 10) is None
        assert binary_search([1, 2, 3, 15, 16], 10) is None

    def test_empty_input(self):
        assert binary_search([], 1) is None

    def test_element_at_boundary(self):
        assert binary_search([1, 2, 3, 4, 5], 5) == 4
        assert binary_search([1, 2, 3, 4, 5], 1) == 0

    def test_maximum_iterations_to_find_element(self):
        assert binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) == 4
        assert binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9) == 9


class TestLowerBound:
    def test_element_exists(self):
        assert lower_bound([1, 2, 3, 4, 5], 3) == 2
        assert lower_bound([1, 2, 3, 4, 5], 2) == 1
        assert lower_bound([1, 2, 3, 4, 5], 4) == 3

    def test_element_not_found(self):
        assert lower_bound([1, 2, 3, 4, 5], 0) == 0
        assert lower_bound([1, 2, 3, 4, 5], 10) == 5
        assert lower_bound([1, 2, 3, 15, 16], 10) == 3

    def test_empty_input(self):
        assert lower_bound([], 1) == 0

    def test_multiple_copies(self):
        assert lower_bound([1, 1, 1, 1, 1, 1], 1) == 0
        assert lower_bound([1, 2, 2, 3, 4, 5], 2) == 1
        assert lower_bound([1, 2, 3, 4, 4, 4], 4) == 3


class TestUpperBound:
    def test_element_exists(self):
        assert upper_bound([1, 2, 3, 4, 5], 3) == 3
        assert upper_bound([1, 2, 3, 4, 5], 2) == 2
        assert upper_bound([1, 2, 3, 4, 5], 4) == 4

    def test_element_not_found(self):
        assert upper_bound([1, 2, 3, 4, 5], 0) == 0
        assert upper_bound([1, 2, 3, 4, 5], 10) == 5
        assert upper_bound([1, 2, 3, 15, 16], 10) == 3

    def test_empty_input(self):
        assert upper_bound([], 1) == 0

    def test_multiple_copies(self):
        assert upper_bound([1, 1, 1, 1, 1, 1], 1) == 6
        assert upper_bound([1, 2, 2, 3, 4, 5], 2) == 3
        assert upper_bound([1, 1, 2, 3, 4, 5], 1) == 2
