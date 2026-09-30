import streamlit as st

# Configuración general de la página
st.set_page_config(page_icon="🧮", page_title="Analisis Turismo", layout="wide")

# Funcion main(): contiene las paginas y las ejecuta al ser seleccionada.
def main():
    principal = st.Page("Principal.py", title="Bienvenidos", icon="👋")
    eda = st.Page("Eda.py", title= "EDA", icon="🔎")
    dashboard = st.Page("Dashboard.py", title= "Dashboard de Incidencias Turisticas", icon="📊")
    etl = st.Page("ETL.py", title="ETL", icon="⚙")
    comparacion = st.Page("Comparacion.py", title="Comparación v1 vs v2", icon="🔀")
    preguntas = st.Page("Preguntas.py", title="Preguntas", icon="❓")

    paginacion = st.navigation([principal, eda, etl, comparacion, preguntas, dashboard])

    paginacion.run()

main()