from algorithms.search import binary_search


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
