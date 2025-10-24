import sys  
import pygame 
import os

WIDTH, HEIGHT = 960, 540  
FPS = 60  

WHITE = (158, 240, 26)  
BLACK = (0, 0, 0)       
BG = (24, 24, 32)        

def main():
    pygame.init()

    BASE = os.path.dirname(__file__)
    FONT_TITLE = os.path.join(BASE, "assets", "fonts", "ARCADE_I.TTF")
    FONT_LIST  = os.path.join(BASE, "assets", "fonts", "Pinecone-Regular.ttf")


    pygame.display.set_caption("Geometry Lab")              
    screen = pygame.display.set_mode((WIDTH, HEIGHT))        
    clock = pygame.time.Clock()

    
    FONDO = os.path.join(BASE, "assets", "img", "fondo-menu.jpg")
    fondo_raw = pygame.image.load(FONDO).convert()          
    fondo = pygame.transform.smoothscale(fondo_raw, (WIDTH, HEIGHT))


    title_font = pygame.font.Font(FONT_TITLE, 72)
    small_font = pygame.font.Font(FONT_LIST, 28)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Dibujo
        screen.blit(fondo, (0, 0))

        title_surface = title_font.render("GEOMETRY LAB", True, WHITE)  # <- ¿typo?
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(title_surface, title_rect)

        niveles = small_font.render("NIVELES", True, (56, 176, 0))
        hint_rect = niveles.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(niveles, hint_rect)

        creadores = small_font.render("CREADORES", True, (56, 176, 0))
        hint_rect = creadores.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(creadores, hint_rect)

        quit_surf = small_font.render("SALIR", True, (56, 176, 0))
        hint_rect = quit_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(quit_surf, hint_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
