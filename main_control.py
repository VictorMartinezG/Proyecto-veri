# main_control.py
# Punto de entrada para la pantalla de control (empleado)

import tkinter as tk
from core.turnos import TurnoManager
from ui.control_ui import ControlUI


def main():
    manager = TurnoManager()
    root = tk.Tk()
    app = ControlUI(root, manager)
    root.mainloop()


if __name__ == "__main__":
    main()

