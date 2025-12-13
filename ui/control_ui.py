import tkinter as tk
from tkinter import messagebox
from core.turnos import TurnoManager
from core.config import GREEN

class ControlUI:
    def __init__(self, root, manager: TurnoManager):
        self.root = root
        self.manager = manager

        self.root.title("Control de Turnos - AIRE")
        self.root.geometry("420x300")
        self.root.configure(bg="#f2f2f2")

        # TÍTULO
        tk.Label(
            root,
            text="Control de Turnos",
            font=("Segoe UI", 18, "bold"),
            bg="#f2f2f2",
            fg="#333"
        ).pack(pady=(20, 10))

        # ENTRADA DE FOLIO
        self.entry = tk.Entry(
            root,
            font=("Segoe UI", 22),
            justify="center"
        )
        self.entry.pack(pady=10)
        self.entry.focus()

        self.entry.bind("<Return>", self.agregar_turno)

        # BOTONES
        btn_frame = tk.Frame(root, bg="#f2f2f2")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Corregir último",
            font=("Segoe UI", 11),
            command=self.corregir_turno,
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Reiniciar día",
            font=("Segoe UI", 11),
            command=self.reiniciar_dia,
            width=15
        ).grid(row=0, column=1, padx=5)

        # MENSAJE DE ESTADO
        self.lbl_status = tk.Label(
            root,
            text="",
            font=("Segoe UI", 11),
            bg="#f2f2f2"
        )
        self.lbl_status.pack(pady=10)

    # -----------------------------
    # FUNCIONES
    # -----------------------------
    def leer_folio(self):
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def agregar_turno(self, event=None):
        folio = self.leer_folio()

        if folio is None:
            self.mostrar_error("Ingresa un número válido")
            return

        if self.manager.agregar_turno(folio):
            self.mostrar_ok(f"Turno {folio} agregado")
            self.entry.delete(0, tk.END)
        else:
            self.mostrar_error("Turno inválido o repetido")

    def corregir_turno(self):
        valor = self.entry.get().strip()

        if not valor.isdigit():
            messagebox.showerror("Error", "Ingresa un número válido")
            return

        numero = int(valor)

        ok = self.manager.corregir_ultimo(numero)

        if not ok:
            messagebox.showerror(
                "Error",
                "No se puede corregir:\n"
                "- El número ya existe\n"
                "- No hay turnos previos"
            )
            return

        self.entry.delete(0, tk.END)
        self.mostrar_ok(f"Último turno corregido a {numero}")

    def reiniciar_dia(self):
        resp = messagebox.askyesno(
            "Confirmar reinicio",
            "¿Seguro que desea reiniciar los turnos del día?"
        )

        if resp:
            self.manager.reiniciar()
            self.mostrar_ok("Turnos reiniciados")

    # -----------------------------
    # MENSAJES
    # -----------------------------
    def mostrar_ok(self, msg):
        self.lbl_status.configure(text=msg, fg=GREEN)

    def mostrar_error(self, msg):
        self.lbl_status.configure(text=msg, fg="red")


