from __future__ import annotations

import sqlite3
import csv
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).parent / "integrated.db"
SEED_PATH = Path(__file__).parent / "data" / "products.csv"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with closing(connect()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK (preco >= 0),
                quantidade_vendida INTEGER NOT NULL CHECK (quantidade_vendida >= 0)
            )
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
        if count == 0 and SEED_PATH.exists():
            with SEED_PATH.open(newline="", encoding="utf-8") as file:
                rows = csv.DictReader(file)
                connection.executemany(
                    "INSERT INTO produtos (produto, categoria, preco, quantidade_vendida) VALUES (?, ?, ?, ?)",
                    [
                        (row["produto"], row["categoria"], float(row["preco"]), int(row["quantidade_vendida"]))
                        for row in rows
                    ],
                )


def all_products() -> list[dict]:
    with closing(connect()) as connection:
        rows = connection.execute("SELECT * FROM produtos ORDER BY produto").fetchall()
        return [dict(row) for row in rows]


def add_product(produto: str, categoria: str, preco: float, quantidade_vendida: int) -> None:
    with closing(connect()) as connection, connection:
        connection.execute(
            "INSERT INTO produtos (produto, categoria, preco, quantidade_vendida) VALUES (?, ?, ?, ?)",
            (produto, categoria, preco, quantidade_vendida),
        )

