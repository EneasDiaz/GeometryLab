import pygame
import sys
from menu_inicio import inicio
from menu_settings import settings

def main():
    pygame.init()
    pygame.mixer.init()

    config = {
        "volumen": 50,
        "brillo": 75,
    }

    pygame.mixer.music.load("assets/sounds/menu.mp3")
    pygame.mixer.music.set_volume(config["volumen"] / 100)
    pygame.mixer.music.play(-1)

    anda = True
    while anda:
        accion = inicio(config)

        if accion == "SETTINGS":
            config = settings(config)
            if config is None:
                anda = False
                break
            pygame.mixer.music.set_volume(config["volumen"] / 100) 

        elif accion == "NIVELES":
            print("ir a seleccionar nivel (después hacemos menu_niveles)")

        elif accion == "CREADORES":
            print("mostrar créditos / creadores")

        elif accion == "SALIR":
            anda = False

    pygame.quit()
    sys.exit()
en_suelo = True
vel_y = 0
gravedad = 1
fuerza_salto = 20

if __name__ == "__main__":
    main()
