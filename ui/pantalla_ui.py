from PIL import Image, ImageTk
import tkinter as tk
from core.turnos import TurnoManager
from core.config import PREVIO_COUNT
import os

try:
    import winsound
    _HAS_WINSOUND = True
except:
    _HAS_WINSOUND = False


GREEN_AIRE = "#9ACD32"
WHITE = "#676767"
TEXT_GRAY = "#FFFFFF"
BORDER_COLOR = GREEN_AIRE
TITLE_BG = GREEN_AIRE
TITLE_TEXT = "#FFFFFF"


class PantallaUI:
    def __init__(self, root, manager: TurnoManager):
        self.root = root
        self.manager = manager
        self.last_turno = None

        self.root.title("Pantalla de Turnos - AIRE")
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # ================= RESOLUCIÓN REAL =================
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        # ================= CANVAS BASE =================
        self.canvas = tk.Canvas(
            root,
            width=self.screen_width,
            height=self.screen_height,
            bg=GREEN_AIRE,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # ================= BARRA SUPERIOR =================
        self.header_height = int(self.screen_height * 0.15)

        self.canvas.create_rectangle(
            0, 0,
            self.screen_width, self.header_height,
            fill=WHITE,
            outline=""
        )

        self.canvas.create_rectangle(
            0,
            self.header_height,
            self.screen_width,
            self.header_height + 4,
            fill=GREEN_AIRE,
            outline=""
        )

        # ================= LOGO HEADER =================
        header_path = "assets/verificacion_responsable.png"
        if os.path.exists(header_path):
            img = Image.open(header_path).resize((700, 70), Image.LANCZOS)
            self.logo_header = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                self.screen_width // 2,
                self.header_height // 2,
                image=self.logo_header
            )

        # ================= TARJETA CENTRAL =================
        card_width = int(self.screen_width * 0.9)
        card_height = int(self.screen_height * 0.65)

        x1 = (self.screen_width - card_width) // 2
        y1 = (self.screen_height - card_height) // 2
        x2 = x1 + card_width
        y2 = y1 + card_height

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=WHITE, outline="")

        # ===== MARCO FOLIOS ANTERIORES =====
        prev_box_x1 = x1 + int(card_width * 0.05)
        prev_box_x2 = x2 - int(card_width * 0.05)
        prev_box_y1 = y1 + int(card_height * 0.08)
        prev_box_y2 = y1 + int(card_height * 0.35)

        self.canvas.create_rectangle(
            prev_box_x1, prev_box_y1,
            prev_box_x2, prev_box_y2,
            outline=BORDER_COLOR,
            width=4
        )

        self.canvas.create_rectangle(
            prev_box_x1,
            prev_box_y1 - 30,
            prev_box_x1 + 260,
            prev_box_y1,
            fill=TITLE_BG,
            outline=""
        )

        self.canvas.create_text(
            prev_box_x1 + 130,
            prev_box_y1 - 15,
            text="FOLIOS ANTERIORES",
            fill=TITLE_TEXT,
            font=("Segoe UI", 16, "bold")
        )

        # ================= TURNOS PREVIOS =================
        top_frame = tk.Frame(self.canvas, bg=WHITE)
        self.prev_labels = []

        for _ in range(PREVIO_COUNT):
            lbl = tk.Label(
                top_frame,
                text="",
                font=("Segoe UI", int(self.screen_height * 0.09)),
                bg=WHITE,
                fg=TEXT_GRAY
            )
            lbl.pack(side="left", expand=True, padx=50)
            self.prev_labels.append(lbl)

        self.canvas.create_window(
            self.screen_width // 2,
            y1 + int(card_height * 0.21),
            window=top_frame
        )

        # ===== MARCO FOLIO ACTUAL =====
        actual_box_x1 = x1 + int(card_width * 0.05)
        actual_box_x2 = x2 - int(card_width * 0.05)
        actual_box_y1 = y1 + int(card_height * 0.45)
        actual_box_y2 = y2 - int(card_height * 0.08)

        self.canvas.create_rectangle(
            actual_box_x1, actual_box_y1,
            actual_box_x2, actual_box_y2,
            outline=BORDER_COLOR,
            width=4
        )

        self.canvas.create_rectangle(
            actual_box_x1,
            actual_box_y1 - 35,
            actual_box_x1 + 220,
            actual_box_y1,
            fill=TITLE_BG,
            outline=""
        )

        self.canvas.create_text(
            actual_box_x1 + 110,
            actual_box_y1 - 18,
            text="FOLIO ACTUAL",
            fill=TITLE_TEXT,
            font=("Segoe UI", 18, "bold")
        )

        # ================= TURNO ACTUAL =================
        center = tk.Frame(self.canvas, bg=WHITE)

        self.lbl_turno = tk.Label(
            center,
            text="Esperando turno...",
            font=("Segoe UI", int(self.screen_height * 0.12), "bold"),
            bg=WHITE,
            fg="white"
        )
        self.lbl_turno.pack(pady=20)

        self.canvas.create_window(
            self.screen_width // 2,
            y1 + int(card_height * 0.68),
            window=center
        )

        # ================= LOGOS PIE =================
        if os.path.exists("assets/logo_aire.png"):
            img = Image.open("assets/logo_aire.png").resize((140, 70))
            self.logo_left = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                30,
                self.screen_height - 30,
                anchor="sw",
                image=self.logo_left
            )

        if os.path.exists("assets/logo_jalisco.png"):
            img = Image.open("assets/logo_jalisco.png").resize((140, 70))
            self.logo_right = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                self.screen_width - 30,
                self.screen_height - 30,
                anchor="se",
                image=self.logo_right
            )

        # ================= MENSAJE PIE DE PÁGINA =================
        self.lbl_mensaje = tk.Label(
            self.canvas,
            text="Favor de pasar al área de entrega de resultados",
            font=("Segoe UI", int(self.screen_height * 0.045), "bold"),
            bg=GREEN_AIRE,
            fg="white"
        )

        self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height - 110,
            window=self.lbl_mensaje
        )

        self.update_loop()

    def play_beep(self):
        if _HAS_WINSOUND:
            try:
                ruta = os.path.join("assets", "sounds", "cambio_turno.wav")
                winsound.PlaySound(
                    ruta,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except:
                pass

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
