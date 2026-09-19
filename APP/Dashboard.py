import streamlit as st
from pathlib import Path
import plotly.express as px
from Eda import carga_de_datos

data = Path(__file__).parent / "archivos" / "df_clean.csv"

# Carga de datos para obtener datos para graficos reutilizando funcion de Modulo Eda
df_final = carga_de_datos(data)

st.markdown("## ✨Visualización", text_alignment="center")

# Grafico de barras
fig1 = px.bar(df_final, x="Agencia", y="Tipo incidente", color="Agencia")
st.plotly_chart(fig1)