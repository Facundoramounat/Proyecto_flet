import flet as ft
import mis_controles as mc

# VP = Vista principal
# VS = Vista secundaria
# VT = Vista terciaria


class VP_Registrar(ft.View):
    def __init__(self, navegationBar):
        super().__init__()
        self.route = "/registrar"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario("Registrar", 20, "#27C8B2"),
            bgcolor="#23182E",
            actions=[
                ft.IconButton(icon=ft.Icons.HISTORY, on_click=lambda e: self.page.go("/historial"), icon_color="#27C8B2"),
            ]
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        mc.MyBotonR("Biceps"),
                        mc.MyBotonR("Pecho"),
                        mc.MyBotonR("Triceps"),
                        mc.MyBotonR("Espalda"),
                        mc.MyBotonR("Hombros"),
                        mc.MyBotonR("Piernas"),
                    ],
                    scroll="auto",
                ),
            )
        ]
        self.navigation_bar = navegationBar
        self.bgcolor = "#CEC0A3"
    
    def did_mount(self):
        if not mc.csv_con_contenido():
            self.appbar.actions[0].visible = False
            self.appbar.actions[0].update()

    def build(self):
        for i in self.controls[0].content.controls:
            i.page = self.page

class VS_Registrar_Opciones(ft.View):
    def __init__(self, navegationBar, diccionario):
        super().__init__()
        self.navigation_bar = navegationBar
        self.appbar = ft.AppBar(
            leading_width=30,
            bgcolor="#23182E",
        )
        self.controls = [
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        mc.Selector_Principal("Ejercicio", diccionario),
                                        mc.Selector("Variacion"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True
                                )
                            ],
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        mc.Series(),
                                        ft.Column(
                                            [
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                                ft.Row(
                                            [
                                                mc.Input("Reps"),
                                                mc.Input("Kg"),
                                            ],
                                            visible=False,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                            ]
                                        ),
                                        ft.Column(height=25),
                                        mc.Boton_Guardar()
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True
                                )
                            ]
                        )                        
                    ],
                    expand=True,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            )
        ]
        self.bgcolor = "#CEC0A3"

    def build(self):
        self.route = self.page.route
        self.appbar.title = mc.Texto_Secundario(self.page.route[11:].capitalize(), 20, "#27C8B2")
        self.controls[0].content.controls[1].controls[0].controls[-1].page = self.page

class VP_Historial(ft.View):
    def __init__(self, navegationBar, diccionario):
        super().__init__()
        self.route = "/historial"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario("Historial", 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.navigation_bar = navegationBar
        self.controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row([
                                ft.Column([
                                        ft.Row([mc.Selector_Filtro("Fecha"), mc.Selector_Filtro("Musculo")], alignment= ft.MainAxisAlignment.CENTER),
                                        ft.Row([mc.Selector_Filtro("Ejercicio", diccionario), mc.Selector_Filtro("Variacion")], alignment= ft.MainAxisAlignment.CENTER),
                                        mc.Boton_Filtrar(),
                                        ft.Column([ft.Text("")], height=30) #Espacio en blanco
                                    ],
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [mc.MyDataTable()],
                                    height= 445,
                                    scroll= ft.ScrollMode.ALWAYS,
                                    expand=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            alignment= ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            )
        ]
        self.bgcolor = "#CEC0A3"

class VP_Entrenar(ft.View):
    def __init__(self, navegationBar):
        super().__init__()
        self.route = "/entrenamiento"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario("Entrenamiento", 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Column([ft.Text("")], height=30),  # Espacio en blanco
                    ],
                ),
            )
        ]
        self.navigation_bar = navegationBar

class VP_Analizar(ft.View):
    def __init__(self, navegationBar):
        super().__init__()
        self.route = "/analisis"

        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario("Analisis", 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                    ],
                ),
            )
        ]
        self.navigation_bar = navegationBar
