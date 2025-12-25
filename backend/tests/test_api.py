from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_search_items():
    # Mock the database connection and cursor
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "alpha"), (2, "alphabet")]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q=alp")
        assert r.status_code == 200
        assert any(x["name"] == "alpha" for x in r.json())

        # Verify the SQL query was executed
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()