import streamlit as st

st.title("🧮 TourOps: Analisis de incidencias turisticas", text_alignment="center")

# Lectura de archivo markdown con la informacion del proyecto.
with open("archivos\principal.md", "r", encoding="utf-8") as mkd:
    st.markdown(mkd.read())