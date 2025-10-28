import pygame 
import sys

ancho, alto = 960, 540  
FPS = 60  

GREEN = (158, 240, 26)  
BLACK = (0, 0, 0)       
BG = (24, 24, 32)   

def settings(volumen_inicial, brillo_inicial):
    
    pygame.init()
    pygame.mixer.init()

    lista_menu = ["VOLUMEN", "BRILLO", "VOLVER"]  
    eleccion = 0

    volumen = volumen_inicial   
    brillo  = brillo_inicial

    pygame.display.set_caption("Geometry Lab - Settings")              
    screen = pygame.display.set_mode((ancho, alto))        
    clock = pygame.time.Clock()

    fondo_convert = pygame.image.load('assets/img/fondo-menu.jpg').convert()          
    fondo = pygame.transform.smoothscale(fondo_convert, (ancho, alto))

    fuente_titulo = pygame.font.Font('assets/fonts/ARCADE_I.TTF', 72)
    fuente_items  = pygame.font.Font('assets/fonts/Pinecone-Regular.ttf', 28)

    titulo = fuente_titulo.render("SETTINGS", True, GREEN) 
    ubic_titulo = titulo.get_rect(center=(ancho // 2, alto // 2 - 40))

    anda = True
    while anda:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    anda = False 

                elif event.key == pygame.K_UP:
                    eleccion = (eleccion - 1) % len(lista_menu)  

                elif event.key == pygame.K_DOWN:
                    eleccion = (eleccion + 1) % len(lista_menu) 

                elif event.key == pygame.K_LEFT:
                    if eleccion == 0:
                        volumen = max(0, volumen - 5)
                        pygame.mixer.music.set_volume(volumen / 100)
                    elif eleccion == 1:
                        brillo = max(0, brillo - 5)

                elif event.key == pygame.K_RIGHT:
                    if eleccion == 0:    
                        volumen = min(100, volumen + 5)
                        pygame.mixer.music.set_volume(volumen / 100)
                    elif eleccion == 1:    
                        brillo = min(100, brillo + 5)

                elif event.key == pygame.K_RETURN:
                    opcion = lista_menu[eleccion]
                    if opcion == "VOLVER":
                        anda = False  #


        screen.blit(fondo, (0, 0))
        screen.blit(titulo, ubic_titulo)

        top_list = alto // 2 + 50
        gap = 70

        bar_width_total = 300      
        bar_height = 10             
        bar_color_bg = (80, 80, 80)   
        bar_color_fg_sel = GREEN
        bar_color_fg_dim = (120, 200, 120)

        for i, label in enumerate(lista_menu):
            elegido = (i == eleccion)

            color_texto = (0, 128, 0) if elegido else (180, 180, 200)          
            list_item = fuente_items.render(label, True, color_texto)
            item_ubic = list_item.get_rect(center=(ancho // 2, top_list + i * gap))
            screen.blit(list_item, item_ubic)


            if label == "VOLUMEN":
                valor = volumen
            elif label == "BRILLO":
                valor = brillo
            else:
                valor = None

            if valor is not None:
                bar_x = ancho // 2 - bar_width_total // 2
                bar_y = item_ubic.bottom + 10  

                pygame.draw.rect(
                    screen,
                    bar_color_bg,
                    (bar_x, bar_y, bar_width_total, bar_height),
                    border_radius=4
                )

                fill_width = int(bar_width_total * (valor / 100))
                pygame.draw.rect(
                    screen,
                    bar_color_fg_sel if elegido else bar_color_fg_dim,
                    (bar_x, bar_y, fill_width, bar_height),
                    border_radius=4
                )


        oscuridad = 200 - int(200 * (brillo / 100))
        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, oscuridad))
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


    return volumen, brillo
