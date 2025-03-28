import uuid
import pytest
import asyncio
from httpx import AsyncClient
from app.main import app

# Використання pytest-asyncio в автоматичному режимі
pytest_plugins = "pytest_asyncio"


@pytest.fixture(scope="function")
def event_loop():
    """Створює окремий event loop для кожного тесту."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    """Асинхронний тест-клієнт FastAPI."""
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture(scope="function")
def test_user():
    """Генерує тестові дані користувача."""
    return {
        "name": "John",
        "surname": "Doe",
        "email": f"testuser_{uuid.uuid4().hex}@example.com",
        "password": "SecurePass123!",
        "city": "Kyiv",
        "phone_number": "+380123456789",
        "nova_post_department": "1",
    }


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient, test_user):
    """Тест реєстрації нового користувача."""
    response = await async_client.post("/auth/register", json=test_user)

    assert response.status_code in [200, 201], \
        f"Unexpected status code: {response.status_code}, response: {response.json()}"

    data = response.json()

    assert "id" in data
    assert data["email"] == test_user["email"]


@pytest.fixture(scope="function")
async def user_token(async_client: AsyncClient, test_user):
    """Отримання токена для зареєстрованого користувача."""
    response = await async_client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200, \
        f"Unexpected status code: {response.status_code}, response: {response.json()}"

    data = response.json()

    # Логування токена для перевірки
    print(f"\n✅ TOKEN DEBUG: {data}")

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]


@pytest.mark.asyncio
async def test_get_user_profile(async_client: AsyncClient, user_token: str, test_user):
    """Тест отримання профілю користувача."""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await async_client.get("/users/me", headers=headers)

    assert response.status_code == 200, \
        f"Unexpected status code: {response.status_code}, response: {response.json()}"

    data = response.json()
    assert data["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_unauthorized_access(async_client: AsyncClient):
    """Тест отримання профілю без авторизації."""
    response = await async_client.get("/users/me")
    assert response.status_code == 401
