import flet as ft
import pandas as pd

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

class Boton_Enviar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.content = Texto_Secundario("Enviar", 20, "#27C8B2")
        self.bgcolor = "#23182E"
        self.border_radius = 20
        self.width = page.width / 2.7
        self.height = self.width / 2.5
        self.alignment = ft.alignment.center
        self.visible = False

        def validar_contenido(controls, padre: ft.Column):
            lista_verificacion = []

            for i in controls:
                if i.visible == True:
                    for c in i.controls:
                        if c.value == "":
                            c.error_text = "Debes rellenar"
                            lista_verificacion.append(False)

            if len(lista_verificacion) > 0:
                padre.update()
                return False
            else:
                return True

        def get_data():
            padre: ft.Column = self.parent
            rows_column_controls = padre.controls[1].controls
            campos_completos = validar_contenido(rows_column_controls, padre.controls[1])

            if campos_completos == False:
                return 

            reps = []
            kg = []

            for control in rows_column_controls:
                if control.visible == False:
                    break

                reps.append(control.controls[0].value)
                kg.append(control.controls[1].value)

            return reps, kg

        def enviar(e):
            try:
                reps, kg = get_data()
            except TypeError:
                return
            
            data = {"Reps": reps, "Kg": kg}

            print(pd.DataFrame(data, index= range(1, len(reps) + 1)))

        self.on_click = enviar


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

        def change_visible(e):
            try:
                num = int(e.control.value)
                
                if num > 6:
                    num = 6
                    e.control.value = 6
            except ValueError:
                return

            padre: ft.Column = self.parent
            rows_Column = padre.controls[1].controls
            boton_enviar = padre.controls[-1]
            boton_enviar.visible = True

            for i in rows_Column:
                i.visible = False

            for i in range(num):
                rows_Column[i].visible = True

            padre.update()

        self.on_change = change_visible
    
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