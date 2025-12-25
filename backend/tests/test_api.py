from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_search_items():
    r = client.get("/items/search?q=alp")
    assert r.status_code == 200
    assert any(x["name"] == "alpha" for x in r.json())