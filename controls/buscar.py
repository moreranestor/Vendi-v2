from flet import *


class Buscar(Container):
    def __init__(self, interruptor=True, change=None):
        super().__init__()
        self.interruptor = interruptor
        self.input = TextField(hint_text="Producto a buscar",
                               color=Colors.RED,
                               hint_style=TextStyle(color=Colors.WHITE, size=12),
                               text_align=TextAlign.LEFT,
                               border_color=Colors.WHITE,
                               border_width=0.5,
                               on_change=change
                               )       
        self.height = 0
        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.input
            ],
        )
    

   
