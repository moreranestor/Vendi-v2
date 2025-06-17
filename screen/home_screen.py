from datetime import datetime, timedelta
from flet import *

from model.cierreModel import CierreModel


class HomeScreen(Container):
    def __init__(self, page: Page, ventas: CierreModel):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = Colors.INDIGO
        self.ventas = ventas

        self.ventas_dia = self.ventas.obtener_cierre_por_fecha(
            fecha=f"{datetime.now().strftime("%d-%m-%Y")}"
        )

        self.ventas_ayer = self.ventas.obtener_cierre_por_fecha(
            fecha=f"{(datetime.now()-timedelta(days=1)).strftime("%d-%m-%Y")}"
        )

        self.ImporteTotal = self.ventas.importe_total_general()

        # datos generales
        self.antier = self.ventas.obtener_cierre_por_fecha(
            fecha=f"{(datetime.now()-timedelta(days=2)).strftime("%d-%m-%Y")}"
        )

        self.mensual = self.ventas.importe_mensual(
            año=f"{datetime.now().strftime('%Y')}",
            mes=f"{datetime.now().strftime('%m')}",
        )
        self.anual = self.ventas.importe_anual(año=f"{datetime.now().strftime('%Y')}")

        self.items_hoy = [
            {
                "icon": Icons.MONEY,
                "title": "Efectivo",
                "subtitle": "Dinero efectivo en caja",
                "value": (
                    f"$ {self.ventas_dia['efectivo']}"
                    if len(self.ventas_dia) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.BALANCE,
                "title": "Gastos",
                "subtitle": "Dinero sacado de la caja",
                "value": (
                    f"$ {self.ventas_dia['gastos']}"
                    if len(self.ventas_dia) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.CREDIT_CARD,
                "title": "Transferencias",
                "subtitle": "Dinero pagado por pasarelas",
                "value": (
                    f"$ {self.ventas_dia['transferencia']}"
                    if len(self.ventas_dia) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.MONETIZATION_ON,
                "title": "Venta final",
                "subtitle": "Dinero total de la venta",
                "value": (
                    f"$ {self.ventas_dia['importe']}"
                    if len(self.ventas_dia) > 0
                    else "No cuadre"
                ),
            },
        ]

        self.items_ayer = [
            {
                "icon": Icons.MONEY,
                "title": "Efectivo",
                "subtitle": "Gastos pagados por caja",
                "value": (
                    f"$ {self.ventas_ayer['efectivo']}"
                    if len(self.ventas_ayer) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.BALANCE,
                "title": "Gastos",
                "subtitle": "Gastos pagados por caja",
                "value": (
                    f"$ {self.ventas_ayer['gastos']}"
                    if len(self.ventas_ayer) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.CREDIT_CARD,
                "title": "Transferencias",
                "subtitle": "Pagos por tarjetas",
                "value": (
                    f"$ {self.ventas_ayer['transferencia']}"
                    if len(self.ventas_ayer) > 0
                    else "No cuadre"
                ),
            },
            {
                "icon": Icons.MONETIZATION_ON,
                "title": "Venta final",
                "subtitle": "Dinero en ventas",
                "value": (
                    f"$ {self.ventas_ayer['importe']}"
                    if len(self.ventas_ayer) > 0
                    else "No cuadre"
                ),
            },
        ]

        # Header with balance and notification icon
        header = Container(
            height=150,
            width=float("inf"),
            padding=padding.only(top=5, bottom=5, left=30, right=20),
            content=Column(
                controls=[
                    Row(
                        controls=[
                            # Balance column
                            Container(
                                content=Text(
                                    "Vendi",
                                    size=20,
                                    color=Colors.WHITE,
                                    weight=FontWeight.BOLD,
                                ),
                            ),
                            Column(
                                height=60,
                                controls=[
                                    Text(
                                        "Balance de las ventas",
                                        size=12,
                                        color=Colors.WHITE60,
                                    ),
                                    Text(
                                        f"${self.ImporteTotal}",
                                        size=22,
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
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            *[
                                GestureDetector(
                                    content=Container(
                                        content=Column(
                                            controls=[
                                                Container(
                                                    bgcolor=Colors.WHITE,
                                                    content=Icon(icon),
                                                    padding=padding.all(6),
                                                    border_radius=border_radius.all(10),
                                                ),
                                                Text(text, color=Colors.WHITE),
                                            ],
                                            spacing=2,
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            alignment=alignment.center,
                                        ),
                                        alignment=alignment.center,
                                        expand=True,
                                        opacity=1.0,
                                        animate_opacity=200,
                                    ),
                                    on_tap=lambda e, a=accion: self.go(e, a),
                                    mouse_cursor=MouseCursor.CLICK,
                                )
                                for icon, text, accion in [
                                    (
                                        Icons.FILE_DOWNLOAD,
                                        "Inventario",
                                        "inventario",
                                    ),
                                    (
                                        Icons.FILE_DOWNLOAD,
                                        "IPV",
                                        "ipv",
                                    ),
                                    (
                                        Icons.FIRE_TRUCK_OUTLINED,
                                        "Movimientos",
                                        "mov",
                                    ),
                                    (
                                        Icons.MONETIZATION_ON_OUTLINED,
                                        "Ventas",
                                        "ventas",
                                    ),
                                ]
                            ]
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        expand=True,
                    ),
                ]
            ),
        )

        # Main content area
        content_area = Container(
            expand=True,
            bgcolor=Colors.GREY_100,
            width=float("inf"),
            border_radius=border_radius.only(top_left=10, top_right=10),
            content=Column(
                scroll=ScrollMode.AUTO,
                controls=[
                    # Add your content components here
                    Text(
                        "Estadísticas",
                        size=16,
                        color=Colors.BLUE_900,
                        weight=FontWeight.BOLD,
                    ),
                    # Example items:
                    Container(
                        padding=padding.all(8),
                        content=Column(
                            controls=[
                                Text(
                                    "HOY",
                                    size=12,
                                    color=Colors.BLACK54,
                                    weight=FontWeight.BOLD,
                                ),
                                ListView(
                                    spacing=1,
                                    padding=5,
                                    auto_scroll=True,
                                    controls=[
                                        Container(
                                            border_radius=border_radius.all(10),
                                            bgcolor=Colors.WHITE,
                                            content=ListTile(
                                                leading=Icon(
                                                    item["icon"], color=Colors.BLUE_700
                                                ),
                                                title=Text(
                                                    item["title"],
                                                    color=Colors.BLUE_700,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                subtitle=Text(
                                                    item["subtitle"],
                                                    color=Colors.BLUE_500,
                                                    size=12,
                                                ),
                                                trailing=Text(
                                                    f'{item["value"]}',
                                                    color=Colors.BLUE_500,
                                                    weight=FontWeight.BOLD,
                                                ),
                                            ),
                                            margin=margin.only(bottom=1),
                                        )
                                        for item in self.items_hoy
                                    ],
                                ),
                                Container(height=8),
                                Text(
                                    "AYER",
                                    size=12,
                                    color=Colors.BLACK54,
                                    weight=FontWeight.BOLD,
                                ),
                                Container(height=8),
                                ListView(
                                    spacing=1,
                                    padding=5,
                                    auto_scroll=True,
                                    controls=[
                                        Container(
                                            border_radius=border_radius.all(10),
                                            bgcolor=Colors.WHITE,
                                            content=ListTile(
                                                leading=Icon(
                                                    item["icon"], color=Colors.BLUE_700
                                                ),
                                                title=Text(
                                                    item["title"],
                                                    color=Colors.BLUE_700,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                subtitle=Text(
                                                    item["subtitle"],
                                                    color=Colors.BLUE_500,
                                                    size=12,
                                                ),
                                                trailing=Text(
                                                    f'{item["value"]}',
                                                    color=Colors.BLUE_500,
                                                    weight=FontWeight.BOLD,
                                                ),
                                            ),
                                            margin=margin.only(bottom=1),
                                        )
                                        for item in self.items_ayer
                                    ],
                                ),
                                Container(height=8),
                                Text(
                                    "Anteriores",
                                    size=12,
                                    color=Colors.BLACK54,
                                    weight=FontWeight.BOLD,
                                ),
                                Container(height=8),
                                Container(
                                    border_radius=border_radius.all(10),
                                    bgcolor=Colors.WHITE,
                                    content=ListTile(
                                        leading=Icon(
                                            Icons.TODAY, color=Colors.BLUE_700
                                        ),
                                        title=Text(
                                            "Importe total",
                                            color=Colors.BLUE_700,
                                            weight=FontWeight.BOLD,
                                        ),
                                        subtitle=Text(
                                            f"{(datetime.now()-timedelta(days=2)).strftime("%d-%b")}",
                                            color=Colors.BLUE_500,
                                            weight=FontWeight.W_500,
                                            size=10,
                                        ),
                                        trailing=Text(
                                            (
                                                f"$ {self.antier['importe']}"
                                                if len(self.antier) > 0
                                                else "No cuadre"
                                            ),
                                            color=(
                                                Colors.GREEN_400
                                                if len(self.antier) > 0
                                                else Colors.RED_500
                                            ),
                                            weight=FontWeight.BOLD,
                                        ),
                                    ),
                                ),
                                Container(
                                    border_radius=border_radius.all(10),
                                    bgcolor=Colors.WHITE,
                                    content=ListTile(
                                        leading=Icon(
                                            Icons.DATE_RANGE, color=Colors.BLUE_700
                                        ),
                                        title=Text(
                                            "Balance mensual",
                                            color=Colors.BLUE_700,
                                            weight=FontWeight.BOLD,
                                        ),
                                        subtitle=Text(
                                            f"{(datetime.now()-timedelta(days=1)).strftime("%b")}",
                                            color=Colors.BLUE_500,
                                            weight=FontWeight.W_500,
                                            size=10,
                                        ),
                                        trailing=Text(
                                            f"$ {self.mensual}",
                                            color=Colors.GREEN_400,
                                            weight=FontWeight.BOLD,
                                        ),
                                    ),
                                ),
                                Container(
                                    border_radius=border_radius.all(10),
                                    bgcolor=Colors.WHITE,
                                    content=ListTile(
                                        leading=Icon(
                                            Icons.DATE_RANGE, color=Colors.BLUE_700
                                        ),
                                        title=Text(
                                            "Balance anual",
                                            color=Colors.BLUE_700,
                                            weight=FontWeight.BOLD,
                                        ),
                                        subtitle=Text(
                                            f"{(datetime.now()).strftime("%Y")}",
                                            color=Colors.BLUE_500,
                                            weight=FontWeight.W_500,
                                            size=10,
                                        ),
                                        trailing=Text(
                                            f"$ {self.anual}",
                                            color=Colors.GREEN_400,
                                            weight=FontWeight.BOLD,
                                        ),
                                    ),
                                ),
                            ],
                            spacing=2,
                        ),
                    ),
                ],
                spacing=5,
            ),
            padding=padding.only(top=10, left=10, right=10, bottom=5),
        )

        self.content = Column(controls=[header, content_area], spacing=0)

    def go(self, e, ruta):
        print(f"/{ruta}")
        if self.page is not None:
            self.page.go(f"/{ruta}")
        else:
            print("Error: Page reference is None")
        self.update()
