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

def main():
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
    
    FONDO = os.path.join(BASE, "assets", "img", "menucam.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()          
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))

    letra_grande = pygame.font.Font(FONT_TITLE, 63)
    letra_chica = pygame.font.Font(FONT_LIST, 28)

    running = True
    while running:
        
        # Dibujo
        screen.blit(fondo, (0, 0))

        canciones = letra_grande.render("CANCIONES: ", True, WHITE)
        hint_canciones_rect = canciones.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 200))
        screen.blit(canciones, hint_canciones_rect)

        cancion_1 = letra_chica.render("MENU: UNDERTALE - START MENU", True, PURPLE)
        hint_cancion_1_rect = cancion_1.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 120))
        screen.blit(cancion_1, hint_cancion_1_rect)

        cancion_2 = letra_chica.render("NIVEL 1: UNDERTALE - HOPES AND DREAMS", True, PINK)
        hint_cancion_2_rect = cancion_2.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 60))
        screen.blit(cancion_2, hint_cancion_2_rect)

        creador_dago = letra_chica.render("NIVEL 2: UNDERTALE - RUDY BUSTER", True, SKY_BLUE)
        hint_creador_dago_rect = creador_dago.get_rect(center=(WIDTH // 2 , HEIGHT // 2 ))
        screen.blit(creador_dago, hint_creador_dago_rect)

        creador_ale = letra_chica.render("NIVEL 3: UNDERTALE - ASGORE", True, BLUE)
        hint_creador_ale_rect = creador_ale.get_rect(center=(WIDTH // 2 , HEIGHT // 2 + 70))
        screen.blit(creador_ale, hint_creador_ale_rect)

        volver = letra_chica.render("VOLVER", True, WHITE)
        hint_volver_rect = volver.get_rect(center=(WIDTH // 2 - 400, HEIGHT // 2 + 220))
        screen.blit(volver, hint_volver_rect)

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
    

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
