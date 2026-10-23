import plotly.express as px
import streamlit as st

from etl_functions import (
    ORDEN_IMPACTO,
    SIN_INFORMACION,
    cargar_datos_limpios,
    cargar_version2,
    cruce_conteo,
    impacto_por_tipo,
    incidencias_unicas,
    pct_sin_informacion,
    resumen_multiplicidad,
    resumen_nulos,
    resumen_por_tipo,
    tabla_mes_tipo,
    top_n_conteo,
)

st.markdown("## 🔍 TourOps: Analisis Exploratorio de Datos", text_alignment="center")
st.divider()


# Decorador @st.cache_data guarda la lectura de los archivos en cache para no repetirla en cada refresh
@st.cache_data
def carga_cruda():
    # Dataset version2 sin procesar: sirve para ver los nulos originales
    return cargar_version2()


@st.cache_data
def carga_limpia():
    # Dataset tratado (nulos imputados): es el mismo que usa el Dashboard
    return cargar_datos_limpios()


# Decorador @st.cache_resource guarda y conserva el reporte generado en memoria en cada refresh
@st.cache_resource(show_spinner=False)
def generacion_reporte(df):
    # Se importa aca (y no arriba) para que el resto de la pagina cargue rapido:
    # ydata_profiling tarda en importarse y genera el reporte recien cuando se pide.
    from ydata_profiling import ProfileReport

    # minimal=True omite las correlaciones y otros calculos pesados
    return ProfileReport(df, minimal=True, title="Perfilado automatico - bitacora version2")


try:
    df_crudo = carga_cruda()
    df = carga_limpia()
except FileNotFoundError as error:
    st.error(f"No se encontro el archivo de datos: {error.filename}")
    st.stop()

tab_visual, tab_calidad, tab_cruces, tab_reporte = st.tabs(
    ["📊 Visualizaciones", "🧹 Calidad de datos", "🔗 Proveedores y servicios", "📑 Reporte automatico"]
)

# ---------- Visualizaciones ----------
with tab_visual:
    multiplicidad = resumen_multiplicidad(df)
    col1, col2 = st.columns(2)
    col1.metric("Registros (filas)", multiplicidad["filas"])
    col2.metric(
        "Incidencias unicas", multiplicidad["incidencias_unicas"],
        help="Cantidad de ID_incidencia distintos. Una incidencia con varios proveedores ocupa varias filas.",
    )
    st.divider()

    st.subheader("¿Qué tipos de incidencias son más frecuentes?")
    tipo_conteo = resumen_por_tipo(df)
    fig_tipo = px.bar(
        tipo_conteo.sort_values("Cantidad"), x="Cantidad", y="Tipo incidente", orientation="h",
    )
    st.plotly_chart(fig_tipo, width="stretch")
    st.caption("Se cuenta sobre incidencias unicas por tipo (ID_incidencia + Tipo incidente), igual que en el Colab.")

    st.divider()

    st.subheader("¿En qué períodos se registran más incidencias?")
    mes_tipo = tabla_mes_tipo(df)
    mes_tipo_largo = mes_tipo.reset_index().melt(
        id_vars="mes", var_name="Tipo incidente", value_name="Cantidad"
    )
    fig_mes = px.bar(
        mes_tipo_largo, x="mes", y="Cantidad", color="Tipo incidente",
        category_orders={"mes": list(mes_tipo.index)},
    )
    fig_mes.update_layout(barmode="stack", xaxis_title="Mes (temporada octubre a mayo)")
    st.plotly_chart(fig_mes, width="stretch")
    st.caption("Las 4 incidencias sin fecha no aparecen en este grafico.")

    st.divider()

    st.subheader("¿Qué impacto tienen estas situaciones?")
    impacto = impacto_por_tipo(df)
    impacto_largo = impacto.reset_index().melt(
        id_vars="Tipo incidente", var_name="Impacto", value_name="Porcentaje"
    )
    fig_impacto = px.bar(
        impacto_largo, x="Porcentaje", y="Tipo incidente", color="Impacto", orientation="h",
        text_auto=".1f",
        color_discrete_map={"Bajo": "#2ec4b6", "Medio": "#ffbf00", "Alto": "#e71d36"},
        category_orders={"Impacto": ORDEN_IMPACTO, "Tipo incidente": list(impacto.index)},
    )
    fig_impacto.update_layout(barmode="stack", xaxis_range=[0, 100], xaxis_title="Porcentaje %")
    st.plotly_chart(fig_impacto, width="stretch")

    st.divider()

    st.subheader("¿Qué tan completos están los datos de proveedor y servicio?")
    col_prov, col_serv = st.columns(2)
    col_prov.metric(
        "Registros sin proveedor", f"{pct_sin_informacion(df, 'Proveedor'):.1f}%",
        help="Porcentaje de filas con 'Sin Informacion' en Proveedor.",
    )
    col_serv.metric(
        "Registros sin servicio", f"{pct_sin_informacion(df, 'Servicio'):.1f}%",
        help="Porcentaje de filas con 'Sin Informacion' en Servicio.",
    )
    st.caption(
        "'Sin Informacion' es el valor mas frecuente de ambas variables, lo que dificulta "
        "encontrar la causa raiz de buena parte de las incidencias. Por eso en el Dashboard "
        "se decidio no mostrar estos registros en los rankings de Top proveedores y Top "
        "servicios (no aportaban informacion util para identificar responsables); el detalle "
        "de cuantos registros faltan queda documentado aca."
    )

# ---------- Calidad de datos ----------
with tab_calidad:
    multiplicidad_cruda = resumen_multiplicidad(df_crudo)
    st.subheader("Multiplicidad de incidencias")
    col1, col2, col3 = st.columns(3)
    col1.metric("Filas", multiplicidad_cruda["filas"])
    col2.metric("Incidencias unicas", multiplicidad_cruda["incidencias_unicas"])
    col3.metric("IDs con varias filas", multiplicidad_cruda["ids_con_varias_filas"])
    st.caption(
        "Cuando una incidencia involucra a mas de un proveedor se registra en filas separadas "
        "que comparten el mismo ID_incidencia (no se concatenan valores en una misma celda)."
    )

    st.divider()

    st.subheader("Valores nulos (version2 sin procesar)")
    st.dataframe(resumen_nulos(df_crudo), hide_index=True, width="stretch")

    st.divider()

    st.subheader("Tratamiento aplicado")
    pax_ambiguo = int((df_crudo["PAX PIDIÓ CAMBIO/CXL?"] == "SI/NO").sum())
    st.markdown(
        f"- `PAX PIDIÓ CAMBIO/CXL?`: {pax_ambiguo} valores 'SI/NO' son ambiguos, se tratan como dato faltante.\n"
        f"- `Proveedor` y `Servicio`: los nulos se reemplazan por '{SIN_INFORMACION[0]}'.\n"
        f"- `Agencia` y `PAX PIDIÓ CAMBIO/CXL?`: los nulos se reemplazan por '{SIN_INFORMACION[1]}'.\n"
        "- `Marca de tiempo`: las filas sin fecha se mantienen sin imputar (limitacion documentada)."
    )
    st.caption(
        "Los registros de octubre 2025 se cargaron manualmente desde una planilla de la empresa "
        "e incorporados a la version2 con el mismo formato que el resto de la bitacora."
    )

# ---------- Proveedores y servicios ----------
with tab_cruces:
    st.markdown(
        "Para saber si las incidencias se reparten parejo o se concentran en actores y prestaciones "
        "especificas, se cruzan los **Top 5 proveedores** y **Top 5 servicios** (igual que en el Colab). "
        "Se cuentan filas y se incluye 'Sin Informacion', en gris."
    )
    COLORES_REGISTRO = {"Con dato": "#1f77b4", "Sin informacion": "#9e9e9e"}
    top_proveedores = top_n_conteo(df, "Proveedor", n=5, incluir_sin_info=True)["Proveedor"].tolist()
    top_servicios = top_n_conteo(df, "Servicio", n=5, incluir_sin_info=True)["Servicio"].tolist()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("¿Qué servicios da cada proveedor?")
        proveedor_sel = st.selectbox("Proveedor (Top 5)", top_proveedores)
        servicios_prov = cruce_conteo(df, "Proveedor", proveedor_sel, "Servicio")
        fig_sp = px.bar(
            servicios_prov.sort_values("Cantidad"), x="Cantidad", y="Servicio", orientation="h",
            color="Registro", color_discrete_map=COLORES_REGISTRO,
        )
        fig_sp.update_layout(showlegend=False, yaxis_title=None)
        st.plotly_chart(fig_sp, width="stretch")

    with col_b:
        st.subheader("¿Qué proveedores dan cada servicio?")
        servicio_sel = st.selectbox("Servicio (Top 5)", top_servicios)
        provs_serv = cruce_conteo(df, "Servicio", servicio_sel, "Proveedor")
        fig_ps = px.bar(
            provs_serv.sort_values("Cantidad"), x="Cantidad", y="Proveedor", orientation="h",
            color="Registro", color_discrete_map=COLORES_REGISTRO,
        )
        fig_ps.update_layout(showlegend=False, yaxis_title=None)
        st.plotly_chart(fig_ps, width="stretch")

    st.divider()
    st.subheader("Diagnostico del Colab")
    st.markdown(
        "**Proveedores criticos**\n"
        "- **P-010:** 37 de sus incidencias estan en el Trek Laguna de Los Tres SIB, donde es el "
        "proveedor de 37 de las 48 incidencias del servicio.\n"
        "- **P-001:** fallas en servicios de gama alta: Trek Laguna de Los Tres - Private guide "
        "(12 casos) y traslados privados a Rio Electrico (5 casos).\n"
        "- **P-011 y P-007:** P-011 concentra imprevistos en traslados punto a punto "
        "(aeropuertos y hoteles); P-007, en actividades lacustres (kayak y navegacion en Lago del Desierto).\n\n"
        "**Servicios criticos**\n"
        "- **Trek Laguna de Los Tres:** la version compartida (SIB) se asocia a P-010; la privada depende de P-001.\n"
        "- **Trek Laguna Torre SIB:** sin un unico proveedor responsable; las incidencias se reparten entre "
        "varios guias individuales (G-005, G-007, G-001, G-015).\n"
        "- **Box Lunch:** cuello de botella en P-009 (6 de las 8 incidencias)."
    )

# ---------- Reporte automatico ----------
with tab_reporte:
    st.caption(
        "Perfilado automatico de la version2 sin procesar. Se genera solo al apretar el boton "
        "y puede tardar un poco la primera vez."
    )
    if st.button("Generar reporte completo"):
        st.session_state["mostrar_reporte"] = True
    if st.session_state.get("mostrar_reporte"):
        try:
            from streamlit_ydata_profiling import st_profile_report

            with st.spinner("Generando reporte..."):
                reporte = generacion_reporte(df_crudo)
            st_profile_report(reporte)
        except ImportError as error:
            st.error(
                f"Falta instalar una libreria del reporte ({error.name}). "
                "Con el entorno activado: pip install -r APP/requirements.txt"
            )
        except Exception as error:
            st.error(f"No se pudo generar el reporte: {error}")