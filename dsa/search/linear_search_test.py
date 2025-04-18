from .linear_search import linear_search


class TestLinearSearch:
    def test_element_exists(self):
        assert linear_search([3, 1, 5, 4, 2], 1) == 1
        assert linear_search([3, 1, 5, 4, 2], 5) == 2
        assert linear_search([3, 1, 5, 4, 2], 4) == 3

    def test_element_not_found(self):
        assert linear_search([3, 1, 5, 4, 2], 0) is None
        assert linear_search([3, 1, 5, 4, 2], 10) is None
        assert linear_search([3, 1, 5, 4, 2], 6) is None

    def test_empty_input(self):
        assert linear_search([], 1) is None

    def test_element_at_boundary(self):
        assert linear_search([3, 1, 5, 4, 2], 2) == 4
        assert linear_search([3, 1, 5, 4, 2], 3) == 0
