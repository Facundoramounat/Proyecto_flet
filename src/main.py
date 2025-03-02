import flet as ft
import Mis_Vistas as mv

def main(page: ft.Page):
    page.title = "Ejercicios APP"
    page.window.maximized = True

    #Configuracion de las rutas
    rutas_principales = ["/registrar", "/entrenamiento", "/analisis"]
    rutas_registro = ["/registrar/pecho", "/registrar/espalda", "/registrar/triceps", "/registrar/biceps", "/registrar/piernas", "/registrar/hombros"]
    
    #Ejercicios para cada sector del cuerpo
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
        "Triceps trasnuca en polea": ["Polea"]
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

    ejercicios_por_ruta = {
        "/registrar/biceps": ejercicios_Biceps,
        "/registrar/pecho": ejercicios_Pecho,
        "/registrar/triceps": ejercicios_Triceps,
        "/registrar/espalda": ejercicios_Espalda,
        "/registrar/hombros": ejercicios_Hombros,
        "/registrar/piernas": ejercicios_Piernas
    }
    

    def cambio_ruta(e):
        page.views.clear()
        
        if page.route == "/registrar" or page.route in rutas_registro:
            page.views.append(mv.VP_Registrar(navigationBar, page))

        if page.route in rutas_registro:
            ejercicios = ejercicios_por_ruta[page.route]
            page.views.append(mv.VS_Registrar_Opciones(navigationBar, page, ejercicios))

        if page.route == "/entrenamiento":
            page.views.append(mv.VP_Entrenar(navigationBar))

        if page.route == "/analisis":
            page.views.append(mv.VP_Analizar(navigationBar))
        
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    #Barra de navegacion
    navigationBar = ft.CupertinoNavigationBar(
        bgcolor= "#23182E",
        inactive_color= "#F1F6E5",
        active_color= "#27C8B2",
        on_change= lambda e: page.go(rutas_principales[e.control.selected_index]),
        destinations= [
            ft.NavigationBarDestination(icon= ft.Icons.CREATE, label= "Registrar"),
            ft.NavigationBarDestination(icon= ft.Icons.FITNESS_CENTER, label= "Entrenamiento"),
            ft.NavigationBarDestination(icon= ft.Icons.ANALYTICS, label= "Analisis"),
        ]
    )

    #FilePicker
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    #Configuracion de la pagina
    page.on_view_pop = view_pop
    page.fonts= {
        "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap",
        "Bebas Neue": "https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap"
    }
    page.adaptive = True
    page.on_route_change = cambio_ruta
    page.go("/registrar")
    page.update()

ft.app(main, name="Contador")