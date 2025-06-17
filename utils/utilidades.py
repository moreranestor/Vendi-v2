def ajuste_imagen_64(imagen):
    imagen = str(imagen)
    a = imagen.removeprefix("b")
    a = a.replace("'", "")
    return a


def print_controls_structure(self, control=None, indent=0):
    """Muestra la estructura de controles en la consola"""
    if control is None:
        control = self.content_area

    print(" " * indent + str(type(control).__name__))
    if hasattr(control, "content"):
        if isinstance(control.content, list):
            for c in control.content:
                self.print_controls_structure(c, indent + 2)
        else:
            self.print_controls_structure(control.content, indent + 2)


