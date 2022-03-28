from os import environ
import asyncio
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.testclient import TestClient

from app.api.services.users import get_user_manager
from app.models.schemas.users import UserCreate
from app.db.base import Base
from app.db.utils import engine
from app.core.config import settings

from sqlalchemy.ext.asyncio import create_async_engine


environ['APP_ENV'] = "test"

@pytest.fixture
async def app() -> FastAPI:
    from app.main import app  # local import for testing purpose
    yield app

@pytest.fixture
async def json_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client

@pytest.fixture
async def urlencoded_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ) as client:
        yield client

@pytest.fixture
def test_user_data():
    return {'email': 'test@test.com', 'password': 'testpass'}


@pytest.fixture
async def test_user(app, json_client, test_user_data) -> None:
    return await json_client.post(
        app.url_path_for("register:register"), json=test_user_data
    )

@pytest.fixture
async def token(app, urlencoded_client, test_user, test_user_data) -> str:

    username = test_user_data.pop('email')
    test_user_data.update({'username': username})

    user_resp = await urlencoded_client.post(
            app.url_path_for("auth:jwt.login"), data=test_user_data
        )
    return user_resp.json().get('access_token')


@pytest.fixture
def authorization_prefix():
    return 'Bearer'

@pytest.fixture
async def authorized_json_client(
    app: FastAPI, token: str, authorization_prefix: str
) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        client.headers = {
            "Authorization": f"{authorization_prefix} {token}",
            **client.headers,
        }
        yield client

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
