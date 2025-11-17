import pygame

def musica_menu(config, forzar=False):
    volumen = config.get("volumen", 100) / 100

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    if forzar or not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("assets/sounds/MusicaMenu/menu.mp3")
        pygame.mixer.music.play(-1)


    pygame.mixer.music.set_volume(volumen)