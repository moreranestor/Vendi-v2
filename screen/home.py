from flet import *
from route import params, Basket
from screen.almacen_screen import StorageScreen
from screen.punto_venta_screen import SellScreen
from screen.opciones_screen import OptionsScreen
from screen.home_screen import HomeScreen
# Clases para cada pantalla (versión simplificada y corregida)

from model.cierreModel import CierreModel

class Home:
    def __init__(self):
        self.selected_index = 0
        self.main_content = Column(expand=True)

    def view(self, page: Page, params: params, basket: Basket):
        # Función para cambiar pestañas
        def _change_tab(e):
            self.selected_index = e.control.selected_index
            self.main_content.controls.clear() 
            _ventas = CierreModel()            

            screens = {
                0: HomeScreen(page=page, ventas=_ventas),
                1: StorageScreen(page=page),
                2: SellScreen(page=page),
                3: OptionsScreen(page=page),
            }
            self.main_content.controls.append(
                screens.get(self.selected_index,HomeScreen(page=page, ventas=_ventas))
            )
            page.update()

        # Configurar contenido inicial
        if not self.main_content.controls:
            _ventas = CierreModel()    
            self.main_content.controls.append(HomeScreen(page=page, ventas=_ventas))

        return View(
            "/home",
            bgcolor=Colors.WHITE,
            padding=0,
            controls=[
                Column(
                    expand=True,
                    controls=[
                        # Contenido principal expandible
                        self.main_content,
                        # Barra de navegación inferior
                        Container(
                            content=NavigationBar(
                                adaptive=True,
                                on_change=_change_tab,
                                selected_index=self.selected_index,
                                # Fondo cuando no está seleccionado
                                destinations=[
                                    NavigationBarDestination(
                                        icon=Icon(Icons.HOME_OUTLINED , color=Colors.BLUE_900) ,
                                        selected_icon=Icon(Icons.HOME , color=Colors.BLUE_900),
                                        label="Inicio",
                                    ),
                                    NavigationBarDestination(
                                        icon=Icon(Icons.INVENTORY_2_OUTLINED , color=Colors.BLUE_900) ,
                                        selected_icon=Icon(Icons.INVENTORY_2 , color=Colors.BLUE_900) ,
                                        label="Almacén",
                                    ),
                                    NavigationBarDestination(
                                        icon=Icon(Icons.MONETIZATION_ON_OUTLINED , color=Colors.BLUE_900) ,
                                        selected_icon=Icon(Icons.MONETIZATION_ON, color=Colors.BLUE_900) ,
                                        label="Cafetería",
                                    ),
                                    NavigationBarDestination(
                                        icon=Icon(Icons.SETTINGS_OUTLINED,color=Colors.BLUE_900) ,
                                        selected_icon=Icon(Icons.SETTINGS,color=Colors.BLUE_900) ,
                                        label="Opciones",
                                    ),
                                ],
                               
                                indicator_color=Colors.with_opacity(
                                    0.7, Colors.GREY_100
                                ),  # Color del indicador
                                bgcolor=Colors.GREY_100,  # Color de fondo de toda la barra
                                height=70,
                                
                                
                  
                                label_behavior=NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,  # Mostrar siempre las etiquetas
                            ),
                            padding=padding.only(bottom=1),
                          
                        ),
                    ],
                    spacing=0,
                )
            ],
        )
