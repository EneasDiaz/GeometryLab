import sys  
import pygame 


def musica_menu(config):
    volumen = config.get("volumen", 100) / 100

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load("assets/sounds/MusicaMenu/menu.mp3")
    pygame.mixer.music.play(-1)

    

    pygame.mixer.music.set_volume(volumen)

