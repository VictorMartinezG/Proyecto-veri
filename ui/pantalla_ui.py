import tkinter as tk
from core.turnos import TurnoManager
from core.config import PREVIO_COUNT
import os

try:
    import winsound
    _HAS_WINSOUND = True
except:
    _HAS_WINSOUND = False

from PIL import Image, ImageTk

GREEN_AIRE = "#9ACD32"
GREEN_DARK = "#FFFFFF"
GRAY_BG = "#70E800"
WHITE = "#676767"
TEXT_GRAY = "#FFFFFF"


class PantallaUI:
    def __init__(self, root, manager: TurnoManager):
        self.root = root
        self.manager = manager
        self.last_turno = None

        self.root.title("Pantalla de Turnos - AIRE")
        self.root.geometry("1280x720")
        self.root.configure(bg=GRAY_BG)

        # ================= CANVAS BASE =================
        self.canvas = tk.Canvas(root, bg=GRAY_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Barra superior
        self.canvas.create_rectangle(0, 0, 1280, 110, fill=WHITE, outline="")
        self.canvas.create_rectangle(0, 110, 1280, 114, fill=GREEN_AIRE, outline="")

        # Tarjeta central
        self.canvas.create_rectangle(120, 150, 1160, 560, fill=WHITE, outline="")

        # ================= TURNOS PREVIOS =================
        top_frame = tk.Frame(self.canvas, bg=WHITE)
        self.prev_labels = []

        for _ in range(PREVIO_COUNT):
            lbl = tk.Label(
                top_frame,
                text="",
                font=("Segoe UI", 22),
                bg=WHITE,
                fg=TEXT_GRAY
            )
            lbl.pack(side="left", expand=True, padx=15)
            self.prev_labels.append(lbl)

        self.canvas.create_window(640, 220, window=top_frame)

        # ================= TURNO ACTUAL =================
        center = tk.Frame(self.canvas, bg=WHITE)

        self.lbl_turno = tk.Label(
            center,
            text="Esperando turno...",
            font=("Segoe UI", 74, "bold"),
            bg=WHITE,
            fg=GREEN_DARK
        )
        self.lbl_turno.pack(pady=30)

        self.canvas.create_window(640, 380, window=center)

        # ================= LOGOS PIE =================
        self.logo_left = None
        self.logo_right = None

        if os.path.exists("assets/logo_aire.png"):
            img = Image.open("assets/logo_aire.png").resize((140, 70))
            self.logo_left = ImageTk.PhotoImage(img)
            self.canvas.create_image(40, 690, anchor="sw", image=self.logo_left)

        if os.path.exists("assets/logo_jalisco.png"):
            img = Image.open("assets/logo_jalisco.png").resize((140, 70))
            self.logo_right = ImageTk.PhotoImage(img)
            self.canvas.create_image(1240, 690, anchor="se", image=self.logo_right)

        self.update_loop()

    def play_beep(self):
        if _HAS_WINSOUND:
            winsound.Beep(1200, 180)

    def update_loop(self):
        self.manager.recargar()
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
