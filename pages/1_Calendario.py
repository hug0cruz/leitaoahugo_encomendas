from auth import protect_page
protect_page()

import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from database import get_encomendas
from pdf_generator import gerar_pdf
from datetime import datetime

st.title("📅 Calendário de Encomendas")

# 🔥 Converter string para YYYY-MM-DD
def to_date_str(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

# 🔥 Buscar dados
data = get_encomendas()

# 🔥 Criar eventos SEM hora (evita timezone bugs)
events = []

for e in data:
    _, produto, nome, telefone, data_str = e

    dia = to_date_str(data_str)

    events.append({
        "title": f"{nome} - {produto}",
        "start": dia,
        "allDay": True
    })

# 🔥 Configuração do calendário
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "pt",
    "selectable": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar_result = calendar(events=events, options=calendar_options)

# 🛑 Evitar crash
if not calendar_result:
    st.stop()

# 🔥 EXTRAIR DATA (ROBUSTO)
selected_date = None

if calendar_result.get("dateClick"):
    click = calendar_result["dateClick"]

    if "dateStr" in click:
        selected_date = click["dateStr"][:10]

    elif "date" in click:
        selected_date = click["date"].split("T")[0]

elif calendar_result.get("eventClick"):
    event = calendar_result["eventClick"]["event"]
    selected_date = event["start"].split("T")[0]

# 🔥 MOSTRAR ENCOMENDAS DO DIA
if selected_date:
    st.subheader(f"📦 Encomendas para {selected_date}")

    encomendas_dia = []

    for e in data:
        if to_date_str(e[4]) == selected_date:
            encomendas_dia.append(e)

    if encomendas_dia:
        df = pd.DataFrame(
            encomendas_dia,
            columns=["ID", "Produto", "Nome", "Telefone", "Data"]
        ).sort_values("Data")

        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📄 Gerar PDF do dia"):
                file = gerar_pdf(encomendas_dia)

                with open(file, "rb") as f:
                    st.download_button(
                        "⬇️ Descarregar PDF",
                        f,
                        file_name=f"encomendas_{selected_date}.pdf"
                    )

        with col2:
            st.metric("Total", len(encomendas_dia))

    else:
        st.warning("Sem encomendas neste dia")

# 🔥 SEPARADOR
st.divider()

# 🔥 INTERVALO DE DATAS
st.subheader("📊 Exportar várias datas")

col1, col2 = st.columns(2)

with col1:
    data_inicio = st.date_input("Data início")

with col2:
    data_fim = st.date_input("Data fim")

if data_inicio and data_fim:

    if data_inicio > data_fim:
        st.error("Data início maior que data fim")

    else:
        encomendas_intervalo = []

        for e in data:
            d = datetime.strptime(e[4], "%Y-%m-%d %H:%M:%S").date()

            if data_inicio <= d <= data_fim:
                encomendas_intervalo.append(e)

        if encomendas_intervalo:
            df = pd.DataFrame(
                encomendas_intervalo,
                columns=["ID", "Produto", "Nome", "Telefone", "Data"]
            ).sort_values("Data")

            st.dataframe(df, use_container_width=True)

            colA, colB = st.columns(2)

            with colA:
                if st.button("📄 Gerar PDF intervalo"):
                    file = gerar_pdf(encomendas_intervalo)

                    with open(file, "rb") as f:
                        st.download_button(
                            "⬇️ Descarregar PDF",
                            f,
                            file_name=f"encomendas_{data_inicio}_a_{data_fim}.pdf"
                        )

            with colB:
                st.metric("Total", len(encomendas_intervalo))

        else:
            st.warning("Sem encomendas nesse intervalo")