from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla
from typing import Dict, List

class CierreModel(DBModelo):
    def __init__(self):
        super(CierreModel, self)
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "cierre"
        self.ID = "id_cierre"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "id_cierre, fecha, trabajador, gastos, transferencia, efectivo, importe"

        self.columnas = {
            "id_cierre": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "fecha": "Text NOT NULL",
            "trabajador": "Text NOT NULL",
            "gastos": "real(10, 2) NOT NULL DEFAULT 0",
            "transferencia": "real(10, 2) NOT NULL DEFAULT 0",
            "efectivo": "real(10, 2) NOT NULL DEFAULT 0",
            "importe": "real(10, 2) NOT NULL DEFAULT 0",
           
        }
        crear_tabla(self.conexion, self.nombretabla, self.columnas)

    def obtener_cierre_por_fecha(self, fecha: str) -> Dict:
        """
        Obtiene el cierre de caja para una fecha específica
        
        Args:
            fecha (str): Fecha en formato 'dd-mm-yyyy'
            
        Returns:
            Dict: Diccionario con los datos del cierre o None si no existe
        """
        try:
            query = f"SELECT {self.campos}, importe-gastos as real  FROM {self.nombretabla} WHERE fecha = ?"
            cursor = self.conexion.cursor()
            cursor.execute(query, (fecha,))
            resultado = cursor.fetchone()
            
            if resultado:
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, resultado))
            return []
            
        except Exception as e:
            print(f"Error al obtener cierre por fecha: {str(e)}")
            return []

    def importe_total_general(self) -> float:
        """
        Calcula el importe total acumulado de todos los cierres
        
        Returns:
            float: Suma total de todos los importes registrados
        """
        try:
            query = f"SELECT SUM(importe) - sum(gastos) as total FROM {self.nombretabla}"
            cursor = self.conexion.cursor()
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado[0] or 0.0
            
        except Exception as e:
            print(f"Error al calcular importe total general: {str(e)}")
            return 0.0

    def importe_mensual(self, mes: int, año: int) -> float:
        """
        Calcula el importe total para un mes y año específicos
        
        Args:
            mes (int): Mes (1-12)
            año (int): Año (ej. 2023)
            
        Returns:
            float: Suma de importes para el mes/año especificado
        """
        try:
            # Formateamos el mes para que siempre tenga 2 dígitos
            mes_str = f"{mes}"
            patron_fecha = f"%-{mes_str}-{año}"
            
            query = f"""
                SELECT SUM(importe) as total 
                FROM {self.nombretabla} 
                WHERE fecha LIKE ?
            """
            cursor = self.conexion.cursor()
            cursor.execute(query, (patron_fecha,))
            resultado = cursor.fetchone()
            return resultado[0] or 0.0
            
        except Exception as e:
            print(f"Error al calcular importe mensual: {str(e)}")
            return 0.0

    def importe_anual(self, año: int) -> float:
        """
        Calcula el importe total para un año específico
        
        Args:
            año (int): Año (ej. 2023)
            
        Returns:
            float: Suma de importes para el año especificado
        """
        try:
            patron_fecha = f"%-{año}"
            
            query = f"""
                SELECT SUM(importe) as total 
                FROM {self.nombretabla} 
                WHERE fecha LIKE ?
            """
            cursor = self.conexion.cursor()
            cursor.execute(query, (patron_fecha,))
            resultado = cursor.fetchone()
            return resultado[0] or 0.0
            
        except Exception as e:
            print(f"Error al calcular importe anual: {str(e)}")
            return 0.0

    def resumen_por_dia(self, mes: int = None, año: int = None) -> List[Dict]:
        """
        Obtiene un resumen de cierres por día, opcionalmente filtrado por mes y/o año
        
        Args:
            mes (int, optional): Mes para filtrar (1-12)
            año (int, optional): Año para filtrar
            
        Returns:
            List[Dict]: Lista de diccionarios con fecha e importe diario
        """
        try:
            condiciones = []
            parametros = []
            
            if mes is not None:
                condiciones.append("SUBSTR(fecha, 4, 2) = ?")
                parametros.append(f"{mes:02d}")
                
            if año is not None:
                condiciones.append("SUBSTR(fecha, 7) = ?")
                parametros.append(str(año))
                
            where_clause = " AND ".join(condiciones) if condiciones else "1=1"
            
            query = f"""
                SELECT 
                    fecha,
                    SUM(importe) as importe_diario,
                    SUM(gastos) as gastos_diarios,
                    SUM(transferencia) as transferencias_diarias,
                    SUM(efectivo) as efectivo_diario
                FROM {self.nombretabla}
                WHERE {where_clause}
                GROUP BY fecha
                ORDER BY fecha
            """
            
            cursor = self.conexion.cursor()
            cursor.execute(query, parametros)
            
            resultados = []
            columnas = [desc[0] for desc in cursor.description]
            
            for fila in cursor.fetchall():
                resultados.append(dict(zip(columnas, fila)))
                
            return resultados
            
        except Exception as e:
            print(f"Error al obtener resumen por día: {str(e)}")
            return []

    
    
    def obtener_todos_los_cierres(self, orden="DESC", limit=None):
        """
        Obtiene todos los registros de cierres
        :param orden: ASC o DESC para el ordenamiento
        :param limit: Límite de registros a devolver (opcional)
        :return: Lista de diccionarios con los cierres
        """
        query = f"SELECT * FROM {self.nombretabla} ORDER BY fecha {orden}"
        if limit:
            query += f" LIMIT {limit}"
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute(query)
            filas =cursor.fetchall()
            columnas = [col[0] for col in cursor.description]
            return [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        except Exception as e:
            print(f"Error al obtener cierres: {e}")
            return []

    def obtener_cierres_por_rango_fechas(self, fecha_inicio, fecha_fin, orden="DESC"):
        
        """
        Obtiene cierres dentro de un rango de fechas
        :param fecha_inicio: Fecha inicial en formato dd-mm-aaaa
        :param fecha_fin: Fecha final en formato dd-mm-aaaa
        :param orden: ASC o DESC para el ordenamiento
        :return: Lista de diccionarios con los cierres
        """
        try:
            # Convertir fechas al formato de la base de datos (asumiendo que se almacenan como TEXT en formato dd-mm-aaaa)
            query = f"""
            SELECT * FROM {self.nombretabla} 
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha {orden}
            """
            cursor = self.conexion.cursor()
            cursor.execute(query, (fecha_inicio, fecha_fin))
            filas = cursor.fetchall()
            columnas = [col[0] for col in cursor.description]
            return [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        except Exception as e:
            print(f"Error al filtrar cierres por fecha: {e}")
            return []

    