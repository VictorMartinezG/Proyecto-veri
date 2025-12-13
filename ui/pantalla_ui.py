import tkinter as tk
from core.turnos import TurnoManager
from core.config import GREEN, PREVIO_COUNT, LOGO_FILE
import os

try:
    import winsound
    _HAS_WINSOUND = True
except:
    _HAS_WINSOUND = False


class PantallaUI:
    def __init__(self, root, manager: TurnoManager):
        self.root = root
        self.manager = manager
        self.last_turno = None

        self.root.title("Pantalla de Turnos - AIRE")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f2f2f2")

        top = tk.Frame(self.root, bg="#f2f2f2")
        top.pack(side="top", fill="x", pady=20)

        self.prev_labels = []
        for _ in range(PREVIO_COUNT):
            lbl = tk.Label(top, text="", font=("Segoe UI", 22),
                           bg="#f2f2f2", fg="#555")
            lbl.pack(side="left", expand=True, padx=10)
            self.prev_labels.append(lbl)

        center = tk.Frame(self.root, bg="#f2f2f2")
        center.pack(expand=True)

        self.logo = None
        if os.path.exists(LOGO_FILE):
            try:
                from PIL import Image, ImageTk
                img = Image.open(LOGO_FILE)
                img = img.resize((320, 140))
                self.logo = ImageTk.PhotoImage(img)
            except:
                pass

        if self.logo:
            tk.Label(center, image=self.logo, bg="#f2f2f2").pack(pady=(0, 10))
        else:
            tk.Label(center, text="AIRE", font=("Segoe UI", 32, "bold"),
                     bg="#f2f2f2", fg="#333").pack(pady=(0, 10))

        self.lbl_turno = tk.Label(center, text="Esperando turno...",
                                  font=("Segoe UI", 74, "bold"),
                                  bg="#f2f2f2", fg=GREEN)
        self.lbl_turno.pack(pady=20)

        self.update_loop()

    def play_beep(self):
        if _HAS_WINSOUND:
            winsound.Beep(1200, 180)

    def update_loop(self):
        self.manager.recargar()  # 🔥 Vuelve a leer el JSON
        turnos = self.manager.turnos

        if turnos:
            actual = self.manager.obtener_actual()
            previos = self.manager.obtener_anteriores(PREVIO_COUNT)

            while len(previos) < PREVIO_COUNT:
                previos.append("")

            if actual != self.last_turno:
                self.play_beep()
                self.last_turno = actual

            for i, v in enumerate(previos):
                self.prev_labels[i].configure(text=str(v) if v else " ")

            self.lbl_turno.configure(text=str(actual))

        else:
            for lbl in self.prev_labels:
                lbl.configure(text=" ")

            self.lbl_turno.configure(text="Esperando turno...")
            self.last_turno = None

        self.root.after(1000, self.update_loop)
