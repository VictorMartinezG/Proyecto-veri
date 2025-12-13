# run_sistema.py
# Lanza pantalla (TV) y control (operador) al mismo tiempo

import subprocess
import sys
import os

PYTHON = sys.executable

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

subprocess.Popen([PYTHON, os.path.join(BASE_DIR, "main_pantalla.py")])
subprocess.Popen([PYTHON, os.path.join(BASE_DIR, "main_control.py")])
