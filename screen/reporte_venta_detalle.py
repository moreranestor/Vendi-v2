from datetime import datetime
from flet import *
from route import params, Basket
from model.VentasModel import VentasModel


class VentasDetalles:
    def __init__(self):
        self.selected_index = 0
        
        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        fecha =params.get('fecha')
        print(fecha)
        self.page = page  # Guardar referencia a la página
        ventasModelo = VentasModel()
        ventas = ventasModelo.findByCampo('fecha_alta', f"{fecha}" )  
        # Crear lista de ventas
        lista_ventas = ListView(
            expand=True,
            spacing=10,
            padding=10,
            controls=[
                Container(
                    bgcolor=Colors.WHITE,
                    border_radius=10,
                    padding=10,
                    shadow=BoxShadow(
                        spread_radius=1,
                        blur_radius=5,
                        color=Colors.BLUE_100,
                        offset=Offset(0, 0),
                    ),
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Icon(Icons.CALENDAR_TODAY, color=Colors.BLUE_700),
                                    Text(
                                        f"{venta['fecha_alta']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Container(width=10),                                   
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Divider(height=1),
                            Row(
                                controls=[
                                    Column(
                                        controls=[
                                            Text(
                                                "Producto",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${venta['nombre']}",
                                                color=Colors.BLUE_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Precio",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${venta['precio']}",
                                                color=Colors.BLUE_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Cantidad", size=12, color=Colors.GREY_600
                                            ),
                                            Text(
                                                f"${venta['cantidad']}",
                                                color=Colors.RED_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Importe", size=12, color=Colors.GREY_600
                                            ),
                                            Text(
                                                f"${venta['cantidad']*venta['precio']}",
                                                color=Colors.GREEN_700,
                                                weight=FontWeight.BOLD,
                                                size=14,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=5,
                                alignment=MainAxisAlignment.SPACE_EVENLY,
                            ),
                        ],
                        spacing=5,
                    ),
                )
                for venta in ventas
            ],
        )

        # Header
        header = Container(
            padding=padding.only(top=5, bottom=0, left=20, right=20),
            bgcolor=Colors.INDIGO,
            content=Row(
                controls=[
                    Row(
                        controls=[
                            IconButton(
                                Icons.ARROW_BACK,
                                icon_color=Colors.INDIGO,
                                on_click=lambda e: page.go("/ventas"),
                                icon_size=16,
                                bgcolor=Colors.WHITE,
                                width=30,
                            ),
                            Text(
                                "Vendi",
                                size=20,
                                color=Colors.WHITE,
                                weight=FontWeight.BOLD,
                            ),
                        ]
                    ),
                    Column(
                        height=60,
                        controls=[
                            Text(
                                "Historial de ventas",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"Listado de la venta de un día.",
                                size=12,
                                color=Colors.WHITE,
                                weight=FontWeight.BOLD,
                            ),
                        ],
                        spacing=2,
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.END,
                    ),  # Notification icon
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        content_area = Container(
            expand=True,
            bgcolor=Colors.GREY_100,
            border_radius=border_radius.only(top_left=10, top_right=10),
            content=Column(
                scroll=ScrollMode.AUTO,
                controls=[lista_ventas],
                spacing=0,
            ),
            
        )

        return View(            
            "/ventas", bgcolor=Colors.INDIGO, padding=0, controls=[header, content_area, ]
        )
    