"""funciones de carga, comparacion y consulta sobre las bitacoras de incidencias.
se usan desde las paginas Streamlit (Comparacion.py, Preguntas.py, Eda.py, Dashboard.py).

Criterio de conteo (el mismo que el Colab de la evidencia 2):
- incidencias: se cuentan por ID_incidencia unico. Una incidencia con mas de un proveedor
  ocupa varias filas que comparten el mismo ID.
- tipo de incidente: se cuenta sobre (ID_incidencia, Tipo incidente) sin duplicados, porque
  hay incidencias que combinan mas de un tipo.
- proveedores y servicios: se cuentan por fila (cada fila es un proveedor o servicio
  involucrado) y los rankings excluyen los registros "Sin Informacion".
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_VERSION1 = RAIZ / "DATOS" / "bitacora_tempo25-26_version1.csv"
RUTA_VERSION2 = RAIZ / "DATOS" / "bitacora_tempo25-26_version2.csv"
RUTA_DF_CLEAN = RAIZ / "APP" / "archivos" / "df_clean.csv"

ORDEN_MESES = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
]
# la temporada va de octubre a mayo, asi que los meses se ordenan desde octubre
ORDEN_TEMPORADA = ORDEN_MESES[9:] + ORDEN_MESES[:9]

ORDEN_TIPOS = ["Cancelación", "Modificación", "Informativo", "Queja"]
ORDEN_IMPACTO = ["Bajo", "Medio", "Alto"]

# valores con los que el tratamiento de datos (Colab) reemplazo los nulos
SIN_INFORMACION = ("Sin Informacion", "No Informado")

# La columna "mes" del CSV viene en ingles (pandas .dt.month_name() por defecto).
MESES_EN_A_ES = {
    "January": "ENERO", "February": "FEBRERO", "March": "MARZO", "April": "ABRIL",
    "May": "MAYO", "June": "JUNIO", "July": "JULIO", "August": "AGOSTO",
    "September": "SEPTIEMBRE", "October": "OCTUBRE", "November": "NOVIEMBRE",
    "December": "DICIEMBRE",
}


def cargar_version1() -> pd.DataFrame:
    return pd.read_csv(RUTA_VERSION1)


def cargar_version2() -> pd.DataFrame:
    return pd.read_csv(RUTA_VERSION2)


def cargar_datos_limpios() -> pd.DataFrame:
    """Dataset ya procesado (basado en version2) que usan las consultas."""
    df = pd.read_csv(RUTA_DF_CLEAN)
    df["mes"] = df["mes"].map(MESES_EN_A_ES).fillna(df["mes"])
    df["Marca de tiempo"] = pd.to_datetime(df["Marca de tiempo"])
    return df


def comparar_versiones(df_v1: pd.DataFrame, df_v2: pd.DataFrame) -> dict:
    """resumen de las diferencias entre version1 y version2, sin cruzar filas."""
    cols_v1, cols_v2 = set(df_v1.columns), set(df_v2.columns)
    columnas_comunes = sorted(cols_v1 & cols_v2)

    nulos_comparados = pd.DataFrame({
        "Version1": df_v1[columnas_comunes].isna().sum(),
        "Version2": df_v2[columnas_comunes].isna().sum(),
    })
    nulos_comparados["Diferencia"] = nulos_comparados["Version2"] - nulos_comparados["Version1"]

    return {
        "filas_v1": len(df_v1),
        "filas_v2": len(df_v2),
        "columnas_solo_v1": sorted(cols_v1 - cols_v2),
        "columnas_solo_v2": sorted(cols_v2 - cols_v1),
        "columnas_comunes": columnas_comunes,
        "nulos_por_columna": nulos_comparados,
    }


# ---------- criterio de conteo (igual que el Colab) ----------

def incidencias_unicas(df: pd.DataFrame) -> pd.DataFrame:
    """una fila por incidencia (ID_incidencia).
    Sirve para contar incidencias y para variables que no cambian dentro de una misma
    incidencia: impacto, agencia, mes y año."""
    return df.drop_duplicates(subset="ID_incidencia")


def incidencias_por_tipo(df: pd.DataFrame) -> pd.DataFrame:
    """una fila por (ID_incidencia, Tipo incidente).
    Evita inflar el conteo cuando una incidencia con varios proveedores repite el mismo
    tipo, pero conserva las incidencias que combinan mas de un tipo."""
    return df.drop_duplicates(subset=["ID_incidencia", "Tipo incidente"])


def excluir_sin_informacion(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """quita las filas donde la columna es nula o vale 'Sin Informacion' / 'No Informado'."""
    return df[df[columna].notna() & ~df[columna].isin(SIN_INFORMACION)]


def pct_sin_informacion(df: pd.DataFrame, columna: str) -> float:
    """porcentaje de registros (filas) sin dato en la columna."""
    if df.empty:
        return 0.0
    return float((df[columna].isna() | df[columna].isin(SIN_INFORMACION)).mean() * 100)


# ---------- consultas ----------

def meses_disponibles(df: pd.DataFrame) -> list[str]:
    presentes = set(df["mes"].dropna()) - {""}
    return [m for m in ORDEN_TEMPORADA if m in presentes]


def _filtrar_por_mes(df: pd.DataFrame, mes: str | None) -> pd.DataFrame:
    if mes and mes != "Todos": #si se indica un mes, filtrar por el mismo
        return df[df["mes"] == mes]
    return df

#los meses se pasm como string en mayusculas
def mayor_incidencia_del_mes(df: pd.DataFrame, mes: str) -> dict | None:
    """incidente mas frecuente en el mes indicado"""
    filtrado = incidencias_por_tipo(_filtrar_por_mes(df, mes))
    if filtrado.empty:
        return None
    conteo = filtrado["Tipo incidente"].value_counts()
    return {"tipo_incidente": conteo.index[0], "cantidad": int(conteo.iloc[0]), "mes": mes}


def resumen_por_tipo(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    filtrado = incidencias_por_tipo(_filtrar_por_mes(df, mes))
    return (
        filtrado["Tipo incidente"].value_counts()
        .rename_axis("Tipo incidente").reset_index(name="Cantidad")
    )


def resumen_por_agencia(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    filtrado = incidencias_unicas(_filtrar_por_mes(df, mes))
    return (
        filtrado["Agencia"].value_counts()
        .rename_axis("Agencia").reset_index(name="Cantidad")
    )


def incidencias_impacto_alto(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    """listado de filas con impacto alto (una por proveedor/servicio involucrado)."""
    filtrado = _filtrar_por_mes(df, mes)
    columnas = ["ID_incidencia", "Tipo incidente", "Agencia", "Servicio", "Impacto", "mes"]
    return filtrado[filtrado["Impacto"] == "Alto"][columnas]

#recordar que las kpis se calculan sobre el df filtrado por mes, no sobre el df completo
def calcular_kpis(df: pd.DataFrame) -> dict:
    """KPIs generales para el encabezado del dashboard de preguntas."""
    if df.empty:
        return {
            "total": 0, "tipo_mas_frecuente": "-", "proveedor_top": "-",
            "pct_impacto_alto": 0.0, "pct_sin_proveedor": 0.0, "pct_sin_servicio": 0.0,
        }

    unicas = incidencias_unicas(df)
    tipos = incidencias_por_tipo(df)["Tipo incidente"]
    proveedores = excluir_sin_informacion(df, "Proveedor")["Proveedor"] #sin nulos ni "Sin Informacion"
    return {
        "total": len(unicas),
        "tipo_mas_frecuente": tipos.mode().iat[0],
        "proveedor_top": proveedores.mode().iat[0] if not proveedores.empty else "-",
        "pct_impacto_alto": (unicas["Impacto"] == "Alto").mean() * 100,
        "pct_sin_proveedor": pct_sin_informacion(df, "Proveedor"),
        "pct_sin_servicio": pct_sin_informacion(df, "Servicio"),
    }


def top_n_conteo(df: pd.DataFrame, columna: str, n: int = 10, incluir_sin_info: bool = False) -> pd.DataFrame:
    """Top N valores mas frecuentes de una columna (ignora nulos).

    Por defecto tambien excluye 'Sin Informacion'. Con incluir_sin_info=True lo deja en el
    ranking (como el Top 5 del Colab) y agrega la columna 'Registro' para poder distinguirlo
    en el grafico: 'Sin informacion' o 'Con dato'.
    """
    base = df[df[columna].notna()] if incluir_sin_info else excluir_sin_informacion(df, columna)
    conteo = (
        base[columna].value_counts().head(n)
        .rename_axis(columna).reset_index(name="Cantidad")
    )
    if incluir_sin_info:
        conteo["Registro"] = conteo[columna].isin(SIN_INFORMACION).map(
            {True: "Sin informacion", False: "Con dato"}
        )
    return conteo


def cruce_conteo(df: pd.DataFrame, filtro_col: str, filtro_valor: str, contar_col: str, n: int = 5) -> pd.DataFrame:
    """Top N de contar_col dentro de las filas donde filtro_col == filtro_valor.
    Ej.: servicios de un proveedor (filtro_col='Proveedor', contar_col='Servicio') o
    proveedores de un servicio. Igual que los cruces del Colab: cuenta filas e incluye
    'Sin Informacion' (marcado en la columna 'Registro')."""
    conteo = (
        df[df[filtro_col] == filtro_valor][contar_col].value_counts().head(n)
        .rename_axis(contar_col).reset_index(name="Cantidad")
    )
    conteo["Registro"] = conteo[contar_col].isin(SIN_INFORMACION).map(
        {True: "Sin informacion", False: "Con dato"}
    )
    return conteo


def evolucion_por_mes(df: pd.DataFrame, anio: int | None = None) -> pd.DataFrame:
    """Cantidad de incidencias unicas por mes, en orden de temporada (oct a may), filtrable por año."""
    base = incidencias_unicas(df)
    filtrado = base if anio in (None, "Todos") else base[base["año"] == anio]
    conteo = filtrado["mes"].value_counts().reindex(ORDEN_TEMPORADA).dropna().astype(int)
    return conteo.rename_axis("mes").reset_index(name="Cantidad")


def anios_disponibles(df: pd.DataFrame) -> list[int]:
    return sorted(int(a) for a in df["año"].dropna().unique())


# ---------- tablas para el EDA ----------

def tabla_mes_tipo(df: pd.DataFrame) -> pd.DataFrame:
    """incidencias por mes (filas, orden de temporada) y tipo (columnas)."""
    base = incidencias_por_tipo(df)
    tabla = pd.crosstab(base["mes"], base["Tipo incidente"])
    return tabla.reindex(ORDEN_TEMPORADA).dropna(how="all").astype(int)


def impacto_por_tipo(df: pd.DataFrame) -> pd.DataFrame:
    """porcentaje de cada impacto dentro de cada tipo de incidente (cada fila suma 100)."""
    base = incidencias_por_tipo(df)
    porcentaje = pd.crosstab(base["Tipo incidente"], base["Impacto"], normalize="index") * 100
    return porcentaje.reindex(
        index=[t for t in ORDEN_TIPOS if t in porcentaje.index],
        columns=[i for i in ORDEN_IMPACTO if i in porcentaje.columns],
    )


def resumen_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """nulos por columna, con su porcentaje sobre el total de filas."""
    nulos = df.isna().sum()
    return (
        pd.DataFrame({
            "Columna": nulos.index,
            "Nulos": nulos.values,
            "% del total": (nulos.values / len(df) * 100).round(1),
        })
        .sort_values("Nulos", ascending=False)
        .reset_index(drop=True)
    )


def resumen_multiplicidad(df: pd.DataFrame) -> dict:
    """cuantas filas hay, cuantas incidencias unicas y cuantas ocupan mas de una fila."""
    filas_por_id = df["ID_incidencia"].value_counts()
    return {
        "filas": len(df),
        "incidencias_unicas": int(df["ID_incidencia"].nunique()),
        "ids_con_varias_filas": int((filas_por_id > 1).sum()),
    }