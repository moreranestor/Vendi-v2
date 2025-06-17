import flet as ft

style = ft.Theme(
    navigation_bar_theme=ft.NavigationBarTheme(
        label_text_style={
            ft.ControlState.DEFAULT: ft.TextStyle(color=ft.Colors.INDIGO, font_family='aBeeZee'),
            ft.ControlState.SELECTED: ft.TextStyle(color=ft.Colors.INDIGO, font_family='aBeeZee'),
        },
    ),
    list_tile_theme=ft.ListTileTheme(
        dense=True,
        
        min_tile_height=40,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=2),
        selected_color=ft.Colors.BLUE_500,
        selected_tile_color=ft.Colors.BLUE_500,
        icon_color=ft.Colors.BLUE_700,
        title_text_style=ft.TextStyle(
            color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_900, size=14, font_family='aBeeZee'
        ),
        subtitle_text_style=ft.TextStyle(color=ft.Colors.BLUE_500, size=12 , font_family='aBeeZee'),
        leading_and_trailing_text_style=ft.TextStyle(color=ft.Colors.RED_500, size=12 , font_family='aBeeZee'),
    
    ),
    text_button_theme=ft.TextButtonTheme(
        bgcolor=ft.Colors.INDIGO,
        foreground_color=ft.Colors.WHITE,
        text_style=ft.TextStyle(font_family='aBeeZee')
    ),
    
    text_theme= ft.TextStyle(font_family='aBeeZee'),
    
)
