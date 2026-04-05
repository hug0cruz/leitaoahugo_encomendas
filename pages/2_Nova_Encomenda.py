import streamlit as st
from database import add_encomenda
from datetime import datetime

from auth import protect_page
protect_page()

st.title("Nova Encomenda")

produto = st.selectbox("Produto", [
    "1 leitão",
    "1/2 leitão",
    "1 dose",
    "Outro"
])

if produto == "Outro":
    produto = st.text_input("Especificar produto")

nome = st.text_input("Nome")
telefone = st.text_input("Telefone (opcional)")
data = st.datetime_input("Data da encomenda")

if st.button("Guardar"):
    if nome and produto:
        add_encomenda(produto, nome, telefone, data.strftime("%Y-%m-%d %H:%M:%S"))
        st.success("Encomenda guardada")
    else:
        st.error("Preenche os campos obrigatórios")