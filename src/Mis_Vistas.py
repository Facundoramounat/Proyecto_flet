import flet as ft
import mis_controles as mc

#VP = Vista principal
#VS = Vista secundaria
#VS = Vista terciaria

class VP_Registrar(ft.View):
    def __init__(self, navegationBar, page:ft.Page):
        super().__init__()
        self.route = "/registrar"
        self.controls = [
            ft.AppBar(),
            ft.TextButton("Ir", on_click=lambda e: page.go("/registrar/biceps")),
            mc.MyBotonR("Biceps", page),
            mc.MyBotonR("Pecho", page),
            mc.MyBotonR("Triceps", page),
            mc.MyBotonR("Espalda", page),
            mc.MyBotonR("Hombros", page),
            mc.MyBotonR("Piernas", page),
        ]
        self.navigation_bar = navegationBar
        self.bgcolor = "#CEC0A3"
    
class VS_Registrar_Opciones(ft.View):
    def __init__(self, navegationBar, page: ft.Page, diccionario):
        super().__init__()
        self.route = page.route
        self.navigation_bar = navegationBar

        self.controls = [
            ft.AppBar(leading_width= 30, title= mc.Texto_Secundario(page.route[11:].capitalize(), 20, "#27C8B2"), bgcolor="#23182E"),
            ft.Column(
                [mc.Selector_Principal("Ejercicio", page, diccionario), mc.Selector("Variacion", page)],
                width= page.width,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    mc.Series(page),
                    ft.Column([
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                            ft.Row([
                                mc.Input("Reps", page),
                                mc.Input("Kg", page)
                            ], visible= False),
                    ]),
                    ft.Column(height= 25),
                    mc.Boton_Enviar(page)
                ],
                width= page.width,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
            )
        ]
        self.bgcolor = "#CEC0A3"

class VP_Entrenar(ft.View):
    def __init__(self, navegationBar):
        super().__init__()
        self.route = "/entrenamiento"
        self.controls = [
            ft.Column([ft.Text("")], height= 30), #Espacio en blanco
            ft.Text("Entrenamiento", color="Blue")
        ]
        self.navigation_bar = navegationBar

class VP_Analizar(ft.View):
    def __init__(self, navegationBar):
        super().__init__()
        self.route = "/analisis"
        self.controls = [
            ft.Column([ft.Text("")], height= 30), #Espacio en blanco
            ft.Text("Analisis", color="Blue")
        ]
        self.navigation_bar = navegationBar