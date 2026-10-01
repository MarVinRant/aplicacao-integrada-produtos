from __future__ import annotations

import os

import requests


API_URL = os.getenv("PRODUCTS_API_URL", "http://127.0.0.1:8503")


def fetch_products() -> list[dict]:
    response = requests.get(f"{API_URL}/produtos", timeout=2)
    response.raise_for_status()
    return response.json()


def create_remote_product(payload: dict) -> None:
    response = requests.post(f"{API_URL}/produtos", json=payload, timeout=2)
    response.raise_for_status()
