from datetime import datetime
from flet import *
from route import params, Basket
from model.cierreModel import CierreModel


class Ventas:
    def __init__(self):
        self.selected_index = 0

        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        self.page = page  # Guardar referencia a la página
        ventas = CierreModel()
        cierres = ventas.obtener_todos_los_cierres(limit=10)

        # Controles de filtrado por fecha
        fecha_inicio = TextField(
            label="Desde",
            hint_text="dd-mm-aaaa",
            width=120,
            border_radius=10,
            content_padding=10,
            height=40,
        )

        fecha_fin = TextField(
            label="Hasta",
            hint_text="dd-mm-aaaa",
            width=120,
            border_radius=10,
            content_padding=10,
            height=40,
        )

        def _mostrar_alerta(titulo, mensaje, error=False):
            """Muestra una alerta al usuario"""
            alerta = AlertDialog(
                title=Row(
                    controls=[
                        Text(titulo),
                        Icon(
                            Icons.ERROR if error else Icons.CHECK_CIRCLE,
                            color=Colors.RED if error else Colors.GREEN,
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
                content=Text(mensaje),
                actions=[
                    TextButton("OK", on_click=lambda e: _cerrar_dialogo(alerta)),
                ],
            )
            page.open(alerta)

        def _cerrar_dialogo(dialogo):
            page.close(dialogo)
            page.update()

        def filtrar_cierres(e):
            # Ejecutar en hilo separado
            ventas = CierreModel()

            # Validar campos
            if not fecha_inicio.value or not fecha_fin.value:
                # _mostrar_alerta("Error", "Debe ingresar ambas fechas.", True)
                cierres_filtrados = ventas.obtener_todos_los_cierres(limit=10)

            # Validar formato de fechas
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio.value, "%d-%m-%Y")
                fecha_fin_dt = datetime.strptime(fecha_fin.value, "%d-%m-%Y")
            except ValueError:
                _mostrar_alerta(
                    "Error", "Formato de fecha inválido. Use dd-mm-aaaa", True
                )
                return

            # Validar rango
            if fecha_inicio_dt > fecha_fin_dt:
                _mostrar_alerta(
                    "Error",
                    "La fecha inicial no puede ser mayor que la final",
                    True,
                )
                return

            # Filtrar cierres
            try:

                cierres_filtrados = ventas.obtener_cierres_por_rango_fechas(
                    fecha_inicio.value, fecha_fin.value
                )

                # Actualizar lista
                lista_cierres.controls.clear()

                lista_cierres.controls = [
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
                                        Icon(
                                            Icons.CALENDAR_TODAY, color=Colors.BLUE_700
                                        ),
                                        Text(
                                            f" {cierre['fecha']}",
                                            weight=FontWeight.BOLD,
                                            size=14,
                                            color=Colors.BLUE_900,
                                        ),
                                        Container(width=10),
                                        Chip(
                                            label=Text("Ver ventas"),
                                            bgcolor=Colors.BLUE_100,
                                            on_click=lambda e, c=cierre: self.mostrar_ventas(
                                                page, c
                                            ),
                                            autofocus=False,
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
                                                    "Efectivo",
                                                    size=12,
                                                    color=Colors.GREY_600,
                                                ),
                                                Text(
                                                    f"${cierre['efectivo']}",
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
                                                    "Transferencias",
                                                    size=12,
                                                    color=Colors.GREY_600,
                                                ),
                                                Text(
                                                    f"${cierre['transferencia']}",
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
                                                    "Gastos",
                                                    size=12,
                                                    color=Colors.GREY_600,
                                                ),
                                                Text(
                                                    f"${cierre['gastos']}",
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
                                                    "Total",
                                                    size=12,
                                                    color=Colors.GREY_600,
                                                ),
                                                Text(
                                                    f"${cierre['importe']}",
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
                    for cierre in cierres_filtrados
                ]
                if not cierres_filtrados:
                    _mostrar_alerta(
                        "error", "No se encontraron cierres en este rango", True
                    )

                ventas.exitConexion()
                lista_cierres.update()
                page.update()

            except Exception as ex:
                _mostrar_alerta(
                    "Error", f"Ocurrió un error al filtrar: {str(ex)}", True
                )

        def _todos(e):
            lista_cierres.controls.clear()

            lista_cierres.controls = [
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
                                        f" {cierre['fecha']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Container(width=10),
                                    Chip(
                                        label=Text("Ver ventas"),
                                        bgcolor=Colors.BLUE_100,
                                        on_click=lambda e, c=cierre: self.mostrar_ventas(
                                            page, c
                                        ),
                                        autofocus=False,
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
                                                "Efectivo",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['efectivo']}",
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
                                                "Transferencias",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['transferencia']}",
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
                                                "Gastos",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['gastos']}",
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
                                                "Total",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['importe']}",
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
                for cierre in cierres
            ]

            lista_cierres.update()
            page.update()

        filtro_container = Container(
            padding=10,
            bgcolor=Colors.GREY_100,
            border_radius=10,
            content=Row(
                controls=[
                    fecha_inicio,
                    fecha_fin,
                    IconButton(
                        icon=Icons.FILTER_ALT,
                        on_click=filtrar_cierres,
                        bgcolor=Colors.BLUE_700,
                        icon_color=Colors.WHITE,
                        height=40,
                    ),
                    IconButton(
                        icon=Icons.ALL_OUT,
                        on_click=_todos,
                        bgcolor=Colors.BLUE_700,
                        icon_color=Colors.WHITE,
                        height=40,
                    ),
                ],
                spacing=5,
                alignment=MainAxisAlignment.END,
            ),
        )

        # Crear lista de cierres
        lista_cierres = ListView(
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
                                        f" {cierre['fecha']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Container(width=10),
                                    Chip(
                                        label=Text("Ver ventas"),
                                        bgcolor=Colors.BLUE_100,
                                        on_click=lambda e, c=cierre: self.mostrar_ventas(
                                            page, c
                                        ),
                                        autofocus=False,
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
                                                "Efectivo",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['efectivo']}",
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
                                                "Transferencias",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"${cierre['transferencia']}",
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
                                                "Gastos", size=12, color=Colors.GREY_600
                                            ),
                                            Text(
                                                f"${cierre['gastos']}",
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
                                                "Total", size=12, color=Colors.GREY_600
                                            ),
                                            Text(
                                                f"${cierre['importe']}",
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
                for cierre in cierres
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
                                on_click=lambda e: page.go("/home"),
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
                                "Historial de cierres de ventas",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"Ahora las puede revizar diariamente.",
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
                controls=[filtro_container, lista_cierres],
                spacing=0,
            ),
        )

        return View(
            "/ventas/detalles",
            bgcolor=Colors.INDIGO,
            padding=0,
            controls=[
                header,
                content_area,
            ],
        )

    def mostrar_ventas(self, cierre):
        # Crear diálogo para mostrar ventas
        dialog = AlertDialog(
            title=Text(f"Ventas del {cierre['fecha']}"),
            content=Column(
                controls=[
                    Text(f"Efectivo: ${cierre['efectivo']}"),
                    Text(f"Transferencias: ${cierre['transferencia']}"),
                    Text(f"Gastos: ${cierre['gastos']}"),
                    Text(
                        f"Total: ${cierre['importe']}",
                        weight=FontWeight.BOLD,
                        color=Colors.GREEN_700,
                    ),
                ],
                spacing=10,
            ),
            actions=[TextButton("Cerrar", on_click=lambda e: self.cerrar_dialogo())],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def cerrar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def mostrar_ventas(self, page, cierre):
        # Navegar a vista de detalle de ventas para este cierre
        page.go(f"/ventas/detalle/{cierre['fecha']}")
