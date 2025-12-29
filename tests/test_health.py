from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

from unittest.mock import patch, Mock

@patch("app.main.requests.get")
def test_country_is_cached(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {
            "name": {"common": "India"},
            "capital": ["New Delhi"],
            "region": "Asia",
            "population": 1400000000,
        }
    ]
    mock_get.return_value = mock_resp

    r1 = client.get("/country/in")
    assert r1.status_code == 200
    assert r1.json()["cached"] is False

    r2 = client.get("/country/in")
    assert r2.status_code == 200
    assert r2.json()["cached"] is True

    assert mock_get.call_count == 1
