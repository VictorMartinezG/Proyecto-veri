import tkinter as tk
from core.turnos import TurnoManager
from ui.pantalla_ui import PantallaUI

if __name__ == "__main__":
    root = tk.Tk()
    manager = TurnoManager()
    PantallaUI(root, manager)
    root.mainloop()
