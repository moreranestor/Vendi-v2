from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla


class ProvedorModel(DBModelo):
    def __init__(self):
        super(ProvedorModel, self)
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "provedores"
        self.ID = "id"
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "id, organismo, nombre, telefono, producto"
        self.columnas = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "organismo": "text(20) NOT NULL",
            "nombre": "text(200) NOT NULL",
            "telefono": "text(200) NOT NULL",
            "producto": "text(200) NOT NULL",
        }

        crear_tabla(self.conexion, self.nombretabla, self.columnas)
