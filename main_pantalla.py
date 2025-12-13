# main_pantalla.py
# Punto de entrada para la pantalla de la TV (display)

import tkinter as tk
from core.turnos import TurnoManager
from ui.pantalla_ui import PantallaUI

def main():
    manager = TurnoManager()
    root = tk.Tk()
    app = PantallaUI(root, manager)
    root.mainloop()

if __name__ == '__main__':
    main()
