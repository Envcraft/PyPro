"""Tests for Production REST API."""

import pytest

# import pytest_asyncio
# from httpx import AsyncClient
# from src.main import app


class TestAuthentication:
    async def test_register_new_user(self) -> None:
        pytest.skip("Implement this test.")

    async def test_register_duplicate_email(self) -> None:
        pytest.skip("Implement this test.")

    async def test_login_correct_credentials(self) -> None:
        pytest.skip("Implement this test.")

    async def test_login_wrong_password(self) -> None:
        pytest.skip("Implement this test.")


class TestTaskCRUD:
    async def test_create_task(self) -> None:
        pytest.skip("Implement this test.")

    async def test_list_tasks_paginated(self) -> None:
        pytest.skip("Implement this test.")

    async def test_cannot_access_other_users_task(self) -> None:
        pytest.skip("Implement this test.")

    async def test_update_task(self) -> None:
        pytest.skip("Implement this test.")

    async def test_delete_task(self) -> None:
        pytest.skip("Implement this test.")
