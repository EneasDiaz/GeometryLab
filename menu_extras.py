import sys
import os
import pygame
from audio import musica_menu

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


    canciones = [
        ("MENU: UNDERTALE - START MENU", (255, 180, 255), "assets/sounds/MusicaMenu/menu.mp3"),
        ("NIVEL 1: UNDERTALE - RUDER BUSTER", (255, 120, 200), "assets/sounds/Lvl1/Ruder_Buster.mp3"),
        ("NIVEL 2: UNDERTALE - ASGORE ", (100, 200, 255), "assets/sounds/Lvl2/ASGORE.mp3"),
        ("NIVEL 3: UNDERTALE - HOPES AND DREAMS", (120, 120, 255), "assets/sounds/Lvl3/Hopes_and_Dreams.mp3"),
    ]

    NUM_OPCIONES = len(canciones) + 1

    eleccion = 0
    pista_actual = None

    anda = True
    while anda:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                anda = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    musica_menu(config)
                    return

                elif event.key == pygame.K_UP:
                    eleccion = (eleccion - 1) % NUM_OPCIONES

                elif event.key == pygame.K_DOWN:
                    eleccion = (eleccion + 1) % NUM_OPCIONES

                elif event.key == pygame.K_RETURN:

                    if eleccion == len(canciones):
                        if pygame.mixer.get_init():
                            pygame.mixer.music.stop()
                        musica_menu(config)
                        return

        if eleccion < len(canciones):
            if eleccion != pista_actual:
                texto, color, ruta_mp3 = canciones[eleccion]
                try:
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    pygame.mixer.music.load(ruta_mp3)
                    pygame.mixer.music.set_volume(config.get("volumen", 100) / 100)
                    pygame.mixer.music.play(-1)
                    pista_actual = eleccion
                except Exception as e:
                    print(f"Error cargando {ruta_mp3}: {e}")
            pass


        ventana.blit(fondo, (0, 0))

        titulo = fuente_titulo.render("CANCIONES", True, WHITE)
        ubic_titulo = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 5 - 30))
        ventana.blit(titulo, ubic_titulo)

        top_info = HEIGHT // 2 - 130


        for i, (texto, color, _) in enumerate(canciones):
            seleccionado = (eleccion == i)
            color_texto = GREEN if seleccionado else color

            item = fuente_texto.render(texto, True, color_texto)
            rect = item.get_rect(center=(WIDTH // 2, top_info + i * 60))
            ventana.blit(item, rect)


        idx_volver = len(canciones)
        seleccionado_volver = (eleccion == idx_volver)
        color_item = GREEN if seleccionado_volver else (180, 180, 200)

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