# -*- mode: python ; coding: utf-8 -*-
"""Receta de PyInstaller para empaquetar la app de escritorio.

Uso: pyinstaller TourOps.spec   (ejecutar desde la raiz del repo)
Resultado: dist/TourOps/TourOps.exe
"""
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

RAIZ = Path.cwd()

datas = [
    # Se bundlea toda la carpeta APP/ (paginas .py + archivos/) y DATOS/ tal cual
    # estan en el repo, para que las rutas que arma etl_functions.py (basadas en
    # __file__) sigan funcionando igual, empaquetado o no.
    (str(RAIZ / "APP"), "APP"),
    (str(RAIZ / "DATOS"), "DATOS"),
]
binaries = []
hiddenimports = []

# Las paginas de Streamlit (App.py, Dashboard.py, Eda.py, etc.) se ejecutan como
# subproceso, no con "import": PyInstaller no las analiza y por lo tanto no detecta
# solo que necesitan estas librerias. Hay que declararlas a mano.
PAQUETES_PESADOS = [
    "streamlit",
    "pandas",
    "plotly",
    "ydata_profiling",
    "streamlit_ydata_profiling",
]
for paquete in PAQUETES_PESADOS:
    d, b, h = collect_all(paquete)
    datas += d
    binaries += b
    hiddenimports += h

# Backend de la ventana nativa (WebView2 via pythonnet/clr)
hiddenimports += ["clr_loader", "pythonnet", "clr"]

# matplotlib elige el backend dinamicamente; el hook de PyInstaller solo detecta
# los backends usados explicitamente en el codigo (via matplotlib.use(...)), y
# ydata_profiling necesita el de SVG para algunos graficos del reporte sin que
# nadie lo pida por nombre en nuestro codigo.
hiddenimports += [
    "matplotlib.backends.backend_svg",
    "matplotlib.backends.backend_agg",
    "matplotlib.backends.backend_pdf",
]

block_cipher = None

a = Analysis(
    [str(RAIZ / "APP" / "desktop_launcher.py")],
    pathex=[str(RAIZ / "APP")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TourOps",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(RAIZ / "APP" / "archivos" / "icono.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="TourOps",
)
