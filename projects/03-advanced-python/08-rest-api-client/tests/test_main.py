"""Tests for REST API Client."""

import pytest

# from src.main import APIClient, APIError


class TestGetRequest:
    def test_successful_get(self) -> None:
        pytest.skip("Implement this test — mock the HTTP response.")

    def test_404_raises_error(self) -> None:
        pytest.skip("Implement this test.")


class TestPostRequest:
    def test_successful_post(self) -> None:
        pytest.skip("Implement this test.")


class TestRetryLogic:
    def test_retries_on_500(self) -> None:
        pytest.skip("Implement this test.")

    def test_no_retry_on_400(self) -> None:
        pytest.skip("Implement this test.")


class TestAuthentication:
    def test_bearer_token_in_header(self) -> None:
        pytest.skip("Implement this test.")

    def test_basic_auth_in_header(self) -> None:
        pytest.skip("Implement this test.")
