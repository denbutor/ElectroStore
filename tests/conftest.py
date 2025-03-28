# import os
# import sys
# from fastapi.testclient import TestClient
#
# import pytest
# from httpx import AsyncClient
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# from app.main import app
#
# @pytest.fixture(scope="module")
# async def async_client():
#     """Фікстура для асинхронного тестування FastAPI."""
#     async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
#         yield client