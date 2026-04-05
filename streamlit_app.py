import streamlit as st
from auth import login
from database import init_db

st.set_page_config(page_title="Gestão de Encomendas")

init_db()

if not login():
    st.stop()

st.title("Sistema de Encomendas de Leitão")

st.sidebar.success("Escolhe uma opção")