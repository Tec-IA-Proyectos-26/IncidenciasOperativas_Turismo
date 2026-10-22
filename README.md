# Reporte de Incidencias Operativas en Turismo

Proyecto ABP orientado al análisis de incidencias operativas en una agencia de turismo receptiva.

## Objetivo

Analizar los registros de incidencias operativas para identificar patrones, problemas recurrentes y oportunidades de mejora en los procesos de la agencia.

## Tecnologías

- Python
- Pandas
- Google Colab
- GitHub

## Integrantes

|     Nombre    |     Usuario   |
| ------------- |:-------------:|
| Ana Aguirre    | [AnaAguirre77](https://github.com/AnaAguirre77) |
| Belen Riquelme | [bely092](https://github.com/bely092) |
| Jorge Paredes  | [GeorgiWalls](https://github.com/GeorgiWalls)  |
| Leandro Cabral | [Leancbal](https://github.com/Leancbal)  |
| Nicolas Farias | [NICOLASFARIAS](https://github.com/NICOLASEFARIAS)|
| Wanda Esquivel | [Wanda126](https://github.com/Wanda126)|

Proyecto realizado por estudiantes del segundo año de la Tecnicatura en Ciencia de Datos e IA (Comisión B2).

## Estructura del proyecto

- `APP/`: aplicación Streamlit (páginas, carga de datos para la app y reporte EDA). Dependencias en `APP/requirements.txt`.
  - `App.py`: punto de entrada, define la navegación entre páginas.
  - `Principal.py`: página de bienvenida.
  - `Eda.py`: análisis exploratorio (perfilado automático) sobre `DATOS/bitacora_tempo25-26_version2.csv`.
  - `ETL.py`: reporte estático del procesamiento de datos.
  - `Comparacion.py`: compara version1 vs version2 (filas, columnas, nulos).
  - `Preguntas.py`: dashboard de incidencias con filtros (fecha, tipo, impacto, proveedor, servicio) y gráficos.
  - `Dashboard.py`: visualización de incidencias por agencia.
  - `etl_functions.py`: funciones de carga y consulta reutilizadas por las páginas.
  - `desktop_launcher.py`: levanta la app como ventana de escritorio nativa (ver abajo).
- `DATOS/`: bitácoras CSV fuente, utilizadas tanto por la app como por el análisis en Google Colab.

## Cómo levantar el proyecto

1. Crear y activar un entorno virtual (una sola vez):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instalar las dependencias:

   ```powershell
   pip install -r APP/requirements.txt
   ```

3. Elegir cómo correrla:

   - **Como app web** (se abre en el navegador en `http://localhost:8501`):

     ```powershell
     streamlit run APP/App.py
     ```

   - **Como app de escritorio** (se abre en una ventana nativa, sin navegador):

     ```powershell
     python APP/desktop_launcher.py
     ```

   Ambas opciones muestran las mismas páginas: Bienvenidos, EDA, ETL, Comparación v1 vs v2, Preguntas y Dashboard.
