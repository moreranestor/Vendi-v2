from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password).hexdigest()


def generar_codigo_unico(datos_base: str) -> str:
    """Genera un hash único a partir de datos base"""
    timestamp = datetime.now().isoformat()
    datos = f"{datos_base}{timestamp}".encode('utf-8')
    return hashlib.sha256(datos).hexdigest()[:16]  # Tomamos los primeros 16 caracteres