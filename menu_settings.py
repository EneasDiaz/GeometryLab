import pygame

ancho, alto = 960, 540
FPS = 60

GREEN = (158, 240, 26)
BLACK = (0, 0, 0)
BG = (80, 80, 80)

def settings(config):

    lista_settings = ["VOLUMEN", "BRILLO", "VOLVER"]
    eleccion = 0

    volumen = config["volumen"]
    brillo  = config["brillo"]

    pygame.display.set_caption("Geometry Lab - Settings")          
    ventana = pygame.display.set_mode((ancho, alto))
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
                return None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                elif event.key == pygame.K_UP:
                    eleccion = (eleccion - 1) % len(lista_settings)

                elif event.key == pygame.K_DOWN:
                    eleccion = (eleccion + 1) % len(lista_settings)

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
                    opcion = lista_settings[eleccion]
                    if opcion == "VOLVER":
                        return {"volumen": volumen,"brillo": brillo}

        ventana.blit(fondo, (0, 0))
        ventana.blit(titulo, ubic_titulo)

        top_list = alto // 2 + 50
        gap = 70

        largo_barra = 300
        alto_barra = 10
        barra_color_bg = BG
        barra_color_select = GREEN
        barra_color_activ = (120, 200, 120)

        for i, label in enumerate(lista_settings):
            elegido = (i == eleccion)

            color_texto = (0, 128, 0) if elegido else (180, 180, 200)     
            list_item = fuente_items.render(label, True, color_texto)
            item_ubic = list_item.get_rect(center=(ancho // 2, top_list + i * gap))
            ventana.blit(list_item, item_ubic)


            if label == "VOLUMEN":
                valor = volumen
            elif label == "BRILLO":
                valor = brillo
            else:
                valor = None

            if valor is not None:
                bar_x = ancho // 2 - largo_barra // 2
                bar_y = item_ubic.bottom + 10

                pygame.draw.rect(ventana,barra_color_bg,(bar_x, bar_y, largo_barra, alto_barra),border_radius=4)

                relleno = int(largo_barra * (valor / 100))
                pygame.draw.rect(ventana,barra_color_select if elegido else barra_color_activ,(bar_x, bar_y, relleno, alto_barra),border_radius=4)


        oscuridad = 200 - int(200 * (brillo / 100))
        filtro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        ventana.blit(filtro, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)