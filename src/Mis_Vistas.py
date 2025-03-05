import flet as ft
import mis_controles as mc
import sys

# VP = Vista principal
# VS = Vista secundaria
# VT = Vista terciaria


class VP_Registrar(ft.View):
    def __init__(self, navegationBar, page: ft.Page):
        super().__init__()
        self.route = "/registrar"

        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario("Registrar", 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        mc.MyBotonR("Biceps", page),
                        mc.MyBotonR("Pecho", page),
                        mc.MyBotonR("Triceps", page),
                        mc.MyBotonR("Espalda", page),
                        mc.MyBotonR("Hombros", page),
                        mc.MyBotonR("Piernas", page),
                    ],
                    scroll="auto",
                ),
            )
        ]
        self.navigation_bar = navegationBar
        self.bgcolor = "#CEC0A3"

class VS_Registrar_Opciones(ft.View):
    def __init__(self, navegationBar, page: ft.Page, diccionario):
        super().__init__()
        self.route = page.route
        self.navigation_bar = navegationBar
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.Texto_Secundario(page.route[11:].capitalize(), 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Column(
                            [
                                mc.Selector_Principal("Ejercicio", page, diccionario),
                                mc.Selector("Variacion", page),
                            ],
                            width=page.width,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                mc.Series(page),
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                        ft.Row(
                                            [
                                                mc.Input("Reps", page),
                                                mc.Input("Kg", page),
                                            ],
                                            visible=False,
                                        ),
                                    ]
                                ),
                                ft.Column(height=25),
                                mc.Boton_Enviar(page),
                            ],
                            width=page.width,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                ),
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
                        ft.Column([ft.Text("")], height=30),  # Espacio en blanco
                    ],
                ),
            )
        ]
        self.navigation_bar = navegationBar
