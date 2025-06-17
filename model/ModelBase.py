import sqlite3 as db
from .dbHelper import *
from threading import Semaphore


class DBModelo:
    def __init__(self, max_connections=5):
        self.error = ""
        self.conexion = ""
        self.nombretabla = ""
        self.ID = ""
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = ""
        self._semaphore = Semaphore(max_connections)
        try:
            self.conexion = self._get_connection
            self.error = "Conexion esta ok"
        except:
            self.error = "No base de dato por: %s" % (getDatabase()).Error()

    def _get_connection(self):
        self._semaphore.acquire()
        conn = sqlite3.connect(getDatabase(), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")  # Mejor para concurrencia
        conn.execute("PRAGMA busy_timeout=3000")  # Timeout de 3 segundos
        return conn
    
    def _close_connection(self):
        self.conexion.close()
        self._semaphore.release()
        

    def getConexionState(self):
        print(self.error)

    def exitConexion(self):
        self.conexion.close()

    def findAll(self, orden=f"ASC", limit=10):
        c = self.conexion.execute(
            f"select * from  %s order by {self.ID} %s" % (self.nombretabla, orden)
        )
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def findID(self, id):
        c = self.conexion.execute(
            "select * from %s where %s = ?" % (self.nombretabla, self.ID), (id,)
        )
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def Sql(self, sql):
        c = self.conexion.execute("%s" % sql)
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def insertar(self, datos: object) -> object:
        # Conectar a la base de datos
        conn = sqlite3.connect(BASEDATO)
        cursor = conn.cursor()
        # Crear la sentencia SQL para insertar datos
        columnas = ", ".join(datos.keys())
        marcadores = ", ".join(["?" for _ in datos])
        valores = tuple(datos.values())
        sql = f"INSERT INTO {self.nombretabla} ({columnas}) VALUES ({marcadores})"
        # Ejecutar la sentencia SQL
        cursor.execute(sql, valores)
        # Guardar los cambios y cerrar la conexión
        conn.commit()
        return cursor.lastrowid

    def update(self, datos, condicion):
        # Conectar a la base de datos
        conn = sqlite3.connect(BASEDATO)
        cursor = conn.cursor()
        # Crear la sentencia SQL para actualizar datos
        set_clause = ", ".join([f"{columna} = ?" for columna in datos.keys()])
        valores = list(datos.values())
        sql = f"UPDATE {self.nombretabla} SET {set_clause} WHERE {condicion}"
        # Ejecutar la sentencia SQL
        cursor.execute(sql, valores)  # Guardar los cambios y cerrar la conexión
        conn.commit()
        print(f"Datos actualizados en la tabla '{self.nombretabla}' exitosamente.")

    def delete(self, id):
        c = self.conexion.execute(
            "delete from %s where %s = ?" % (self.nombretabla, self.ID), (id,)
        )
        self.conexion.commit()
        return c.fetchall()

    def count(self):
        c = self.conexion.execute("select * from %s" % (self.nombretabla))
        return len(c.fetchall())

    def getID(self, campo, valor):
        c = self.conexion.execute(
            "select id from %s where %s=? " % (self.nombretabla, campo), (valor,)
        )
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def getData(self, condicion=None):
        if condicion:
            c = self.conexion.execute(
                f"select * from {self.nombretabla} where {condicion} "
            )
        else:
            c = self.conexion.execute(f"select * from {self.nombretabla}")
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def findByCampo(self, campo, valor):
        c = self.conexion.execute(
            "select * from %s where %s=? " % (self.nombretabla, campo), (valor,)
        )
        filas = c.fetchall()
        columnas = [col[0] for col in c.description]
        resul = [{columnas[i]: fila[i] for i in range(len(columnas))} for fila in filas]
        return resul

    def getFields(self):
        r = self.campos()
        return r

    def __str__(self) -> str:
        return self.conexion.__str__

    def deleteParamts(self, campo, valor):
        c = self.conexion.execute(
            "delete from %s where %s = %s" % (self.nombretabla, campo, valor)
        )
        self.conexion.commit()
        return c.fetchall()

    def limpiar(self):
        c = self.conexion.execute("delete from %s " % (self.nombretabla))
        self.conexion.commit()
        return c.fetchall()
