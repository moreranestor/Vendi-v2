import sqlite3
import os
from pathlib import Path

TITULO="Vendi"
URL="data/vendi.db"
#BASE_DIR=Path(__file__).resolve().parent.parent
os.makedirs('data', exist_ok=True)
BASEDATO=URL

def tabla_existe(conn,Tabla_nombre): 
    cursor = conn.cursor()    
    # Ejecutar la consulta para verificar si la tabla existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (Tabla_nombre,))    
    # Obtener el resultado
    result = cursor.fetchone()    
    # Cerrar la conexión
    #conn.close()    
    # Devolver True si la tabla existe, de lo contrario False
    return result is not None
    
def getDatabase(): 
    return sqlite3.connect(BASEDATO)        
 
def crear_tabla(conn,nombre_tabla, columnas):  
    cursor = conn.cursor()    
    # Crear la sentencia SQL para crear la tabla
    columnas_definicion = ', '.join([f"{columna} {tipo}" for columna, tipo in columnas.items()])

    sql = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({columnas_definicion})"    
    
    # Ejecutar la sentencia SQL
    cursor.execute(sql)    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    #conn.close()
    
  


