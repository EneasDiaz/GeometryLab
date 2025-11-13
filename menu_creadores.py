import sys
import pygame
import os

WIDTH, HEIGHT = 960, 540
FPS = 60

WHITE = (255, 255, 255)
GREEN = (158, 240, 26)

SKY_BLUE = (34, 130, 156)
BLUE = (30, 60, 140)
PURPLE = (80, 20, 180)
PINK = (153, 46, 157)

def creadores(config):
    pygame.init()

    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")

    pygame.display.set_caption("Geometry Lab - Creadores")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    FONDO = os.path.join(BASE, "assets", "img", "fondos", "menucam.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))

    letra_grande = pygame.font.Font(FONT_TITLE, 63)
    letra_chica  = pygame.font.Font(FONT_LIST, 28)


    opciones = ["VOLVER"]
    eleccion = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_UP:
                    eleccion = 0

                if event.key == pygame.K_DOWN:
                    eleccion = 0

                if event.key == pygame.K_RETURN:
                    return

        screen.blit(fondo, (0, 0))

        titulo_creadores = letra_grande.render("CREADORES", True, WHITE)
        r_titulo = titulo_creadores.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(titulo_creadores, r_titulo)


        joaco = letra_chica.render("JOACO  CAVALLARO  ASENSIO", True, PURPLE)
        r_joaco = joaco.get_rect(center=(WIDTH // 2 - 190, HEIGHT // 2 - 150))
        screen.blit(joaco, r_joaco)

        eneas = letra_chica.render("ENEAS DIAZ", True, PINK)
        r_eneas = eneas.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 - 200))
        screen.blit(eneas, r_eneas)

        dago = letra_chica.render("DAGO FONTANELLA TARDICO", True, SKY_BLUE)
        r_dago = dago.get_rect(center=(WIDTH // 2 + 180, HEIGHT // 2 - 95))
        screen.blit(dago, r_dago)

        ale = letra_chica.render("ALEJANDRO OLIVERO", True, BLUE)
        r_ale = ale.get_rect(center=(WIDTH // 2 + 180, HEIGHT // 2 + 135))
        screen.blit(ale, r_ale)

        juan = letra_chica.render("JUAN URIARTE", True, PINK)
        r_juan = juan.get_rect(center=(WIDTH // 2 - 190, HEIGHT // 2 + 110))
        screen.blit(juan, r_juan)


        seleccionado = (eleccion == 0)
        color = GREEN if seleccionado else WHITE

        volver = letra_chica.render("VOLVER", True, color)
        r_volver = volver.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 220))
        screen.blit(volver, r_volver)


        brillo = config.get("brillo", 100)
        oscuridad = 200 - int(200 * (brillo / 100))
        filtro = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        screen.blit(filtro, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    creadores(config)
