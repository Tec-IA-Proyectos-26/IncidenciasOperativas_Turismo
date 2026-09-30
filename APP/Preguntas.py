import plotly.express as px
import streamlit as st

from etl_functions import (
    anios_disponibles,
    calcular_kpis,
    cargar_datos_limpios,
    evolucion_por_mes,
    top_n_conteo,
)

st.markdown("## Preguntas sobre Incidencias", text_alignment="center")
st.markdown("#### Análisis de Incidencias y Patrones")
st.divider()

df = cargar_datos_limpios()

# ---------- Filtros para aplicar

fecha_min, fecha_max = df["Marca de tiempo"].min().date(), df["Marca de tiempo"].max().date()
rango_fecha = st.sidebar.date_input("Fecha", value=(fecha_min, fecha_max), min_value=fecha_min, max_value=fecha_max)

tipos_sel = st.sidebar.multiselect(
    "Tipo de Incidencia", sorted(df["Tipo incidente"].dropna().unique()), placeholder="Elegir opciones"
)
impacto_sel = st.sidebar.multiselect(
    "Impacto", sorted(df["Impacto"].dropna().unique()), placeholder="Elegir opciones"
)
proveedor_sel = st.sidebar.multiselect(
    "Proveedor", sorted(df["Proveedor"].dropna().unique()), placeholder="Elegir opciones"
)
servicio_sel = st.sidebar.multiselect(
    "Servicio", sorted(df["Servicio"].dropna().unique()), placeholder="Elegir opciones"
)

df_filtrado = df.copy()
if len(rango_fecha) == 2:
    desde, hasta = rango_fecha
    fecha = df_filtrado["Marca de tiempo"]
    # Las filas sin fecha (NaT) se mantienen siempre: no hay forma de saber si caen
    # dentro del rango, y descartarlas rompia el "seleccionar todos los datos".
    df_filtrado = df_filtrado[
        fecha.isna() | ((fecha.dt.date >= desde) & (fecha.dt.date <= hasta))
    ]
if tipos_sel:
    df_filtrado = df_filtrado[df_filtrado["Tipo incidente"].isin(tipos_sel)]
if impacto_sel:
    df_filtrado = df_filtrado[df_filtrado["Impacto"].isin(impacto_sel)]
if proveedor_sel:
    df_filtrado = df_filtrado[df_filtrado["Proveedor"].isin(proveedor_sel)]
if servicio_sel:
    df_filtrado = df_filtrado[df_filtrado["Servicio"].isin(servicio_sel)]

# ---------- KPIs ----------
kpis = calcular_kpis(df_filtrado)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incid.", kpis["total"])
col2.metric("Tipo más frecuente", kpis["tipo_mas_frecuente"])
col3.metric("Proveedor con más incid.", kpis["proveedor_top"])
col4.metric("% Impacto Alto", f"{kpis['pct_impacto_alto']:.1f}%")

st.divider()

# ---------- Pregunta 1 ----------
st.subheader("¿Qué tipos de incidencias son más frecuentes?")
tipo_conteo = top_n_conteo(df_filtrado, "Tipo incidente")
fig1 = px.bar(
    tipo_conteo.sort_values("Cantidad"), x="Cantidad", y="Tipo incidente", orientation="h",
)
st.plotly_chart(fig1, width='stretch')

st.divider()

# ---------- Pregunta 2 ----------
st.subheader("¿Qué servicios o proveedores concentran incidencias?")
col_prov, col_serv = st.columns(2)

proveedor_conteo = top_n_conteo(df_filtrado, "Proveedor")
fig_proveedor = px.bar(
    proveedor_conteo.sort_values("Cantidad"), x="Cantidad", y="Proveedor", orientation="h",
    title="Top proveedores",
)
col_prov.plotly_chart(fig_proveedor, width='stretch')

servicio_conteo = top_n_conteo(df_filtrado, "Servicio")
fig_servicio = px.bar(
    servicio_conteo.sort_values("Cantidad"), x="Cantidad", y="Servicio", orientation="h",
    title="Top servicios",
)
col_serv.plotly_chart(fig_servicio, width='stretch')

st.divider()

# ---------- Pregunta 3 ----------
st.subheader("¿En qué períodos se registran más incidencias?")
opciones_anio = ["Todos"] + anios_disponibles(df_filtrado)
anio_sel = st.selectbox("Año", opciones_anio)
evolucion = evolucion_por_mes(df_filtrado, anio_sel)
fig_evolucion = px.line(evolucion, x="mes", y="Cantidad", markers=True)
st.plotly_chart(fig_evolucion, width='stretch')

st.divider()

# ---------- Pregunta 4 ----------
st.subheader("¿Qué impacto tienen estas situaciones?")
col_donut, col_kpi = st.columns(2)

impacto_conteo = df_filtrado["Impacto"].value_counts().rename_axis("Impacto").reset_index(name="Cantidad")
fig_donut = px.pie(impacto_conteo, values="Cantidad", names="Impacto", hole=0.4)
col_donut.plotly_chart(fig_donut, width='stretch')

col_kpi.metric("Impacto Alto", f"{kpis['pct_impacto_alto']:.1f}%", help="Porcentaje de incidencias con impacto alto sobre el total filtrado")

st.divider()

# ---------- Pregunta 5 ----------
#st.subheader("¿?")
#st.info("A definir")
