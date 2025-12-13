import json
import os

class TurnoManager:
    """
    Clase que maneja TODA la lógica del sistema de turnos.
    Guarda, carga, valida, corrige y reinicia los turnos.
    """

    def __init__(self, json_path="data/turnos.json"):
        self.json_path = json_path
        self.turnos = self._cargar_turnos()

    # -----------------------------
    # CARGAR / GUARDAR ARCHIVO JSON
    # -----------------------------
    def _cargar_turnos(self):
        """
        Carga los turnos desde el archivo JSON.
        Si no existe, lo crea vacío.
        """
        if not os.path.exists(self.json_path):
            return []

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("turnos", [])
        except:
            return []

    def _guardar_turnos(self):
        """
        Guarda la lista de turnos en el JSON.
        """
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump({"turnos": self.turnos}, f, indent=4)

    # -----------------------------
    # FUNCIONES PRINCIPALES
    # -----------------------------
    def agregar_turno(self, numero):
        """
        Agrega un turno nuevo (1–1000), sin repetir.
        Regresa True si se agregó, False si ya existe o es inválido.
        """

        if not isinstance(numero, int):
            return False

        if numero < 1 or numero > 1000:
            return False

        if numero in self.turnos:
            return False

        self.turnos.append(numero)
        self._guardar_turnos()
        return True

    def corregir_ultimo(self, nuevo_numero):
        """
        Permite corregir SOLO el último turno agregado.
        """
        if not self.turnos:
            return False

        if nuevo_numero in self.turnos[:-1]:
            return False

        self.turnos[-1] = nuevo_numero
        self._guardar_turnos()
        return True

    def reiniciar(self):
        """
        Borra todos los turnos del día.
        """
        self.turnos = []
        self._guardar_turnos()

    # -----------------------------
    # FUNCIONES PARA LA PANTALLA
    # -----------------------------
    def obtener_actual(self):
        """
        Devuelve el último turno, o None si no hay turnos.
        """
        if self.turnos:
            return self.turnos[-1]
        return None

    def obtener_anteriores(self, cantidad=5):
        """
        Devuelve los últimos N turnos anteriores al actual.
        """
        if len(self.turnos) <= 1:
            return []

        return self.turnos[-(cantidad+1):-1]
    
    def recargar(self):
        """
        Recarga los turnos desde el archivo JSON.
        """
        self.turnos = self._cargar_turnos()
  