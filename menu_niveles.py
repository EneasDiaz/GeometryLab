import sys
import os
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60

WHITE = (255, 255, 255)
GREEN = (158, 240, 26)
BLACK = (0, 0, 0)

def niveles(config):
    pygame.init()

    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")

    pygame.display.set_caption("Geometry Lab - Niveles")
    ventana = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Fondo
    FONDO = os.path.join(BASE, "assets", "img", "fondos", "fondo-menu.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))

    fuente_titulo = pygame.font.Font(FONT_TITLE, 70)
    fuente_item  = pygame.font.Font(FONT_LIST, 40)

    
    opciones = ["NIVEL 1", "NIVEL 2", "NIVEL 3", "VOLVER"]
    eleccion = 0

    anda = True
    while anda:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                anda = False

            elif event.type == pygame.KEYDOWN:

                
                if event.key == pygame.K_ESCAPE:
                    from menu_inicio import inicio
                    inicio(config)
                    return

                
                elif event.key == pygame.K_LEFT:
                    if eleccion in [0, 1, 2]:
                        eleccion = (eleccion - 1) % 3

                elif event.key == pygame.K_RIGHT:
                    if eleccion in [0, 1, 2]:
                        eleccion = (eleccion + 1) % 3

                
                elif event.key == pygame.K_UP:
                    if eleccion == 3:
                        eleccion = 1

                elif event.key == pygame.K_DOWN:
                    if eleccion in [0, 1, 2]:
                        eleccion = 3


                elif event.key == pygame.K_RETURN:
                    opcion = opciones[eleccion]

                    if opcion == "NIVEL 1":
                        print("Cargar nivel 1")
                    elif opcion == "NIVEL 2":
                        print("Cargar nivel 2")
                    elif opcion == "NIVEL 3":
                        print("Cargar nivel 3")
                    elif opcion == "VOLVER":
                        return


        ventana.blit(fondo, (0, 0))


        titulo = fuente_titulo.render("NIVELES", True, WHITE)
        ubic_titulo = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 5 - 30))
        ventana.blit(titulo, ubic_titulo)


        y_niveles = HEIGHT // 2 - 40

        x1 = WIDTH // 2 - 250
        x2 = WIDTH // 2
        x3 = WIDTH // 2 + 250

        coords = [(x1, y_niveles), (x2, y_niveles), (x3, y_niveles)]

        for i, (texto, (cx, cy)) in enumerate(zip(opciones[:3], coords)):
            seleccionado = (eleccion == i)
            color = GREEN if seleccionado else (180, 180, 200)

            item = fuente_item.render(texto, True, color)
            rect = item.get_rect(center=(cx, cy))
            ventana.blit(item, rect)

        seleccionado = (eleccion == 3)
        color = GREEN if seleccionado else (180, 180, 200)

        volver_item = fuente_item.render("VOLVER", True, color)
        volver_rect = volver_item.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
        ventana.blit(volver_item, volver_rect)

        brillo = config.get("brillo", 100)
        oscuridad = 200 - int(200 * (brillo / 100))
        filtro = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        ventana.blit(filtro, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    niveles(config)
