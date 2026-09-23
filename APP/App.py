import streamlit as st

# Configuración general de la página
st.set_page_config(page_icon="🧮", page_title="Analisis Turismo", layout="wide")

# Funcion main(): contiene las paginas y las ejecuta al ser seleccionada.
def main():
    principal = st.Page("Principal.py", title="Bienvenidos", icon="👋")
    eda = st.Page("Eda.py", title= "EDA", icon="🔎")
    dashboard = st.Page("Dashboard.py", title= "Dashboard de Incidencias Turisticas", icon="📊")
    etl = st.Page("ETL.py", title="ETL", icon="⚙")

    paginacion = st.navigation([principal, eda, etl, dashboard])

    paginacion.run()

main()