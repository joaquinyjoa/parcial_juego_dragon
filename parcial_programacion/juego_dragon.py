from configuracion import *
from modulo import *
import pygame
import random
import sys

pygame.init()

#titulo
pygame.display.set_caption(titulo)

#fondo de pantalla--------------------------------------------------------------------
try:
    # Configuración de la ventana
    ventana = pygame.display.set_mode((WIDTH, HEIGHT))
    fondo = generar_fondo(WIDTH, HEIGHT, ruta_fondo)
except pygame.error as e:
    print(f"Error al configurar la ventana o cargar el fondo: {e}")
    sys.exit(1)

#icono--------------------------------------------------------------------
icono = generar_icono(ruta_icono)

#musica de fondo--------------------------------------------------------------------
pygame.mixer.music.load(ruta_musica_fondo)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#control FPS------------------------------------------------------------------
reloj = pygame.time.Clock()

#inicio
fuente = generar_mensaje(mensaje, color_letras, 50, (100,50))
# Texto en los botones

rectangulo_jugar = generar_mensaje(boton_jugar, color_letras, 60,(165, 200))
rectangulo_salir = generar_mensaje(boton_salir, color_letras, 60,(175, 300))
#item
item_imagen = pygame.image.load(ruta_item)
item_imagen = pygame.transform.scale(item_imagen, (ancho_item, alto_item))

item_x = random.randint(0, 165)
item_y = random.randint(0, HEIGHT - alto_item)

#creacion de enemigos
datos = generar_enemigos(num_enemigos, ruta_enemigo, enemigo_width, enemigo_height)
enemigos = datos["enemigos"]
contador_disparo = datos["contador_disparo"]
tiempo_disparo = datos["tiempo_disparo"]

sonido_colision = pygame.mixer.Sound(ruta_colision)
sonido_colision_enemigo = pygame.mixer.Sound(ruta_colision_enemigo)
sonido_ganador = pygame.mixer.Sound(ruta_sonido_ganador)
sonido_perdedor = pygame.mixer.Sound(ruta_sonido_perdedor)

juego_en_ejecucion = True
pantalla_pelea = False
pantalla_ganador = False
tecla_espacio_presionada = False

clock = pygame.time.Clock()

while juego_en_ejecucion:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_en_ejecucion = False
        if pantalla_pelea == False and evento.type == pygame.MOUSEBUTTONDOWN:
            if rectangulo_jugar["rectangulo"].collidepoint(evento.pos):
                pantalla_pelea = True  # Iniciar la pantalla de pelea
                pygame.mixer.music.stop()  # Detener la música de fondo actual
                pygame.mixer.music.load(ruta_musica_pelea)  # Cargar la música de pelea
                pygame.mixer.music.play(-1)

            elif rectangulo_salir["rectangulo"].collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    ventana.blit(fondo, (0, 0))

    if pantalla_pelea == False:
        pygame.draw.rect(ventana, fondo_naranja, (150, 190, 210, 60))
        pygame.draw.rect(ventana, fondo_naranja, (150, 295, 170, 50))
        ventana.blit(rectangulo_jugar["texto"], rectangulo_jugar["rectangulo"])
        ventana.blit(rectangulo_salir["texto"], rectangulo_salir["rectangulo"])
        ventana.blit(fuente["texto"], fuente["rectangulo"])
    else:
        # Lógica y dibujo de la pantalla de pelea
        fondo = generar_fondo(WIDTH, HEIGHT, ruta_pelea)

        imagen_jugador = pygame.image.load(ruta_personaje)
        rect_jugador = imagen_jugador.get_rect()

        proyectil_imagen = pygame.image.load(ruta_proyectil)
        proyectil_rect = proyectil_imagen.get_rect()

        proyectil_imagen_enemigo = pygame.image.load(ruta_proyectil_enemigo)
        proyectil_rect_enemigo = proyectil_imagen.get_rect()

        fuente_vidas = pygame.font.Font(None, 36)  # Fuente para el texto de las vidas
        texto_vidas = fuente_vidas.render(f'Vidas: {vidas_jugador}', True, color_vidas)
        ventana.blit(texto_vidas, (10, 10))  # Muestra el texto en la esquina superior izquierda

        manejo = manejar_jugador(player_x, player_y, speed, rect_jugador, tecla_espacio_presionada, proyectiles)

        player_x = manejo["player_x"]
        player_y = manejo["player_y"]
        tecla_espacio_presionada = manejo["tecla_espacio_presionada"]
        proyectiles = manejo["proyectiles"]
        
        ventana.blit(imagen_jugador, (player_x, player_y))

        # Dibujar el item en la pantalla
        ventana.blit(item_imagen, (item_x, item_y))
        
        item_rect = pygame.Rect(item_x, item_y, ancho_item, alto_item)
        jugador_rect = pygame.Rect(player_x, player_y, rect_jugador.width, rect_jugador.height)
        
        if jugador_rect.colliderect(item_rect):
            # El jugador colisiona con el item, activa el disparo triple
            proyectil_derecha = player_x + rect_jugador.width - 25
            proyectil_arriba = player_y
            proyectiles.append([proyectil_derecha, proyectil_arriba])
            
            proyectil_centro = player_x + rect_jugador.width - 25
            proyectil_medio = player_y + rect_jugador.height // 2 - 30
            proyectiles.append([proyectil_centro, proyectil_medio])
            
            proyectil_abajo = player_x + rect_jugador.width - 25
            proyectil_inferior = player_y + rect_jugador.height - 50
            proyectiles.append([proyectil_abajo, proyectil_inferior])
            
            # Mueve el item a una nueva posición aleatoria
            item_x = random.randint(0, 165)
            item_y = random.randint(0, HEIGHT)

        nuevos_proyectiles = []

        for proyectil in proyectiles:
            proyectil_x, proyectil_y = proyectil
            proyectil_x += 5  # Mover el proyectil hacia la derecha
            proyectil[0] = proyectil_x
            ventana.blit(proyectil_imagen, (proyectil_x, proyectil_y))
            # Agregar el proyectil a la nueva lista si no ha salido de la pantalla
            if proyectil_x < WIDTH:
                nuevos_proyectiles.append(proyectil)
        
        proyectiles = nuevos_proyectiles

        proyectiles_a_eliminar = []
 
        for enemigo in enemigos:
            enemigo_imagen = enemigo[0]
            enemigo_x = enemigo[1]
            enemigo_y = enemigo[2]
            tiempo_disparo = enemigo[3]
            contador_disparo = enemigo[4]
            velocidad_individual = enemigo[5]
            direccion_individual = enemigo[6]
            
            if direccion_individual == -1:
                enemigo_y -= velocidad_individual
                if enemigo_y < 0:
                    enemigo_y = 0
                    direccion_individual = 1
            elif direccion_individual == 1:
                enemigo_y += velocidad_individual
                if enemigo_y > HEIGHT - enemigo_imagen.get_height():
                    enemigo_y = HEIGHT - enemigo_imagen.get_height()
                    direccion_individual = -1
                    
            contador_disparo += 1
            enemigo[2] = enemigo_y
            enemigo[6] = direccion_individual
            ventana.blit(enemigo_imagen, (enemigo_x, enemigo_y))

            if contador_disparo >= tiempo_disparo:
                proyectil_x = enemigo_x
                proyectil_y = enemigo_y
                proyectiles_enemigos.append([proyectil_x, proyectil_y])
                contador_disparo = 0
                tiempo_disparo = random.randint(60, 120)
    
            enemigo[4] = contador_disparo

        proyectiles_a_eliminar = []
        proyectiles_enemigos_a_eliminar = []

        for proyectil_enemigo in proyectiles_enemigos:
            proyectil_x,proyectil_y = proyectil_enemigo
            proyectil_x -= 5  # Mover el proyectil hacia la izquierda
            proyectil_enemigo[0] = proyectil_x
            ventana.blit(proyectil_imagen_enemigo, (proyectil_x, proyectil_y))
            proyectil_rect_enemigo = pygame.Rect(proyectil_x, proyectil_y, proyectil_imagen_enemigo.get_width(), proyectil_imagen_enemigo.get_height())

            if proyectil_rect_enemigo.colliderect(jugador_rect):
                proyectiles_a_eliminar.append(proyectil_enemigo)
                vidas_jugador -= 10 
                puntaje -= 5  
                sonido_colision_enemigo.play()
            
            if proyectil_x < 0:
                proyectiles_a_eliminar.append(proyectil_enemigo)

        for proyectil_enemigo in proyectiles_a_eliminar:
            if proyectil_enemigo in proyectiles_enemigos:
                proyectiles_enemigos.remove(proyectil_enemigo)
         
        enemigos_a_eliminar = []

        for proyectil in proyectiles:
            proyectil_x, proyectil_y = proyectil
            proyectil_x += 5 
            proyectil[0] = proyectil_x
            ventana.blit(proyectil_imagen, (proyectil_x, proyectil_y))
            proyectil_rect = pygame.Rect(proyectil_x, proyectil_y, proyectil_imagen.get_width(), proyectil_imagen.get_height())
            
            for enemigo in enemigos:
                enemigo_rect = pygame.Rect(enemigo[1], enemigo[2], enemigo[0].get_width(), enemigo[0].get_height())
                if proyectil_rect.colliderect(enemigo_rect):
                    proyectiles_a_eliminar.append(proyectil)
                    enemigos_a_eliminar.append(enemigo)
                    puntaje += 10  # Suma 10 puntos por eliminar un enemigo
                    sonido_colision.play()

        for proyectil in proyectiles_a_eliminar:
            if proyectil in proyectiles:
                proyectiles.remove(proyectil)

        for enemigo in enemigos_a_eliminar:
            if enemigo in enemigos:
                enemigos.remove(enemigo)

        puntaje_data = guardar_puntaje(puntaje)
        if len(enemigos) == 0 and not pantalla_ganador:
            pantalla_ganador = True
            resultado = mostrar_pantalla_ganador(ventana, ruta_ganador, WIDTH, HEIGHT, puntaje)
            sonido_ganador.play()
            puntaje = cargar_puntaje("puntaje.json")

        while pantalla_ganador:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pantalla_ganador = False
                    juego_en_ejecucion = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if resultado == "Continuar":
                        # Reiniciar el juego
                        pantalla_ganador = False
                        pantalla_pelea = False
                        fondo = generar_fondo(WIDTH, HEIGHT, ruta_fondo)
                        pygame.mixer.music.load(ruta_musica_fondo)
                        pygame.mixer.music.play(-1)
                        puntaje = 0
                        vidas_jugador = 100
                        datos = generar_enemigos(num_enemigos, ruta_enemigo, enemigo_width, enemigo_height)
                        enemigos = datos["enemigos"]
                        contador_disparo = datos["contador_disparo"]
                        tiempo_disparo = datos["tiempo_disparo"]
                    elif resultado == "Salir":
                        pantalla_ganador = False
                        juego_en_ejecucion = False

        if vidas_jugador <= 0:
            vidas_jugador = 0
            resultado = mostrar_pantalla_perdedor(ventana, ruta_perdedor, WIDTH, HEIGHT, puntaje)
            sonido_perdedor.play()
            puntaje = cargar_puntaje("puntaje.json")

        while vidas_jugador == 0:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    vidas_jugador = -1
                    juego_en_ejecucion = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if resultado == "Continuar":
                        vidas_jugador = 100
                        puntaje = 0
                        fondo = generar_fondo(WIDTH, HEIGHT, ruta_fondo)
                        pygame.mixer.music.load(ruta_musica_pelea)
                        pygame.mixer.music.play(-1)
                        enemigos = datos["enemigos"]
                        contador_disparo = datos["contador_disparo"]
                        tiempo_disparo = datos["tiempo_disparo"]
                    elif resultado == "Salir":
                        vidas_jugador = -1  # Salir del bucle y del juego
                        juego_en_ejecucion = False
                
    pygame.display.flip()

    reloj.tick(FPS)  # Control de FPS

pygame.quit()
sys.exit()
