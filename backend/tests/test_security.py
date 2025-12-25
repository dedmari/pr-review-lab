from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sql_injection_or_attack():
    """Test that OR injection attempts don't return all records"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q=' OR '1'='1")
        assert r.status_code == 200

        # Verify the parameterized query was used (preventing injection)
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert "' OR '1'='1" in call_args[0][1][0]  # The malicious input is treated as data


def test_sql_injection_comment_attack():
    """Test that comment injection attempts are handled safely"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q=' --")
        assert r.status_code == 200

        # Verify the parameterized query was used
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert "' --" in call_args[0][1][0]


def test_sql_injection_union_attack():
    """Test that UNION injection attempts are prevented"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q=' UNION SELECT 1,2 --")
        assert r.status_code == 200

        # Verify the parameterized query was used
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert "UNION" in call_args[0][1][0]  # Treated as search text, not SQL


def test_sql_injection_drop_table_attack():
    """Test that DROP TABLE injection attempts are prevented"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q='; DROP TABLE items; --")
        assert r.status_code == 200

        # Verify the parameterized query was used
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert "DROP TABLE" in call_args[0][1][0]  # Treated as search text


def test_sql_injection_multiple_statements():
    """Test that multiple statement injection attempts are prevented"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q='; SELECT * FROM users; --")
        assert r.status_code == 200

        # Verify only one query was executed
        assert mock_cursor.execute.call_count == 1

        # Verify the parameterized query was used
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert "SELECT * FROM users" in call_args[0][1][0]  # Treated as search text


def test_legitimate_search_works():
    """Test that legitimate searches still work correctly"""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "alpha"), (2, "alphabet")]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.get_conn", return_value=mock_conn):
        r = client.get("/items/search?q=alp")
        assert r.status_code == 200
        assert len(r.json()) == 2
        assert r.json()[0]["name"] == "alpha"

        # Verify the parameterized query was used correctly
        call_args = mock_cursor.execute.call_args
        assert call_args[0][0] == "SELECT id, name FROM items WHERE name LIKE ?"
        assert call_args[0][1][0] == "%alp%"
