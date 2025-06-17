
import os
from flet import *
import sqlite3
import json
from datetime import datetime
import logging

from model.NotasModel import NotasModel
from model.ProductoModel import ProductoModel
from model.EntSalVenModel import EntSalVenModel
from model.ProvedorModel import ProvedorModel
from model.UsuariosModel import UsuariosModel
from model.cierreModel import CierreModel
from model.VentasModel import VentasModel
from model.Sqlite_sequence   import Sqlite_sequence
from config.config import URL


# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OptionsScreen(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.expand = True
        self.page = page
        self.bgcolor = Colors.INDIGO

        # Elementos de la UI
        self.header = None
        self.content_area = None

        # Referencias
        self.nombre_cliente_ref = Ref[TextField]()
        self.telefono_cliente_ref = Ref[TextField]()
        self.email_cliente_ref = Ref[TextField]()
        self.Nit_cliente_ref = Ref[TextField]()
        
        # Variables para exportación
        self.export_file_path = Text("")
        self.import_file_path = Text("")  
        
        # Inicializar file pickers
        self.file_picker_import = FilePicker()
        self.page.overlay.append(self.file_picker_import) 
       
        self._build_ui()
        self._cargar_datos_cliente()
        self.page.update()

    def _build_ui(self):
        # Header
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
                                        "Configuración del sistema.",
                                        size=12,
                                        color=Colors.WHITE60,
                                    ),
                                    Text(
                                        f"Mantenga siempre una salva de sus datos.",
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

       
        # Formulario de datos del cliente
        cliente_form = Container(
            padding=10,
            content=Column(
                controls=[
                    Text("Datos Personales", size=16, weight=FontWeight.BOLD, color=Colors.BLUE_ACCENT),
                    TextField(
                        ref=self.nombre_cliente_ref,
                        label="Nombre",
                        hint_text="Ingrese nombre completo",
                        width=300,
                        
                    ),
                    TextField(
                        ref=self.telefono_cliente_ref,
                        label="Teléfono",
                        hint_text="Ingrese número de teléfono",
                        width=300,
                        keyboard_type=KeyboardType.PHONE,
                    ),
                    TextField(
                        ref=self.email_cliente_ref,
                        label="Email",
                        hint_text="Ingrese dirección de email",
                        width=300,
                        keyboard_type=KeyboardType.EMAIL,
                    ),
                    TextField(
                        ref=self.Nit_cliente_ref,
                        label="Nit",
                        hint_text="Nit",
                        width=300,
                        keyboard_type=KeyboardType.EMAIL,
                    ),
                    ElevatedButton(
                        "Guardar Datos",
                        icon=Icons.SAVE,
                        on_click=self._guardar_datos_cliente,
                    ),
                ],
                spacing=10,
            ),
        )

        # Sección de exportación/importación
        data_management = Container(
            padding=10,
            content=Column(
                controls=[
                    Text("Gestión de Datos", size=16, weight=FontWeight.BOLD),
                    Row(
                        controls=[
                            ElevatedButton(
                                "Exportar Datos",
                                icon=Icons.UPLOAD_FILE,
                                on_click=self._exportar_datos,
                            ),
                            self.export_file_path,
                        ]
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                "Importar Datos",
                                icon=Icons.IMPORT_EXPORT,
                                on_click=self._importar_datos,
                            ),
                            self.import_file_path,
                        ]
                    ),
                    ElevatedButton(
                        "Respaldar Base de Datos",
                        icon=Icons.BACKUP,
                        on_click=self._respaldar_bd,
                    ),
                    ElevatedButton(
                        "Restaurar Base de Datos",
                        icon=Icons.RESTORE,
                        on_click=self._restaurar_bd,
                        color=Colors.RED,
                    ),
                ],
                spacing=10,
            ),
        )

        # Contenido principal
        self.content_area = Container(
            expand=True,
            bgcolor=Colors.GREY_100,
            width=float("inf"),
            border_radius=border_radius.only(top_left=10, top_right=10),
            padding=padding.only(top=15, left=15, right=15),
            content=Column(
                scroll=ScrollMode.AUTO,
                controls=[
                    cliente_form,
                    Divider(height=20),
                    data_management,
                    Divider(height=20),
                    self._build_advanced_options(),
                ],
            ),
        )

        self.content = Column(controls=[self.header, self.content_area], spacing=0)

    
    def _cargar_datos_cliente(self):
        """Carga los datos del cliente desde la base de datos si existen"""
        try:
            _usuario = UsuariosModel()
            
            # Obtener datos del cliente con ID 1
            datos = _usuario.findID(1)
            
            if not datos:  # Si no hay datos o la lista está vacía
                logger.info("El cliente no existe en la base de datos")
                return
            
            # Asumimos que findID retorna una lista de diccionarios
            cliente = datos[0]  # Tomamos el primer registro
          

            # Verificar que las referencias existen
            if not hasattr(self, 'nombre_cliente_ref') or not self.nombre_cliente_ref.current:
                print("Error: Referencia nombre_cliente_ref no está configurada correctamente")
                return
            
            # Asignar valores con verificación de campos
            self.nombre_cliente_ref.current.value = cliente.get('nombre') or ""
            self.telefono_cliente_ref.current.value = cliente.get('telefono') or ""
            self.email_cliente_ref.current.value = cliente.get('email') or ""
            self.Nit_cliente_ref.current.value = cliente.get('nit') or ""   
           
            # Forzar actualización
            # self.nombre_cliente_ref.current.update()
            # self.telefono_cliente_ref.current.update()
            # self.email_cliente_ref.current.update()
            # self.Nit_cliente_ref.current.update()
                        
        except Exception as ex:
            logger.error(f"Error al cargar datos del cliente: {ex}")            
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(ex)}", True
            )
        finally:         
            self.page.update()
    
    def _build_advanced_options(self):
        return Container(
            padding=10,
            content=Column(
                controls=[
                    Text("Opciones Avanzadas", size=16, weight=FontWeight.BOLD),                   
                    ElevatedButton(
                        "Limpiar Base de Datos",
                        icon=Icons.DELETE_FOREVER,
                        on_click=self._limpiar_bd,
                        color=Colors.RED,
                    ),
                ],
                spacing=10,
            ),
        )

    # Métodos para manejar acciones
    def _guardar_datos_cliente(self, e):
        
        data ={
            'nombre':self.nombre_cliente_ref.current.value,
            'telefono': self.telefono_cliente_ref.current.value,
            'email': self.email_cliente_ref.current.value,
            'nit':self.Nit_cliente_ref.current.value,
        }
     
        try:           
            _usuario=UsuariosModel()
            datos =_usuario.findID(1)
            if len(datos) > 0:
                # Actualizar
                _usuario.update(data,1)
            else:
                # Insertar nuevo
                _usuario.insertar(data)
            
            self._mostrar_alerta("Éxito", "Datos personales guardados satisfactoriamente")
         
        except Exception as ex:
            logger.error(f"Error al guardar datos del cliente: {ex}")
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(ex)}", True
            )
        finally:           
            self.page.update()

    def _exportar_datos(self, e):
        try:
            def save_file_result(e: FilePickerResultEvent):
                if e.path:
                    self.export_file_path.value = f"Exportando a: {e.path}"
                    self.page.update()
                    
                    # Obtener instancias de los modelos
                    producto_model = ProductoModel()
                    notas_model = NotasModel()
                    venta_model = VentasModel()
                    usuario_model = UsuariosModel()
                    cierre_model = CierreModel()
                    ent_sal_ven_model = EntSalVenModel()
                    proveedor_model = ProvedorModel()  # Asegúrate de que este sea el nombre correcto
                    
                    # Obtener todos los datos de cada modelo
                    datos = {
                        "productos": producto_model.findAll(),
                        "ventas": venta_model.findAll(),
                        "clientes": usuario_model.findAll(),
                        "cierres": cierre_model.findAll(),
                        "movimientos": ent_sal_ven_model.findAll(),
                        "proveedores": proveedor_model.findAll(),
                        "notas":notas_model.findAll(),
                        "fecha_exportacion": datetime.now().isoformat(),
                        "metadata": {
                            "version": "1.0",
                            "aplicacion": "Vendi",
                            "total_registros": {
                                "productos": len(producto_model.findAll()),                                
                                # ... otros contadores
                            }
                        }
                    }

                    # Exportar a JSON
                    with open(e.path, "w", encoding='utf-8') as f:
                        json.dump(datos, f, indent=4, ensure_ascii=False, default=str)

                    self.export_file_path.value = f"Datos exportados a: {e.path}"
                    self._mostrar_alerta("Éxito",  f"Datos exportados a: {e.path}")
                    
            # Configurar y mostrar el file picker
            if not hasattr(self.page, 'file_picker_export'):
                self.page.file_picker_export = FilePicker(on_result=save_file_result)
                self.page.overlay.append(self.page.file_picker_export)
                self.page.update()
            
            self.page.file_picker_export.save_file(
                file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                allowed_extensions=["json"]
            )
            
        except Exception as ex:
            logger.error(f"Error al exportar datos: {ex}")
            self._mostrar_alerta(
                "Error", f"No se pudieron cargar los productos: {str(ex)}", True
            )
           
        finally:
            self.page.update()
    
    def _importar_datos(self, e):
        try:
            def pick_files_result(e: FilePickerResultEvent):
                if not e.files:
                    return
                
                if not hasattr(self, 'page') or self.page is None:
                    self._mostrar_alerta("Error", "No se puede acceder a la página principal", True)
                    return
                            
                file_path = e.files[0].path               
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Inicializar modelos
                    producto_model = ProductoModel()
                    venta_model = VentasModel()
                    usuario_model = UsuariosModel()
                    cierre_model = CierreModel()
                    ent_sal_ven_model = EntSalVenModel()
                    proveedor_model = ProductoModel()
                    notas_model = NotasModel()
                    
                    # Contadores para resultados
                    resultados = {
                        'productos': {'nuevos': 0, 'existentes': 0},
                        'ventas': {'nuevos': 0, 'existentes': 0},
                        'clientes': {'nuevos': 0, 'existentes': 0},
                        'cierres': {'nuevos': 0, 'existentes': 0},
                        'movimientos': {'nuevos': 0, 'existentes': 0},
                        'proveedores': {'nuevos': 0, 'existentes': 0},
                        'notas': {'nuevos': 0, 'existentes': 0}
                    }
                    
                    # Importar productos (ejemplo)
                    if 'productos' in data:
                        for producto in data['productos']:
                            # Verificar si el producto ya existe
                            existente = producto_model.findByCampo('id_prod',producto.get('id_prod'))
                            if not existente:
                               
                                producto_model.insertar(producto)
                                resultados['productos']['nuevos'] += 1
                            else:
                                resultados['productos']['existentes'] += 1
                                
                    if 'notas' in data:
                        for nota in data['notas']:
                            # Verificar si el producto ya existe
                            existente = notas_model.findByCampo('id_notas',nota.get('id_notas'))
                            if not existente:
                               
                                notas_model.insertar(nota)
                                resultados['productos']['nuevos'] += 1
                            else:
                                resultados['productos']['existentes'] += 1
                    
                    # Importar ventas (ejemplo)
                    if 'ventas' in data:
                        for venta in data['ventas']:
                            # Verificar por algún campo único (ej: código de venta)
                            existente = venta_model.findByCampo('id_venta',venta.get('id_venta'))
                            if not existente:
                                
                                venta_model.insertar(venta)
                                resultados['ventas']['nuevos'] += 1
                            else:
                                resultados['ventas']['existentes'] += 1
                                
                     # Importar cierres (ejemplo)
                    if 'cierres' in data:
                        for cierre in data['cierres']:
                            # Verificar por algún campo único (ej: código de venta)
                            existente = cierre_model.findByCampo('id_cierre',cierre.get('id_cierre'))
                            if not existente:
                               
                                cierre_model.insertar(cierre)
                                resultados['cierres']['nuevos'] += 1
                            else:
                                resultados['cierres']['existentes'] += 1
                                
                                
                        # Importar cierres (ejemplo)
                    if 'clientes' in data:
                        for usuario in data['clientes']:
                            # Verificar por algún campo único (ej: código de venta)
                            existente = usuario_model.findByCampo('id',usuario.get('id'))
                            if not existente:
                               
                                usuario_model.insertar(usuario)
                                resultados['clientes']['nuevos'] += 1
                            else:
                                resultados['clientes']['existentes'] += 1
                                
                        # Importar cierres (ejemplo)
                    if 'movimientos' in data:
                        for movimiento in data['movimientos']:
                            # Verificar por algún campo único (ej: código de venta)
                            existente = ent_sal_ven_model.findByCampo('id_mov',movimiento.get('id_mov'))
                            if not existente:
                               
                                ent_sal_ven_model.insertar(movimiento)
                                resultados['movimientos']['nuevos'] += 1
                            else:
                                resultados['movimientos']['existentes'] += 1
                                
                    if 'proveedores' in data:
                        for proveedores in data['proveedores']:
                            # Verificar por algún campo único (ej: código de venta)
                            existente = proveedor_model.findByCampo('id',proveedores.get('id'))
                            if not existente:
                              
                                proveedor_model.insertar(proveedores)
                                resultados['proveedores']['nuevos'] += 1
                            else:
                                resultados['proveedores']['existentes'] += 1
                    
                    # Repetir lógica para otros modelos...
                    
                    # Mostrar resultados
                    resumen = "\n".join(
                        [f"{k.capitalize()}: +{v['nuevos']} nuevos, {v['existentes']} existentes" 
                        for k, v in resultados.items()]
                    )
                    
                    self.import_file_path.value = "Importación completada"
                    self._mostrar_alerta("Éxito",  f"Importación completada")
                    
                except Exception as ex:
                    logger.error(f"Error durante importación: {ex}")
                    self._mostrar_alerta(
                    "Error", f"No se pudieron cargar los productos: {str(ex)}", True
            )
                finally:
                    self.page.update()
            
            
            if not hasattr(self.page, 'file_picker_import'):
                self.page.file_picker_import = FilePicker(on_result=pick_files_result)
                self.page.overlay.append(self.page.file_picker_import)
                self.page.update()
            
            self.page.file_picker_import.pick_files(
                allowed_extensions=["json"],
                dialog_title="Seleccionar archivo de respaldo"
            )
            
        except Exception as ex:
            logger.error(f"Error al iniciar importación: {ex}")          
            self._mostrar_alerta(
                    "Error", f"Error al iniciar importación: {ex}", True
            )  
        
        finally:
            self.page.update()

    
    def _respaldar_bd(self, e):
        try:
            # Primero verificar si el archivo de origen existe
            if not os.path.exists('data/vendi.db'):
                print(os.path.exists('data/vendi.db'))
                self._mostrar_alerta("Error", "No se encontró la base de datos original", True)
                return

            def save_file_result(e: FilePickerResultEvent):
                if e.path:
                    try:
                        import shutil
                        # Crear directorio si no existe
                        os.makedirs('data', exist_ok=True)
                        shutil.copy2('data/vendi.db', e.path)
                        self._mostrar_alerta("Éxito", f"Base de datos respaldada en: {e.path}")
                    except Exception as ex:
                        logger.error(f"Error al copiar archivo: {ex}")
                        self._mostrar_alerta("Error", f"Error al copiar archivo: {e.path}", True)
                self.page.update()

            # Configurar el file picker
            if not hasattr(self.page, 'backup_file_picker'):
                self.page.backup_file_picker = FilePicker(on_result=save_file_result)
                self.page.overlay.append(self.page.backup_file_picker)
                self.page.update()

            # Sugerir nombre por defecto con fecha
            default_name = f"vendi_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            self.page.backup_file_picker.save_file(
                file_name=default_name,
                allowed_extensions=["db"]
            )

        except Exception as ex:
            logger.error(f"Error al respaldar BD: {ex}")
            self._mostrar_alerta("Error", f"Error al respaldar BD: {ex}", True)
        finally:
            self.page.update()
    
    
    def _restaurar_bd(self, e):
        try:
            def load_file_result(e: FilePickerResultEvent):
                if e.files:
                    try:
                        file_path = e.files[0].path
                        import shutil
                        # Crear directorio data si no existe
                        os.makedirs('data', exist_ok=True)
                        shutil.copy2(file_path, "data/vendi.db")
                        self._mostrar_alerta("Éxito", "Base de datos restaurada correctamente")
                    except Exception as ex:
                        logger.error(f"Error al restaurar BD: {ex}")
                        self._mostrar_alerta("Error", f"Error al restaurar BD: {ex}", True)
                self.page.update()

            # Configurar el file picker
            if not hasattr(self.page, 'restore_file_picker'):
                self.page.restore_file_picker = FilePicker(on_result=load_file_result)
                self.page.overlay.append(self.page.restore_file_picker)
                self.page.update()

            self.page.restore_file_picker.pick_files(
                allowed_extensions=["db"],
                dialog_title="Seleccionar archivo de respaldo de base de datos"
            )

        except Exception as ex:
            logger.error(f"Error al restaurar BD: {ex}")
            self._mostrar_alerta("Error", f"Error al restaurar BD: {ex}", True)
        finally:
            self.page.update()
            
            
    def _limpiar_bd(self, e):
       
        def confirm_clean(e):
            self._cerrar_dialogo(self.dialog)          
            try:
                producto_model = ProductoModel()
                venta_model = VentasModel()
                usuario_model = UsuariosModel()
                cierre_model = CierreModel()
                ent_sal_ven_model = EntSalVenModel()
                proveedor_model = ProvedorModel()  # Asegúrate de que este sea el nombre correcto
                sqlite_sequence= Sqlite_sequence() 
                
                producto_model.limpiar()
                venta_model.limpiar()
                usuario_model.limpiar()
                cierre_model.limpiar()
                proveedor_model.limpiar()
                ent_sal_ven_model.limpiar()                
                sqlite_sequence.limpiar()
                
                self._mostrar_alerta("Éxito", "Base de datos vaciada correctamente")   
                self._cerrar_dialogo(self.dialog) 
            except Exception as ex:
                logger.error(f"Error al limpiar BD: {ex}")                
                self._mostrar_alerta("Error", f"Error al limpiar BD: {ex}", True)
            finally:
              
               self.page.update()

        self.dialog = AlertDialog(
            title=Text("Confirmar"),
            content=Text(
                "¿Está seguro que desea limpiar toda la base de datos? Esta acción no se puede deshacer."
            ),
            actions=[
                TextButton(
                    "Cancelar",
                    on_click=lambda e:  self._cerrar_dialogo(self.dialog),
                ),
                TextButton("Limpiar", on_click=confirm_clean),
            ],
        ) 
        self._mostrar_dialogo(self.dialog )       
        self.page.update()


    
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