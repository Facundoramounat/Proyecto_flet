import flet as ft
import mis_controles as mc

# VP = Vista principal
# VS = Vista secundaria
# VT = Vista terciaria


class VP_Registrar(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/registrar"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.MyTexto("Registrar", 20, "#27C8B2"),
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
                    ]
                ),
            )
        ]
    
    def did_mount(self):
        if not mc.csv_con_contenido():
            self.appbar.actions[0].visible = False
            self.appbar.actions[0].update()

    def build(self):
        self.navigation_bar = self.page.navigation_bar
        for i in self.controls[0].content.controls:
            i.page = self.page

class VS_Registrar_Opciones(ft.View):
    def __init__(self):
        super().__init__()
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
                                        mc.Selector_Principal("Ejercicio"),
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

    def build(self):
        self.route = self.page.route
        self.navigation_bar = self.page.navigation_bar
        self.appbar.title = mc.MyTexto(self.page.route[11:].capitalize(), 20, "#27C8B2")

        rows_colunm = self.controls[0].content

        rows_colunm.controls[1].controls[0].controls[-1].page = self.page
        rows_colunm.controls[0].controls[0].controls[0].page = self.page
    
class VP_Historial(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/historial"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.MyTexto("Historial", 20, "#27C8B2"),
            bgcolor="#23182E",
        )
        self.controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row([
                                ft.Column([
                                        ft.Row([mc.Selector_Filtro("Fecha"), mc.Selector_Filtro("Musculo")], alignment= ft.MainAxisAlignment.CENTER),
                                        ft.Row([mc.Selector_Filtro("Ejercicio"), mc.Selector_Filtro("Variacion")], alignment= ft.MainAxisAlignment.CENTER),
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
                                    scroll= ft.ScrollMode.ADAPTIVE,
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
    
    def build(self):
        self.navigation_bar = self.page.navigation_bar

class VP_Entrenar(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/entrenamiento"
        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.MyTexto("Entrenamiento", 20, "#27C8B2"),
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
    
    def build(self):
        self.navigation_bar = self.page.navigation_bar

class VP_Analizar(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/analisis/general"

        df = mc.get_Dataframe()
        if df.empty:
            self.controls = [
                ft.SafeArea(
                    expand=True,
                    content= ft.Container(
                        expand=True,
                        content= ft.Text(
                            value="No hay datos",
                            text_align= ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center
                    )
                )
            ]
            return

        self.appbar = ft.AppBar(
            leading_width=30,
            title=mc.MyTexto("Analisis: General", 20, "#27C8B2"),
            bgcolor="#23182E",
            actions=[mc.Opciones()]
        )
        self.controls = [
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            [
                                mc.Selector_Tipo_De_Periodo(["Dia", "Semana", "Mes"])
                            ]
                        ),
                        ft.Row([mc.Lista_Fechas()], alignment=ft.MainAxisAlignment.CENTER),
                        mc.Grafico_General_Pie(),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        mc.Selector_Categoria(["Entrenamientos", "Series", "Media Reps (x ejercicio)"])
                                    ],
                                    expand=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.START
                                ),
                                ft.Column(
                                    [
                                        mc.Selector_Tipo_Dato(["Numero", "%"])
                                    ],
                                    expand=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.END
                                )
                            ]
                        )
                    ]
                ),
            )
        ]
    
    def build(self):
        self.navigation_bar = self.page.navigation_bar

class VS_Analizar_Musculos(ft.View):
    def __init__(self):
        super().__init__()
        self.controls = [
            ft.SafeArea(
                expand = True,
                content= ft.Column(
                    expand= True,
                    scroll= ft.ScrollMode.HIDDEN,
                    controls= [
                        ft.Row(
                            [
                                ft.Column([mc.Selector_Principal("Ejercicio", analisis=True)], expand=True),
                                ft.Column([mc.Selector("Variacion", analisis=True)], expand=True, horizontal_alignment=ft.CrossAxisAlignment.END)
                            ]
                        ),
                        ft.Row(
                            [
                                mc.Fechas_analisis_especifico(),
                                mc.Selector_Peso_Reps(options=["Peso", "Repeticiones"])
                            ], 
                            vertical_alignment= ft.CrossAxisAlignment.END,
                            alignment= ft.MainAxisAlignment.CENTER,
                            height= 70
                        ),
                        mc.Grafico_BarChart(),
                        ft.Row([ft.Text("No hay datos")], visible=False , alignment=ft.MainAxisAlignment.CENTER),
                    ]
                )
            )
        ]

    def build(self):
        self.route = self.page.route
        self.navigation_bar = self.page.navigation_bar
        titulo = mc.MyTexto(f"Analisis: {self.page.route[10:].capitalize()}", 20, "#27C8B2")
        
        self.appbar = ft.AppBar(
            leading_width=30,
            title= titulo,
            bgcolor="#23182E",
            actions=[mc.Opciones()]
        )