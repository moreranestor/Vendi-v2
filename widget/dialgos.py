
from flet import *
def alerta(accion,mensaje,titulo,error=False):
    return AlertDialog(
            title=Row(
                controls=[
                    Text(titulo),
                    Icon(Icons.ERROR if error else Icons.CHECK_CIRCLE, 
                         color=Colors.RED if error else Colors.GREEN),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=Text(mensaje),
            actions=[
                TextButton("OK", on_click=accion),
            ],
        )
