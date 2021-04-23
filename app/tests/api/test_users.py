from typing import Dict
from app.tests.conftest import default_user, default_superuser
from app.core.config import settings
from asyncio import AbstractEventLoop as EventLoop
from fastapi.testclient import TestClient
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import get_random_user_me, get_random_user_by_superuser
import pytest


def test_read_users_superuser(
    client: TestClient,
    event_loop: EventLoop,
    normal_user_token_headers: Dict[str, str],
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.API_STR}/users/", headers=superuser_token_headers)
    users = r.json()
    assert len(users) >= 2
    for user in users:
        assert "email" in user
        assert "created_at" in user


def test_create_user_superuser(
    client: TestClient,
    event_loop: EventLoop,
    superuser_token_headers: Dict[str, str],
) -> None:
    data = get_random_user_by_superuser().dict()

    r = client.post(
        f"{settings.API_STR}/users/", headers=superuser_token_headers, json=data
    )

    current_user = r.json()
    assert r.status_code == 200
    assert current_user["email"] == data["email"]


def test_read_user_me_superuser(
    client: TestClient,
    event_loop: EventLoop,
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.API_STR}/users/me/", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == default_superuser.is_active
    assert current_user["is_superuser"] == default_superuser.is_superuser
    assert current_user["email"] == default_superuser.email


def test_read_users_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_STR}/users/", headers=normal_user_token_headers)
    assert r.status_code == 400


def test_create_user_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    data = get_random_user_by_superuser().dict()
    r = client.post(
        f"{settings.API_STR}/users/", headers=normal_user_token_headers, json=data
    )
    assert r.status_code == 400


def test_read_user_me_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_STR}/users/me/", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == default_user.is_active
    assert current_user["is_superuser"] == default_user.is_superuser
    assert current_user["email"] == default_user.email