"""Levanta la app Streamlit como servidor local y la muestra en una ventana nativa.

Uso: python desktop_launcher.py
"""
import subprocess
import sys
import time
from pathlib import Path

import webview
import requests

PUERTO = 8501
URL = f"http://localhost:{PUERTO}"
APP_PY = Path(__file__).parent / "App.py"


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


def main():
    proceso = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", str(APP_PY),
            "--server.headless", "true", "--server.port", str(PUERTO),
        ],
    )
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
