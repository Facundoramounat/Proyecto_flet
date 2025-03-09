import flet as ft
import asyncio
import pandas as pd
from datetime import date
import os

def get_CSV_path():
    return os.path.join(os.getcwd(), "datos.csv")

def csv_con_contenido():
    df = pd.read_csv(get_CSV_path())
    
    if df.empty:
        return False
        
    return True

def crear_csv():
    df = pd.DataFrame()
    df.to_csv(get_CSV_path())

def existe():
    return os.path.exists(get_CSV_path())

class MyBotonR(ft.Container):
    def __init__(self, text: str):
        super().__init__()
        self.content = MyTexto(text.upper(), 30, "#27C8B2")
        self.bgcolor = "#23182E"
        self.alignment = ft.alignment.center
        self.height = 108
        self.ink = True 
        self.border_radius = 15
        self.on_click = lambda e: self.page.go(f"{self.page.route}/{text.lower()}")

class Boton_Guardar(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = MyTexto("Guardar", 20, "#27C8B2")
        self.bgcolor = "#23182E"
        self.border_radius = 25
        self.width = 150
        self.height = 60
        self.alignment = ft.alignment.center
        self.visible = False
        self.scale = ft.transform.Scale(scale=1)
        self.animate_scale = ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        self.on_click = self.animation
        self.on_animation_end = self.guardar

    def validar_contenido(self, controls, padre: ft.Column):
        lista_verificacion = []

        for i in controls:
            if i.visible == False:
                break
    
            for c in i.controls:
                if c.value == "" or c.value == None:
                    c.error_text = ""
                    lista_verificacion.append(False)

        if len(lista_verificacion) > 0:
            padre.update()
            return False
        else:
            return True

    def get_parents(self):
        padre: ft.Column = self.parent
        row_Selector: ft.Row = padre.parent.parent.controls[0]
        rows_column_controls = padre.controls[1].controls

        return padre, row_Selector, rows_column_controls

    def get_data(self):
        padre, row_Selector, rows_column_controls = self.get_parents()
        
        ejercicios_column = row_Selector.controls[0]
        contenido_a_evaluar = [ejercicios_column] + rows_column_controls
        
        campos_completos = self.validar_contenido(contenido_a_evaluar, padre.parent.parent)
        
        if campos_completos == False:
            return 
        
        fecha = date.today().strftime('%d/%m/%y')
        ejercicio = ejercicios_column.controls[0].value
        variacion = ejercicios_column.controls[1].value
        reps = []
        kg = []
        musculo = self.page.route[11:].capitalize()

        for control in rows_column_controls:
            if control.visible == False:
                break
            
            reps.append(control.controls[0].value)
            kg.append(control.controls[1].value)
        
        return fecha, ejercicio, variacion, reps, kg, musculo

    def guardar(self, e):
        try:
            fecha, ejercicio, variacion, reps, kg, musculo = self.get_data()
        except TypeError:
            return
        
        data = pd.DataFrame({"Fecha": fecha, 
                             "Ejercicio": ejercicio, 
                             "Variacion": variacion, 
                             "Reps": reps, 
                             "Kg": kg,
                             "Musculo": musculo})
        file_path = get_CSV_path()

        if not csv_con_contenido():
            data.to_csv(file_path, index=False)
        else:
            df = pd.read_csv(file_path)

            df = pd.concat([data, df], ignore_index=True)
            df.to_csv(file_path, index=False)
        
        self.page.go(self.page.views[0].route)

    async def animation(self, e):
        self.scale = 0.7
        self.update()

        await asyncio.sleep(0.21)

        self.scale = 1
        self.update()
            
class MyTexto(ft.Text):
    def __init__(self, text, size, color= "Black"):
        super().__init__()
        self.value= text
        self.size= size
        self.color= color

class Estilo:
    def __init__(self):
        self.label_style = ft.TextStyle(color="White", weight= "Bold")
        self.filled = True
        self.fill_color = "#23182E"
        self.color = "#27C8B2"
        self.text_align = ft.TextAlign.CENTER
        self.border_radius = 10

class Input(ft.TextField):
    def __init__(self, label):
        super().__init__()
        style = Estilo()
        
        self.label = label
        self.label_style = style.label_style
        self.filled = style.filled
        self.fill_color = style.fill_color
        self.color = style.color
        self.text_align = style.text_align
        self.keyboard_type = ft.KeyboardType.NUMBER
        self.border_radius = style.border_radius
        self.width = 180

        def sacar_errorText(e):
            self.error_text = None
            self.update()

        self.on_change = sacar_errorText

class Series(Input):
    def __init__(self):
        super().__init__("Series")

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
    def __init__(self, label):
        super().__init__()
        style = Estilo()
        self.label = label
        self.label_style = style.label_style
        self.filled = style.filled
        self.fill_color = style.fill_color
        self.color = style.color
        self.border_radius = style.border_radius
        self.width = 350

        def sacar_errorText(e):
            self.error_text = None
            self.update()
        self.on_change = sacar_errorText
    
    def build(self):
        return super().build()

class Selector_Principal(Selector):
    def __init__(self, label, diccionario: dict):
        super().__init__(label)
        self.options = [ft.dropdown.Option(i) for i in diccionario.keys()]

        def sacar_errorText():
            self.error_text = None
            self.update()

        def cambiar_variaciones(e):
            padre: ft.Column = self.parent
            variaciones_selector: Selector = padre.controls[1]   #Controles de la columna
            lista_variaciones = diccionario[e.control.value]
            
            variaciones_selector.options = [ft.dropdown.Option(i) for i in lista_variaciones]

            if len(lista_variaciones) == 1:
                variaciones_selector.value = lista_variaciones[0]

            variaciones_selector.update()
            sacar_errorText()

        self.on_change = cambiar_variaciones

class MyDataTable(ft.DataTable):
    def __init__(self):
        super().__init__(columns=[ft.DataColumn(ft.Text(""))])
        file = pd.read_csv(get_CSV_path())
        file = file.drop(["Musculo", "Fecha"], axis=1)

        #Columnas
        columnas = []
        for i in file.columns:
            columna = ft.DataColumn(
                ft.Row(
                    [
                        ft.Text(i, text_align=ft.TextAlign.CENTER, expand=True),
                    ],
                    expand= True,
                    alignment= ft.MainAxisAlignment.END
                ),
                heading_row_alignment= ft.MainAxisAlignment.CENTER,
            )

            columnas.append(columna)
        self.columns = columnas

        #Filas
        self.original_Rows = []
        for i in range(file.shape[0]):
            celdas = []

            for a in file.iloc[i].tolist():
                celda = ft.DataCell(
                    content=ft.Row(
                        [ft.Text(value=a, text_align= ft.TextAlign.CENTER, expand=True)],
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    )
                )
                celdas.append(celda)
            
            self.original_Rows.append(ft.DataRow(celdas))
        
        self.rows= self.original_Rows
        self.bgcolor = "#23182E"
        self.heading_row_color = "#27C8B2"
        self.heading_text_style = ft.TextStyle(size=16, color="#D9406B", weight="BOLD")
        self.vertical_lines = ft.BorderSide(2, color= "Black")
        self.border_radius = 10
        self.expand=True
        self.horizontal_margin = 20
        self.column_spacing = 30

class Selector_Filtro(Selector):
    def __init__(self, label, diccionarios: list = None):
        super().__init__(label)
        self.width = 180
        self.dics = diccionarios
        file = pd.read_csv(get_CSV_path())
        self.enable_filter = True

        if label != "Variacion":
            try:
                df_filtered = file[label].unique().tolist()
            except KeyError:
                self.options = [ft.dropdown.Option(i) for i in ["Vacio", "Biceps", "Pecho", "Triceps", "Espalda", "Hombros", "Piernas"]]
            else:
                df_filtered = ["Vacio"] + df_filtered
                self.options = [ft.dropdown.Option(i) for i in df_filtered]        

        if label == "Ejercicio":
            self.on_change = self.cambiar_variaciones
        
    def cambiar_variaciones(self, e):
        if e.control.value == "Vacio":
            return

        for i in self.dics:
            if e.control.value in i.keys():
                self.dict = i
                break

        variaciones: Selector_Filtro = self.parent.controls[1]
        variaciones.options = [ft.dropdown.Option(i) for i in ["Vacio"] + self.dict[e.control.value]]
        variaciones.update()

class Boton_Filtrar(Boton_Guardar):
    def __init__(self, dic_list = None):
        super().__init__()
        self.content = MyTexto("Filtrar", 20, "#27C8B2")
        self.visible = True
        self.on_click = self.animation
        self.on_animation_end = self.filtrar
        self.dic_list = dic_list

    def get_filtros(self):
        filtros = {}

        for i in range(2):
            for a in self.parent.controls[i].controls:
                if a.value != None and a.value != "Vacio":
                    filtros[a.label] = a.value
        return filtros

    def filtrar(self, e):
        filtros: dict = self.get_filtros()
        tabla: MyDataTable = self.parent.parent.parent.controls[1].controls[0].controls[0]

        if filtros == {}:
            tabla.rows = tabla.original_Rows
            tabla.update()
            return
        
        df = pd.read_csv(get_CSV_path())
        condiciones = []

        for filtro, valor in filtros.items():
            condiciones.append(df[filtro] == valor)
        
        filtro_final = None

        for condicion in condiciones:
            if filtro_final is None:
                filtro_final = condicion
            else:
                filtro_final &= condicion 
        
        new_df = df[filtro_final].drop(["Musculo", "Fecha"], axis=1)

        rows = []
        for i in range(new_df.shape[0]):
            celdas = []

            for a in new_df.iloc[i].tolist():
                celda = ft.DataCell(
                    content=ft.Row(
                        [ft.Text(value=a, text_align= ft.TextAlign.CENTER, expand=True)],
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    )
                )
                celdas.append(celda)
            
            rows.append(ft.DataRow(celdas))

        tabla.rows = rows
        tabla.update()

    async def animation(self, e):
        self.scale = 0.7
        self.update()

        await asyncio.sleep(0.21)

        self.scale = 1
        self.update()