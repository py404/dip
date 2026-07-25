from unittest.mock import patch

import pytest
from dip_api.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_get_settings():
    with patch.dict(
        "os.environ",
        {
            "API_HOST": "0.0.0.0",
            "API_PORT": "8000",
            "LOG_LEVEL": "info",
        },
    ):
        yield


def test_health_returns_200() -> None:
    client = TestClient(app)
    response = client.get("/health")
    print(response.json())

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "api_host": "0.0.0.0",
        "api_port": "8000",
        "log_level": "info",
    }
