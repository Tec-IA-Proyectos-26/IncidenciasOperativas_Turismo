import plotly.express as px
import streamlit as st

from etl_functions import cargar_datos_limpios, excluir_sin_informacion, resumen_por_agencia

# Los datos se cargan desde etl_functions (importar Eda ejecutaba toda la pagina de EDA)
df_final = cargar_datos_limpios()

st.markdown("## ✨ Visualización - Reporte de Incidencias por Agencia", text_alignment="center")

# Grafico de barras: incidencias unicas por agencia (sin las que no informan agencia)
incidencias_agencia = excluir_sin_informacion(resumen_por_agencia(df_final), "Agencia")
fig1 = px.bar(incidencias_agencia, x="Agencia", y="Cantidad", color="Agencia")
st.plotly_chart(fig1, width="stretch")