import sys  
import pygame 
from menu_settings import settings

ancho, alto = 960, 540
FPS = 60
GREEN = (158, 240, 26) 
BLACK = (0, 0, 0)
BG = (80, 80, 80)

def inicio():
    pygame.init()
    pygame.mixer.init()

    volumen_actual = 50
    brillo_actual  = 75

    pygame.mixer.music.load("assets/sounds/menu.mp3")
    pygame.mixer.music.set_volume(volumen_actual / 100)
    pygame.mixer.music.play(-1)

    lista_inicio = ["NIVELES", "CREADORES", "SETTING", "SALIR"] 
    eleccion = 0

    pygame.display.set_caption("Geometry Lab")
    ventana = pygame.display.set_mode((ancho, alto))
    clock = pygame.time.Clock()

    fondo_convert = pygame.image.load('assets/img/fondo-menu.jpg').convert()       
    fondo = pygame.transform.smoothscale(fondo_convert, (ancho, alto))

    fuente_titulo = pygame.font.Font('assets/fonts/ARCADE_I.TTF', 72)
    fuente_items  = pygame.font.Font('assets/fonts/Pinecone-Regular.ttf', 28)

    titulo = fuente_titulo.render("GEOMETRY LAB", True, GREEN)
    ubic_titulo = titulo.get_rect(center=(ancho // 2, alto // 2 - 40))

    anda = True
    while anda:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                anda = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    anda = False

                elif event.key == pygame.K_UP:
                    eleccion = (eleccion - 1) % len(lista_inicio)

                elif event.key == pygame.K_DOWN:
                    eleccion = (eleccion + 1) % len(lista_inicio)

                elif event.key == pygame.K_RETURN:
                    opcion = lista_inicio[eleccion]

                    if opcion == "NIVELES":
                        print("Entrar a NIVELES...")

                    elif opcion == "CREADORES":
                        print("Mostrar CREADORES...")

                    elif opcion == "SETTING":
                        volumen_actual, brillo_actual = settings(volumen_actual, brillo_actual)

                    elif opcion == "SALIR":
                        anda = False


        ventana.blit(fondo, (0, 0))
        ventana.blit(titulo, ubic_titulo)


        top_list = alto // 2 + 50
        gap = 50


        for i, label in enumerate(lista_inicio):
            elegido = (i == eleccion)
            color = (0, 128, 0) if elegido else (180, 180, 200)       
            list_item = fuente_items.render(label, True, color)
            item_ubic = list_item.get_rect(center=(ancho // 2, top_list + i * gap))
            ventana.blit(list_item, item_ubic)


        oscuridad = 200 - int(200 * (brillo_actual / 100))
        filtro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        ventana.blit(filtro, (0, 0))


        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    inicio()
