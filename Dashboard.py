import streamlit as st
import plotly.express as px
from Eda import carga_de_datos

url_raw = "https://raw.githubusercontent.com/Tec-IA-Proyectos-26/IncidenciasOperativas_Turismo/main/DATOS/bitacora_tempo25-26_version1.csv"

# Carga de datos para obtener datos para graficos reutilizando funcion de Modulo Eda
df = carga_de_datos(url_raw)

st.markdown("## ✨Visualización", text_alignment="center")

# Grafico de barras
fig1 = px.bar(df, x="Agencia", y="Tipo incidente", color="Agencia")
st.plotly_chart(fig1)