import tkinter as tk
from core.turnos import TurnoManager
from ui.control_ui import ControlUI

if __name__ == "__main__":
    root = tk.Tk()
    manager = TurnoManager()
    ControlUI(root, manager)
    root.mainloop()
