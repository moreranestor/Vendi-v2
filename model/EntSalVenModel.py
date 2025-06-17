from datetime import datetime
from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla
from .ProductoModel import ProductoModel


class EntSalVenModel(DBModelo):
    def __init__(self):
        super(EntSalVenModel, self)
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "productos_entr_sali"
        self.ID = "id_mov"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "id_mov, id_prod, codigo, estado, entradas, salidas, ventas, detalles, fecha_alta, activo"

        self.columnas = {
            "id_mov": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "id_prod": "INTEGER NOT NULL",
            "codigo": "Text(255) NOT NULL",
            "estado": "real(10, 2) NOT NULL DEFAULT 0",
            "entradas": "real(10, 2) NOT NULL DEFAULT 0",
            "salidas": "real(10, 2) NOT NULL DEFAULT 0",
            "ventas": "real(10, 2) NOT NULL DEFAULT 0",
            "detalles": "Text(255)",
            "fecha_alta": "Text NOT NULL",
            "activo": "INTEGER DEFAULT 1",
        }
        crear_tabla(self.conexion, self.nombretabla, self.columnas)

    def getVentasIpvFecha(self, f1=None, f2=None):
        try:
            # Manejo de fechas
            if not f1 and not f2:
                # Si no se proporcionan fechas, usar el día actual
                ff1 = ff2 = datetime.now().strftime("%d-%m-%Y")
            else:
                ff1 = f1 if f1 else f2
                ff2 = f2 if f2 else f1

            sql = """
                SELECT 
                        p.id_prod as id,
                        p.codigo,
                        p.nombre,
                        p.moneda,
                        p.precio as precio_venta,
                        p.compra as precio_compra,
                        
                        COALESCE((
                            SELECT SUM(entradas - salidas - ventas) 
                            FROM productos_entr_sali 
                            WHERE id_prod = p.id_prod AND fecha_alta < ?
                        ), 0) as stock_inicial,
                        
                        COALESCE((
                            SELECT SUM(entradas) 
                            FROM productos_entr_sali 
                            WHERE id_prod = p.id_prod 
                            AND fecha_alta BETWEEN ? AND ?
                        ), 0) as entradas,
                        
                        COALESCE((
                            SELECT SUM(salidas) 
                            FROM productos_entr_sali 
                            WHERE id_prod = p.id_prod 
                            AND fecha_alta BETWEEN ? AND ?
                        ), 0) as salidas,	
                        
                        COALESCE((
                            SELECT SUM(ventas) 
                            FROM productos_entr_sali 
                            WHERE id_prod = p.id_prod 
                            AND fecha_alta BETWEEN ? AND ?
                        ), 0) as ventas,
                        
                        COALESCE((
                            SELECT SUM(entradas - salidas - ventas) 
                            FROM productos_entr_sali 
                            WHERE id_prod = p.id_prod 
                            AND fecha_alta <= ?
                        ), 0) as stock_actual
                        
                    FROM producto p
                    WHERE p.activo = 1 
                    GROUP BY p.id_prod, p.codigo, p.nombre, p.moneda, p.precio, p.compra
            """
            #print(sql.replace('?', '{}').format(ff1, ff1, ff2, ff1, ff2, ff1, ff2, ff2))
            # Ejecutar con parámetros (orden corregido)
            c = self.conexion.execute(
                sql,
                [
                    ff1,    # stock_inicial (fecha < ff1)
                    ff1, ff2,  # entradas
                    ff1, ff2,  # salidas
                    ff1, ff2,  # ventas
                    ff2     # stock_actual (fecha <= ff2)
                ]
            )

            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en consulta: {str(e)}")
            return []