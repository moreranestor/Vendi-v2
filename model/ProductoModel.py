from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla


class ProductoModel(DBModelo):
    def __init__(self):
        
        super(ProductoModel, self).__init__()       
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "producto"
        self.ID = "id_prod"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "(codigo, nombre, precio, compra, unidad, categoria, activo, moneda, fecha_alta, fecha_edit)"
        self.columnas = {
            "id_prod": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "codigo": "text(20) NOT NULL",
            "nombre": "text(200) NOT NULL",
            "precio": "real(10, 2) NOT NULL DEFAULT 0",
            "compra": "real(10, 2) NOT NULL DEFAULT 0",
            "unidad": "text(200) NOT NULL",
            "categoria": "text(200) NOT NULL",
            "activo": "integer(4) NOT NULL DEFAULT 1",
            "moneda": "TEXT DEFAULT CUP",
            "fecha_alta": "text",
            "fecha_edit": "text",
        }

        crear_tabla(self.conexion, self.nombretabla, self.columnas)

    def consulata(self, cat=None, activo=1):
        """
        Obtiene productos con sus existencias, filtrables por categoría y estado

        Args:
            cat (str, optional): Categoría para filtrar. 'Todos' obtiene todas las categorías. Defaults to None.
            activo (int, optional): Estado activo (1) o inactivo (0). Defaults to 1.

        Returns:
            list: Lista de diccionarios con los productos y sus existencias
        """
        try:
            # Base query with parameterized inputs
            base_query = """
                SELECT p.*, 
                    SUM(p_es.entradas) - SUM(p_es.salidas) - SUM(p_es.ventas) as existencias 
                FROM producto p 
                INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod
                WHERE p.activo = ?
                {category_filter}
                GROUP BY p.id_prod 
                ORDER BY p.id_prod ASC
            """

            # Build the query safely
            params = [activo]
            if cat and cat != "Todos":
                category_filter = "AND p.categoria = ?"
                params.append(cat)
            else:
                category_filter = ""

            final_query = base_query.format(category_filter=category_filter)

            # Execute with parameters
            c = self.conexion.execute(final_query, params)

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en consulata: {str(e)}")
            # Consider logging the error properly
            return []

    def consulataCodigo(self, id):
        """Obtiene las existencias actuales de un producto por su ID"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
            SELECT SUM(p_es.entradas) - SUM(p_es.salidas) - SUM(p_es.ventas) as existencias 
            FROM producto p 
            INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod  
            WHERE p.id_prod = ?
            """
            c = self.conexion.execute(query, (id,))
            resultado = c.fetchone()

            # Manejar caso cuando no hay registros
            if resultado is None or resultado[0] is None:
                return 0

            return int(resultado[0])

        except Exception as e:
            print(f"Error al obtener existencias: {str(e)}")
            return 0

    def getMov(self, cat=None, activo=1):
        """
        Obtiene productos con sus existencias, filtrables por categoría y estado

        Args:
            cat (str, optional): Categoría para filtrar. 'Todos' obtiene todas las categorías. Defaults to None.
            activo (int, optional): Estado activo (1) o inactivo (0). Defaults to 1.

        Returns:
            list: Lista de diccionarios con los productos y sus existencias
        """
        try:
            # Base query with parameterized inputs
            base_query = """
                SELECT p.*, 
                    SUM(p_es.entradas) as entradas, SUM(p_es.salidas) as salidas,SUM(p_es.ventas) as ventas 
                FROM producto p 
                INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod
                WHERE p.activo = ?
                {category_filter}
                GROUP BY p.id_prod 
                ORDER BY p.id_prod ASC
            """

            # Build the query safely
            params = [activo]
            if cat and cat != "Todos":
                category_filter = "AND p.categoria = ?"
                params.append(cat)
            else:
                category_filter = ""

            final_query = base_query.format(category_filter=category_filter)

            # Execute with parameters
            c = self.conexion.execute(final_query, params)

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en consulata: {str(e)}")
            # Consider logging the error properly
            return []

    def getEntSalVent(self, id, estado):
        """
        Obtiene productos con sus existencias, filtrables por categoría y estado

        Args:
            id (int, optional): id para filtrar. 'Todos' obtiene todas las categorías. Defaults to None.
            activo (int, optional): Estado activo (1) o inactivo (0). Defaults to 1.

        Returns:
            list: Lista de diccionarios con los productos y sus existencias
        """
        try:
            # Base query with parameterized inputs
            base_query = """
               SELECT p.codigo, p.nombre, p.id_prod, p_es.entradas as entradas, p_es.salidas as salidas, p_es.ventas as ventas, p_es.fecha_alta, p_es.codigo as vale, p_es.detalles 
                FROM producto p 
                INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod
				WHERE p_es.id_prod= ? and p_es.estado = ?
                GROUP BY p_es.id_mov 
                ORDER BY p_es.fecha_alta DESC
            """

            # Execute with parameters
            c = self.conexion.execute(base_query, [id, estado])

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en consulata: {str(e)}")
            # Consider logging the error properly
            return []

    def getExistencia(self, cat=None, activo=1):
        """
        Obtiene productos con sus existencias, filtrables por categoría y estado

        Args:
            cat (str, optional): Categoría para filtrar. 'Todos' obtiene todas las categorías. Defaults to None.
            activo (int, optional): Estado activo (1) o inactivo (0). Defaults to 1.

        Returns:
            list: Lista de diccionarios con los productos y sus existencias
        """
        try:
            # Base query with parameterized inputs
            base_query = """
                SELECT p.*, 
                    SUM(p_es.entradas) - SUM(p_es.salidas) - SUM(p_es.ventas) as existencias 
                FROM producto p 
                INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod
                WHERE p.activo = ?
                {category_filter}
                GROUP BY p.id_prod 
                ORDER BY p.id_prod ASC
            """

            # Build the query safely
            params = [activo]
            if cat and cat != "Todos":
                category_filter = "AND p.categoria = ?"
                params.append(cat)
            else:
                category_filter = ""

            final_query = base_query.format(category_filter=category_filter)

            # Execute with parameters
            c = self.conexion.execute(final_query, params)

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en getExistencia: {str(e)}")
            # Consider logging the error properly
            return []

    def getExistenciaCodigo(self, id):
        """Obtiene las existencias actuales de un producto por su ID"""
        try:
            # Usar parámetros para evitar SQL injection
            query = """
            SELECT SUM(p_es.entradas) - SUM(p_es.salidas) - SUM(p_es.ventas) as existencias 
            FROM producto p 
            INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod  
            WHERE p.id_prod = ?
            """
            c = self.conexion.execute(query, (id,))
            resultado = c.fetchone()

            # Manejar caso cuando no hay registros
            if resultado is None or resultado[0] is None:
                return []

            return int(resultado[0])

        except Exception as e:
            print(f"Error al obtener getExistenciaCodigo: {str(e)}")
            return []

    def getInventario(self, activo=1):
        """
        Obtiene productos con sus existencias, filtrables  y estado y que no sean cero

        Args:
            activo (int, optional): Estado activo (1) o inactivo (0). Defaults to 1.

        Returns:
            list: Lista de diccionarios con los productos y sus existencias
        """
        try:
            # Base query with parameterized inputs
            base_query = """
                SELECT p.*, 
                    SUM(p_es.entradas) - SUM(p_es.salidas) - SUM(p_es.ventas) as existencias 
                FROM producto p 
                INNER JOIN productos_entr_sali p_es ON p.id_prod = p_es.id_prod
                WHERE p.activo = ?     
                GROUP BY p.id_prod 
                ORDER BY p.id_prod ASC
            """

            # Build the query safely
            params = [activo]
            # Execute with parameters
            c = self.conexion.execute(base_query, params)

            # Process results
            filas = c.fetchall()
            if not filas:
                return []

            columnas = [col[0] for col in c.description]
            return [
                {columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas
            ]

        except Exception as e:
            print(f"Error en getExistencia: {str(e)}")
            # Consider logging the error properly
            return []
