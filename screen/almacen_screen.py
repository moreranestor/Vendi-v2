from datetime import date, datetime, time
import hashlib
from flet import *
from model.ProductoModel import ProductoModel
from model.EntSalVenModel import EntSalVenModel
from controls.buscar import Buscar
from utils.hash_password import generar_codigo_unico
from utils.constantes import CATEGORIAS, UNIDADES
from utils.validationes import Validaciones as Validaciones
from controls.inputs import *



class StorageScreen(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.expand = True
        self.page = page
        self.bgcolor = Colors.INDIGO

        self.product_id = 0

        self.buscar_estado = 0
        self.papelera_estado = 1

        self.texto_productos = None
        self.texto_buscando = None
        self.header = None

        self.content_area = None
        self.icon_buscar = None
        self.icon_buscar_cerrar = None

        # variables de ventanas modales
        self.dlg_modal = None
        self.dlg_modal_editar = None
        self.dlg_modal_entradas = None
        self.dlg_modal_salidas = None

        # unidades
        self.unidades = UNIDADES
        # categorias
        self.categorias = CATEGORIAS

        self.index_categoria = 0

        # variables para los formularios
        self.codigo = TextInput(label="Código")
        self.nombre = TextInput(label="Nombre")
        self.compra = TextInput(
            label="Precio de compra",
            valor=format(0, ".2f"),
            keyboard=KeyboardType.NUMBER,
        )
        self.venta = TextInput(
            label="Precio de venta",
            valor=format(0, ".2f"),
            keyboard=KeyboardType.NUMBER,
        )
        self.categoria = Dropdown(
            label="Categorías",
            hint_text="Seleccione su categoría",
            options=[dropdown.Option(x) for x in self.categorias if x != "Todos"],
            autofocus=True,
            expand=True,
        )
        self.unidad = Dropdown(
            label="Unidad de medida",
            hint_text="Seleccione su unidad de medidad",
            options=[dropdown.Option(x) for x in self.unidades],
            autofocus=True,
            expand=True,
        )
        self.moneda = Dropdown(
            label="Moneda",
            hint_text="Seleccione tipo de moneda",
            options=[dropdown.Option(x) for x in ["CUP", "USD", "MLC"]],
            autofocus=True,
            expand=True,
        )
        self.activo = Switch(
            label="Activar producto", label_position=LabelPosition.RIGHT, value=True
        )
        self.entrada = TextInput(
            label="Cantidad de productos",
            valor=format(0, ".0f"),
            keyboard=KeyboardType.NUMBER,
        )
        self.salida = TextInput(
            label="Cantidad de productos",
            valor=format(0, ".0f"),
            keyboard=KeyboardType.NUMBER,
        )
        self.detalles = TextInput(label="Detalles")

        # Lista de productos
        self.productos = []
        self.product_list_view = ListView(expand=True, spacing=5, auto_scroll=True)

        # acutualizar
        self.actualizar_productos()
        # Inicializar UI
        self._build_ui()

    # self.page.update()

    def _build_ui(self):
        # Crear los widget primero
        # Header
        self.texto_productos = Container(
            content=Text(
                (
                    f"{len(self.productos)} Producto"
                    if len(self.productos) == 1
                    else f"{len(self.productos)} Productos"
                ),
                size=16,
                color=Colors.BLUE_900,
                weight=FontWeight.BOLD,
            ),
            padding=padding.only(left=10),
            expand=True,
            visible=True,
        )
        self.texto_buscando = Container(
            content=TextInputSearch("Buscando...", change=self.filtrar_por_busqueda),
           
            padding=padding.only(left=10),
            expand=True,
            visible=False,
        )

        self.icon_buscar = IconButton(
            icon=Icons.SEARCH,
            visible=True,
            on_click=self._toggle_busqueda,
            tooltip="Buscar",
        )
        self.icon_buscar_cerrar = IconButton(
            icon=Icons.SEARCH_OFF,
            visible=False,
            on_click=self._toggle_busqueda,
            tooltip="Cancelar",
        )

        self.icon_papelera = IconButton(
            icon=Icons.DELETE_SWEEP,
            visible=True,
            on_click=self._toggle_busqueda_papelera,
            tooltip="Ver papelera",
        )
        self.icon_papelera_cerrar = IconButton(
            icon=Icons.DELETE,
            icon_color=Colors.RED_500,
            visible=False,
            on_click=self._toggle_busqueda_papelera,
            tooltip="Cerrar papelera",
        )

        # construir header
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
                                        "Administre su almacén más fácil que nunca.",
                                        size=12,
                                        color=Colors.WHITE60,
                                    ),
                                    Text(
                                        f"Con Vendi todo es mas rápido",
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
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                ]
            ),
        )

       

        # Construir la lista de productos
        self._build_product_list(self.productos)

        self.content_area = Container(
            expand=True,
            bgcolor=Colors.GREY_100,
            width=float("inf"),
            border_radius=border_radius.only(top_left=10, top_right=10),
            content=Column(
                width=float("inf"),
                spacing=2,
                controls=[
                    # Header con botones
                    Row(
                        controls=[
                            self.texto_productos,
                            self.texto_buscando,
                            self.icon_buscar,
                            self.icon_buscar_cerrar,
                            IconButton(
                                icon=Icons.ADD,
                                on_click=lambda _: self.page.open(self.dlg_modal),
                                tooltip="Adicionar",
                            ),
                            # IconButton(
                            #     icon=Icons.UPDATE,
                            #     on_click=lambda _: self.actualizar_productos(),
                            #     tooltip="Actualizar"
                            # ),
                            self.icon_papelera,
                            self.icon_papelera_cerrar,
                        ],
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    # Categorías
                    Container(
                        height=70,
                        padding=padding.symmetric(horizontal=10),
                        content=Row(
                            scroll=ScrollMode.AUTO,
                            controls=[
                                OutlinedButton(
                                    text=f"{cat}",
                                    on_click=lambda e, cat=cat: self.filtrar_por_categoria(
                                        cat
                                    ),
                                    style=ButtonStyle(
                                        shape=StadiumBorder(),
                                    ),
                                )
                                for cat in self.categorias
                            ],
                            spacing=2,
                        ),
                    ),
                    # Lista de productos
                    Container(
                        padding=padding.symmetric(vertical=8, horizontal=8),
                        expand=True,
                        content=(
                            self.product_list_view
                            if len(self.productos) > 0
                            else self._build_empty_state()
                        ),
                    ),
                ],
            ),
            padding=padding.only(top=10, left=10, right=10, bottom=0),
        )

        self.content = Column(
            controls=[
                self.header,
                self.content_area,
            ],
            spacing=0,
        )

        # Diálogos modales
        self._build_dialogs()

    def _build_product_list(self, productos):
        """Construye la lista de productos"""
        if not hasattr(self, "product_list_view"):
            self.product_list_view = ListView(expand=True, spacing=5, auto_scroll=True)

        self.product_list_view.controls.clear()

        for producto in productos:
            self.product_list_view.controls.append(
                Container(
                    border_radius=border_radius.all(5),
                    bgcolor=Colors.WHITE,
                    content=ListTile(
                        leading=GestureDetector(
                            content=Container(
                                content=Text(
                                    f"{format(producto['existencias'], ".2f")}",
                                    color=Colors.WHITE,
                                    size=14,
                                ),
                                width=50,
                                height=25,
                                border_radius=border_radius.all(20),
                                bgcolor=self._get_color_existencias(
                                    producto["existencias"]
                                ),
                                alignment=alignment.center,
                            ),
                            on_double_tap=lambda e, p=producto: print(
                                f"Producto: {p['nombre']}"
                            ),
                        ),
                        title=Row(
                            controls=[
                                Container(
                                    content=Text(f"{producto['nombre']}"),
                                    expand=True,
                                ),
                                Container(
                                    content=Text(
                                        f"$ {format(producto['precio'], ".2f")}",
                                        color=Colors.GREEN_500,
                                        size=12,
                                    ),
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=CrossAxisAlignment.CENTER,
                        ),
                        subtitle=Row(
                            controls=[
                                Container(
                                    content=Text(
                                        f"Compra: ${format(producto['precio'], ".2f")}"
                                    ),
                                    expand=True,
                                ),
                                Container(
                                    content=Text(
                                        f"30% - ${format(self._calcular_porcentaje(producto['compra']), ".2f")}",
                                        color=Colors.RED_500,
                                    ),
                                ),
                            ],
                            spacing=20,
                        ),
                        trailing=PopupMenuButton(
                            tooltip="Opciones",
                            icon=Icon(Icons.MORE_VERT, color=Colors.RED_500),
                            items=[
                                PopupMenuItem(text=f"{producto['nombre']}"),
                                PopupMenuItem(
                                    text="Visualizar",
                                    on_click=lambda e, p=producto: self.mostrar_producto(
                                        p
                                    ),
                                    icon=Icons.PREVIEW,
                                ),
                                PopupMenuItem(
                                    text="Entrada",
                                    on_click=lambda e, p=producto: self.entrar_producto(
                                        p
                                    ),
                                    icon=Icons.ARROW_CIRCLE_DOWN_OUTLINED,
                                    disabled=(producto["activo"] == 0),
                                ),
                                PopupMenuItem(
                                    text="Salida",
                                    on_click=lambda e, p=producto: self.sacar_producto(
                                        p
                                    ),
                                    icon=Icons.ARROW_CIRCLE_UP_OUTLINED,
                                    disabled=(
                                        producto["existencias"] <= 0
                                        or producto["activo"] == 0
                                    ),
                                ),
                                PopupMenuItem(
                                    text="Editar",
                                    on_click=lambda e, p=producto: self.editar_producto(
                                        p
                                    ),
                                    icon=Icons.EDIT,
                                    disabled=(producto["activo"] == 0),
                                ),
                                PopupMenuItem(
                                    text="Eliminar",
                                    on_click=lambda e, p=producto: self.eliminar_producto(
                                        e, p
                                    ),
                                    icon=Icons.DELETE,
                                    disabled=(producto["activo"] == 0),
                                ),
                                PopupMenuItem(
                                    text="RECUPERAR",
                                    on_click=lambda e, p=producto: self.restaurar_producto(
                                        e, p
                                    ),
                                    icon=Icons.DELETE_SWEEP,
                                    disabled=(producto["activo"] == 1),
                                ),
                            ],
                        ),
                    ),
                    padding=padding.all(0),
                )
            )

    def _build_empty_state(self):
        """Construye el estado vacío cuando no hay productos"""
        return Container(
            content=Column(
                controls=[
                    Text("Tienda sin productos.", color=Colors.BLUE_900, size=18),
                    Text(
                        "Para crear un nuevo producto,", color=Colors.BLUE_500, size=16
                    ),
                    Text("seleccione el botón", color=Colors.BLUE_500, size=16),
                    Icon(Icons.ADD),
                    Text("en la barra superior.", color=Colors.BLUE_500, size=16),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=Colors.WHITE,
            padding=padding.all(20),
            width=float("inf"),
        )

    def _build_dialogs(self):
        """Construye todos los diálogos modales"""
        self.dlg_modal_mostrar = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Previsualizar producto", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    self.codigo,
                    self.nombre,
                    self.categoria,
                    self.moneda,
                    self.unidad,
                    self.compra,
                    self.venta,
                    self.activo,
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_modal_mostrar),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        # Diálogo para agregar producto
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Nuevo producto", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    self.codigo,
                    self.nombre,
                    self.categoria,
                    self.moneda,
                    self.unidad,
                    self.compra,
                    self.venta,
                    self.activo,
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Aceptar", on_click=self.crear_producto),
                TextButton(
                    "Cerrar", on_click=lambda e: self._cerrar_dialogo(self.dlg_modal)
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        # Diálogo para editar producto
        self.dlg_modal_editar = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Editar producto", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    self.nombre,
                    self.categoria,
                    self.moneda,
                    self.unidad,
                    self.compra,
                    self.venta,
                    self.activo,
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Guardar", on_click=self._editar_producto),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_modal_editar),
                ),
            ],
        )

        # Diálogo para entradas
        self.dlg_modal_entradas = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Entradas producto", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    self.codigo,
                    self.nombre,
                    self.entrada,
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Aceptar", on_click=self._procesar_entrada),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_modal_entradas),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        # Diálogo para salidas
        self.dlg_modal_salidas = AlertDialog(
            modal=True,
            title=Column(
                controls=[
                    Text("Vendi", color=Colors.INDIGO, weight=FontWeight.BOLD, size=18),
                    Text("Salidas de producto", color=Colors.INDIGO_500, size=15),
                ],
                spacing=0,
            ),
            content=Column(
                controls=[
                    self.codigo,
                    self.nombre,
                    self.detalles,
                    self.salida,
                ],
                scroll=ScrollMode.AUTO,
            ),
            actions=[
                TextButton("Aceptar", on_click=self._procesar_salida),
                TextButton(
                    "Cerrar",
                    on_click=lambda e: self._cerrar_dialogo(self.dlg_modal_salidas),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def _toggle_busqueda(self, e):
        """Alterna entre el modo de búsqueda y normal"""
        self.buscar_estado = 1 if self.buscar_estado == 0 else 0
        self.texto_productos.visible = self.buscar_estado == 0
        self.texto_buscando.visible = self.buscar_estado == 1
        self.icon_buscar.visible = self.buscar_estado == 0
        self.icon_buscar_cerrar.visible = self.buscar_estado == 1
        if self.buscar_estado == 0:
            self.texto_buscando.content.value = ""
            self.actualizar_productos()
        self.update()

    def _toggle_busqueda_papelera(self, e):
        """Alterna entre el modo de búsqueda y normal"""
        self.papelera_estado = 1 if self.papelera_estado == 0 else 0
        self.icon_papelera.visible = self.papelera_estado == 1
        if self.papelera_estado == 0:
            self.actualizar_productos_papelera()
        self.icon_papelera_cerrar.visible = self.papelera_estado == 0
        if self.papelera_estado == 1:
            self.actualizar_productos()
        self.update()

    def _calcular_porcentaje(self, precio):
        """Calcula el 30% de un precio"""
        return round(float(precio) * 0.3, 2) + precio

    def _mostrar_dialogo(self, dialog):
        """Muestra un diálogo modal"""
        self.page.open(dialog)
        self.page.update()

    def _cerrar_dialogo(self, dialog):
        """Cierra un diálogo modal"""
        self.codigo.read_only = False
        self.nombre.read_only = False
        self.venta.read_only = False
        self.compra.read_only = False
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

    def actualizar_productos(self):
        """Actualiza la lista de productos desde la base de datos"""
        if not hasattr(self, "page") or self.page is None:
            return

        try:
            _productosEntidad = ProductoModel()
            self.productos = _productosEntidad.getExistencia(self.index_categoria, 1)

            # Reconstruir la lista de productos
            self._build_product_list(self.productos)

            # Actualizar UI solo si los controles existen
            if hasattr(self, "texto_productos") and self.texto_productos is not None:
                self.texto_productos.content.value = (
                    f"{len(self.productos)} ITEM"
                    if len(self.productos) == 1
                    else f"{len(self.productos)} ITEMS"
                )
                self.texto_productos.update()

            if hasattr(self, "content_area") and self.content_area is not None:
                # Actualizar el contenido basado en si hay productos o no
                self.content_area.content.controls[-1].content = (
                    self.product_list_view
                    if len(self.productos) > 0
                    else self._build_empty_state()
                )
                self.content_area.update()

        except Exception as e:
            print(f"Error al actualizar productos: {str(e)}")
            # Opcional: mostrar mensaje de error al usuario
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(e)}", True
            )

    def actualizar_productos_papelera(self):
        """Actualiza la lista de productos desde la base de datos"""
        if not hasattr(self, "page") or self.page is None:
            return

        try:
            _productosEntidad = ProductoModel()
            self.productos = _productosEntidad.getExistencia(self.index_categoria, 0)

            # Reconstruir la lista de productos
            self._build_product_list(self.productos)

            # Actualizar UI solo si los controles existen
            if hasattr(self, "texto_productos") and self.texto_productos is not None:
                self.texto_productos.content.value = (
                    f"{len(self.productos)} ITEM"
                    if len(self.productos) == 1
                    else f"{len(self.productos)} ITEMS"
                )
                self.texto_productos.update()

            if hasattr(self, "content_area") and self.content_area is not None:
                # Actualizar el contenido basado en si hay productos o no
                self.content_area.content.controls[-1].content = (
                    self.product_list_view
                    if len(self.productos) > 0
                    else self._build_empty_state()
                )
                self.content_area.update()

        except Exception as e:
            # Opcional: mostrar mensaje de error al usuario
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(e)}", True
            )

    def crear_producto(self, e):
        """Crea un nuevo producto"""
        _producto = ProductoModel()
        _entradaSalida = EntSalVenModel()

        # Validar campos
        if not self._validar_campos():
            return
        # Preparar datos
        data = {
            "codigo": self.codigo.value,
            "nombre": self.nombre.value,
            "precio": self.venta.value,
            "compra": self.compra.value,
            "unidad": self.unidad.value,
            "categoria": self.categoria.value,
            "activo": 1 if self.activo.value else 0,
            "moneda": self.moneda.value,
            "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
            "fecha_edit": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
        }

        try:
            # Insertar producto
            id_producto = _producto.insertar(data)

            if id_producto > 0:
                # Registrar entrada/salida
                dataES = {
                    "id_prod": id_producto,
                    "codigo": generar_codigo_unico('Vendi'),
                    "estado": "C",
                    "entradas": 0,
                    "salidas": 0,
                    "ventas": 0,
                    "activo": data["activo"],
                    "detalles": "Producto creado",
                    "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
                }
                _entradaSalida.insertar(dataES)

                # Actualizar UI
                self._mostrar_alerta("Éxito", "Producto adicionado satisfactoriamente")
                self._limpiar_formulario()
                self._cerrar_dialogo(self.dlg_modal)
                self.actualizar_productos()

            else:
                self._mostrar_alerta("Error", "No se pudo insertar el producto", True)

        except Exception as ex:
            self._mostrar_alerta("Error", f"Ocurrió un error: {str(ex)}", True)

    # validacion
    def _validar_campos(self):
        """Valida los campos del formulario"""
        validacion = True
        # Validar código
        if len(self.codigo.value) < 4:
            self.codigo.error_text = "El código debe tener al menos 4 caracteres"
            validacion = False
        else:
            producto = ProductoModel().getID("codigo", self.codigo.value)
            if len(producto) > 0:
                self.codigo.error_text = "Este código ya existe"
                validacion = False

        # Validar nombre
        if len(self.nombre.value) < 2:
            self.nombre.error_text = "El nombre debe tener al menos 2 caracteres"
            validacion = False

        # Validar categoría
        if not self.categoria.value:
            self.categoria.error_text = "Seleccione una categoría"
            validacion = False

        # Validar moneda
        if not self.moneda.value:
            self.moneda.error_text = "Seleccione una moneda"
            validacion = False

        # Validar unidad
        if not self.unidad.value:
            self.unidad.error_text = "Seleccione una unidad de medida"
            validacion = False

        # Validar precios
        if not Validaciones.valid_number(self.venta.value):
            self.venta.error_text = "Precio no válido"
            validacion = False

        if not Validaciones.valid_number(self.compra.value):
            self.compra.error_text = "Precio no válido"
            validacion = False

        # Actualizar controles con errores
        if not validacion:
            self.codigo.update()
            self.nombre.update()
            self.categoria.update()
            self.moneda.update()
            self.unidad.update()
            self.venta.update()
            self.compra.update()
            time.sleep(3)
            self._limpiar_errores()

        return validacion

    def _validar_campos_editar(self):
        """Valida los campos del formulario"""
        validacion = True
        # Validar código

        # Validar nombre
        if len(self.nombre.value) < 2:
            self.nombre.error_text = "El nombre debe tener al menos 2 caracteres"
            validacion = False

        # Validar categoría
        if not self.categoria.value:
            self.categoria.error_text = "Seleccione una categoría"
            validacion = False

        # Validar moneda
        if not self.moneda.value:
            self.moneda.error_text = "Seleccione una moneda"
            validacion = False

        # Validar unidad
        if not self.unidad.value:
            self.unidad.error_text = "Seleccione una unidad de medida"
            validacion = False

        # Validar precios
        if not Validaciones.valid_number(self.venta.value):
            self.venta.error_text = "Precio no válido"
            validacion = False

        if not Validaciones.valid_number(self.compra.value):
            self.compra.error_text = "Precio no válido"
            validacion = False

        # Actualizar controles con errores
        if not validacion:
            self.nombre.update()
            self.categoria.update()
            self.moneda.update()
            self.unidad.update()
            self.venta.update()
            self.compra.update()
            time.sleep(3)
            self._limpiar_errores_edicion()

        return validacion

    # limpiar  formularios
    def _limpiar_formulario(self):
        """Limpia el formulario de agregar producto"""
        self.product_id = 0
        self.codigo.value = ""
        self.nombre.value = ""
        self.categoria.value = None
        self.moneda.value = None
        self.unidad.value = None
        self.venta.value = format(0, ".2f")
        self.compra.value = format(0, ".2f")
        self.activo.value = True
        self.codigo.update()
        self.nombre.update()
        self.categoria.update()
        self.moneda.update()
        self.unidad.update()
        self.venta.update()
        self.compra.update()

    def _limpiar_errores(self):
        """Limpia los mensajes de error"""
        # Verifica si el control está en la página
        self.codigo.error_text = ""
        self.codigo.update()
        self.nombre.error_text = ""
        self.nombre.update()
        self.categoria.error_text = ""
        self.categoria.update()
        self.moneda.error_text = ""
        self.moneda.update()
        self.unidad.error_text = ""
        self.unidad.update()
        self.venta.error_text = ""
        self.venta.update()
        self.compra.error_text = ""
        self.compra.update()
        self.update()

    def editar_producto(self, producto):
        """Prepara el diálogo para editar un producto"""

        self.product_id = producto["id_prod"]
        self.codigo.value = producto["codigo"]
        self.nombre.value = producto["nombre"]
        self.categoria.value = producto["categoria"]
        self.moneda.value = producto["moneda"]
        self.unidad.value = producto["unidad"]
        self.venta.value = producto["precio"]
        self.compra.value = producto["compra"]
        self.activo.value = producto["activo"]
        self._mostrar_dialogo(self.dlg_modal_editar)

    def _editar_producto(self, e):
        """Guarda los cambios de un producto editado"""

        _producto = ProductoModel()

        # Validar campos
        if not self._validar_campos_editar():
            return

        # Preparar datos
        data = {
            "codigo": self.codigo.value,
            "nombre": self.nombre.value,
            "precio": self.venta.value,
            "compra": self.compra.value,
            "unidad": self.unidad.value,
            "categoria": self.categoria.value,
            "activo": 1 if self.activo.value else 0,
            "moneda": self.moneda.value,
            "fecha_edit": date.today().strftime("%d-%m-%Y"),
        }

        try:
            # Insertar producto
            _producto.update(data, f"id = '{self.product_id}'")
            # Actualizar UI
            self._mostrar_alerta("Éxito", "Producto editado satisfactoriamente")
            self._limpiar_formulario_editar()
            self._cerrar_dialogo(self.dlg_modal_editar)
            self.actualizar_productos()
        except Exception as ex:
            self._mostrar_alerta("Error", f"Ocurrió un error: {str(ex)}", True)

        self._cerrar_dialogo(self.dlg_modal_editar)
        self.actualizar_productos()

    def _limpiar_errores_edicion(self):
        """Limpia los mensajes de error"""
        # Verifica si el control está en la página
        self.nombre.error_text = ""
        self.nombre.update()
        self.categoria.error_text = ""
        self.categoria.update()
        self.moneda.error_text = ""
        self.moneda.update()
        self.unidad.error_text = ""
        self.unidad.update()
        self.venta.error_text = ""
        self.venta.update()
        self.compra.error_text = ""
        self.compra.update()
        self.update()

    def _limpiar_formulario_editar(self):
        """Limpia el formulario de agregar producto"""
        self.product_id = 0
        self.nombre.value = ""
        self.categoria.value = None
        self.moneda.value = None
        self.unidad.value = None
        self.venta.value = format(0, ".2f")
        self.compra.value = format(0, ".2f")
        self.activo.value = True
        self.nombre.update()
        self.categoria.update()
        self.moneda.update()
        self.unidad.update()
        self.venta.update()
        self.compra.update()

    def eliminar_producto(self, e, producto):
        """Elimina un producto"""
        _producto = ProductoModel()
        _producto.update({"activo": 0}, f"id = {producto['id']}")
        # Implementar lógica de eliminación
        self.actualizar_productos()

    def ver_papelera_producto(
        self,
        e,
    ):
        # Implementar lógica de eliminación
        self.actualizar_productos_papelera()

    def restaurar_producto(self, e, producto):
        """Elimina un producto"""
        _producto = ProductoModel()
        _producto.update({"activo": 1}, f"id = {producto['id']}")
        # Implementar lógica de eliminación
        self.actualizar_productos_papelera()

    # mostrar

    def mostrar_producto(self, producto):
        """Prepara el diálogo para editar un producto"""

        self.codigo.value = producto["codigo"]
        self.nombre.value = producto["nombre"]
        self.categoria.value = producto["categoria"]
        self.moneda.value = producto["moneda"]
        self.unidad.value = producto["unidad"]
        self.venta.value = producto["precio"]
        self.compra.value = producto["compra"]

        self.codigo.read_only = True
        self.nombre.read_only = True
        self.venta.read_only = True
        self.compra.read_only = True

        self._mostrar_dialogo(self.dlg_modal_mostrar)

    # entradas

    def entrar_producto(self, producto):
        """Prepara el diálogo para registrar una entrada"""
        self.producto_id = producto["id_prod"]
        self.codigo.value = producto["codigo"]
        self.codigo.read_only = True
        self.nombre.value = producto["nombre"]
        self.nombre.read_only = True
        self.entrada.value = "0"
        self._mostrar_dialogo(self.dlg_modal_entradas)

    def _procesar_entrada(self, e):
        """Procesa una entrada de producto con validaciones mejoradas"""
        try:
            _entradaSalida = EntSalVenModel()

            if not self._validar_campos_entradas():
                return

            # Obtener existencias actuales
            cantidad_entrada = float(self.entrada.value)

            # Validar cantidad positiva
            if cantidad_entrada <= 0:
                self.entrada.error_text = "La cantidad debe ser mayor que 0"
                self.entrada.update()
                return

            # Preparar datos para registro
            dataES = {
                "id_prod": self.producto_id,
                "codigo": generar_codigo_unico('Vendi'),
                "estado": "E",
                "entradas": cantidad_entrada,
                "salidas": 0,
                "ventas": 0,
                "activo": 1,
                "detalles": "Entradas ",
                "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
            }

            # Registrar salida
            if _entradaSalida.insertar(dataES):
                self._mostrar_alerta(
                    "Éxito", "Entrada de productos registrada correctamente"
                )
                self._limpiar_formulario_entradas()
                self._cerrar_dialogo(self.dlg_modal_entradas)
                self.actualizar_productos()
            else:
                self._mostrar_alerta("Error", "No se pudo registrar la entrada", True)

        except ValueError:
            self.salida.error_text = "La cantidad debe ser un número válido"
            self.salida.update()
        except Exception as ex:
            self._mostrar_alerta(
                "Error", f"Ocurrió un error inesperado: {str(ex)}", True
            )

    def _validar_campos_entradas(self):
        """Valida los campos del formulario de entradas"""
        valid = True

        if not self.entrada.value or not self.entrada.value.strip():
            self.entrada.error_text = "Ingrese la cantidad a entrar"
            valid = False

        if not Validaciones.valid_number(self.entrada.value):
            self.entrada.error_text = "Error número invalido"
            valid = False

        if not valid:
            self.entrada.update()

        return valid

    def _limpiar_formulario_entradas(self):
        """Limpia el formulario de entradas"""
        self.producto_id = 0
        self.codigo.value = ""
        self.nombre.value = ""
        self.entrada.value = 0
        self.entrada.error_text = ""
        self.entrada.update()
        self.nombre.update()
        self.codigo.update()
        self.entrada.update()

    # Salidas
    def sacar_producto(self, producto):
        """Prepara el diálogo para registrar una salida"""
        self.producto_id = producto["id_prod"]
        self.codigo.value = producto["codigo"]
        self.codigo.read_only = True
        self.nombre.value = producto["nombre"]
        self.nombre.read_only = True
        self.salida.value = "0"
        self.detalles.value = ""

        self._mostrar_dialogo(self.dlg_modal_salidas)

    def _procesar_salida(self, e):
        """Procesa una salida de producto con validaciones mejoradas"""
        try:

            _producto = ProductoModel()
            _entradaSalida = EntSalVenModel()

            if not self._validar_campos_salida():
                return

            # Obtener existencias actuales
            existencias = _producto.getExistenciaCodigo(self.producto_id)
            cantidad_entrada = float(self.salida.value)

            # Validar existencias suficientes
            if existencias < cantidad_entrada:
                self.salida.error_text = (
                    f"Existencias insuficientes. Disponibles: {existencias}"
                )
                self.salida.update()
                return

            # Validar cantidad positiva
            if cantidad_entrada <= 0:
                self.salida.error_text = "La cantidad debe ser mayor que 0"
                self.salida.update()
                return

            # Preparar datos para registro
            dataES = {
                "id_prod": self.producto_id,
                "codigo": generar_codigo_unico("Vendi"),
                "estado": "S",
                "entradas": 0,
                "salidas": cantidad_entrada,
                "ventas": 0,
                "activo": 1,
                "detalles": self.detalles.value.strip(),
                "fecha_alta": datetime.now().strftime("%d-%m-%Y"),  # Formato ISO
            }

            # Registrar salida
            if _entradaSalida.insertar(dataES):
                self._mostrar_alerta(
                    "Éxito", "Salida de productos registrada correctamente"
                )
                self._limpiar_formulario_salida()
                self._cerrar_dialogo(self.dlg_modal_salidas)
                self.actualizar_productos()
            else:
                self._mostrar_alerta("Error", "No se pudo registrar la salida", True)

        except ValueError:
            self.salida.error_text = "La cantidad debe ser un número válido"
            self.salida.update()
        except Exception as ex:
            self._mostrar_alerta(
                "Error", f"Ocurrió un error inesperado: {str(ex)}", True
            )

    def _validar_campos_salida(self):
        """Valida los campos del formulario de salida"""
        valid = True

        if not self.salida.value or not self.salida.value.strip():
            self.salida.error_text = "Ingrese la cantidad a sacar"
            valid = False

        if not self.detalles.value or not self.detalles.value.strip():
            self.detalles.error_text = "Ingrese los detalles de la salida"
            valid = False

        if not valid:
            self.salida.update()
            self.detalles.update()

        return valid

    def _limpiar_formulario_salida(self):
        """Limpia el formulario de salida"""
        self.producto_id = 0
        self.codigo.value = ""
        self.nombre.value = ""
        self.salida.value = 0
        self.detalles.value = ""
        self.salida.error_text = ""
        self.detalles.error_text = ""
        self.salida.update()
        self.detalles.update()
        self.nombre.update()
        self.codigo.update()

    def _get_color_existencias(self, cantidad):
        """Devuelve el color según el rango de existencias"""
        if cantidad <= 0.0:
            return Colors.RED_900  # Rojo oscuro para 0 o negativo
        elif 0 < cantidad < 10:
            return Colors.RED_500  # Rojo para 1-10
        elif 11 <= cantidad <= 30:
            return Colors.ORANGE_700  # Naranja para 11-30
        else:
            return Colors.BLUE_700  # Azul para más de 30

    def filtrar_por_categoria(self, categoria):
        """Filtra productos por categoría"""
        # Implementar lógica de filtrado
        self.index_categoria = categoria
        self.actualizar_productos()

    def filtrar_por_busqueda(self, event):
        """Filtra productos por categoría"""
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

        self._build_product_list(lista)

        self.texto_productos.content.value = (
            f"{len(self.productos)} ITEM"
            if len(self.productos) == 1
            else f"{len(self.productos)} ITEMS"
        )
        self.texto_productos.update()

        self.content_area.content.controls[-1].content = (
            self.product_list_view
            if len(self.productos) > 0
            else self._build_empty_state()
        )
        self.content_area.update()
        self.page.update()
    