from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla


class NotasModel(DBModelo):
    def __init__(self):
        super(NotasModel, self)
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "notas"
        self.ID = "id_notas"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "id_notas, detalles, deuda, fecha_alta pagada"

        self.columnas = {
            "id_notas": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "detalles": "Text(255)",
            "deuda": "real(10, 2) NOT NULL DEFAULT 0",
            "cantidad": "real(10, 2) NOT NULL DEFAULT 0",
            "fecha_alta": "Text NOT NULL",
            "pagada": "INTEGER",
        }

        crear_tabla(self.conexion, self.nombretabla, self.columnas)

    def getNotasGlobalFecha(self, fecha):
        """Obtiene las notas actuales de un producto por su producto"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
                     SELECT *
                     from notas
                     where fecha_alta = ? GROUP by id_notas
            """
            c = self.conexion.execute(query, (fecha,))

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error al obtener existencias: {str(e)}")
            return []

    def getnotasporFecha(self, fecha):
        """Obtiene las notas actuales de un producto por su producto"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
                     SELECT *
                     from notas
                     where fecha_alta = ? GROUP by id_notas
            """
            c = self.conexion.execute(query, (f"{fecha}",))

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error al obtener existencias: {str(e)}")
            return []

    def cancelar(self, codigo):
        """Obtiene las notas actuales de un producto por su producto"""
        try:          
            query = f"""                
                DELETE FROM notas WHERE codigo = '{codigo}';                
                """
            self.conexion.execute(query)
            self.conexion.commit()
            print(f"Registros con código {codigo} eliminados correctamente")

        except sqlite3.Error as e:
            self.conexion.rollback()
            print(f"Error al eliminar: {e}")
            return 0
        finally:
            return True
        
    