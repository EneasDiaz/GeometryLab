import sys  
import pygame 
import os
import menu

# #Largo y Ancho 
WIDTH = 960
HEIGHT = 540  
FPS = 60  
MARGEN = 100

#Colores
WHITE = (255, 255, 255)
GREEN = (158, 240, 26)  
SKY_BLUE = (34, 130, 156)
BLUE = (30, 60, 140)
PURPLE = (80, 20, 180)
BLACK = (0, 0, 0)       
BG = (24, 24, 32)        

def submenu():
    pygame.init()

    # Para inicializacion de sonido
    pygame.mixer.init() #inicializa el motor de ruido
    pygame.mixer.music.load("assets/sounds/MusicaMenu/menu.mp3") #inicializa el motor de ruido
    pygame.mixer.music.set_volume(0.5) # ver mas adelante y mejorar el ajuste de la musica
    pygame.mixer.music.play(-1) #ciclo infinito de la musica

    # Path para las letras del juego
    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")

    # Titulo de la ventana saliente
    pygame.display.set_caption("TP Grupal")              
    screen = pygame.display.set_mode((WIDTH, HEIGHT))        
    clock = pygame.time.Clock()

    # Fondo cubitos del jeugo
    FONDO = os.path.join(BASE, "assets", "img", "fondo-menu.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()          
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))

    # Letras del juego con distintos tamanios 
    title_font = pygame.font.Font(FONT_TITLE, 70)
    medium_font = pygame.font.Font(FONT_LIST, 40)
    small_font = pygame.font.Font(FONT_LIST, 25)

    running = True
    while running:
        

        # Formato/Textos del menu/submenus
        screen.blit(fondo, (0, 0))

        title_niveles = title_font.render("NIVELES:", True, WHITE) 
        title_rect = title_niveles.get_rect(center=(WIDTH // 3 , HEIGHT // 5 - 60))
        screen.blit(title_niveles, title_rect)

        primer_nivel_titulo= medium_font.render("NIVEL 1", True, SKY_BLUE)
        hint_lvl1_rect = primer_nivel_titulo.get_rect(center=(WIDTH // 2 - 300 , HEIGHT // 2 - 60))
        screen.blit(primer_nivel_titulo, hint_lvl1_rect)

        segundo_nivel_titulo = medium_font.render("NIVEL 2", True, BLUE)
        hint_lvl2_rect = segundo_nivel_titulo.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 60))
        screen.blit(segundo_nivel_titulo, hint_lvl2_rect)

        tercer_nivel_titulo = medium_font.render("NIVEL 3", True, PURPLE)
        hint_lvl3_rect = tercer_nivel_titulo.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2 - 60))
        screen.blit(tercer_nivel_titulo, hint_lvl3_rect)

        quit_surf = small_font.render("VOLVER", True, WHITE)
        hint_volver_rect = quit_surf.get_rect(center=(WIDTH // 2 - 400, HEIGHT // 2 + 220))
        screen.blit(quit_surf, hint_volver_rect)

        setting_surf = small_font.render("OPCIONES", True, WHITE)
        hint_opciones_rect = setting_surf.get_rect(center=(WIDTH // 2 + 380, HEIGHT // 2 + 220))
        screen.blit(setting_surf, hint_opciones_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    if hint_lvl1_rect.collidepoint(event.pos):
                        print("lvl1")
                    elif hint_lvl2_rect.collidepoint(event.pos):
                        print("lvl2")
                    elif hint_lvl3_rect.collidepoint(event.pos):
                        print("lvl3")
                    elif hint_volver_rect.collidepoint(event.pos):
                        print("volver al menu")
                    elif hint_opciones_rect.collidepoint(event.pos):
                        print("config")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    submenu()




