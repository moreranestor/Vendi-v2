from flet import *


class TextInput(TextField):
    def __init__(self, label="",width=None, change=None, error="", keyboard=KeyboardType.TEXT, valor="", readonly=False):
        super().__init__()
        self.keyboard = keyboard
        self.label = label
        self.width = width
        self.hint_text = label
        self.color = Colors.BLACK
        self.hint_style = TextStyle(color=Colors.BLACK, size=12)
        self.text_align = TextAlign.LEFT
        self.border_color = Colors.BLACK
        self.border_width = 0.5
        self.on_change = change
        self.error_text = error
        self.value = valor
        self.read_only = readonly
        
class TextInputSearch(TextField):
    def __init__(self, label="",width=None, change=None, error="", keyboard=KeyboardType.TEXT, valor="", readonly=False):
        super().__init__()
        self.keyboard = keyboard
        self.label = label
        self.width = width
        self.hint_text = label
        self.color = Colors.BLACK
        self.hint_style = TextStyle(color=Colors.BLACK, size=12)
        self.text_align = TextAlign.LEFT
        self.border_color = Colors.BLACK
        self.border_width = 0.5
        self.on_change = change
        self.error_text = error
        self.value = valor
        self.read_only = readonly
        self.height=30
        self.border_radius=border_radius.all(20)





