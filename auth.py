import streamlit as st

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


def login():
    init_session()

    if st.session_state.logged_in:
        return True

    st.title("Login")

    user = st.text_input("Utilizador")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):
        if user == "leitao" and password == "leitao":
            st.session_state.logged_in = True
            st.success("Login feito")
            st.rerun()
        else:
            st.error("Credenciais erradas")

    return False


def protect_page():
    init_session()

    if not st.session_state.logged_in:
        st.error("Acesso bloqueado. Faz login primeiro.")
        st.stop()