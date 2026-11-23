"""Tests for Expense Tracker."""

import pytest

# from src.main import (
#     add_expense, delete_expense, get_total,
#     get_category_totals, get_largest_expense, filter_by_category
# )


class TestGetTotal:
    def test_total_of_multiple_expenses(self) -> None:
        pytest.skip("Implement this test.")

    def test_total_of_empty_list(self) -> None:
        pytest.skip("Implement this test.")


class TestCategoryTotals:
    def test_multiple_categories(self) -> None:
        pytest.skip("Implement this test.")


class TestLargestExpense:
    def test_finds_largest(self) -> None:
        pytest.skip("Implement this test.")

    def test_empty_list_returns_none(self) -> None:
        pytest.skip("Implement this test.")


class TestFilterByCategory:
    def test_filters_correctly(self) -> None:
        pytest.skip("Implement this test.")

    def test_nonexistent_category_returns_empty(self) -> None:
        pytest.skip("Implement this test.")


class TestDeleteExpense:
    def test_deletes_existing(self) -> None:
        pytest.skip("Implement this test.")

    def test_returns_false_for_nonexistent_id(self) -> None:
        pytest.skip("Implement this test.")
