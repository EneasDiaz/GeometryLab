import sys
import os
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60

WHITE = (255, 255, 255)
GREEN = (158, 240, 26)
BLACK = (0, 0, 0)

def extras(config):
    pygame.init()

    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")

    pygame.display.set_caption("Geometry Lab - Extras")
    ventana = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Fondo
    FONDO = os.path.join(BASE, "assets", "img", "fondos", "menucam.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))

    fuente_titulo = pygame.font.Font(FONT_TITLE, 63)
    fuente_texto  = pygame.font.Font(FONT_LIST, 28)


    opciones = ["VOLVER"]
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

                elif event.key == pygame.K_UP:
                    eleccion = (eleccion - 1) % len(opciones)

                elif event.key == pygame.K_DOWN:
                    eleccion = (eleccion + 1) % len(opciones)

                elif event.key == pygame.K_RETURN:
                    opcion = opciones[eleccion]

                    if opcion == "VOLVER":
                        return


        ventana.blit(fondo, (0, 0))


        titulo = fuente_titulo.render("CANCIONES", True, WHITE)
        ubic_titulo = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 5 - 30))
        ventana.blit(titulo, ubic_titulo)


        labels = [
            ("MENU: UNDERTALE - START MENU", (255, 180, 255)),
            ("NIVEL 1: UNDERTALE - HOPES AND DREAMS", (255, 120, 200)),
            ("NIVEL 2: UNDERTALE - RUDY BUSTER", (100, 200, 255)),
            ("NIVEL 3: UNDERTALE - ASGORE", (120, 120, 255)),
        ]

        top_info = HEIGHT // 2 - 130
        for i, (texto, color) in enumerate(labels):
            item = fuente_texto.render(texto, True, color)
            rect = item.get_rect(center=(WIDTH // 2, top_info + i * 60))
            ventana.blit(item, rect)


        seleccionado = (eleccion == 0)
        color_item = GREEN if seleccionado else (180, 180, 200)

        volver = fuente_texto.render("VOLVER", True, color_item)
        rect_volver = volver.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 180))
        ventana.blit(volver, rect_volver)


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
    extras(config)
