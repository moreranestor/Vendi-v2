import decimal
import re

class Validaciones:
    def __init__(self) ->None:
        pass
    
    def valid_email(self,correo):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, correo) is not None

    @staticmethod
    def valid_number(d):
        try:
            d = float(d)
        except ValueError:
            return False

        if isinstance(d, float) or isinstance(d, int):
            return True
        else:
            return False
    
    @staticmethod
    def valid_user(usuario):
        if len(usuario) < 0:
            return False        
        return True

    @staticmethod
    def valid_codigo(text):
        if len(text) < 4:
            return False
        return True

    @staticmethod
    def valid_pass(password):
        if len(password) < 0:
            return False        
        return True
    
    @staticmethod
    def valid_password_new(password):
        # La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True

