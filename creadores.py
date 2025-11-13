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
BLACK = (0, 0, 0)       
BG = (24, 24, 32)

def nosotros(config):
    pygame.init()
    
    # Para inicializacion de sonido
    pygame.mixer.init() #inicializa el motor de ruido
    pygame.mixer.music.load("assets/sounds/MusicaMenu/menu.mp3") #inicializa el motor de ruido
    pygame.mixer.music.set_volume(0.5) # ver mas adelante y mejorar el ajuste de la musica
    pygame.mixer.music.play(-1) #ciclo infinito de la musica

    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")


    pygame.display.set_caption("TP Grupal")              
    screen = pygame.display.set_mode((WIDTH, HEIGHT))        
    clock = pygame.time.Clock()

    
    FONDO = os.path.join(BASE, "assets", "img", "fondos","menucam.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()          
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))


    letra_grande = pygame.font.Font(FONT_TITLE, 63)
    letra_chica = pygame.font.Font(FONT_LIST, 28)

    running = True
    while running:
        
        # Dibujo
        screen.blit(fondo, (0, 0))

        creadores = letra_grande.render("CREADORES", True, WHITE)
        hint_creadores_rect = creadores.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
        screen.blit(creadores, hint_creadores_rect)

        creador_joaco = letra_chica.render("JOACO  CAVALLARO  ASENSIO", True, PURPLE)
        hint_creador_joaco_rect = creador_joaco.get_rect(center=(WIDTH // 2 - 190, HEIGHT // 2 - 150))
        screen.blit(creador_joaco, hint_creador_joaco_rect)

        creador_eneas = letra_chica.render("ENEAS DIAZ", True, PINK)
        hint_creador_eneas_rect = creador_eneas.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 - 200))
        screen.blit(creador_eneas, hint_creador_eneas_rect)

        creador_dago = letra_chica.render("DAGO FONTANELLA TARDICO", True, SKY_BLUE)
        hint_creador_dago_rect = creador_dago.get_rect(center=(WIDTH // 2 + 180, HEIGHT // 2 - 95))
        screen.blit(creador_dago, hint_creador_dago_rect)

        creador_ale = letra_chica.render("ALEJANDRO OLIVERO", True, BLUE)
        hint_creador_ale_rect = creador_ale.get_rect(center=(WIDTH // 2 + 180, HEIGHT // 2 + 135))
        screen.blit(creador_ale, hint_creador_ale_rect)

        creador_juan = letra_chica.render("JUAN URIARTE", True, PINK)
        hint_creador_juan_rect = creador_juan.get_rect(center=(WIDTH // 2 - 190, HEIGHT // 2 + 110))
        screen.blit(creador_juan, hint_creador_juan_rect)

        volver = letra_chica.render("VOLVER", True, WHITE)
        hint_volver_rect = volver.get_rect(center=(WIDTH // 2 - 400, HEIGHT // 2 + 220))
        screen.blit(volver, hint_volver_rect)

        musica = letra_chica.render("MUSICA", True, WHITE)
        hint_musica_rect = musica.get_rect(center=(WIDTH // 2 + 380, HEIGHT // 2 + 220))
        screen.blit(musica, hint_musica_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    if hint_volver_rect.collidepoint(event.pos):
                        print("Volvio al menu")
                    if hint_musica_rect.collidepoint(event.pos):
                        print("Entro a la seccion de canciones")
    

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    config = {"brillo": 100, "volumen":100}
    nosotros(config)
