import streamlit as st

from etl_functions import cargar_version1, cargar_version2, comparar_versiones

st.markdown("## 🔀 Comparación Version1 vs Version2", text_alignment="center")
st.divider()

df_v1 = cargar_version1()
df_v2 = cargar_version2()
resumen = comparar_versiones(df_v1, df_v2)

col1, col2 = st.columns(2)
col1.metric("Filas Version1", resumen["filas_v1"]) 
col2.metric("Filas Version2", resumen["filas_v2"])

col1.write(f"**Columnas solo en Version1:** {resumen['columnas_solo_v1'] or 'ninguna'}")
col2.write(f"**Columnas solo en Version2:** {resumen['columnas_solo_v2'] or 'ninguna'}")

st.subheader("Valores nulos por columna (comunes a ambas versiones)")
st.dataframe(resumen["nulos_por_columna"], width='stretch')
