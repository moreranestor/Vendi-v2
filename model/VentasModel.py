from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla


class VentasModel(DBModelo):
    def __init__(self):
        super(VentasModel, self)
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "ventas"
        self.ID = "id_venta"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "id_venta, id_prod,id_mov, nombre, precio, cantidad, fecha_alta"

        self.columnas = {
            "id_venta": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL", 
            "id_prod": "INTEGER NOT NULL",
            "codigo": "Text(255) NOT NULL",
            "nombre": "Text(255)",
            "precio": "real(10, 2) NOT NULL DEFAULT 0",
            "cantidad": "real(10, 2) NOT NULL DEFAULT 0",
            "fecha_alta": "Text NOT NULL",
        }

        crear_tabla(self.conexion, self.nombretabla, self.columnas)

    def getVentasGlobalFecha(self, fecha):
        """Obtiene las ventas actuales de un producto por su producto"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
                     SELECT nombre,sum(cantidad) as cantidad , precio ,sum(cantidad) * precio as  importe, codigo
                     from ventas
                     where fecha_alta = ? GROUP by id_prod
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

    def getVentasporFecha(self, fecha):
        """Obtiene las ventas actuales de un producto por su producto"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
                     SELECT nombre,cantidad, precio , cantidad * precio as importe , codigo
                     from ventas
                     where fecha_alta = ? GROUP by id_venta
            """
            c = self.conexion.execute(query, (f'{fecha}',))

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
        """Obtiene las ventas actuales de un producto por su producto"""
        try:
            # Usar parámetros para evitar SQL injection
            query = f"""               
                DELETE FROM productos_entr_sali WHERE codigo = '{codigo}';                
                """
            self.conexion.execute(query)
            query = f"""                
                DELETE FROM ventas WHERE codigo = '{codigo}';                
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
