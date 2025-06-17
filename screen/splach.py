
from flet import *
from route import params, Basket
from model.ProductoModel import ProductoModel
from model.EntSalVenModel import EntSalVenModel
from model.ProvedorModel import ProvedorModel
from model.UsuariosModel import UsuariosModel
from model.cierreModel import CierreModel
from model.VentasModel import VentasModel
class Splach:
    def __init__(self):
        self.iniciarDatos()
    
    def iniciarDatos(self):
        p=ProductoModel()
        e=EntSalVenModel()
        u=UsuariosModel()
        a=ProvedorModel()        
        a=CierreModel()  
        a=VentasModel()              
        
    def view(self, page: Page, params: params, basket: Basket):
        print(params)

        return View(
            "/",
            controls=[
                Container(                    
                    content=Column(                        
                        controls=[
                            Image(src="splash_android.png", width=page.window.width/1.5),
                            TextButton(
                                "Comenzar", on_click=lambda _: page.go(f"/home")
                            ),                        
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,

                        width=float('inf'),
                        height=float("inf"),
                        
                        
                        
                    ),
                    expand=True, 
                    padding=padding.only(bottom=50, top=100)        

                    
                    
                ),
            ],
        )
