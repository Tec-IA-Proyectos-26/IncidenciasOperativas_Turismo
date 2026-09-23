import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report

st.markdown("## 🔍 TourOps: Analisis Exploratorio de Datos", text_alignment="center")
st.divider()

# Link del dataset que vamos a utilizar
url_raw = "https://raw.githubusercontent.com/Tec-IA-Proyectos-26/IncidenciasOperativas_Turismo/main/DATOS/bitacora_tempo25-26_version1.csv"

# Lectura del archivo de la url
# Decorador @st.cache_data guarda la apertura del archivo en cache para no repetir la apertura en cada refresh
@st.cache_data
def carga_de_datos(url_raw):
    return pd.read_csv(url_raw)

# Generacion de reporte EDA del archivo
# Decorador @st.cache_resourse guarda y conserva el reporte generado en memoria en cada refresh
@st.cache_resource
def generacion_reporte(df):
    profile = ProfileReport(df)
    return profile

df = carga_de_datos(url_raw)
reporte = generacion_reporte(df)

# Condicion que ejecuta si la variable df fue cargada con datos
# Cambiar estructura de codigo por bloque try <-
if df is not None:
    st_profile_report(reporte)
