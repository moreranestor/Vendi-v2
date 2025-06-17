from .ModelBase import *
import sqlite3 as db
from .dbHelper import crear_tabla

class UsuariosModel(DBModelo):
    def __init__(self):   
        super(UsuariosModel,self)  
        self.conexion=db.connect(BASEDATO)      
        self.nombretabla="usuarios"
        self.ID="id"
        self.IDRelacion=""
        self.join=""
        self.joinCampo=""
        self.campos="(id,nombre,email, telefono, nit, fecha)"
        self.columnas = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'nombre': 'TEXT',
                'email': 'TEXT',
                'telefono': 'TEXT',
                'nit': 'TEXT',
                'fecha': 'TEXT',
              } 
       
        
        crear_tabla(self.conexion,self.nombretabla, self.columnas)         
    

        
    

    

 

