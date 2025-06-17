import flet as ft
from route.routing import Routing, path
from screen.reporte_ipv import IPV
from screen.reporte_mov import Movimientos
from screen.reporte_inventario import Inventario
from screen.reporte_venta_detalle import VentasDetalles
from screen.reporte__mov_detalle import MovimientosEntradasDetalles
from screen.reporte__mov_detalle import MovimientosSalidasDetalles
from screen.reporte__mov_detalle import MovimientosVentasDetalles
from screen.reporte_venta import Ventas
from screen.splach import Splach
from screen.home import Home
from style.styles import *

def main(page: ft.Page):
    page.theme = page.dark_theme = style
    
    app_routers = [
        path(url="/", clear=True, view=Splach().view),
        path(url="/home", clear=True, view=Home().view),
        path(url="/ventas", clear=True, view=Ventas().view),
        path(url="/ventas/detalle/:fecha", clear=True, view=VentasDetalles().view),
        path(url="/mov", clear=True, view=Movimientos().view),
        path(url="/mov/detalle/e/:id_prod", clear=True, view=MovimientosEntradasDetalles().view),        
        path(url="/mov/detalle/s/:id_prod", clear=True, view=MovimientosSalidasDetalles().view),
        path(url="/mov/detalle/v/:id_prod", clear=True, view=MovimientosVentasDetalles().view),
        path(url="/ipv", clear=True, view=IPV().view),
        path(url="/inventario", clear=True, view=Inventario().view),
    ]

    Routing(page=page, app_routes=app_routers)
    page.fonts = {
        "aBeeZee": "ABeeZee-Regular",
    }
    page.window.width = 400
    page.window.max_width= 400
    page.window.resizable = False
    page.window.maximizable = False
    page.go(page.route)


ft.app(main) 
