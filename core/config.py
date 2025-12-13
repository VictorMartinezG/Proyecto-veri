from pathlib import Path
import os

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]

# Directorios importantes
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Asegurar que existan
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Archivo JSON de turnos
TURNOS_FILE = DATA_DIR / "turnos.json"

# Color verde institucional
GREEN = "#8CC63F"

# Cantidad de turnos previos a mostrar
PREVIO_COUNT = 5

# Rango válido de folios
MIN_FOLIO = 1
MAX_FOLIO = 1000

# Recursos
LOGO_FILE = ASSETS_DIR / "logo_aire.png"
BEEP_FILE = ASSETS_DIR / "beep.wav"
