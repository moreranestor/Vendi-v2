from datetime import datetime
from flet import *
from route import params, Basket
from model.EntSalVenModel import EntSalVenModel


class IPV:
    def __init__(self):
        self.selected_index = 0
        self.main_content = Column(expand=True)
        self.expand = True
        self.dialog = None  # Referencia al diálogo

    def view(self, page: Page, params: params, basket: Basket):
        self.page = page  # Guardar referencia a la página
        ESVModel = EntSalVenModel()
     

        movimietos = ESVModel.getVentasIpvFecha()

        # Controles de filtrado por fecha
        busqueda = TextField(
            label="Buscar",
            hint_text="Nombre o código",
            width=200,
            border_radius=10,
            content_padding=10,
            height=30,
            on_change=lambda e: filtrar_moviminetos(e),
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

        def filtrar_moviminetos(e):
            # Ejecutar en hilo separado
            ESVModel = EntSalVenModel()

            # Validar campos
            if not busqueda.value or not busqueda.value:
                # _mostrar_alerta("Error", "Debe ingresar ambas fechas.", True)
                moviminetos_filtrados = ESVModel.getVentasIpvFecha()

            # Filtrar moviminetos
            try:
                moviminetos_filtrados = [
                    movimiento
                    for movimiento in movimietos
                    if busqueda.value in movimiento["codigo"]
                ]
                if len(moviminetos_filtrados) == 0:
                    moviminetos_filtrados = [
                        movimiento
                        for movimiento in movimietos
                        if busqueda.value in movimiento["nombre"]
                    ]
                    
               
                # Actualizar lista
                lista_moviminetos.controls.clear()

                lista_moviminetos.controls = [
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
                                    Text(
                                        f" {mov['codigo']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Text(
                                        f" {mov['nombre']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Container(width=1),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Divider(height=1),
                            Row(
                                controls=[
                                    Column(
                                        controls=[
                                            Text(
                                                "Inicio",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{format(mov['stock_inicial'], ".2f")}",
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
                                                "Entradas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['entradas']}",
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
                                                "salidas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['salidas']}",
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
                                                "Ventas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['ventas']}",
                                                color=Colors.GREEN_700,
                                                weight=FontWeight.BOLD,
                                                size=14,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Final",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{format(mov['stock_actual'], ".2f")}",
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
                    for mov in moviminetos_filtrados
                ]  if moviminetos_filtrados else [
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
                                        Text(
                                            f"No productos con esos parametros",
                                            weight=FontWeight.BOLD,
                                            size=14,
                                            color=Colors.BLUE_900,
                                        ),                                       
                                        Container(width=1),
                                       ],
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                Divider(height=1),
                               
                                 
                                
                            ],
                            spacing=5,
                        ),
                    )
                ]           
                

                ESVModel.exitConexion()
                lista_moviminetos.update()
                page.update()

            except Exception as ex:
                _mostrar_alerta(
                    "Error", f"Ocurrió un error al filtrar: {str(ex)}", True
                )

        filtro_container = Container(
            padding=10,
            bgcolor=Colors.GREY_100,
            border_radius=10,
            content=Row(
                controls=[
                    Container(width=10),
                    busqueda,
                ],
                vertical_alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=float("inf"),
        )

        # Crear lista de moviminetos
        lista_moviminetos = ListView(
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
                                    Text(
                                        f" {mov['codigo']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Text(
                                        f" {mov['nombre']}",
                                        weight=FontWeight.BOLD,
                                        size=14,
                                        color=Colors.BLUE_900,
                                    ),
                                    Container(width=1),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Divider(height=1),
                            Row(
                                controls=[
                                    Column(
                                        controls=[
                                            Text(
                                                "Inicio",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{format(mov['stock_inicial'], ".2f")}",
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
                                                "Entradas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['entradas']}",
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
                                                "salidas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['salidas']}",
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
                                                "Ventas",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{mov['ventas']}",
                                                color=Colors.GREEN_700,
                                                weight=FontWeight.BOLD,
                                                size=14,
                                            ),
                                        ],
                                        expand=1,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        controls=[
                                            Text(
                                                "Final",
                                                size=12,
                                                color=Colors.GREY_600,
                                            ),
                                            Text(
                                                f"{format(mov['stock_actual'], ".2f")}",
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
                for mov in movimietos
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
                                "Ipv de almacén.",
                                size=12,
                                color=Colors.WHITE60,
                            ),
                            Text(
                                f"La revición es control y amistad.",
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
                controls=[filtro_container, lista_moviminetos if len(movimietos)> 0 else Container(
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
                                        Text(
                                            f"No productos con esos parametros",
                                            weight=FontWeight.BOLD,
                                            size=14,
                                            color=Colors.BLUE_900,
                                        ),                                       
                                        Container(width=1),
                                       ],
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                Divider(height=1),
                               
                                 
                                
                            ],
                            spacing=5,
                        ),
                    )],
                spacing=0,
            ),
        )

        return View(
            "/ipv",
            bgcolor=Colors.INDIGO,
            padding=0,
            controls=[
                header,
                content_area,
            ],
        )

    def mostrar_Mov(self, mov):
        # Crear diálogo para mostrar ESVModel
        dialog = AlertDialog(
            title=Text(f"Movimientos del {mov['fecha']}"),
            content=Column(
                controls=[
                    Text(f"Entradas: ${mov['entradas']}"),
                    Text(f"Salidas: ${mov['salidas']}"),
                    Text(f"Ventas: ${mov['ventas']}"),
                    Text(
                        f"Existencias: ${mov['entradas']-mov['salidas']-mov['ventas']}",
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

    def cerrar_dialogo(self, dialogo):
        self.page.close(dialogo)
        self.page.update()

    def mostrar_e(self, page, mov):
        # Navegar a vista de detalle de ESVModel para este mov
        print()
        page.go(f"/mov/detalle/e/{mov['id_prod']}")

    def mostrar_s(self, page, mov):
        # Navegar a vista de detalle de ESVModel para este mov
        page.go(f"/mov/detalle/s/{mov['id_prod']}")

    def mostrar_v(self, page, mov):
        # Navegar a vista de detalle de ESVModel para este mov
        page.go(f"/mov/detalle/v/{mov['id_prod']}")
