import flet as ft

import asyncio
import pandas as pd
import datetime as dt
from locale import setlocale, LC_TIME
import calendar
import os
from jnius import autoclass

def get_CSV_path():
    return os.path.join(os.getcwd(), "datos.csv")

def get_Dataframe():
    return pd.read_csv(get_CSV_path())

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

def get_diccionario() -> dict:
    ejercicios_Biceps = {
        "Curl biceps": ["Supino", "Neutro", "Concentrado", "Rotacion"],
        "Biceps con barra": ["Barra W", "Barra Z", "Barra romana"],
        "Biceps en polea": ["Unilateral", "Soga"]
    }
    ejercicios_Pecho = {
        "Press plano": ["Barra", "Maquina", "Mancuernas"],
        "Press inclinado": ["Mancuernas", "Maquina"],
        "Press declinado": ["Mancuernas", "Maquina"],
        "Apertura": ["Mancuernas", "Maquina", "Polea"],
        "Flexiones": ["Rodilla apoyadas", "Tradicionales"],
        "Pull over": ["Mancuernas"],
        "Press en polea": ["Polea"]
    }
    ejercicios_Triceps = {
        "Triceps en polea": ["Soga", "Agarre fijo", "Unilateral"],
        "Fondos de triceps": ["Estructura", "Banco"],
        "Patada de burro": ["Mancuernas"],
        "Triceps con mancuerna": ["Mancuernas y unilateral"],
        "Triceps con disco": ["Disco"],
        "Triceps trasnuca": ["Polea"]
    }
    ejercicios_Espalda = {
        "Dominadas": ["Supino", "Prono cerrado", "Prono abierto"],
        "Dorsalera": ["Supino", "Prono cerrado", "Prono abierto", "Neutro", "Neutro abierto"],
        "Remo T": ["Neutro", "Abierto"],
        "Remo": ["Maquina", "Mancuernas", "Polea"],
        "Traccion en anillos": ["Anillos"],
        "Posteriores": ["Maquina", "Mancuernas", "Polea"],
        "Pullover": ["Agarre fijo", "Soga"],
        "Press": ["Polea"]
    }
    ejercicios_Hombros = {
        "Press de hombros": ["Maquina", "Mancuernas", "Mancuernas neutro"],
        "Vuelos": ["Laterales", "Lateral en polea", "Frontales"],
        "Remo al menton": ["Barra"],
        "Press Arnold": ["Mancuernas"],
        "Posteriores": ["Maquina", "Mancuernas", "Polea"]
    }
    ejercicios_Piernas = {
        "Sentadilla": ["Barra", "Disco", "Mancuernas"],
        "Sentadilla sumo": ["Mancuerna", "Barra"],
        "Peso muerto": ["Barra", "Mancuernas"],
        "Puente": ["Barra", "Disco"],
        "Estocadas": ["Barra", "Mancuernas"],
        "Cajon": ["Saltos", "Subidas"],
        "Maquina Hack": ["Cuadriceps", "Gluteos"],
        "Maquinas": ["Prensa", "Cuadriceps", "Izquiotibiales", "Gluteos"],
        "Bulgaras": ["Tradicionales", "Mancuernas"],
        "Banco de hiperextensiones": ["Banco"],
        "Patada de gluteos": ["Polea"],
        "Aductores": ["Maquina", "Polea"],
        "Abductores": ["Maquina", "Polea"],
    }

    ejercicios_por_musculo = {
        "Biceps": ejercicios_Biceps,
        "Pecho": ejercicios_Pecho,
        "Triceps": ejercicios_Triceps,
        "Espalda": ejercicios_Espalda,
        "Hombros": ejercicios_Hombros,
        "Piernas": ejercicios_Piernas
    }
    return ejercicios_por_musculo

class MyBotonR(ft.Container):
    def __init__(self, text: str):
        super().__init__()
        self.content = MyTexto(text.upper(), 30, "#27C8B2")
        self.bgcolor = "#23182E"
        self.alignment = ft.alignment.center
        self.ink = True 
        self.border_radius = 15
        self.on_click = lambda e: self.page.go(f"{self.page.route}/{text.lower()}")
        self.expand = True

class Boton_Guardar(ft.Container):
    def __init__(self, text):
        super().__init__()
        self.content = MyTexto(text, 20, "#27C8B2")
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
        
        fecha = dt.date.today().strftime("%d/%m/%y")
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
            df = get_Dataframe()

            df = pd.concat([data, df], ignore_index=True)
            df.to_csv(file_path, index=False)
        
        self.page.go(self.page.views[0].route)

    def set_visible(self, visible: bool):
        self.visible = visible
        self.update()

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
    
    def setear_hint_text(self, text):
        self.hint_text = text
        self.update()

class Series(Input):
    def __init__(self):
        super().__init__("Series")
        self.visible = False
        self.on_change = self.modificar_inputs

    def modificar_inputs(self, e):
        num = self.verificar_numero()
        if type(num) != int:
            return

        self.rows_Column: ft.Column = self.parent.controls[1].controls
        boton_Guardar: Boton_Guardar = self.parent.controls[-1]
        data = self.get_datos()
        self.ocultar_todas_Rows()

        for i in range(num):
            row: ft.Row = self.rows_Column[i]

            if data == None:
                texts = [None, None]
                self.agregar_hints_texts(row= row, texts=texts)
            else:
                try:
                    texts = [data["Reps"][i], data["Kg"][i]]
                    self.agregar_hints_texts(row= row, texts=texts)
                except IndexError:
                    pass
                
            row.visible = True
            boton_Guardar.visible = True
            row.update()
            boton_Guardar.update()

    def get_datos(self) -> dict:
        df = self.get_df_filtered()
        data = {
            "Series": [],
            "Reps": [],
            "Kg": []
        }
        
        if type(df) != pd.DataFrame:
            return 

        series = len(df["Reps"])
        for i in range(series):
            data["Series"].append(i+1)
            data["Reps"].append(df["Reps"][i])
            data["Kg"].append(df["Kg"][i])
        
        return data
        
    def get_df_filtered(self):
        df = get_Dataframe()

        ejercicio: Selector_Principal = self.parent.parent.parent.controls[0].controls[0].controls[0]
        variacion: Selector = self.parent.parent.parent.controls[0].controls[0].controls[1]

        condiciones = [
            df["Ejercicio"] == ejercicio.value,
            df["Variacion"] == variacion.value
        ]

        df_filtered = df[condiciones[0] & condiciones[1]]
        if df_filtered.empty:
            return

        fecha = df_filtered["Fecha"].unique().tolist()[0]
        df_filtered = df[df["Fecha"] == fecha]
        df_filtered = df_filtered[["Reps", "Kg"]]
        
        return df_filtered

    def agregar_hints_texts(self, row: ft.Row, texts: list):        
        for i, a in zip(row.controls, texts):
            i.setear_hint_text(text= a)

    def verificar_numero(self):
        try:
            num = int(self.value)
                
            if num > 6:
                num = 6
                self.value = 6
            
            return num
        except ValueError:
            return
    
    def ocultar_todas_Rows(self):
        for i in self.rows_Column:
            i.visible = False
            i.update()

    def set_visible(self, visible: bool):
        self.visible = visible

        try:
            self.setear_hint_text(text=self.get_datos()["Series"][-1])
        except TypeError:
            self.setear_hint_text(text=None)
        
        self.modificar_inputs(None)
    
class Selector(ft.Dropdown):
    def __init__(self, label, analisis: bool = False):
        super().__init__()
        style = Estilo()
        self.label = label
        self.label_style = style.label_style
        self.filled = style.filled
        self.fill_color = style.fill_color
        self.color = style.color
        self.border_radius = style.border_radius
        self.analisis = analisis

        if analisis:
            self.width = 180
        else:       
            self.width = 350
            self.on_change = self.agregar_series

    def did_mount(self):
        if self.analisis:
            self.on_change = self.cambiar_datos_grafico

    def agregar_series(self, e):
        series: Series = self.parent.parent.parent.controls[1].controls[0].controls[0]
        series.set_visible(True)
        series.update()

    def cambiar_datos_grafico(self, e):
        lista_fechas : Fechas_analisis_especifico = self.parent.parent.parent.controls[1].controls[0]
        lista_fechas.set_datos()

class Selector_Principal(Selector):
    def __init__(self, label, analisis: bool = False):
        super().__init__(label, analisis)
        self.on_change = self.cambiar_variaciones
        self.analisis = analisis
    
    def did_mount(self):
        pass
    
    def build(self):
        if self.analisis:
            musculo = self.page.route[10:].capitalize()
        else:
            musculo = self.page.route[11:].capitalize()
        
        self.ejercicios = get_diccionario()[musculo]
        self.options = [ft.dropdown.Option(i) for i in self.ejercicios.keys()]

    def cambiar_variaciones(self, e):
        padre: ft.Column = self.parent
        
        if self.analisis:
            variaciones_selector: Selector = padre.parent.controls[1].controls[0]
        else:
            variaciones_selector: Selector = padre.controls[1]   #Controles de la columna
        
        lista_variaciones = self.ejercicios[e.control.value]
        variaciones_selector.options = [ft.dropdown.Option(i) for i in lista_variaciones]

        variaciones_selector.value = lista_variaciones[0]
        
        variaciones_selector.update()

        if self.analisis:
            self.cambiar_datos_grafico(None)
        else:
            variaciones_selector.agregar_series(None)

class MyDataTable(ft.DataTable):
    def __init__(self):
        super().__init__(columns=[ft.DataColumn(ft.Text(""))])
        self.filtrar_tabla(get_Dataframe())

        self.bgcolor = "#23182E"
        self.heading_row_color = "#27C8B2"
        self.heading_text_style = ft.TextStyle(size=16, color="#D9406B", weight="BOLD")
        self.vertical_lines = ft.BorderSide(2, color= "Black")
        self.border_radius = 10
        self.expand=True
        self.horizontal_margin = 20
        self.column_spacing = 30

    def filtrar_tabla(self, data):
        file = data.drop(["Musculo", "Fecha"], axis=1)

        #Columnas
        columnas = []
        for i in file.columns:
            columna = ft.DataColumn(
                label= ft.Row(
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
        self.data = data

class Selector_Filtro(Selector):
    def __init__(self, label):
        super().__init__(label)
        self.width = 180
        self.file = get_Dataframe()
        self.enable_filter = True

        self.dic = get_diccionario()
        self.dic_values = self.dic.values()

        try:
            df_filtered = self.file[label].unique().tolist()
        except KeyError:
            self.options = [ft.dropdown.Option(i) for i in [" "] + self.dic.keys()]
        else:
            df_filtered = [" "] + df_filtered
            self.options = [ft.dropdown.Option(i) for i in df_filtered]
        
        self.original_options = self.options    
        self.on_change = self.setear_tabla
    
    def setear_tabla(self, e):
        tabla: MyDataTable = self.parent.parent.parent.parent.controls[1].controls[0].controls[0]
        condiciones = self.get_condiciones()
        df_filtered = self.file.copy()

        for i in condiciones:
            df_filtered = df_filtered[i]

        tabla.filtrar_tabla(df_filtered)
        tabla.update()
        self.setear_filtros(tabla)

    def setear_filtros(self, tabla):
        for i in self.selectores_filtros:
            if i == self:
                continue

            label = i.label
            df_filtered = [" "] + tabla.data[label].unique().tolist()
            options = [ft.dropdown.Option(i) for i in df_filtered]
            
            i.options = options
            i.update()
            
    def get_condiciones(self):
        df = self.file
        filtros = self.get_filtros()
        condiciones = []
        
        for i in filtros.keys():
            condicion = df[i] == filtros[i]
            condiciones.append(condicion)
        
        return condiciones

    def get_filtros(self):
        controles_columna_padre = self.parent.parent.controls
        self.selectores_filtros = controles_columna_padre[0].controls + controles_columna_padre[1].controls
        filtros = {}

        for i in self.selectores_filtros:
            if i.value != None and i.value != " ":
                if i == self:
                    filtros[self.label] = self.value
                    continue
                filtros[i.label] = i.value
        
        return filtros

class Grafico_General_Pie(ft.PieChart):
    def __init__(self):
        super().__init__()
        self.iconos = {"Biceps": r"\images\biceps.png",
                        "Pecho": r"\images\pecho.png",
                        "Triceps": r"\images\triceps.png",
                        "Espalda": r"\images\espalda.png",
                        "Hombros": r"\images\hombro.png",
                        "Piernas": r"\images\pierna.png"}
        self.colors = {
            "Biceps": "#27C8B2",
            "Pecho": "#CEC0A3",
            "Triceps": "#D9406B",
            "Espalda": "#9966CC",
            "Hombros": "#F08080",
            "Piernas": "#E1AD01"
        }
        self.porcentaje = False

    def set_to_porcentaje(self):
        self.porcentaje = True
        values = [i.title for i in self.sections]
        total_values = sum(values)

        for i in self.sections:
            new_value = i.title * 100 / total_values
            new_title = f"{round(new_value, 0)}%"
            i.title = new_title
        
        self.update()
    
    def set_to_numero(self):
        self.porcentaje = False
        for i in range(len(self.sections)):
            self.sections[i].title = self.data["Value"][i]
        
        self.update()

    def set_sections(self, data):
        self.data = data
        secciones = []
        text_style = ft.TextStyle(
            color="White",
            weight="Bold",
            size= 18
        )

        for i in range(len(data["Musculo"])):
            badge = ft.Container(
                ft.Image(
                    src= self.iconos[data["Musculo"][i]],
                    width= 50,
                    height=50,
                    scale= 0.8
                ),
                bgcolor= "White",
                border_radius=25
            )
            parte = ft.PieChartSection(
                value= data["Value"][i],
                color= self.colors[data["Musculo"][i]],
                title= data["Value"][i],
                title_style= text_style,
                title_position= 0.6,
                badge= badge,
                badge_position= 0 if len(data["Musculo"]) > 1 else -0.9,
                radius= 80
            )
            secciones.append(parte)
        self.sections = secciones
        
class Selector_Tipo_De_Periodo(ft.CupertinoSlidingSegmentedButton):
    def __init__(self, periodos: list):
        super().__init__([])
        
        controls = []
        for i in periodos:
            control = ft.Container(
                ft.Text(i, size=18, expand=True, color="White", weight="Bold"),
                alignment= ft.alignment.center,
                height=40,
                width= 80
            )
            controls.append(control)
        self.controls = controls

        self.padding=ft.padding.symmetric()
        self.thumb_color= "#27C8B2"
        self.selected_index = 0
        self.expand = True
        self.bgcolor = "#23182E"
    
    def did_mount(self):
        self.on_change= self.actualizar_controladores
    
    def actualizar_controladores(self, e):
        lista_fechas: Lista_Fechas = self.parent.parent.controls[1].controls[0]
        lista_fechas.cambiar_periodo()
        
class Lista_Fechas(ft.Row):
    def __init__(self):
        super().__init__()
        self.scroll = ft.ScrollMode.HIDDEN
        self.data: pd.DataFrame = get_Dataframe()
        self.spacing = 20
        self.height = 30
        self.width = 172

    def did_mount(self):
        self.tipo_periodo: Selector_Tipo_De_Periodo = self.parent.parent.controls[0].controls[0]
        self.selector_categorias: Selector_Categoria = self.parent.parent.controls[3].controls[0].controls[0]
        self.cambiar_periodo(inicio=True)

    def cambiar_periodo(self, inicio = False):
        self.controls = self.get_controls()
        self.controls[-1].content.color = "#27C8B2"
        self.scroll_to(offset=-1)
        self.update()

        if not inicio:
            self.selector_categorias.set_data(None)
        
    def get_controls(self):
        tipo = self.tipo_periodo.selected_index
        if tipo == 0:
            fechas = self.get_days()
        elif tipo == 1:
            fechas = self.get_Weeks()
        else:
            fechas = self.get_Months()
        
        texts = [self.get_text_styled(i) for i in fechas.keys()]
        controls = [self.get_container(i, a) for i, a in zip(texts, fechas.values())]
        self.fechas = controls[-1].data

        return controls

    def get_days(self):
        fechas = self.data["Fecha"].sort_index(ascending=False).unique().tolist()
        days = {}
        for i in fechas:
            nombre = i[:5]
            days[nombre] = [i]

        return days
    
    def get_Weeks(self):
        all_fechas: list = self.data["Fecha"].sort_index(ascending=False).unique().tolist()
        fechas_semana = {}
        for i in all_fechas:
            i = dt.datetime.strptime(i, "%d/%m/%y")

            dia_semana = i.weekday()
            lunes = i - dt.timedelta(days=dia_semana)

            fechas = []
            for a in range(7):
                dia = lunes + dt.timedelta(days=a)
                fechas.append(dia.strftime("%d/%m/%y"))

            key = f"{fechas[0][:5]}-{fechas[-1][:5]}"
            fechas_semana[key] = fechas
            
            all_fechas = list(filter(lambda x: x not in fechas_semana, all_fechas))

        return fechas_semana

    def get_meses(self, df):
        fechas: list = df["Fecha"].unique().tolist()
        fechas.reverse()
        meses = [int(i[3:5]) for i in fechas]
        return meses

    def get_Months(self):
        meses= self.get_meses(self.data)
        año = dt.datetime.now().year

        fechas_por_mes = {}
        setlocale(LC_TIME, 'es_ES.UTF-8')

        for mes in meses:
            nombre_mes = calendar.month_name[mes]
            dias_mes = calendar.monthrange(año, mes)[1]
            fechas_mes = []

            for dia in range(1, dias_mes + 1):
                fecha = dt.date(day=dia, month=mes, year=año).strftime("%d/%m/%y")
                fechas_mes.append(fecha)
            
            fechas_por_mes[nombre_mes.capitalize()] = fechas_mes
        
        return fechas_por_mes

    def get_text_styled(self, text):
        return ft.Text(
            value= text,
            size= 15
        )

    def get_container(self, control, fechas):
        return ft.Container(
            content= control,
            on_click= self.cambiar_datos,
            alignment=ft.alignment.center,
            height=40,
            data = fechas
        )

    def cambiar_datos(self, e):
        self.cambiar_color(e)
        self.fechas = e.control.data
        self.selector_categorias.set_data(None)

    def cambiar_color(self, e):
        e.control.content.color = "#27C8B2"

        for i in self.controls:
            text_color = i.content.color

            if text_color != "White" and i != e.control:
                i.content.color = "White"
        self.update()

class Selector_Tipo_Dato(Selector):
    def __init__(self, options: list):
        super().__init__("")
        self.width = 180
        self.scale = 0.9
        self.options = [ft.dropdown.Option(text=i) for i in options]
        self.value = self.options[0].text
        self.on_change= self.cambiar_tipo_dato

    def did_mount(self):
        self.grafico: Grafico_General_Pie = self.get_grafico()
        
    def get_grafico(self):
        return self.parent.parent.parent.controls[2]

    def cambiar_tipo_dato(self, e):
        value= self.value
        
        if value == "Numero":
            self.grafico.set_to_numero()
        else:
            self.grafico.set_to_porcentaje()

class Selector_Categoria(Selector_Tipo_Dato):
    def __init__(self, options: list):
        super().__init__(options)
        self.on_change= self.set_data
    
    def did_mount(self):
        self.grafico = self.get_grafico()
        self.selector_fecha = self.get_selector()
        self.set_data(None)

    def get_selector(self):
        return self.parent.parent.parent.controls[1].controls[0]

    def set_data(self, e):
        value = self.value
        self.df = get_Dataframe()

        if value == "Entrenamientos":
            data = self.get_data_Entrenamientos()
        elif value == "Series":
            data = self.get_data_Series()
        else:
            data = self.get_data_Reps()

        self.grafico.set_sections(data)

        if self.grafico.porcentaje:
            self.grafico.set_to_porcentaje()
        else:
            self.grafico.set_to_numero()

    def get_df(self):
        #Filtra el dataframe por fecha
        fechas = self.selector_fecha.fechas
        df = self.df[self.df["Fecha"].isin(fechas)]

        return df

    def get_data_Entrenamientos(self):
        df= self.get_df()

        new_data = {"Musculo": [], "Value": []}

        for i in df["Fecha"].unique().tolist():
            musculos_entrenados = df[df["Fecha"] == i]["Musculo"].unique().tolist()
            for a in musculos_entrenados:
                filtered_df: pd.DataFrame = df[df["Musculo"] == a]
                ejercicios_hechos = filtered_df["Ejercicio"].unique()

                value = 0
                for b in ejercicios_hechos:
                    ejercicios: pd.DataFrame = filtered_df[filtered_df["Ejercicio"] == b]
                    num = len(ejercicios["Variacion"].value_counts().values)
                    value += num
                
                lista_musculos: list = new_data["Musculo"]
                if a in lista_musculos:
                    ind = lista_musculos.index(a)
                    new_data["Value"][ind] += value
                else:
                    new_data["Musculo"].append(a)
                    new_data["Value"].append(value)
        
        return new_data
    
    def get_data_Series(self):
        df = self.get_df()
        
        new_data = {"Musculo": [], "Value": []}
        
        for i in df["Fecha"].unique().tolist():
            musculos_entrenados = df[df["Fecha"] == i]["Musculo"].unique().tolist()
            for a in musculos_entrenados:
                filtered_df = df[(df["Musculo"] == a) & (df["Fecha"] == i)]
                series = len(filtered_df["Ejercicio"])

                lista_musculos: list = new_data["Musculo"]
                if a in lista_musculos:
                    ind = lista_musculos.index(a)
                    new_data["Value"][ind] += series
                else:
                    new_data["Musculo"].append(a)
                    new_data["Value"].append(series)

        return new_data

    def get_data_Reps(self):
        df= self.get_df()
        new_data = {"Musculo": [], "Value": []}
        promedios_dias = {}

        for i in df["Fecha"].unique().tolist():
            musculos_entrenados = df[df["Fecha"] == i]["Musculo"].unique().tolist()
            
            for a in musculos_entrenados:
                ejercicios_hechos = df[df["Musculo"] == a]["Ejercicio"].unique()
                promedios = []

                for b in ejercicios_hechos:
                    filtered_df = df[df["Ejercicio"] == b]
                    variaciones = filtered_df["Variacion"].value_counts().keys()

                    for c in variaciones:
                        series = filtered_df[filtered_df["Variacion"] == c]
                        promedio_reps = series["Reps"].mean()
                        promedios.append(promedio_reps)

                value = self.promedio(promedios)

                lista: list = promedios_dias.keys()
                if a in lista:
                    promedios_dias[a].append(value)
                else:
                    promedios_dias[a] = [value]
        
        general_value = [self.promedio(i) for i in promedios_dias.values()]
        
        new_data["Musculo"] = list(promedios_dias.keys())
        new_data["Value"] = general_value

        return new_data

    def promedio(self, lista):
        promedio = round(sum(lista)/len(lista), 1)

        if promedio.is_integer():
            promedio = int(promedio)
        return promedio
    
class Opciones(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        musculos = self.get_musculos()
        items = ["General", None] + musculos

        self.items = [ft.PopupMenuItem(content=self.get_text(i), on_click=self.cambiar_ruta) for i in items]
        self.icon = ft.Icons.LIST
        self.icon_size = 28
        self.icon_color = "#27C8B2"
        self.bgcolor = "#23182E"

    def did_mount(self):
        self.cambiar_color()
        
    def get_musculos(self) -> list:
        df = get_Dataframe()
        return df["Musculo"].unique().tolist()
    
    def get_text(self, text):
        if text == None:
            return text
        
        return ft.Text(
            value= text,
            text_align= ft.TextAlign.CENTER,
            weight= "Bold",
            color="White",
            size= 15
        )

    def cambiar_ruta(self, e):
        self.page.go(f"/analisis/{e.control.content.value.lower()}")
    
    def cambiar_color(self):
        values = []
        for i in self.items:
            if i.content == None:
                values.append(i.content)
                continue

            values.append(i.content.value)
        
        ind = values.index(self.page.route[10:].capitalize())
        self.items[ind].content.color = "#27C8B2"
        self.items[ind].content.update()

class Fechas_analisis_especifico(Lista_Fechas):
    def __init__(self):
        super().__init__()
        self.visible = False
        self.grafico = ""
        self.selector_peso_reps = ""
        self.informacion_detallada = ""
        self.width = 168
        self.fechas_actuales = None
        self.fechas_mes_anterior = None
    
    def did_mount(self):
        pass
    
    def get_Months(self, df: pd.DataFrame):
        meses= self.get_meses(df)
        fechas = df["Fecha"].unique().tolist()
        setlocale(LC_TIME, 'es_ES.UTF-8')

        meses_dict = {}
        for i in meses:
            mes = calendar.month_name[i].capitalize()
            dias = []
            for a in fechas:
                if int(a[3:5]) == int(i):
                    dias.append(a)
            
            meses_dict[mes] = dias
        
        return meses_dict

    def verificar_informacion(self, datos):
        if "" in [self.grafico, self.selector_peso_reps, self.informacion_detallada]:
            self.grafico: Grafico_BarChart = self.parent.parent.controls[2]
            self.selector_peso_reps: Selector_Peso_Reps = self.parent.controls[1].controls[0]
            self.informacion_detallada: Informacion_Detallada = self.parent.parent.controls[4]

        if datos == {}:
            self.set_visible(False)
            self.agregar_mensaje(True)
            return None
        elif self.visible == False:
            self.set_visible(True)
            self.agregar_mensaje(False)
            return True

    def set_datos(self):
        meses_y_fechas = self.get_Months(self.get_df_Filtered()) #Las keys son los meses y los values son las fechas
        
        if self.verificar_informacion(meses_y_fechas) == None:
            return

        texts = [self.get_text_styled(i) for i in meses_y_fechas.keys()]
        controls = [self.get_container(i, a) for i, a in zip(texts, meses_y_fechas.values())]
        tipo = self.parent.controls[1].controls[0].value

        self.controls = controls
        self.controls[-1].content.color = "#27C8B2"
        self.scroll_to(offset=-1)
        self.update()

        self.cambiar_fechas_actuales(self.controls[-1].data)
        
        try:
            self.cambiar_fechas_mes_anterior(self.controls[-2].data)
        except IndexError:
            self.cambiar_fechas_mes_anterior(self.controls[-1].data)

        self.grafico.modificar_datos(tipo=tipo)
        self.informacion_detallada.modificar_datos()

    def get_ejercicio(self):
        ejercicio = self.parent.parent.controls[0].controls[0].controls[0].value
        variacion = self.parent.parent.controls[0].controls[1].controls[0].value

        return ejercicio, variacion

    def get_df_Filtered(self):
        ejercicio, variacion = self.get_ejercicio()
        df = get_Dataframe()

        condicion_1 = df["Ejercicio"] == ejercicio
        condicion_2 = df["Variacion"] == variacion
        df_filtered = df[condicion_1 & condicion_2]

        return df_filtered

    def agregar_mensaje(self, visible: bool):
        self.parent.parent.controls[-1].visible = visible
        self.parent.parent.controls[-1].update()

    def cambiar_datos(self, e):
        self.cambiar_color(e)
        tipo = self.parent.controls[1].controls[0].value
        self.cambiar_fechas_actuales(e.control.data)
        
        ind = self.controls.index(e.control) - 1
        if ind < 0:
            ind = 0
        
        self.cambiar_fechas_mes_anterior(self.controls[ind].data)

        self.grafico.modificar_datos(tipo=tipo)
        self.informacion_detallada.modificar_datos()
        
    def set_visible(self, visible: bool):
        self.visible = visible
        self.update()

        self.grafico.set_visible(visible)
        self.selector_peso_reps.set_visible(visible)
        self.informacion_detallada.set_visible(visible)

    def cambiar_fechas_actuales(self, fechas):
        self.fechas_actuales = fechas

    def cambiar_fechas_mes_anterior(self, fechas):
        self.fechas_mes_anterior = fechas

class Grafico_BarChart(ft.BarChart):
    def __init__(self):
        super().__init__()
        self.horizontal_grid_lines = ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        )
        self.tooltip_bgcolor = ft.Colors.with_opacity(0.5, ft.Colors.GREY_300)
        self.border = ft.border.all(1, ft.Colors.GREY_400)
        self.bottom_axis = ft.ChartAxis(
            title= ft.Text(
                value= "DIA",
                text_align= ft.TextAlign.CENTER,
                style= ft.TextStyle(
                    size= 20,
                    letter_spacing= 10
                )
            ),
            title_size= 30
        )
        self.left_axis = ft.ChartAxis(
            title=ft.Text(
                text_align= ft.TextAlign.CENTER,
                style= ft.TextStyle(
                    size= 20,
                    letter_spacing= 10
                )
            ),
            title_size= 25,
            labels_size= 40,
        )
        self.visible = False
        self.bgcolor = "#23182E"

    def did_mount(self):
        self.fechas: Fechas_analisis_especifico = self.parent.controls[1].controls[0]

    def modificar_datos(self, tipo: str):        
        fechas = self.fechas.fechas_actuales

        df = self.fechas.get_df_Filtered()
        df = df[df["Fecha"].isin(fechas)]
        
        groups, labels, left_title, max_y= self.get_BarGroups_y_Labels(df, tipo)
        
        self.bar_groups = groups
        self.bottom_axis.labels = labels
        self.left_axis.title.value = left_title

        intervals = {
            (0, 25): 2.5,
            (25, 50): 5,
            (50, 75): 7.5,
            (75, 100): 10,
            (100, 125): 12.5,
            (125, 150): 15,
            (150, 175): 17.5,
            (175, 200): 20,
            (200, 225): 22.5,
            (225, 250): 25,
            (250, 275): 27.5,
            (275, 300): 30,
            (300, 325): 32.5,
            (325, 350): 35,
            (350, 375): 37.5,
            (375, 400): 40,
            (400, 425): 42.5,
            (425, 450): 45,
            (450, 475): 47.5,
            (475, 500): 50
        }

        for (min_y, max_range_y), interval in intervals.items():
            if min_y < max_y <= max_range_y:
                self.left_axis.labels_interval = interval
                self.horizontal_grid_lines.interval = interval
                break

        self.update()

    def get_BarGroups_y_Labels(self, df: pd.DataFrame, tipo: str):
        bars = []
        horizontal_Labels = []
        fechas: list = df["Fecha"].unique().tolist()
        fechas.reverse()
        
        left_title = tipo.upper()

        for i in fechas:
            pos = fechas.index(i)
            df_filtered = df[df["Fecha"] == i]
            
            bars.append(ft.BarChartGroup(
                x= pos,
                bar_rods= self.get_bars(df_filtered, tipo)
            ))
            horizontal_Labels.append(ft.ChartAxisLabel(
                value= pos,
                label= ft.Container(ft.Text(i[:2]))
            ))
        
        max_y = 0
        for i in bars:
            bar: ft.BarChartRod = i.bar_rods[0]
            if bar.to_y > max_y:
                max_y = bar.to_y

        return bars, horizontal_Labels, left_title, max_y
    
    def get_bars(self, df: pd.DataFrame, tipo: str):
        if tipo == "Peso":
            data = df["Kg"].mean()
        else:
            data = df["Reps"].mean()
            
        return [ft.BarChartRod(
            from_y=0,
            to_y=data,
            color="#D9406B",
            border_radius= 0,
            width= 15
        )]

    def set_visible(self, visible):
        self.visible = visible
        self.update()

class Selector_Peso_Reps(Selector_Tipo_Dato):
    def __init__(self, options: list):
        super().__init__(options)
        self.visible = False
        self.on_change = self.setear_datos
    
    def did_mount(self):
        pass

    def setear_datos(self, e):
        fechas = self.parent.parent.controls[0].fechas_actuales
        grafico: Grafico_BarChart = self.get_grafico()
        tipo = self.value

        grafico.modificar_datos(fechas= fechas, tipo= tipo)
    
    def set_visible(self, visible):
        self.visible = visible
        self.update()

class Informacion_Detallada(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.titulos = ["PR:", "Peso respecto al mes anterior:", "Series hechas usualmente:", "Media peso levantado (Mes):", "Media series hechas (Mes):"]
        self.controls = [
            ft.Row(
                controls= [
                    ft.Column(
                        expand=True, 
                        controls=[
                            ft.Text(
                                value= i,
                                size= 16,
                                weight= "Bold"
                            )
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                value= "",
                                size= 16,
                                color= "#27C8B2"
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    )
                ],
                height= 35
            ) for i in self.titulos
        ]
        self.visible = False

    def did_mount(self):
        self.fae: Fechas_analisis_especifico = self.parent.controls[1].controls[0]

    def modificar_datos(self):
        funciones = [
            self.get_PR,
            self.get_Peso_Respecto_Mes_Anterior,
            self.get_Series_Hechas_Usualmente,
            self.get_Media_Peso_Levantado,
            self.get_Media_Series_Hechas
        ]

        for control, funcion in zip(self.controls, funciones):
            text: ft.Text = control.controls[1].controls[0]
            text.value = funcion()

        texto: ft.Text = self.controls[1].controls[1].controls[0]
        
        if "-" in texto.value:
            texto.color = "Red"
        else:
            texto.color = "Green"

        self.update()

    def get_df_filtered(self):
        df: pd.DataFrame = self.fae.get_df_Filtered()   #Devuelve el DataFrame con los ejercicios pero con todas las fechas
        
        return df[df["Fecha"].isin(self.fae.fechas_actuales)]

    def get_PR(self):
        df = self.get_df_filtered()
        pr = df["Kg"].max()
        pr = int(pr) if pr.is_integer() else pr

        return pr

    def get_Peso_Respecto_Mes_Anterior(self):
        df_con_todas_las_fechas = self.fae.get_df_Filtered()

        df_mes_actual: pd.DataFrame = df_con_todas_las_fechas[df_con_todas_las_fechas["Fecha"].isin(self.fae.fechas_actuales)]
        df_mes_anterior: pd.DataFrame = df_con_todas_las_fechas[df_con_todas_las_fechas["Fecha"].isin(self.fae.fechas_mes_anterior)]

        media_mes_actual = df_mes_actual["Kg"].mean()
        media_mes_anterior = df_mes_anterior["Kg"].mean()

        texto = f"{self.calcular_porcentaje(media_mes_anterior, media_mes_actual)}%"
        return texto

    def calcular_porcentaje(self, valor_inicial: float, valor_final: float):
        diferencia = valor_final - valor_inicial
        porcentaje = (diferencia / valor_inicial) * 100
        porcentaje = int(porcentaje) if porcentaje.is_integer() else round(porcentaje, 2)

        return porcentaje

    def get_Series_Hechas_Usualmente(self):
        df = self.get_df_filtered()
        fechas = df["Fecha"].unique().tolist()
        conteo = {}

        for i in fechas:
            num = len(df[df["Fecha"] == i])

            if num in conteo.keys():
                conteo[num] += 1
            else:
                conteo[num] = 1

        mayor = max(conteo.values())
        for i in conteo.keys():
            if conteo[i] == mayor:
                return i

    def get_Media_Peso_Levantado(self):
        df = self.get_df_filtered()
        media = df["Kg"].mean()
        media = int(media) if media.is_integer() else round(media, 2)

        return media

    def get_Media_Series_Hechas(self):
        df = self.get_df_filtered()
        fechas = df["Fecha"].unique().tolist()
        series = []

        for i in fechas:
            num_series = len(df[df["Fecha"] == i])
            series.append(num_series)
        
        media = sum(series) / len(series)
        media = int(media) if media.is_integer() else round(media, 2)
        return media

    def set_visible(self, visible):
        self.visible = visible
        self.update()