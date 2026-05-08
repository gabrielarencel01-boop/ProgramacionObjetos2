import pandas as pd
import os

class RegistroBackend:
    def __init__(self, filename="usuarios.csv"):
        self.filename = filename
        self.columnas = ["Nombre", "Carrera", "Edad"]
        self.df = self._cargar_o_crear_df()

    def _cargar_o_crear_df(self):
        """Carga el archivo existente o crea uno nuevo si no existe."""
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        return pd.DataFrame(columns=self.columnas)

    def registrar_usuario(self, nombre, carrera, edad):
        """Valida los datos y los añade al DataFrame."""
        if not nombre or not carrera or not edad:
            raise ValueError("Todos los campos son obligatorios.")
        
        try:
            edad_int = int(edad)
        except ValueError:
            raise ValueError("La edad debe ser un número entero.")

        nueva_fila = pd.DataFrame([[nombre, carrera, edad_int]], columns=self.columnas)
        self.df = pd.concat([self.df, nueva_fila], ignore_index=True)
        
        # Guardar automáticamente en CSV para persistencia
        self.df.to_csv(self.filename, index=False)
        return True

    def obtener_datos(self):
        return self.df
