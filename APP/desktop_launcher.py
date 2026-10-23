"""Levanta la app Streamlit como servidor local y la muestra en una ventana nativa

"""
import subprocess
import sys
import time
from pathlib import Path

import requests
import webview

PUERTO = 8501
URL = f"http://localhost:{PUERTO}"

# Flag interno: cuando el .exe empaquetado se relanza a si mismo con este
# argumento, en vez de abrir la ventana corre el servidor de Streamlit
FLAG_SERVIDOR = "--correr-streamlit"


def _ruta_app_py() -> Path:
    if getattr(sys, "frozen", False):
        # El .exe empaquetado tiene al lado las carpetas APP/ y DATOS/, con la
        # misma estructura que el repo (ver TourOps.spec), asi que etl_functions.py
        # no necesita saber si esta empaquetado o no
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        return base / "APP" / "App.py"
    return Path(__file__).parent / "App.py"


APP_PY = _ruta_app_py()


def _esperar_servidor(timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            if requests.get(URL, timeout=1).status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(0.5)
    return False


def _correr_servidor_streamlit():
    """Corre Streamlit en este mismo proceso"""
    import streamlit.web.cli as stcli

    sys.argv = [
        "streamlit", "run", str(APP_PY),
        "--server.headless=true", f"--server.port={PUERTO}",
        # Empaquetado, streamlit detecta un .git ancestro (el del propio repo,
        # porque dist/ queda adentro) y se cree "modo desarrollo", lo que bloquea
        # --server.port. Se fuerza a false para evitarlo.
        "--global.developmentMode=false",
    ]
    stcli.main()


def _lanzar_proceso_streamlit():
    """Arranca 'streamlit run App.py' en un subproceso, empaquetado o no."""
    if getattr(sys, "frozen", False):
        # El propio .exe actua de interprete: se relanza a si mismo con el
        # flag oculto para correr el servidor en vez de abrir la ventana de nuevo.
        comando = [sys.executable, FLAG_SERVIDOR]
    else:
        comando = [
            sys.executable, "-m", "streamlit", "run", str(APP_PY),
            "--server.headless", "true", "--server.port", str(PUERTO),
        ]
    return subprocess.Popen(comando)


def main():
    if FLAG_SERVIDOR in sys.argv:
        _correr_servidor_streamlit()
        return

    proceso = _lanzar_proceso_streamlit()
    try:
        if not _esperar_servidor():
            raise RuntimeError("El servidor de Streamlit no respondio a tiempo.")
        webview.create_window("TourOps: Análisis de incidencias turísticas", URL, width=1200, height=800)
        webview.start(gui="edgechromium")
    finally:
        proceso.terminate()
        proceso.wait(timeout=10)


if __name__ == "__main__":
    main()
