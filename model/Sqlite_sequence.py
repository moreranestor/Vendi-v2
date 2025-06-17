from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla

class Sqlite_sequence(DBModelo):
    def __init__(self):
        super(Sqlite_sequence, self).__init__()
        self.conexion = db.connect(BASEDATO)
        self.nombretabla = "sqlite_sequence"
        self.ID = ""
        self.IDRelacion = ""
        self.join = ""
        self.joinCampo = ""
        self.campos = "(name, seq)"
       