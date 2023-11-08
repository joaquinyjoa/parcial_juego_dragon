import pygame
import json
import random
import sys

def guardar_puntaje(puntaje):
    """
    Guarda el puntaje del jugador en un archivo JSON.

    Args:
        puntaje (int): El puntaje a guardar.

    Returns:
        None
    """
    puntaje_data = {"puntaje": puntaje}
    with open("puntaje.json", "w") as archivo_json:
        json.dump(puntaje_data, archivo_json)

def cargar_puntaje(archivo):
    """
    Carga el puntaje del jugador desde un archivo JSON.

    Returns:
        int: El puntaje cargado. Si el archivo no existe, retorna 0.
    """
    try:
        with open(archivo, 'r') as file:
            puntaje_data = json.load(file)
    except FileNotFoundError:
        puntaje_data = 0

    return puntaje_data

def mostrar_pantalla_ganador(ventana, ruta, WIDTH, HEIGHT, puntaje):
    """
    Muestra la pantalla de ganador con el puntaje del jugador y opciones.

    Args:
        ventana: La ventana de Pygame.
        ruta_ganador (str): La ruta de la imagen de fondo de ganador.
        WIDTH (int): Ancho de la ventana.
        HEIGHT (int): Alto de la ventana.
        puntaje (int): El puntaje del jugador.

    Returns:
        str: "Continuar" si el jugador elige continuar, "Salir" si elige salir.
    """
    fondo = generar_fondo(WIDTH, HEIGHT, ruta)
    ventana.blit(fondo, (0, 0))

    fuente_ganador = pygame.font.Font(None, 60)
    mensaje_ganador = fuente_ganador.render("¡Ganaste la partida!", True, (0, 0, 0))
    mensaje_puntaje = fuente_ganador.render(f"Puntaje: {puntaje}", True, (0, 0, 0))

    mensaje_ganador_rect = mensaje_ganador.get_rect()
    mensaje_puntaje_rect = mensaje_puntaje.get_rect()

    mensaje_ganador_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    mensaje_puntaje_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    ventana.blit(mensaje_ganador, mensaje_ganador_rect)
    ventana.blit(mensaje_puntaje, mensaje_puntaje_rect)

    fuente_boton = pygame.font.Font(None, 40)
    texto_continuar = fuente_boton.render("Continuar Jugando", True, (0, 0, 0))
    texto_salir = fuente_boton.render("Salir", True, (0, 0, 0))

    rectangulo_continuar = texto_continuar.get_rect()
    rectangulo_salir = texto_salir.get_rect()

    rectangulo_continuar.center = (WIDTH // 2, HEIGHT // 2 + 120)
    rectangulo_salir.center = (WIDTH // 2, HEIGHT // 2 + 200)

    ventana.blit(texto_continuar, rectangulo_continuar)
    ventana.blit(texto_salir, rectangulo_salir)

    pygame.display.flip()
    resultado = None
    bandera = True
    while bandera:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bandera = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectangulo_continuar.collidepoint(evento.pos):
                    resultado = "Continuar"
                elif rectangulo_salir.collidepoint(evento.pos):
                    resultado = "Salir"
                return resultado

def mostrar_pantalla_perdedor(ventana, ruta, WIDTH, HEIGHT, puntaje):
    """
    Muestra la pantalla de perdedor con opciones.

    Args:
        ventana: La ventana de Pygame.
        ruta_perdedor (str): La ruta de la imagen de fondo de perdedor.
        WIDTH (int): Ancho de la ventana.
        HEIGHT (int): Alto de la ventana.

    Returns:
        str: "Continuar" si el jugador elige continuar, "Salir" si elige salir.
    """
    continuar = "Continuar Jugando"
    salir = "SALIR"
    letras = (0, 0, 0)
    fondo = generar_fondo(WIDTH, HEIGHT, ruta)
    ventana.blit(fondo, (0, 0))
    
    fuente_perdedor = pygame.font.Font(None, 60)
    perdedor = fuente_perdedor.render("¡Perdiste!", True, (255, 255, 255))
    mensaje_puntaje = fuente_perdedor.render(f"Puntaje: {puntaje}", True, (255, 255, 255))

    perdedor_rect = perdedor.get_rect()
    mensaje_puntaje_rect = mensaje_puntaje.get_rect()

    perdedor_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    mensaje_puntaje_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
    
    ventana.blit(mensaje_puntaje, mensaje_puntaje_rect)
    ventana.blit(perdedor, perdedor_rect)
    
    fuente_boton = pygame.font.Font(None, 40)
    texto_continuar = fuente_boton.render(continuar, True, letras)
    texto_salir = fuente_boton.render(salir, True, letras)
    
    rectangulo_continuar = texto_continuar.get_rect()
    rectangulo_salir = texto_salir.get_rect()
    
    rectangulo_continuar.center = (WIDTH // 2, HEIGHT // 2 + 120)
    rectangulo_salir.center = (WIDTH // 2, HEIGHT // 2 + 200)
    
    ventana.blit(texto_continuar, rectangulo_continuar)
    ventana.blit(texto_salir, rectangulo_salir)
    
    pygame.display.flip()

    resultado = None
    bandera = True
    while bandera:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bandera = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectangulo_continuar.collidepoint(evento.pos):
                    resultado = "Continuar"
                elif rectangulo_salir.collidepoint(evento.pos):
                    resultado = "Salir"
                return resultado
            
def manejar_jugador(player_x, player_y, speed, rect_jugador, tecla_espacio_presionada, proyectiles):
    """
    Maneja el movimiento del jugador y el disparo.

    Args:
        player_x (int): La posición X del jugador.
        player_y (int): La posición Y del jugador.
        speed (int): La velocidad de movimiento.
        rect_jugador: El rectángulo que representa al jugador.
        tecla_espacio_presionada (bool): Indica si la tecla de espacio está presionada.
        proyectiles (list): Lista de proyectiles.

    Returns:
        dict: Un diccionario que contiene los valores actualizados:
            - "player_x" (int): Nueva posición X del jugador.
            - "player_y" (int): Nueva posición Y del jugador.
            - "tecla_espacio_presionada" (bool): Si la tecla de espacio está presionada.
            - "proyectiles" (list): Lista de proyectiles actualizada.
    """
    HEIGHT = 600

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= speed
    if keys[pygame.K_RIGHT] and player_x < 200:
        player_x += speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - rect_jugador.height:
        player_y += speed

    if keys[pygame.K_SPACE] and not tecla_espacio_presionada:
        tecla_espacio_presionada = True
        proyectil_x = player_x + rect_jugador.width - 25
        proyectil_y = player_y + rect_jugador.height // 2 - 30 
        lista_proyectiles = [proyectil_x, proyectil_y]
        proyectiles.append(lista_proyectiles)

    if not keys[pygame.K_SPACE]:
        tecla_espacio_presionada = False

    movimiento_jugador = {
        "player_x": player_x,
        "player_y": player_y,
        "tecla_espacio_presionada": tecla_espacio_presionada,
        "proyectiles": proyectiles
    }

    return movimiento_jugador

def generar_enemigos(cantidad, ruta, enemigo_width, enemigo_height):

    """
    Genera una lista de enemigos con propiedades aleatorias.

    Parameters:
    cantidad (int): El número de enemigos que se deben generar.

    Returns:
    dict: Un diccionario que contiene una lista de enemigos, un contador de disparo y un intervalo de tiempo.
    """
    enemigos = []
    for i in range(cantidad):
        enemigo_imagen = pygame.image.load(ruta)
        enemigo_imagen = pygame.transform.scale(enemigo_imagen, (enemigo_width, enemigo_height))
        enemigo_x = random.randint(400, 750)
        enemigo_y = random.randint(0, 500)
        tiempo_disparo = random.randint(60, 120)
        contador_disparo = 0
        velocidad_individual = 2 
        direccion_individual = random.choice([-1, 1])
        lista_enemigos = [enemigo_imagen, enemigo_x, enemigo_y, tiempo_disparo, contador_disparo, velocidad_individual, direccion_individual]
        enemigos.append(lista_enemigos)

    datos = {"enemigos": enemigos, 
            "contador_disparo": contador_disparo,
            "tiempo_disparo": tiempo_disparo,
            }

    return datos

def generar_mensaje(mensaje, color_letra:tuple, tamaño, tamaño_rectangulo:tuple):
    try:
        # Mensaje de inicio
        fuente = pygame.font.Font(None, tamaño)
        mensaje_text = fuente.render(mensaje, True, color_letra)
        mensaje_rect = mensaje_text.get_rect()
        mensaje_rect.topleft = tamaño_rectangulo
        dato_mensaje = {"texto" : mensaje_text,
                        "rectangulo" : mensaje_rect}
    except pygame.error as e:
        print(f"Error al configurar el mensaje inicial: {e}")
        sys.exit(1)
    
    return dato_mensaje

def generar_icono(ruta_icono:str):
    try:
        icono = pygame.image.load(ruta_icono)
        pygame.display.set_icon(icono)
    except pygame.error as e:
        print(f"Error al cargar el icono: {e}")
        sys.exit(1)
    return icono

def generar_fondo(WIDTH, HEIGHT, ruta):
    fondo = pygame.image.load(ruta)
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    return fondo


