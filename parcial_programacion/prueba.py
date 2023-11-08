import pygame
import random

# Inicializa Pygame
pygame.init()

# Define las dimensiones de la ventana
ancho_ventana = 800
alto_ventana = 600

# Crea la ventana
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Movimiento de Cuadrados")

# Define los colores
color_cuadrado = (0, 128, 255)

# Crea una lista de cuadrados con posiciones, velocidades y direcciones aleatorias
cuadrados = []
for _ in range(5):
    tamano = 50
    x = random.randint(0, ancho_ventana - tamano)
    y = random.randint(0, alto_ventana - tamano)
    velocidad = random.randint(1, 10)
    direccion = random.choice([-1, 1])
    cuadrados.append((x, y, tamano, velocidad, direccion))

# Configura un reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Borra la ventana
    ventana.fill((0, 0, 0))

    # Mueve y dibuja los cuadrados
    nuevos_cuadrados = []
    for x, y, tamano, velocidad, direccion in cuadrados:
        if direccion == -1:
            y -= velocidad
            if y < 0:
                y = 0
                direccion = 1
        else:
            y += velocidad
            if y > alto_ventana - tamano:
                y = alto_ventana - tamano
                direccion = -1
        nuevos_cuadrados.append((x, y, tamano, velocidad, direccion))
    cuadrados = nuevos_cuadrados

    # Dibuja los cuadrados
    for x, y, tamano, _, _ in cuadrados:
        pygame.draw.rect(ventana, color_cuadrado, (x, y, tamano, tamano))

    # Actualiza la ventana
    pygame.display.flip()

    # Limita la velocidad de fotogramas
    reloj.tick(30)

# Cierra Pygame
pygame.quit()
