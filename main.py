import pygame
import sys
import random

pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Lab")


NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)


reloj = pygame.time.Clock()

jugador = pygame.Rect(50, 500, 50, 50)  # x, y, ancho, alto
piso = pygame.Rect(0, 550, 800, 50)
obstaculo = pygame.Rect(800, 500, 50, 50)
vel = 5


pygame.quit()
sys.exit()
en_suelo = True
vel_y = 0
gravedad = 1
fuerza_salto = 20


while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()


    if teclas[pygame.K_SPACE] and en_suelo:
        vel_y = -fuerza_salto
        en_suelo = False


    vel_y += gravedad
    jugador.y += vel_y
    jugador.x += vel


    if jugador.bottom >= ALTO - 50:
        jugador.bottom = ALTO - 50
        vel_y = 0
        en_suelo = True



    if obstaculo.right < 0:
        obstaculo.x = ANCHO + random.randint(100, 300)

    if jugador.colliderect(obstaculo):
        print("💥 ¡Colisión! Reiniciando obstáculo...")
        obstaculo.x = ANCHO + random.randint(100, 300)

    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, AZUL, jugador)
    pygame.draw.rect(pantalla, ROJO, obstaculo)
    pygame.draw.rect(pantalla, BLANCO, piso)
    pygame.display.flip()


    reloj.tick(60)
