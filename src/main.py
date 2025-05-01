import flet as ft
import Mis_Vistas as mv
import mis_controles as mc

def main(page: ft.Page):
    #Configuracion de las rutas
    nav_Rutas = ["/registrar", "/entrenamiento", "/analisis/general"]
    rutas_registro_registrar = ["/registrar/pecho", "/registrar/espalda", "/registrar/triceps", "/registrar/biceps", "/registrar/piernas", "/registrar/hombros"]
    rutas_registro_analizar = [i.replace("registrar", "analisis") for i in rutas_registro_registrar]
   
    #Creacion de csvs
    if not mc.existe_Datos_Csv():
        mc.crear_Datos_Csv()
    
    if not mc.existe_ejercicios_perso_Csv():
        mc.crear_ejercicios_perso_Csv()

    def cambio_ruta(e):
        page.views.clear()
        
        if page.route in ["/registrar", "/historial", "/formulario"] or page.route in rutas_registro_registrar:
            page.views.append(mv.VP_Registrar())

        if page.route == "/formulario":
            page.views.append(mv.VP_Formulario_Ejercicio())

        if page.route == "/historial":
            page.views.append(mv.VP_Historial())

        if page.route in rutas_registro_registrar:
            page.views.append(mv.VS_Registrar_Opciones())

        if page.route == "/entrenamiento":
            page.views.append(mv.VP_Entrenar())

        if page.route == "/analisis/general":
            page.views.append(mv.VP_Analizar())
        
        if page.route in rutas_registro_analizar:
            page.views.append(mv.VS_Analizar_Musculos())

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        page.update()

    #Barra de navegacion
    navigationBar = ft.CupertinoNavigationBar(
        bgcolor= "#23182E",
        inactive_color= "#F1F6E5",
        active_color= "#27C8B2",
        on_change= lambda e: page.go(nav_Rutas[e.control.selected_index]),
        destinations= [
            ft.NavigationBarDestination(icon= ft.Icons.CREATE, label= "Registrar"),
            ft.NavigationBarDestination(icon= ft.Icons.FITNESS_CENTER, label= "Entrenamiento"),
            ft.NavigationBarDestination(icon= ft.Icons.ANALYTICS, label= "Analisis"),
        ]
    )
    
    #Configuracion de la pagina
    page.navigation_bar = navigationBar
    page.on_view_pop = view_pop
    page.fonts= {
        "Montserrat": "Montserrat-Medium.ttf"
    }
    page.theme = ft.Theme(font_family= "Montserrat")
    page.theme_mode = ft.ThemeMode.DARK
    page.on_route_change = cambio_ruta
    page.go("/registrar")


ft.app(main, name="Contador", assets_dir="assets")