from fastapi import FastAPI
from pydantic import BaseModel, Field

from integrated_db import add_product, all_products, initialize


class ProductCreate(BaseModel):
    produto: str = Field(min_length=2)
    categoria: str = Field(min_length=2)
    preco: float = Field(ge=0)
    quantidade_vendida: int = Field(ge=0)


app = FastAPI(title="Produtos Integrados", version="1.0.0")
initialize()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/produtos")
def products(categoria: str | None = None) -> list[dict]:
    items = all_products()
    if categoria:
        return [item for item in items if item["categoria"].lower() == categoria.lower()]
    return items


@app.post("/produtos", status_code=201)
def create_product(payload: ProductCreate) -> dict[str, str]:
    add_product(**payload.model_dump())
    return {"status": "created"}

