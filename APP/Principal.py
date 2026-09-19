from pathlib import Path
import streamlit as st

st.title("🧮 TourOps: Analisis de incidencias turisticas", text_alignment="center")

# Lectura de archivo markdown con la informacion del proyecto.
ruta_md = Path(__file__).parent / "archivos" / "principal.md"
with open(ruta_md, "r", encoding="utf-8") as mkd:
    st.markdown(mkd.read())