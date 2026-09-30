"""funciones de carga, comparacion y consulta sobre las bitacoras de incidencias.
se usan desde las paginas Streamlit (Comparacion.py, Preguntas.py).
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


def meses_disponibles(df: pd.DataFrame) -> list[str]:
    presentes = set(df["mes"].dropna()) - {""}
    return [m for m in ORDEN_MESES if m in presentes]


def _filtrar_por_mes(df: pd.DataFrame, mes: str | None) -> pd.DataFrame:
    if mes and mes != "Todos": #si se indica un mes, filtrar por el mismo
        return df[df["mes"] == mes]
    return df

#los meses se pasm como string en mayusculas
def mayor_incidencia_del_mes(df: pd.DataFrame, mes: str) -> dict | None:
    """incidente mas frecuente en el mes indicado"""
    filtrado = _filtrar_por_mes(df, mes)
    if filtrado.empty:
        return None
    conteo = filtrado["Tipo incidente"].value_counts()
    return {"tipo_incidente": conteo.index[0], "cantidad": int(conteo.iloc[0]), "mes": mes}


def resumen_por_tipo(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    filtrado = _filtrar_por_mes(df, mes)
    return (
        filtrado["Tipo incidente"].value_counts()
        .rename_axis("Tipo incidente").reset_index(name="Cantidad")
    )


def resumen_por_agencia(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    filtrado = _filtrar_por_mes(df, mes)
    return (
        filtrado["Agencia"].value_counts()
        .rename_axis("Agencia").reset_index(name="Cantidad")
    )


def incidencias_impacto_alto(df: pd.DataFrame, mes: str | None = None) -> pd.DataFrame:
    filtrado = _filtrar_por_mes(df, mes)
    columnas = ["ID_incidencia", "Tipo incidente", "Agencia", "Servicio", "Impacto", "mes"]
    return filtrado[filtrado["Impacto"] == "Alto"][columnas]

#recordar que las kpis se calculan sobre el df filtrado por mes, no sobre el df completo
def calcular_kpis(df: pd.DataFrame) -> dict:
    """KPIs generales para el encabezado del dashboard de preguntas."""
    if df.empty:
        return {"total": 0, "tipo_mas_frecuente": "-", "proveedor_top": "-", "pct_impacto_alto": 0.0}

    proveedores = df["Proveedor"].dropna() #se eliminan los nulos en los proveedores 
    return {
        "total": len(df),
        "tipo_mas_frecuente": df["Tipo incidente"].mode().iat[0],
        "proveedor_top": proveedores.mode().iat[0] if not proveedores.empty else "-",
        "pct_impacto_alto": (df["Impacto"] == "Alto").mean() * 100,
    }


def top_n_conteo(df: pd.DataFrame, columna: str, n: int = 10) -> pd.DataFrame:
    """Top N valores mas frecuentes de una columna (ignora nulos)."""
    return (
        df[columna].dropna().value_counts().head(n)
        .rename_axis(columna).reset_index(name="Cantidad")
    )


def evolucion_por_mes(df: pd.DataFrame, anio: int | None = None) -> pd.DataFrame:
    """Cantidad de incidencias por mes, en orden cronologico, filtrable por año."""
    filtrado = df if anio in (None, "Todos") else df[df["año"] == anio]
    conteo = filtrado["mes"].value_counts().reindex(ORDEN_MESES).dropna()
    return conteo.rename_axis("mes").reset_index(name="Cantidad")


def anios_disponibles(df: pd.DataFrame) -> list[int]:
    return sorted(int(a) for a in df["año"].dropna().unique())
