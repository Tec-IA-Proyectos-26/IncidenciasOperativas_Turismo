import streamlit as st
from pathlib import Path
# importamos el modulo components que es una libreria nativa de streamlit para renderizar html
# import streamlit.components.v1 as components

st.markdown("## 🛠 TourOps: Procesamiento de Datos", text_alignment="center")
st.divider()

ruta_html = Path(__file__).parent / "archivos" / "ETL_html.html"

# Version anterior components.html quedo deprecado streamlit pide usar st.iframe en su lugar
# with open(ruta_html,"r", encoding="utf-8") as etl:
#     contenido = etl.read()
# components.html(contenido, height=1200, scrolling=True)
# st.iframe acepta un Path a un archivo HTML local y lo lee/embebe el solo,
# sin necesidad de abrirlo manualmente como antes
st.iframe(ruta_html, height=1200)