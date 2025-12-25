import os
import sqlite3
from fastapi import FastAPI, Query

app = FastAPI()

DB_PATH = os.environ.get("DB_PATH", "backend/app/app.db")


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


@app.on_event("startup")
def startup() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
    )
    cur.executemany(
        "INSERT OR IGNORE INTO items(id, name) VALUES (?, ?)",
        [(1, "alpha"), (2, "beta"), (3, "gamma")],
    )
    conn.commit()
    conn.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/search")
def search_items(q: str = Query(min_length=1, max_length=50)):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT id, name FROM items WHERE name LIKE '%{q}%'")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1]} for r in rows]