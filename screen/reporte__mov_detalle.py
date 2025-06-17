from datetime import datetime
from flet import *
from route import params, Basket
from model.ProductoModel import ProductoModel


class MovimientosEntradasDetalles:
    def __init__(self):
        self.selected_index = 0

        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        id = params.get("id_prod")
        print(id)
        self.page = page  # Guardar referencia a la página

        productoModel = ProductoModel()
        _producto = productoModel.getEntSalVent(id, "S")
        # Crear lista de _producto
        lista = ListView(
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
                                    Row(
                                        controls=[
                                            Icon(
                                                Icons.CALENDAR_TODAY,
                                                color=Colors.BLUE_700,
                                            ),
                                            Text(
                                                f"{venta['fecha_alta']}",
                                                weight=FontWeight.BOLD,
                                                size=14,
                                                color=Colors.BLUE_900,
                                            ),
                                        ]
                                    ),
                                    Container(width=10),
                                    Text(
                                        f"{venta['vale']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
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
                                                f"{venta['nombre']}",
                                                color=Colors.BLUE_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=3,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Código",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{venta['codigo']}",
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
                                                "Salidas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{venta['salidas']}",
                                                color=Colors.RED_700,
                                                weight=FontWeight.BOLD,
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
                for venta in _producto
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
                                on_click=lambda e: page.go("/mov"),
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
                                "Historial de las salidas.",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"Vendi, tu amigo del control.",
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
                controls=[lista],
                spacing=0,
            ),
        )

        return View(
            "/mov/detalle/s",
            bgcolor=Colors.INDIGO,
            padding=0,
            controls=[
                header,
                content_area,
            ],
        )


class MovimientosSalidasDetalles:
    def __init__(self):
        self.selected_index = 0

        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        id = params.get("id_prod")

        self.page = page  # Guardar referencia a la página

        productoModel = ProductoModel()
        _producto = productoModel.getEntSalVent(id, "S")
        # Crear lista de _producto
        lista = ListView(
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
                                    Row(
                                        controls=[
                                            Icon(
                                                Icons.CALENDAR_TODAY,
                                                color=Colors.BLUE_700,
                                            ),
                                            Text(
                                                f"{venta['fecha_alta']}",
                                                weight=FontWeight.BOLD,
                                                size=14,
                                                color=Colors.BLUE_900,
                                            ),
                                        ]
                                    ),
                                    Container(width=10),
                                    Text(
                                        f"{venta['vale']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
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
                                                f"{venta['nombre']}",
                                                color=Colors.BLUE_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=3,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Código",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{venta['codigo']}",
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
                                                "Salidas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{venta['salidas']}",
                                                color=Colors.RED_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=5,
                                alignment=MainAxisAlignment.SPACE_EVENLY,
                            ),
                            Row(
                                controls=[
                                    Row(
                                        controls=[
                                            Icon(
                                                Icons.NOTE,
                                                color=Colors.BLUE_700,
                                            ),
                                            Text(
                                                f"{venta['detalles']}",
                                                weight=FontWeight.BOLD,
                                                size=14,
                                                color=Colors.BLUE_900,
                                            ),
                                        ]
                                    ),                                    
                                ],
                                alignment=MainAxisAlignment.START,
                            ),
                        ],
                        spacing=5,
                    ),
                )
                for venta in _producto
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
                                on_click=lambda e: page.go("/mov"),
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
                                "Historial de las salidas.",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"Vendi, tu amigo del control.",
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
                controls=[lista],
                spacing=0,
            ),
        )

        return View(
            "/mov/detalle/s",
            bgcolor=Colors.INDIGO,
            padding=0,
            controls=[
                header,
                content_area,
            ],
        )


class MovimientosVentasDetalles:
    def __init__(self):
        self.selected_index = 0

        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        id = params.get("id_prod")

        self.page = page  # Guardar referencia a la página

        productoModel = ProductoModel()
        _producto = productoModel.getEntSalVent(id, "V")
        # Crear lista de _producto
        lista = ListView(
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
                                    Row(
                                        controls=[
                                            Icon(
                                                Icons.CALENDAR_TODAY,
                                                color=Colors.BLUE_700,
                                            ),
                                            Text(
                                                f"{venta['fecha_alta']}",
                                                weight=FontWeight.BOLD,
                                                size=14,
                                                color=Colors.BLUE_900,
                                            ),
                                        ]
                                    ),
                                    Container(width=10),
                                    Text(
                                        f"{venta['vale']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
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
                                                f"{venta['nombre']}",
                                                color=Colors.BLUE_700,
                                                weight=FontWeight.BOLD,
                                            ),
                                        ],
                                        expand=3,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Código",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{venta['codigo']}",
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
                                                "Ventas", size=12, color=Colors.GREY_600
                                            ),
                                            Text(
                                                f"{venta['ventas']}",
                                                color=Colors.RED_700,
                                                weight=FontWeight.BOLD,
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
                for venta in _producto
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
                                on_click=lambda e: page.go("/mov"),
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
                                "Historial de las ventas.",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"Vendi, tu amigo del control.",
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
                controls=[lista],
                spacing=0,
            ),
        )

        return View(
            "/mov/detalle/v",
            bgcolor=Colors.INDIGO,
            padding=0,
            controls=[
                header,
                content_area,
            ],
        )
