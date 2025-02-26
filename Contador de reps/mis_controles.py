import flet as ft

class MyBotonR(ft.Container):
    def __init__(self, text: str, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = Texto_Principal(text.upper(), 30)
        self.bgcolor = "#F7F5F7"
        self.alignment = ft.alignment.center
        self.width = page.width
        self.height = 116
        self.on_click = lambda e: page.go(f"{page.route}/{text.lower()}")
        self.ink = True
        self.border_radius = 15

class Texto_Principal(ft.Text):
    def __init__(self, text, size):
        super().__init__()
        self.value = text
        self.size = size
        self.color = "#D9406B"
        self.font_family = "Bebas Neue"
    
class Texto_Secundario(ft.Text):
    def __init__(self, text, size, color= "Black"):
        super().__init__()
        self.value= text
        self.size= size
        self.color= color
        self.font_family = "Montserrat"

class Estilo:
    def __init__(self, page):
        self.label_style = ft.TextStyle(color="White", font_family="Montserrat", weight= "Bold")
        self.filled = True
        self.fill_color = "#23182E"
        self.color = "#27C8B2"
        self.text_align = ft.TextAlign.CENTER
        self.border_radius = 10

class Input(ft.TextField):
    def __init__(self, label, page: ft.Page):
        super().__init__()
        style = Estilo(page)
        
        self.label = label
        self.label_style = style.label_style
        self.filled = style.filled
        self.fill_color = style.fill_color
        self.color = style.color
        self.text_align = style.text_align
        self.keyboard_type = ft.KeyboardType.NUMBER
        self.border_radius = style.border_radius
        self.width = page.width / 2.15

class Series(Input):
    def __init__(self, page: ft.Page):
        super().__init__("Series", page)
        self.value = 0

        def agregar(e):
            lista_Row = []
            try:
                num = int(e.control.value)
            except ValueError:
                return

            for i in range(num):
                lista_Row.append(
                    ft.Row(
                        [
                            Input("Reps", page),
                            Input("Kg", page)
                        ]
                    )
                )
        
            column = ft.Column(lista_Row)
            control_column = self.parent #Accede a la Columna de la Vista

            if len(control_column.controls) == 1:
                control_column.controls.append(column)
                control_column.update()
            else:
                control_column.controls.pop()
                control_column.controls.append(column)
                control_column.update()



        self.on_change = agregar
    
class Selector(ft.Dropdown):
    def __init__(self, label, page: ft.Page):
        super().__init__()
        style = Estilo(page)
        self.label = label
        self.label_style = style.label_style
        self.filled = style.filled
        self.fill_color = style.fill_color
        self.color = style.color
        self.border_radius = style.border_radius
        self.width = page.width / 1.2
        self.visible = False

class Selector_Principal(Selector):
    def __init__(self, label, page, diccionario: dict):
        super().__init__(label, page)
        self.visible = True
        self.options = [ft.dropdown.Option(i) for i in diccionario.keys()]

        def cambiar_variaciones(e):
            padre: ft.Column = self.parent
            variaciones_selector: Selector = padre.controls[1]   #Controles de la columna
            lista_variaciones = diccionario[e.control.value]
            
            variaciones_selector.options = [ft.dropdown.Option(i) for i in lista_variaciones]

            if len(lista_variaciones) == 1:
                variaciones_selector.value = lista_variaciones[0]
                

            if variaciones_selector.visible == False:
                variaciones_selector.visible = True

            variaciones_selector.update()

        self.on_change = cambiar_variaciones