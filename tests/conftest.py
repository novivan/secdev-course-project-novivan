# tests/conftest.py
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]  # поднимаемся на уровень выше tests/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from app.main import app
except ImportError as e:
    raise ImportError(f"Не удалось импортировать app.main. sys.path: {sys.path}") from e

@pytest.fixture
def client():
    return TestClient(app)
