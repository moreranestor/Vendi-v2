from datetime import date, datetime, time

from typing import Dict, List
from flet import (
    Page,
    Container,
    Column,
    Row,
    Text,
    ListView,
    IconButton,
    AlertDialog,
    Tabs,
    Tab,
    padding,
    border_radius,
    Colors,
    Icon,
    ListTile,
    FontWeight,
    MainAxisAlignment,
    CrossAxisAlignment,
    KeyboardType,
    ScrollMode,
)
from utils.hash_password import generar_codigo_unico
from utils.validationes import Validaciones as Validaciones
from controls.inputs import *
from model.ProductoModel import ProductoModel
from model.VentasModel import VentasModel
from model.NotasModel import NotasModel
from model.EntSalVenModel import EntSalVenModel
from model.cierreModel import CierreModel
import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SellScreen(Container):
    """
     Pantalla de ventas que muestra productos disponibles y registra nuevas ventas.

     Attributes:
         page (Page): Referencia a la página principal de Flet.
         productos (List[Dict]): Lista de productos disponibles.
         precios (List[Dict]): Lista de ventas registradas.
         importe_total (float): Total acumulado de ventas.

    Permite:
     - Visualizar productos en stock
     - Registrar ventas
     - Cancelar ventas
     - Realizar cierre de caja diario
    """

    def __init__(self, page: Page):
        super().__init__()
        self.id = 0
        self.expand = True
        self.page = page
        self.bgcolor = Colors.INDIGO

        # Inicialización de atributos
        self.header = None
        self.content_area = None
        self.icon_buscar = None
        self.dlg_vender = None
        self.navTabIndex = 0
        self.codigo_unico = ""
        self.select_estado = 0
        self.importe_total = 0
        self.productos: List[Dict] = []
        self.ventas: List[Dict] = []
        self.notas: List[Dict] = []
        # iniciar referencias
        self.importe_total_ref = Ref[Text]()
        self.tab_ventas_ref = Ref[Tab]()
        self.tab_disponibilidad_ref = Ref[Tab]()

        # variables para los formularios  venta

        self.codigo = TextInput(label="Código")
        self.nombre = TextInput(label="Nombre")
        self.precio = TextInput(
            label="Precio venta", valor=format(0, ".2f"), keyboard=KeyboardType.NUMBER
        )
        self.cantidad = TextInput(
            label="Cantidad", valor=format(0, ".0f"), keyboard=KeyboardType.NUMBER
        )

        # variables del formulario de cierre

        self.fecha = TextInput(label="Fecha")
        self.trabajador = TextInput(label="Trabajador")
        self.importe = TextInput(
            label="Importe de venta",
            valor=format(0, ".2f"),
            keyboard=KeyboardType.NUMBER,
        )
        self.gastos = TextInput(
            label="Gastos", valor=format(0, ".0f"), keyboard=KeyboardType.NUMBER
        )
        self.transferencia = TextInput(
            label="Transferencias", valor=format(0, ".0f"), keyboard=KeyboardType.NUMBER
        )
        self.efectivo = TextInput(
            label="Efectivo", valor=format(0, ".0f"), keyboard=KeyboardType.NUMBER
        )

        self.detalles = TextInput(label="Detalles")
        self.deuda = TextInput(
            label="deudas", valor=format(0, ".0f"), keyboard=KeyboardType.NUMBER
        )
        self.Cantidad_notas = TextInput(
            label="Cantidad de productos", valor="0", keyboard=KeyboardType.NUMBER
        )

        # variables del componentes barra de accion
        self.buscar = TextInputSearch(
            label="Buscar", width=150, change=lambda e: self.filtrar_por_busqueda(e)
        )
        self.buscar.visible = True
        self.buscar.expand = (True,)
        self.botonCierre = Container(
            content=TextButton(
                "Cerrar venta", on_click=lambda e: self._cierre_venta(e), width=300
            ),
            visible=False,
            expand=True,
        )
        self.limpiar = Container(
            content=TextButton(
                "Vaciar lista",
                on_click=lambda e: self._vaciar_lista_venta(e),
                style=ButtonStyle(
                    color=Colors.WHITE,
                    bgcolor=Colors.RED,
                ),
            ),
            visible=False,
            expand=True,
        )

        self.addNota = Container(
            content=TextButton(
                "Adicionar",
                on_click=lambda e: self._addNota(e),
               
            ),
            visible=False,
            expand=True,
        )

        self._componentes()
        # recargas dde la ventana
        self.actualizar_productos()
        self.actualizar_ventas()
        self.actualizar_notas()
        self._build_ui()

        self.page.update()

    def _componentes(self):
        # Crear los controles primero
        # componentes de la ventana
        self.accionesBar = Container(
            padding=padding.only(top=1, bottom=1, left=20, right=20),
            content=Row(
                controls=[
                    Container(expand=True),
                    self.buscar,
                    self.limpiar,
                    self.botonCierre,
                    self.addNota,
                ],
                vertical_alignment=MainAxisAlignment.END,
                width=float("inf"),
            ),
            visible=True,
        )
        self.product_list_view = ListView(expand=True, spacing=5, auto_scroll=True)
        self.product_list_ventas_view = ListView(
            expand=True, spacing=5, auto_scroll=True
        )
        self.notas_list_ventas_view = ListView(expand=True, spacing=5, auto_scroll=True)

    def _build_ui(self):
        # Crear los controles primero

        self.header = Container(
            height=70,
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
                                        "Balance de venta.",
                                        size=12,
                                        color=Colors.WHITE60,
                                    ),
                                    Text(
                                        f"$ {self.importe_total}",
                                        size=22,
                                        color=Colors.WHITE,
                                        weight=FontWeight.BOLD,
                                        ref=self.importe_total_ref,
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
                ]
            ),
        )

        self.content_area = Container(
            expand=True,
            bgcolor=Colors.GREY_100,
            width=float("inf"),
            border_radius=border_radius.only(top_left=10, top_right=10),
            padding=padding.only(top=5, left=10, right=10, bottom=0),
            content=Column(
                controls=[
                    Tabs(
                        selected_index=0,
                        expand=True,
                        tabs=[
                            Tab(
                                "Disponibles en tienda",
                                content=(
                                    self.product_list_view
                                    if len(self.productos) > 0
                                    else self._construir_estado_vacio_productos()
                                ),
                                ref=self.tab_disponibilidad_ref,
                            ),
                            Tab(
                                f"Ventas del dia: {len(self.ventas)}",
                                content=(
                                    self.product_list_ventas_view
                                    if len(self.ventas) > 0
                                    else self._construir_estado_vacio_ventas()
                                ),
                                ref=self.tab_ventas_ref,
                            ),
                            Tab(
                                "Notas del día",
                                content=(
                                    self.notas_list_ventas_view
                                    if len(self.productos) > 0
                                    else self._construir_estado_vacio_notas()
                                ),
                                ref=self.tab_disponibilidad_ref,
                            ),
                        ],
                        on_change=lambda e,: self._toggle_accion(e),
                        padding=padding.all(8),
                    ),
                    self.accionesBar,
                ],
            ),
        )

        self.content = Column(
            controls=[
                self.header,
                self.content_area,
            ],
            spacing=0,
        )

        # dialogos

        self.dlg_vender = AlertDialog(
            modal=True,
            bgcolor=Colors.WHITE,
            title=Column(
                controls=[
                    Text(
                        "Vender",
                        color=Colors.INDIGO,
                        weight=FontWeight.BOLD,
                        size=14,
                    ),
                    Text(
                        "producto",
                        color=Colors.INDIGO_500,
                        weight=FontWeight.W_500,
                        size=12,
                    ),
                ]
            ),
            content=Column(
                controls=[
                    Container(
                        self.codigo,
                        padding=1,
                    ),
                    Container(
                        self.nombre,
                        padding=0,
                    ),
                    Container(
                        self.precio,
                        padding=1,
                    ),
                    Container(
                        self.cantidad,
                        padding=1,
                    ),
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Vender", on_click=lambda e: self._procesar_venta(e)),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_vender),
                    style=ButtonStyle(
                        color=Colors.WHITE,
                        bgcolor=Colors.RED,
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.dlg_modal_cierre = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Previsualizar datos", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    Container(
                        self.fecha,
                        padding=1,
                    ),
                    Container(
                        self.trabajador,
                        padding=0,
                    ),
                    Container(
                        self.gastos,
                        padding=1,
                    ),
                    Container(
                        self.transferencia,
                        padding=1,
                    ),
                    Container(
                        self.efectivo,
                        padding=1,
                    ),
                    Container(
                        self.importe,
                        padding=1,
                    ),
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Cerrar día", on_click=lambda e: self._procesar_cierre(e)),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_modal_cierre),
                    style=ButtonStyle(
                        color=Colors.WHITE,
                        bgcolor=Colors.RED,
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.dlg_notas = AlertDialog(
            modal=True,
            bgcolor=Colors.WHITE,
            title=Column(
                controls=[
                    Text(
                        "Adicionar ",
                        color=Colors.INDIGO,
                        weight=FontWeight.BOLD,
                        size=14,
                    ),
                    Text(
                        "Nueva Nota",
                        color=Colors.INDIGO_500,
                        weight=FontWeight.W_500,
                        size=12,
                    ),
                ]
            ),
            content=Column(
                controls=[
                    Container(
                        self.detalles,
                        padding=1,
                    ),
                    Container(
                        self.deuda,
                        padding=0,
                    ),
                    Container(
                        self.Cantidad_notas,
                        padding=1,
                    ),
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Adicionar", on_click=lambda e: self._procesar_nota(e)),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_notas),
                    style=ButtonStyle(
                        color=Colors.WHITE,
                        bgcolor=Colors.RED,
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def _build_product_list(self, productos):
        """Construye la lista de productos"""
        if not hasattr(self, "product_list_view"):
            self.product_list_view = ListView(expand=True, spacing=2, auto_scroll=True)

        self.product_list_view.controls.clear()
        # Filtrar productos con existencia > 0 antes del bucle
        productos_disponibles = [p for p in productos if p["existencias"] > 0]
        self.productos = productos_disponibles
        for producto in productos_disponibles:
            self.product_list_view.controls.append(
                Container(
                    border_radius=border_radius.all(5),
                    bgcolor=Colors.WHITE,
                    content=ListTile(
                        leading=Text(
                            f"{format(producto['existencias'], ".2f") }",                            
                            color=Colors.GREEN_500,
                            size=16,
                        ),
                        title=Row(
                            controls=[
                                Container(
                                    content=Text(f"{producto['nombre']} "),
                                    expand=True,
                                ),
                                Container(
                                    content=Text(
                                        f"${format(producto['precio'], '.2f')}",
                                        color=Colors.RED_500,
                                        size=12,
                                    ),
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                        ),
                        trailing=IconButton(
                            icon=Icons.MONETIZATION_ON,
                            tooltip="Vender",
                            bgcolor=Colors.YELLOW_500,
                            width=20,
                            height=20,
                            icon_size=18,
                            on_click=lambda e, p=producto: self.realizar_venta(p),
                        ),
                    ),
                    padding=padding.all(0),
                    margin=margin.only(top=5),
                )
            )

    def _build_venta_list(self, ventas):
        """Construye la lista de productos"""
        if not hasattr(self, "product_list_ventas_view"):
            self.product_list_ventas_view = ListView(
                expand=True, spacing=1, auto_scroll=True
            )
        self.product_list_ventas_view.controls.clear()
        for venta in ventas:
            self.product_list_ventas_view.controls.append(
                Container(
                    border_radius=border_radius.all(5),
                    bgcolor=Colors.WHITE,
                    content=ListTile(
                        leading=Column(
                            controls=[
                                Text(
                                    f"Cantidad",
                                    color=Colors.GREEN_500,
                                    size=12,
                                    weight=FontWeight.BOLD,
                                ),
                                Text(
                                    f"{venta['cantidad']}",
                                    color=Colors.GREEN_500,
                                    size=12,
                                    weight=FontWeight.BOLD,
                                ),
                            ],
                            spacing=2,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        title=Row(
                            controls=[
                                Container(
                                    content=Text(f"{venta['nombre']} "),
                                    expand=True,
                                ),
                                Container(
                                    content=Text(
                                        f"${venta['importe']}",
                                        color=Colors.GREEN_500,
                                        size=12,
                                    ),
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                        ),
                        subtitle=Text(
                            f"${venta['precio']}",
                            color=Colors.RED_500,
                            size=12,
                        ),
                        trailing=IconButton(
                            icon=Icons.CANCEL,
                            tooltip="Cancelar",
                            bgcolor=Colors.GREY_300,
                            width=20,
                            height=20,
                            icon_size=18,
                            on_click=lambda e, p=venta: self._cancelar_venta(e, p),
                        ),
                    ),
                    padding=padding.all(0),
                    margin=margin.only(top=5),
                )
            )
            # Actualizar la vista si ya existe

    def _build_notas_list(self, notas):
        """Construye la lista de notas"""
        if not hasattr(self, "_build_notas_list"):
            self.notas_list_ventas_view = ListView(
                expand=True, spacing=2, auto_scroll=True
            )

        self.notas_list_ventas_view.controls.clear()
        # Filtrar productos con existencia > 0 antes del bucle
        notas_disponibles = [p for p in notas]
        self.notas = notas_disponibles
        for notas in notas_disponibles:
            self.notas_list_ventas_view.controls.append(
                Container(
                    border_radius=border_radius.all(5),
                    bgcolor=Colors.WHITE,
                    content=ListTile(
                        subtitle=Text(f"{notas['cantidad']} "),
                        title=Row(
                            controls=[
                                Container(
                                    content=Text(f"{notas['detalles']} "),
                                    expand=True,
                                ),
                                Container(
                                    content=Text(
                                        f"${format(notas['deuda'], '.2f')}",
                                        color=Colors.RED_500,
                                        size=12,
                                    ),
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                        ),
                        trailing=(
                            IconButton(
                                icon=Icons.CHECK_CIRCLE,
                                tooltip="Pagar",
                                bgcolor=Colors.YELLOW_500,
                                width=20,
                                height=20,
                                icon_size=18,
                            )
                            if notas["pagada"] == 1
                            else IconButton(
                                icon=Icons.ERROR_OUTLINE_SHARP,
                                tooltip="Pagar",
                                bgcolor=Colors.YELLOW_500,
                                width=20,
                                height=20,
                                icon_size=18,
                                on_click=lambda e, n=notas: self._cerrarNota(e,n),
                            )
                        ),
                    ),
                    padding=padding.all(0),
                    margin=margin.only(top=5),
                )
            )

    def _construir_estado_vacio_productos(self):
        """Construye el estado vacío cuando no hay productos"""
        return Container(
            content=Column(
                controls=[
                    Text(
                        "No hay productos disponibles", color=Colors.BLUE_900, size=18
                    ),
                    Text(
                        "Para agregar nuevos productos:", color=Colors.BLUE_500, size=16
                    ),
                    Icon(Icons.INVENTORY_2_OUTLINED),
                    Text(
                        "1. Vaya a la sección de Almacén",
                        color=Colors.BLUE_500,
                        size=16,
                    ),
                    Text("2. Agregue nuevos productos", color=Colors.BLUE_500, size=16),
                    Text("3. Ingrese existencias", color=Colors.BLUE_500, size=16),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=Colors.WHITE,
            padding=padding.all(20),
            width=float("inf"),
        )

    def _construir_estado_vacio_ventas(self):
        """Muestra estado cuando no hay ventas registradas"""
        return Container(
            content=Column(
                controls=[
                    Text(
                        "No hay ventas registradas hoy", color=Colors.BLUE_900, size=18
                    ),
                    Text(
                        "Para registrar una nueva venta:",
                        color=Colors.BLUE_500,
                        size=16,
                    ),
                    Text("1. Seleccione un producto", color=Colors.BLUE_500, size=16),
                    IconButton(
                        icon=Icons.MONETIZATION_ON,
                        tooltip="Vender",
                        bgcolor=Colors.YELLOW_500,
                        width=20,
                        height=20,
                        icon_size=18,
                    ),
                    Text("2. Ingrese la cantidad", color=Colors.BLUE_500, size=16),
                    Text("3. Confirme la venta", color=Colors.BLUE_500, size=16),
                    IconButton(
                        icon=Icons.REFRESH,
                        on_click=lambda e: self.actualizar_ventas(),
                        tooltip="Actualizar",
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=Colors.WHITE,
            padding=padding.all(20),
            width=float("inf"),
        )

    def _construir_estado_vacio_notas(self):
        """Muestra estado cuando no hay ventas registradas"""
        return Container(
            content=Column(
                controls=[
                    Text(
                        "No hay notas registradas hoy", color=Colors.BLUE_900, size=18
                    ),
                    Text(
                        "Para registrar una nueva nota:", color=Colors.BLUE_500, size=16
                    ),
                    Text(
                        "1. llene los datos de la nota", color=Colors.BLUE_500, size=16
                    ),
                    TextButton(
                        "Adicionar",
                        on_click=lambda e: self._addNota(e),                        
                    ),
                    IconButton(
                        icon=Icons.REFRESH,
                        on_click=lambda e: self.actualizar_ventas(),
                        tooltip="Actualizar",
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=Colors.WHITE,
            padding=padding.all(20),
            width=float("inf"),
        )

    # ---------------------------
    # Métodos de Datos
    # ---------------------------

    def actualizar_productos(self):
        """
        Actualiza la lista de productos desde la base de datos.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """

        if not hasattr(self, "page") or self.page is None:
            logger.warning("No se puede actualizar productos: página no disponible")
            return False

        try:

            logger.info("Actualizando lista de productos...")
            _productosEntidad = ProductoModel()
            self.productos = _productosEntidad.getExistencia(0, 1)

            # Reconstruir la lista de productos
            self._build_product_list(self.productos)
            logger.debug(f"Productos obtenidos: {len(self.productos)} items")

            if hasattr(self, "content_area") and self.content_area is not None:
                # Actualizar el contenido basado en si hay productos o no
                self.content_area.content.controls[0].tabs[0].content = (
                    self.product_list_view
                    if len(self.productos) > 0
                    else self._construir_estado_vacio_productos()
                )
                self.content_area.update()

            return True

        except Exception as e:
            logger.error(f"Error al actualizar productos: {str(e)}", exc_info=True)
            # Opcional: mostrar mensaje de error al usuario
            self._mostrar_alerta(
                "Error",
                "No se pudieron cargar los productos. Consulte el registro de errores.",
                True,
            )
            return False

    def actualizar_ventas(self):
        """Actualiza la lista de productos desde la base de datos"""
        if not hasattr(self, "page") or self.page is None:
            return

        try:
            _notas = VentasModel()
            self.ventas = _notas.getVentasporFecha(date.today().strftime("%d-%m-%Y"))
            try:
                self.importe_total = sum(
                    float(v.get("importe", 0)) for v in self.ventas
                )

                if self.importe_total_ref.current:  # Verifica si la referencia existe
                    self.importe_total_ref.current.value = f"$ {self.importe_total:.2f}"
                    self.importe_total_ref.current.update()  # Fuerza la actualización

                if self.tab_ventas_ref.current:  # Verifica si la referencia existe
                    self.tab_ventas_ref.current.text = (
                        f"Ventas del dia: {len(self.ventas)}"
                    )
                    self.tab_ventas_ref.current.update()  # Fuerza la actualización

            except (TypeError, ValueError) as e:
                logger.warning("Error calculando total")
                self.importe_total = 0.0

            # Reconstruir la lista de productos
            self._build_venta_list(self.ventas)

            if hasattr(self, "self.header") and self.header is not None:
                # Actualizar el contenido basado en si hay productos o no
                self.header.update()

            if hasattr(self, "content_area") and self.content_area is not None:
                # Actualizar el contenido basado en si hay productos o no

                self.content_area.content.controls[0].tabs[1].content = (
                    self.product_list_ventas_view
                    if len(self.ventas) > 0
                    else self._construir_estado_vacio_ventas()
                )
                self.content_area.update()

        except Exception as e:
            #     # Opcional: mostrar mensaje de error al usuario
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(e)}", True
            )

    def actualizar_notas(self):
        """Actualiza la lista de productos desde la base de datos"""
        if not hasattr(self, "page") or self.page is None:
            return

        try:
            _notas = NotasModel()
            self.notas = _notas.getnotasporFecha(date.today().strftime("%d-%m-%Y"))

            # Reconstruir la lista de productos
            self._build_notas_list(self.notas)

            if hasattr(self, "self.header") and self.header is not None:
                # Actualizar el contenido basado en si hay productos o no
                self.header.update()

            if hasattr(self, "content_area") and self.content_area is not None:
                # Actualizar el contenido basado en si hay productos o no

                self.content_area.content.controls[0].tabs[2].content = (
                    self.notas_list_ventas_view
                    if len(self.notas) > 0
                    else self._construir_estado_vacio_notas()
                )
                self.content_area.update()

        except Exception as e:
            #     # Opcional: mostrar mensaje de error al usuario
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar las notas: {str(e)}", True
            )

    # ---------------------------
    # Métodos de dialogos
    # __________

    def _mostrar_dialogo(self, dialog):
        """Muestra un diálogo modal"""
        self.page.open(dialog)
        self.page.update()

    def _cerrar_dialogo(self, dialog):
        """Cierra un diálogo modal"""
        self.page.close(dialog)
        self.page.update()

    def _mostrar_alerta(self, titulo, mensaje, error=False):
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
                TextButton("OK", on_click=lambda e: self._cerrar_dialogo(alerta)),
            ],
        )
        self._mostrar_dialogo(alerta)

    # entradas

    def realizar_venta(self, producto):
        """Prepara el diálogo para registrar una venta"""
        self.id = producto["id_prod"]
        self.codigo.value = producto["codigo"]  # Asumiento que hay un campo código
        self.nombre.value = producto["nombre"]  # Asegurar asignar el nombre
        self.precio.value = str(producto["precio"])  # Convertir a string
        self.cantidad.value = "0"
        self._mostrar_dialogo(self.dlg_vender)

    def _procesar_venta(self, e):
        """
        Procesa una venta de producto con validaciones completas.

        Args:
            e: Evento de click del botón.

        Raises:
            ValueError: Si los datos de entrada no son válidos.
            Exception: Si ocurre un error al registrar la venta.
        """
        logger.info("Iniciando proceso de venta...")

        try:
            if not self._validar_campos_venta():
                return
            _producto = ProductoModel()

            # Obtener existencias actuales
            existencias = _producto.getExistenciaCodigo(self.id)

            cantidad_vender = float(self.cantidad.value)
            logger.debug(
                f"Intentando vender {cantidad_vender} unidades de producto ID {self.id}"
            )

            if existencias < cantidad_vender:
                error_msg = "Existencias_insuficientes".format(existencias)
                self.cantidad.error_text = error_msg
                self.cantidad.update()
                logger.warning(error_msg)
                return

            if cantidad_vender <= 0:
                error_msg = "Error_cantidad"
                self.cantidad.error_text = error_msg
                self.cantidad.update()
                logger.warning(error_msg)
                return

            # Registrar venta
            venta_data = self._preparar_datos_venta(cantidad_vender)
            if not self._registrar_venta(venta_data):
                raise Exception("Error al registrar venta")

            # Registrar movimiento
            movimiento_data = self._preparar_datos_mov(cantidad_vender, self.id)
            if not self._registrar_mov(movimiento_data):
                raise Exception("Error al registrar movimiento")

            self._finalizar_venta_exitosa()

        except ValueError as ve:
            logger.error(f"Error de valor: {str(ve)}", exc_info=True)
            self._mostrar_alerta("Error", str(ve), True)
        except Exception as ex:
            logger.error(f"Error inesperado: {str(ex)}", exc_info=True)
            self._mostrar_alerta(
                "Error",
                "No se pudieron cargar los productos. Consulte el registro de errores.",
                True,
            )

    def _preparar_datos_venta(self, cantidad: float) -> Dict:
        """Prepara los datos para registrar una venta."""
        self.codigo_unico = generar_codigo_unico("Vendi")
        return {
            "codigo": self.codigo_unico,
            "id_prod": self.id,
            "nombre": self.nombre.value,
            "precio": float(self.precio.value),
            "cantidad": cantidad,
            "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
        }

    def _registrar_venta(self, venta_data: Dict) -> bool:
        """Intenta registrar la venta en la base de datos."""
        try:
            _venta = VentasModel()
            return _venta.insertar(venta_data)

        except Exception as e:
            logger.error(f"Error al insertar venta: {str(e)}")
            self.codigo_unico = ""
            return False

    def _finalizar_venta_exitosa(self) -> None:
        """Realiza las acciones finales después de una venta exitosa."""
        self.codigo_unico = ""
        self._mostrar_alerta("Éxito", "venta_exitosa")
        self._limpiar_formulario_venta()
        self._cerrar_dialogo(self.dlg_vender)
        self.actualizar_ventas()
        self.actualizar_productos()
        logger.info("Venta registrada exitosamente")

    def _limpiar_formulario_venta(self) -> None:
        """Restablece el formulario de venta a sus valores iniciales."""
        self.id = 0
        for campo in [self.codigo, self.nombre, self.precio, self.cantidad]:
            campo.value = ""
            campo.error_text = None
            campo.update()
        logger.debug("Formulario de venta limpiado")

    def _cancelar_venta(self, e, venta):
        """
        Procesa una cancelacion de venta de producto con validaciones completas.

        Args:
            e: Evento de click del botón.

        Raises:
            ValueError: Si los datos de entrada no son válidos.
            Exception: Si ocurre un error al registrar la venta.
        """
        logger.info("Iniciando proceso de cancelacion venta...")

        try:
            _venta = VentasModel()
            _venta.cancelar(venta["codigo"])
            self._finalizar_cancelacion_exitosa()

        except ValueError as ve:
            logger.error(f"Error de valor: {str(ve)}", exc_info=True)
            self._mostrar_alerta("Error", str(ve), True)
        except Exception as ex:
            logger.error(f"Error inesperado: {str(ex)}", exc_info=True)
            self._mostrar_alerta(
                "Error",
                "No se pudo cancelar la venta. Consulte el registro de errores.",
                True,
            )

    def _validar_campos_venta(self) -> bool:
        """
        Valida los campos del formulario de venta.

        Returns:
            bool: True si todos los campos son válidos, False en caso contrario.
        """
        valid = True
        campos = {
            self.cantidad: "Existencias insuficientes. Disponibles: {}",
            self.precio: "La cantidad debe ser mayor que 0",
        }

        for campo, mensaje_error in campos.items():
            if not campo.value or not campo.value.strip():
                campo.error_text = mensaje_error
                valid = False
                logger.warning(f"Campo vacío: {campo.label}")

        if not Validaciones.valid_number(self.cantidad.value):
            self.cantidad.error_text = "Error número invalido"
            valid = False
            logger.warning("Cantidad no es un número válido")

        if not valid:
            self.page.update()

        return valid

    def _vaciar_lista_venta(self, e):
        """Preparendo vaciar la lista"""
        logger.info("Preparendo vaciar la lista...")

        try:
            _venta = VentasModel()
            all_venta = _venta.findByCampo(
                "fecha_alta", f"{date.today().strftime('%d-%m-%Y')}"
            )

            for venta in all_venta:
                _venta.cancelar(venta["codigo"])

            self._finalizar_cancelacion_exitosa()

        except ValueError as ve:
            logger.error(f"Error de valor: {str(ve)}", exc_info=True)
            self._mostrar_alerta("Error", str(ve), True)
        except Exception as ex:
            logger.error(f"Error inesperado: {str(ex)}", exc_info=True)
            self._mostrar_alerta(
                "Error",
                "No se pudo cancelar la venta. Consulte el registro de errores.",
                True,
            )

    def _finalizar_eliminar_exitosa(self) -> None:
        """Realiza las acciones finales después de una cancelacion exitosa."""
        self._mostrar_alerta("Éxito", "Eliminacion exitosa")
        self.actualizar_ventas()
        self.actualizar_productos()
        logger.info("Ventas limpiadas exitosamente")

    def _preparar_datos_mov(self, cantidad: float, id: int) -> Dict:
        """Prepara los datos para registrar una venta."""
        return {
            "id_prod": id,
            "estado": "V",
            "codigo": self.codigo_unico,
            "entradas": 0,
            "salidas": 0,
            "ventas": cantidad,
            "activo": 1,
            "detalles": "Venta",
            "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
        }

    def _registrar_mov(self, venta_data: Dict) -> bool:
        """Intenta registrar la venta en la base de datos."""
        try:
            _entradamov = EntSalVenModel()
            return _entradamov.insertar(venta_data)
        except Exception as e:
            logger.error(f"Error al insertar venta: {str(e)}")
            self.codigo_unico = ""
            return False

    def _finalizar_cancelacion_exitosa(self) -> None:
        """Realiza las acciones finales después de una cancelacion exitosa."""
        self._mostrar_alerta("Éxito", "Cancelación exitosa")
        self.actualizar_ventas()
        self.actualizar_productos()
        logger.info("Venta registrada exitosamente")

    # BUSQUEDAS

    def filtrar_por_busqueda(self, event):
        """Filtra productos por categoría"""
        self.actualizar_productos()
        search_term = event.control.value.lower().strip()
        lista = (
            [
                p
                for p in self.productos
                if search_term
                in p["nombre"].lower()  # Assuming each product has a 'nombre'
                or search_term in p["codigo"].lower()
            ]
            if search_term != ""
            else self.productos
        )

        if search_term == "":
            self._build_product_list(self.productos)
        else:
            self._build_product_list(lista)

        self.content_area.content.controls[0].tabs[0].content = (
            self.product_list_view
            if len(self.productos) > 0
            else self._construir_estado_vacio_productos()
        )

        self.content_area.update()
        self.page.update()

    # TOGGLES

    def _toggle_accion(self, e):
        """Alterna entre los diferentes estados de la interfaz"""
        self.select_estado = e.control.selected_index

        print(f"Estado actual: {self.select_estado}")  # Debug

        # Configurar visibilidad de controles
        self.buscar.visible = self.select_estado in [
            0,
        ]

        self.botonCierre.visible = self.select_estado in [1]
        self.limpiar.visible = self.select_estado in [1]

        self.addNota.visible = self.select_estado in [2]

        # Actualizar controles (mejor hacerlo una sola vez)
        self.accionesBar.update()

    # ERRES DE vENTA

    def _cierre_venta(self, e):
        """Prepares and shows the sales closing dialog"""
        logger.info("Preparing sales closing dialog...")

        # Set initial values for the closing dialog
        self.fecha.value = date.today().strftime("%d-%m-%Y")
        self.trabajador.value = ""  # You should replace this with actual user
        self.importe.value = f"{self.importe_total:.2f}"
        self.gastos.value = "0"
        self.transferencia.value = "0"
        self.efectivo.value = "0"

        # Show the dialog
        self._mostrar_dialogo(self.dlg_modal_cierre)

    def _procesar_cierre(self, e):
        """
        Processes the sales closing with complete validations.

        Args:
            e: Button click event.

        Raises:
            ValueError: If input data is invalid.
            Exception: If an error occurs while processing the closing.
        """
        logger.info("Starting closing process...")

        try:
            # Validate fields
            if not self._validar_campos_cierre():
                return

            # Process the closing (you'll need to implement this)
            # This is where you would save the closing data to your database

            # For example:
            closing_data = {
                "fecha": self.fecha.value,
                "trabajador": self.trabajador.value,
                "importe": float(self.importe.value),
                "gastos": float(self.gastos.value),
                "transferencia": float(self.transferencia.value),
                "efectivo": float(self.efectivo.value),
            }

            logger.debug(f"Closing data: {closing_data}")

            # Here you would call your model to save the closing

            # Example:
            # if not VentasModel().registrar_cierre(closing_data):
            #     raise Exception("Error al registrar cierre")
            cierreEntidad = CierreModel()

            verificarcierre = cierreEntidad.findByCampo("fecha", self.fecha.value)
            if len(verificarcierre) == 0:
                cierreEntidad.insertar(closing_data)
                self._mostrar_alerta(
                    "Éxito",
                    f"Cierre de ventas del día: {self.fecha.value}, fue registrado correctamente",
                )
            else:
                cierreEntidad.update(closing_data, f"fecha = '{self.fecha.value}'")
                self._mostrar_alerta(
                    "Éxito",
                    f"Cierre de ventas del día: {self.fecha.value}, ha sido actualizado correctamente",
                )

            # Reset sales for new day
            self.importe_total = 0
            self.importe_total_ref.current.value = "$ 0.00"
            self.importe_total_ref.current.update()
            self.actualizar_ventas()

        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}", exc_info=True)
            self._mostrar_alerta("Error", str(ve), True)
        except Exception as ex:
            logger.error(f"Unexpected error: {str(ex)}", exc_info=True)
            self._mostrar_alerta("Error", "Error al procesar el cierre", True)

    def _validar_campos_cierre(self) -> bool:
        """
        Validates the closing form fields.

        Returns:
            bool: True if all fields are valid, False otherwise.
        """
        valid = True
        campos = {
            self.importe: "Total de importe incorrecto",
            self.gastos: "Gastos inválidos",
            self.transferencia: "Transferencia inválida",
            self.efectivo: "Efectivo inválido",
        }

        for campo, mensaje_error in campos.items():
            if not campo.value or not Validaciones.valid_number(campo.value):
                campo.error_text = mensaje_error
                valid = False
                logger.warning(f"Invalid field: {campo.label}")

        # Additional validation - check that cash matches total
        try:
            total = float(self.importe.value)
            gastos = float(self.gastos.value)
            transferencia = float(self.transferencia.value)
            efectivo = float(self.efectivo.value)

            if abs((transferencia + efectivo + gastos) - total) > 0.01:
                self.efectivo.error_text = "La suma no coincide con el importe"
                valid = False
        except ValueError:
            pass

        if not valid:
            self.page.update()

        return valid

    def _addNota(self, e):
        """Prepares and shows the notas dialog with default values"""
        logger.info("Preparing notas dialog...")

        try:
            # Set default values
            self.detalles.value = " "  # Replace with actual user if available
            self.deuda.value = "0"
            self.Cantidad_notas.value = "0"

            # Reset any previous error states
            self._reset_field_errors()

            # Show the dialog
            self._mostrar_dialogo(self.dlg_notas)

        except Exception as ex:
            logger.error(f"Error preparing notas dialog: {ex}", exc_info=True)
            self._mostrar_alerta(
                "Error", "No se pudo preparar el diálogo de notas", True
            )

    def _procesar_nota(self, e):
        """
        Processes the nota creation with complete validations and database insertion.

        Args:
            e: Button click event.
        """
        logger.info("Starting nota processing...")

        if not self._validar_campos_nota():
            logger.warning("Validation failed, not processing nota")
            return

        try:
            # Prepare nota data
            nota_data = {
                "fecha_alta": date.today().strftime("%d-%m-%Y"),
                "detalles": self.detalles.value.strip(),
                "deuda": float(self.deuda.value),
                "cantidad": float(self.Cantidad_notas.value),
                # Add any additional fields needed by your NotasModel
            }

            logger.debug(f"Nota data to be inserted: {nota_data}")

            # Insert into database
            notas_model = NotasModel()
            inserted_id = notas_model.insertar(nota_data)

            if not inserted_id:
                raise Exception("No se recibió ID de la nota insertada")

            logger.info(f"La nota fue registrada correctamente con ID ID: {inserted_id}")

            # Show success and refresh
            self._mostrar_alerta(
                "Éxito", f"La nota fue registrada correctamente con ID: {inserted_id}"
            )

            # Close dialog and refresh data
            self._cerrar_dialogo(self.dlg_notas)
            self.actualizar_notas()

        except ValueError as ve:
            logger.error(f"Number format error: {ve}", exc_info=True)
            self._mostrar_alerta(
                "Error", "Formato numérico inválido en los campos", True
            )
        except Exception as ex:
            logger.error(f"Error processing nota: {ex}", exc_info=True)
            self._mostrar_alerta("Error", f"Error al procesar la nota: {str(ex)}", True)

    def _validar_campos_nota(self) -> bool:
        """
        Validates the nota form fields.

        Returns:
            bool: True if all fields are valid, False otherwise.
        """
        valid = True
        self._reset_field_errors()

        # Validate required fields
        if not self.detalles.value or not self.detalles.value.strip():
            self.detalles.error_text = "Detalle es requerido"
            valid = False

        # Validate numeric fields
        numeric_fields = {self.deuda: "Deuda", self.cantidad: "Cantidad"}

        for field, field_name in numeric_fields.items():
            if not field.value:
                field.error_text = f"{field_name} es requerido"
                valid = False
            elif not Validaciones.valid_number(field.value):
                field.error_text = f"{field_name} debe ser numérico"
                valid = False
            elif float(field.value) < 0:
                field.error_text = f"{field_name} no puede ser negativo"
                valid = False

        # Additional business logic validation if needed
        # For example, check if cantidad >= deuda if that's a requirement

        if not valid:
            self.page.update()
            logger.warning("Nota validation failed")

        return valid

    def _reset_field_errors(self):
        """Resets all error states in the nota form fields"""
        fields = [self.detalles, self.deuda, self.cantidad]
        for field in fields:
            field.error_text = None

    def _cerrarNota(self, e, nota):
        """
            Processes the nota edicion with complete validations and database insertion.

            Args:
                e: Button click event.
            """
        logger.info("Starting nota processing...")

        try:
            # Prepare nota data
            nota_data = {
                "pagada": 1,              
                # Add any additional fields needed by your NotasModel
            }

            logger.debug(f"Nota data to be editada: {nota_data}")

            # Insert into database
            notas_model = NotasModel()
            notas_model.update(nota_data, f"id_notas={nota['id_notas']}" )

            logger.info(f"Nota editada successfully with ID: {nota['id_notas']}")

            # Show success and refresh
            self._mostrar_alerta(
                "Éxito", f"La nota fue registrada correctamente con ID: {nota['id_notas']}"
            )
           # Close dialog and refresh data    
            self.actualizar_notas()

        except ValueError as ve:
            logger.error(f"Number format error: {ve}", exc_info=True)
            self._mostrar_alerta(
                "Error", "Formato numérico inválido en los campos", True
            )
        except Exception as ex:
            logger.error(f"Error processing nota: {ex}", exc_info=True)
            self._mostrar_alerta("Error", f"Error al procesar la nota: {str(ex)}", True)    
        
