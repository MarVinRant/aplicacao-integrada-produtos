from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from client import create_remote_product, fetch_products
from integrated_db import add_product, all_products, initialize


st.set_page_config(page_title="Produtos Integrados", page_icon=":material/hub:", layout="wide")
initialize()
st.title(":material/hub: Aplicação integrada de produtos")
st.caption("SQLite + FastAPI + Streamlit")

with st.expander("Adicionar produto"):
    with st.form("add_product"):
        produto = st.text_input("Produto")
        categoria = st.text_input("Categoria")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        quantidade = st.number_input("Itens vendidos", min_value=0, step=1)
        if st.form_submit_button("Salvar"):
            if produto.strip() and categoria.strip():
                payload = {
                    "produto": produto.strip(),
                    "categoria": categoria.strip(),
                    "preco": preco,
                    "quantidade_vendida": quantidade,
                }
                try:
                    create_remote_product(payload)
                    st.success("Produto enviado pela API para o SQLite.")
                except Exception:
                    add_product(**payload)
                    st.warning("API indisponível; produto salvo diretamente no SQLite.")
                st.rerun()
            st.error("Produto e categoria são obrigatórios.")

try:
    data = pd.DataFrame(fetch_products())
    st.caption("Fonte atual: API FastAPI")
except Exception:
    data = pd.DataFrame(all_products())
    st.caption("Fonte atual: SQLite local (API indisponível)")
if data.empty:
    st.info("Cadastre o primeiro produto para visualizar os indicadores.")
else:
    with st.container(horizontal=True):
        st.metric("Produtos", len(data), border=True)
        st.metric("Preço médio", f"R$ {data['preco'].mean():,.2f}", border=True)
        st.metric("Itens vendidos", int(data["quantidade_vendida"].sum()), border=True)
    st.dataframe(data, hide_index=True)

