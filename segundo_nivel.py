import pygame
from pygame.locals import *
import sys

pygame.init() 
pygame.mixer.init() 



def el_nivel_2(config):
    nivel_terminado = False

    NOMBRE_ARCHIVO_MUSICA = "assets_nivel1/ASGORE.mp3" 
    try:
        pygame.mixer.music.load(NOMBRE_ARCHIVO_MUSICA) 
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(0.5) 
        print(f"ÉXITO: '{NOMBRE_ARCHIVO_MUSICA}' cargada y reproduciéndose.")
    except pygame.error as e:
        print(f"ATENCIÓN: Error al cargar o reproducir la música: {e}")

    vec = pygame.math.Vector2 
    HEIGHT = 450
    WIDTH = 900
    ACC = 0.5
    FRIC = -0.12
    FPS = 60

    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    #Cargar Fondo
    try:
        fondo = pygame.image.load("assets_nivel1/fondo2.jpg").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
        fondo_ok = True
    except pygame.error as e:
        print(f"ATENCIÓN: No se pudo cargar la imagen de fondo: {e}. Usando color sólido.")
        fondo = None
        fondo_ok = False

    # --------------------------- CLASES ---------------------------
    class portal_cohete(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=40):
            super().__init__()
            imagen = pygame.image.load("assets_nivel1/portal.png").convert_alpha()
            imagen = pygame.transform.scale(imagen, (80, 80))
            self.surf = imagen
            self.rect = self.surf.get_rect(topleft=(x, y))

    class portal_cubo(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=40):
            super().__init__()
            imagen = pygame.image.load("assets_nivel1/portal.png").convert_alpha()
            imagen = pygame.transform.scale(imagen, (80, 80))
            self.surf = imagen
            self.rect = self.surf.get_rect(topleft=(x, y))

    class GravityBlock(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=40, image_path="assets_nivel1/diamante.png"):
            super().__init__()
            self.surf = pygame.image.load(image_path).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
            self.rect = self.surf.get_rect(topleft=(x, y))

    class Spike(pygame.sprite.Sprite):
        def __init__(self, x, y, width=40, height=40, direction=None):
            super().__init__()
            self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
            rojo_claro = (255, 100, 100)
            # Si no se pasa dirección, intentar deducir por y
            if direction is None:
                if y < 200:  
                    direction = "down"
                else:
                    direction = "up"
            # Dibujar triángulo según dirección
            if direction == "up":
                pygame.draw.polygon(self.surf, rojo_claro, [(0, height), (width/2, 0), (width, height)])
            elif direction == "down":
                pygame.draw.polygon(self.surf, rojo_claro, [(0, 0), (width/2, height), (width, 0)])
            self.rect = self.surf.get_rect(topleft=(x, y))

    class JumpPad(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=10):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((0, 0, 255)) # Color Azul
            self.rect = self.surf.get_rect(topleft=(x, y))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            try:
                imagen = pygame.image.load('assets_nivel1/skin_geometrydash.jpg').convert_alpha() 
                self.surf = pygame.transform.scale(imagen, (30, 30))
            except pygame.error as e:
                print(f"ATENCIÓN: Error al cargar la imagen del cubo: {e}. Usando color de respaldo.")
                # Color de respaldo si la imagen falla
                self.surf = pygame.Surface((30, 30))
                self.surf.fill((128,255,40)) 

            self.rect = self.surf.get_rect(center = (10, 420))
            self.pos = vec((10, 385))
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.saltable = False
            self.inverted = False 
            self.modo_cohete = False 

        def move(self):
            self.vel.x = 8
            # GRAVEDAD DINÁMICA / MOVIMIENTO COHETE 
            if self.modo_cohete:
                self.vel.y += 0.23 
                mouse = pygame.mouse.get_pressed()
                if mouse[2]: 
                    self.vel.y -= 0.28 
                self.rect.midbottom = self.pos 
            elif self.inverted:
                self.vel.y -= 0.23 
            else:
                self.vel.y += 0.23 
            self.pos += self.vel 
            
            #REORIENTACIÓN DEL CUBO 
            if not self.modo_cohete:
                if self.inverted:
                    self.rect.midtop = self.pos 
                else:
                    self.rect.midbottom = self.pos 

        def update(self):
            global portales_cohete, portales_cubo 

            #ACTIVACIÓN DEL COHETE 
            cohete_hit = pygame.sprite.spritecollideany(self, portales_cohete)
            if cohete_hit:
                self.modo_cohete = True
                self.inverted = False 
                self.vel.y = 0 
                cohete_hit.kill() 
            
            #LÓGICA DE SALIDA DEL COHETE (VUELTA AL CUBO) 
            cubo_hit = pygame.sprite.spritecollideany(self, portales_cubo)
            if cubo_hit:
                self.modo_cohete = False
                self.inverted = False 
                self.vel.y = 0 
                cubo_hit.kill() 

            hits = pygame.sprite.spritecollide(self, platforms, False)
            
            #LÓGICA DE ATERRIZAJE 
            if not self.modo_cohete:
                if self.inverted:
                    if self.vel.y < 0:
                        if hits:
                            self.pos.y = hits[0].rect.bottom - 1 
                            self.vel.y = 0
                            self.saltable = True
                        else:
                            self.saltable = False
                else:
                    if self.vel.y > 0: 
                        if hits:
                            self.pos.y = hits[0].rect.top + 1
                            self.vel.y = 0
                            self.saltable = True
                        else:
                            self.saltable = False
            else:
                self.saltable = True 

        def jump(self):
            if not self.modo_cohete: # Solo el cubo puede saltar (el cohete usa el mouse en move())
                if self.saltable:
                    jump_force = 5 if self.inverted else -5 
                    self.vel.y = jump_force
                    self.saltable = False
                
        def salto(self): 
            self.jump() 

    class platform(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            pygame.sprite.Sprite.__init__(self)
            try:
                self.surf = pygame.image.load("assets_nivel1/plataforma.jpg").convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (w, h))
            except:
                self.surf = pygame.Surface((w, h))
                self.surf.fill((0, 255, 0))

            self.rect = self.surf.get_rect(topleft=(x, y))
            # Spike invisible 
            spike_width = 5  
            self.left_spike = pygame.Rect(x - spike_width, y, spike_width, h)

        def check_collision(self, player_rect):
            if self.rect.colliderect(player_rect):
                return "platform"  
            elif self.left_spike.colliderect(player_rect):
                return "spike_left" 
            return None
        
    class Meta(pygame.sprite.Sprite):
        def __init__(self, x, y, size=40):
            super().__init__()
            self.surf = pygame.Surface((size, size))
            self.surf.fill((255, 255, 255))  
            self.rect = self.surf.get_rect(topleft=(x, y))

    # --------------------------- GRUPOS Y OBJETOS ---------------------------
    platforms = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    jump_pads = pygame.sprite.Group() 
    gravity_blocks = pygame.sprite.Group() 
    portales_cohete = pygame.sprite.Group() 
    portales_cubo = pygame.sprite.Group() 
    meta_group = pygame.sprite.Group()
    meta_final = Meta(51500, 310)  
    meta_group.add(meta_final)
    all_sprites.add(meta_final)   

    # Segmento 1 del piso: Va de X=0 a X=4000
    platforms.add(platform(0, HEIGHT - 20, 4900, 20)) 
    platforms.add(platform(600, 380, 100, 20))#1
    platforms.add(platform(900, 350, 340, 20))#2
    platforms.add(platform(1300, 380, 100, 20))#3
    platforms.add(platform(1800, 180, 60, 20))#4
    platforms.add(platform(1800, 120, 60, 20))#4
    platforms.add(platform(2120, 300, 60, 20))#5
    platforms.add(platform(2420, 380, 60, 20))#6
    platforms.add(platform(2900, 365, 60, 20))#7 salta desde piso
    platforms.add(platform(3200, 365, 470, 20))#8 plataforma continua techo
    platforms.add(platform(3900, 385, 470, 20))#9 plataforma continua techo,sube
    platforms.add(platform(4400, 350, 520, 20))#10 Aquiiiiiiiiiiiiiiiiiiiiii
    platforms.add(platform(5200, 330, 150, 20))#11
    platforms.add(platform(5600, 330, 150, 20))#12
    platforms.add(platform(6000, 330, 150, 20))#13
    platforms.add(platform(6400, 330, 150, 20))#14
    platforms.add(platform(6800, 330, 150, 20))#15
    platforms.add(platform(6700, 385, 300, 20))#16 plataforma debajo de otra
    platforms.add(platform(7500, 270, 150, 20))#17
    platforms.add(platform(8150, 180, 50, 20))#18
    platforms.add(platform(8300, 210, 50, 20))#19
    platforms.add(platform(8450, 240, 50, 20))#20
    platforms.add(platform(8600, 270, 90, 20))#21
    platforms.add(platform(8750, 300, 60, 20))#22
    platforms.add(platform(8900, 270, 1100, 20))#23
    platforms.add(platform(10200, 320, 50, 20))#24
    platforms.add(platform(10500, 280, 50, 20))#25
    platforms.add(platform(10800, 240, 50, 20))#26
    platforms.add(platform(11100, 200, 400, 20))#27
    platforms.add(platform(11600, 250, 400, 20))#28
    platforms.add(platform(12100, 200, 400, 20))#29
    platforms.add(platform(12600, 100, 600, 20))#30
    platforms.add(platform(13300, 140, 400, 20))#31
    platforms.add(platform(13800, 170, 600, 20))#32
    platforms.add(platform(13800, 250, 400, 20))#32
    platforms.add(platform(14600, 220, 50, 20))#33
    platforms.add(platform(14900, 260, 50, 20))#34
    platforms.add(platform(15200, 300, 50, 20))#35
    platforms.add(platform(16000, 350, 50, 20))#36
    platforms.add(platform(16300, 310, 50, 20))#37
    platforms.add(platform(16600, 270, 200, 20))#38
    platforms.add(platform(17000, 100, 2400, 20))# Pasillo Techo superior
    platforms.add(platform(17000, 380, 2400, 20))# Pasillo Suelo inferior
    platforms.add(platform(32750, 380, 700, 20))#39
    #Saltos Medios espaciados.
    platforms.add(platform(33750, 380, 80, 20))#40
    platforms.add(platform(34050, 330, 80, 20))#41
    platforms.add(platform(34300, 280, 80, 20))#42
    platforms.add(platform(34700, 280, 80, 20))#43: Plataforma Alta 
    platforms.add(platform(35150, 350, 100, 20))#44: Tierra 
    platforms.add(platform(35500, 290, 60, 20))#45: Plataforma Alta 
    platforms.add(platform(35900, 370, 100, 20))#46: Mini-Plat 1
    platforms.add(platform(36200, 320, 80, 20))#47: Mini-Plat 2
    platforms.add(platform(36500, 270, 80, 20))#48: Mini-Plat 3
    platforms.add(platform(36700, 320, 80, 20))#49: Mini-Plat 4
    platforms.add(platform(36850, 380, 450, 20))#50: Plataforma Larga 
    platforms.add(platform(37500, 330, 80, 20))#51: Caída 1
    platforms.add(platform(37800, 290, 80, 20))#52: Caída 2
    platforms.add(platform(38100, 240, 80, 20))#53: Caída 3 (Punto más alto)
    platforms.add(platform(38550, 310, 70, 20))#54
    platforms.add(platform(39000, 380, 100, 20))#56
    platforms.add(platform(39300, 330, 100, 20))#57
    platforms.add(platform(39600, 280, 100, 20))#58
    platforms.add(platform(39900, 250, 400, 20))#59 
    platforms.add(platform(40400, 220, 200, 20))#60
    platforms.add(platform(40800, 190, 200, 20))#61
    platforms.add(platform(41200, 160, 500, 20))#62
    platforms.add(platform(41900, 200, 5700, 20))#63: Al principio pinchos
    platforms.add(platform(42800, 140, 1700, 20))#64
    platforms.add(platform(44700, 70, 2800, 20))#65
    platforms.add(platform(47800, 150, 200, 20))#66
    platforms.add(platform(48300, 170, 200, 20))#67
    platforms.add(platform(48700, 190, 400, 20))#68
    platforms.add(platform(49300, 270, 1400, 20))#69
    platforms.add(platform(50900, 310, 300, 20))#70

    # --- PINCHOS EN ONDAS REPETITIVAS (GENERADOS POR BUCLE) ---
    NUM_ONDAS = 6 # Número de veces que se repite el patrón
    ANCHO_ONDA = 600 # Ancho horizontal de una onda 
    POSICION_INICIO_X = 20450 

    for i in range(NUM_ONDAS):
        # Calcula el desplazamiento horizontal para esta repetición
        OFFSET_X = POSICION_INICIO_X + i * ANCHO_ONDA

        # 1. Segmento superior (Sube y Baja)
        platforms.add(platform(OFFSET_X + 0, 180, 100, 20)) # Base izquierda (Y=180)
        platforms.add(platform(OFFSET_X + 100, 130, 100, 20)) # Sube 1
        platforms.add(platform(OFFSET_X + 200, 80, 100, 20)) # Sube 2 (Pico superior - Y=80)
        platforms.add(platform(OFFSET_X + 300, 80, 100, 20)) # Meseta superior
        platforms.add(platform(OFFSET_X + 400, 130, 100, 20)) # Baja 1
        platforms.add(platform(OFFSET_X + 500, 180, 100, 20)) # Baja 2 (llega al nivel inicial)
        # 2. Segmento inferior (Baja y Sube, en espejo)
        platforms.add(platform(OFFSET_X + 50, 420, 100, 20))  # Base izquierda inferior (Y=420)
        platforms.add(platform(OFFSET_X + 150, 370, 100, 20)) # Baja 1 inferior
        platforms.add(platform(OFFSET_X + 250, 320, 100, 20)) # Baja 2 (Valle inferior - Y=320)
        platforms.add(platform(OFFSET_X + 350, 320, 100, 20)) # Meseta inferior
        platforms.add(platform(OFFSET_X + 450, 370, 100, 20))# Sube 1 inferior
        platforms.add(platform(OFFSET_X + 550, 420, 100, 20)) # Sube 2 (llega al nivel inicial)

    # --- PILARES VERTICALES CON PATRÓN FIJO, EXTENDIDO A 60 PILARES ---
    NUM_PILARES = 60 # 🚨 EXTENSIÓN: El doble de longitud
    ESPACIO_ENTRE_PILARES = 80 
    POSICION_INICIO_PILAR_X = 24500 
    ANCHO_PILAR = 20 
    HEIGHT = 450 

    ALTURAS_PILAR = [
        80, # Pasaje MUY Ancho (370px libre)
        120, # Pasaje Ancho (310px libre)
        150, # Pasaje Medio (250px libre) <-- Máximo obstáculo
        150, # Pasaje Medio (250px libre)
        120, # Pasaje Ancho (310px libre)
        80, # Pasaje MUY Ancho (370px libre)
    ]
    NUM_PATRONES = len(ALTURAS_PILAR)

    for i in range(NUM_PILARES):
        
        OFFSET_X = POSICION_INICIO_PILAR_X + i * ESPACIO_ENTRE_PILARES
        ALTURA = ALTURAS_PILAR[i % NUM_PATRONES]
        # Generar el pilar 
        if i % 2 == 0:
            platforms.add(platform(
                OFFSET_X, 
                0, # Empieza en el techo
                ANCHO_PILAR, 
                ALTURA 
            ))
        else:
            # Pila impar: Levantado del SUELO
            platforms.add(platform(
                OFFSET_X, 
                HEIGHT - ALTURA, 
                ANCHO_PILAR, 
                ALTURA 
            ))

    # --- DEFINICIÓN DE VARIABLES PARA PLATAFORMAS HORIZONTALES ---
    NUM_PLAT_HORIZONTALES = 20
    POSICION_INICIO_HORIZONTALES_X = 29300
    LARGO_PLAT = 50
    ALTO_PLAT = 20
    ESPACIO_X = 150 # Espacio horizontal entre el inicio de cada plataforma

    ALTURAS_Y = [
        100, # Superior, cerca del techo
        180, # Medio-Superior
        270, # Medio-Inferior
        350, # Inferior, cerca del suelo
    ]
    NUM_ALTURAS = len(ALTURAS_Y)

    # POSICIONES Y FIJAS 
    POSICIONES_Y_FIJAS = [
        100, 270, 350, 180, 100, 350, 270, 100, 180, 350, 
        100, 270, 180, 350, 100, 270, 180, 350, 270, 100
    ]
    # --- BUCLE 1: GENERACIÓN DE PLATAFORMAS HORIZONTALES FIJAS ---
    for i in range(NUM_PLAT_HORIZONTALES):
        
        OFFSET_X = POSICION_INICIO_HORIZONTALES_X + i * ESPACIO_X
        Y_POS = POSICIONES_Y_FIJAS[i]
        
        platforms.add(platform(
            OFFSET_X, 
            Y_POS, 
            LARGO_PLAT, 
            ALTO_PLAT
        ))    

    #----------PORTAL COHETE
    portal_cohete_nuevo = portal_cohete(16870, 240, 40, 40) 
    portales_cohete.add(portal_cohete_nuevo)
    all_sprites.add(portal_cohete_nuevo)
    # --- PORTAL DE SALIDA DEL MODO COHETE 
    portal_cubo_salida = portal_cubo(32800, 300, 40, 40) 
    portales_cubo.add(portal_cubo_salida)
    all_sprites.add(portal_cubo_salida)

    # --- ADICIÓN MANUAL DEL BLOQUE INVERSOR ---
    inversor = GravityBlock(12500, 180) 
    gravity_blocks.add(inversor)
    all_sprites.add(inversor)
    inversor2 = GravityBlock(15700, 170) 
    gravity_blocks.add(inversor2)
    all_sprites.add(inversor2)


    #------------------OBSTÁCULOS-------------------------
    #------------BUCLE DE PINCHOS
    for i in range(NUM_ONDAS):
        OFFSET_X = POSICION_INICIO_X + i * ANCHO_ONDA
        # --- PINCHOS PARA UNA SOLA ONDA --- 
        # Base izquierda (superior)
        for j in range(2): # 2 pinchos
            spikes.add(Spike(OFFSET_X + 20 + j*30, 180 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 20 + j*30, 180, 15, 10)) # Arriba
        # Sube 1
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 100 + 20 + j*30, 130 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 100 + 20 + j*30, 130, 15, 10)) # Arriba
        # Sube 2 (Pico superior)
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 200 + 20 + j*30, 80 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 200 + 20 + j*30, 80, 15, 10)) # Arriba
        # Meseta superior
        for j in range(3): # Más pinchos en la sección recta
            spikes.add(Spike(OFFSET_X + 300 + 20 + j*30, 80 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 300 + 20 + j*30, 80, 15, 10)) # Arriba
        # Baja 1
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 400 + 20 + j*30, 130 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 400 + 20 + j*30, 130, 15, 10)) # Arriba
        # Baja 2
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 500 + 20 + j*30, 180 + 20 - 10, 15, 10)) # Abajo
            spikes.add(Spike(OFFSET_X + 500 + 20 + j*30, 180, 15, 10)) # Arriba

        # Pinchos en el segmento inferior
        # Base izquierda inferior
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 50 + 20 + j*30, 420, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 50 + 20 + j*30, 420 + 20 - 10, 15, 10)) # Abajo
        # Baja 1 inferior
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 150 + 20 + j*30, 370, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 150 + 20 + j*30, 370 + 20 - 10, 15, 10)) # Abajo
        # Baja 2 (Valle inferior)
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 250 + 20 + j*30, 320, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 250 + 20 + j*30, 320 + 20 - 10, 15, 10)) # Abajo
        # Meseta inferior
        for j in range(3):
            spikes.add(Spike(OFFSET_X + 350 + 20 + j*30, 320, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 350 + 20 + j*30, 320 + 20 - 10, 15, 10)) # Abajo
        # Sube 1 inferior
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 450 + 20 + j*30, 370, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 450 + 20 + j*30, 370 + 20 - 10, 15, 10)) # Abajo
        # Sube 2 inferior
        for j in range(2):
            spikes.add(Spike(OFFSET_X + 550 + 20 + j*30, 420, 15, 10)) # Arriba
            spikes.add(Spike(OFFSET_X + 550 + 20 + j*30, 420 + 20 - 10, 15, 10)) # Abajo

    spikes.add(Spike(1040, 320))#Pincho en plataforma elevada
    spikes.add(Spike(2910, 325))#Pincho en plataforma elevada
    spikes.add(Spike(4650, 310))#Pincho en plataforma elevada
    spikes.add(Spike(6800, 320, 15, 10))#16
    spikes.add(Spike(6820, 320, 15, 10))#16
    spikes.add(Spike(6840, 320, 15, 10))#16
    spikes.add(Spike(6860, 320, 15, 10))#16
    spikes.add(Spike(6880, 320, 15, 10))#16
    spikes.add(Spike(6900, 320, 15, 10))#16
    spikes.add(Spike(6920, 320, 15, 10))#16
    spikes.add(Spike(6940, 320, 15, 10))#16
    spikes.add(Spike(8750, 290, 15, 10))#22
    spikes.add(Spike(8770, 290, 15, 10))#22
    spikes.add(Spike(8790, 290, 15, 10))#22
    spikes.add(Spike(8810, 290, 15, 10))#22
    spikes.add(Spike(9200, 240))#23
    spikes.add(Spike(9225, 240))#23
    spikes.add(Spike(9600, 240))#23
    spikes.add(Spike(9625, 240))#23
    spikes.add(Spike(12000, 230))#28
    spikes.add(Spike(12850, 100))#30
    spikes.add(Spike(42500, 180, direction="up"))
    spikes.add(Spike(43200, 100, direction="up"))
    spikes.add(Spike(43600, 100, direction="up"))
    spikes.add(Spike(44100, 100, direction="up"))
    spikes.add(Spike(49800, 230, direction="up"))
    spikes.add(Spike(50300, 230, direction="up"))
    spikes.add(Spike(51300, 280))
    spikes.add(Spike(51300, 180,direction="down"))

    #Pinchos superior e inferior de del recorrido
    for i in range(185):
        spikes.add(Spike(4900 + i*40, 420))

    for i in range(110):
        spikes.add(Spike(12500 + i*40, 3, direction="down"))

    for i in range(150):
        spikes.add(Spike(32800 + i*40, 800))

    #------------Serie de pinchos final
    inicio_x = 45200     
    num_repeticiones = 6 
    pincho_ancho = 90     
    espacio_vacio = 300  

    for i in range(num_repeticiones):
        # 1. Calcular la posición X para esta repetición
        posicion_x = inicio_x + i * (pincho_ancho + espacio_vacio)
        pincho = Spike(posicion_x, 90,direction="down") 
        spikes.add(pincho)
        all_sprites.add(pincho)
        
    inicio2_x = 45000     
    num_repeticiones2 = 8 
    pincho_ancho2 = 90     
    espacio_vacio2 = 300   

    for i in range(num_repeticiones):
        # 1. Calcular la posición X para esta repetición
        posicion2_x = inicio2_x + i * (pincho_ancho2 + espacio_vacio2)
        pincho = Spike(posicion2_x, 170, direction="up") 
        spikes.add(pincho)
        all_sprites.add(pincho)

    # -----------TÚNEL CON PINCHOS

    for i in range(50):
        spikes.add(Spike(550 + i*40, 420))

    for i in range(12):#pinchos arriba plataforma
        spikes.add(Spike(3200 + i*40, 330))

    for i in range(12):#pinchos bajo plataforma
        spikes.add(Spike(3900 + i*40, 395))

    for i in range(60): 
        spikes.add(Spike(17000 + i*40, 370, 15, 10))#En el suelo
        spikes.add(Spike(17000 + i*40, 120, 15, 10))#En el techo

    #----------PINCHOS EN PLATAFORMAS COLGANTES
    ANCHO_PINCHO = 15
    ALTO_PINCHO = 10 

    for i in range(NUM_PILARES):

        OFFSET_X = POSICION_INICIO_PILAR_X + i * ESPACIO_ENTRE_PILARES
        ALTURA = ALTURAS_PILAR[i % NUM_PATRONES]
        # Calcular la posición X centrada para el pincho
        spike_x = OFFSET_X + (ANCHO_PILAR // 2) - (ANCHO_PINCHO // 2)
        
        if i % 2 == 0:
            # PINCHO PARA PILAR DEL TECHO
            spike_y = ALTURA - ALTO_PINCHO 
            spike = Spike(spike_x, spike_y, ANCHO_PINCHO, ALTO_PINCHO)
            spikes.add(spike)
        else:
            # PINCHO PARA PILAR DEL SUELO
            spike_y = HEIGHT - ALTURA 
            spike = Spike(spike_x, spike_y, ANCHO_PINCHO, ALTO_PINCHO)
            spikes.add(spike)

    #-----------BUCLE PARA ESQUIVAR PINCHOS
    ANCHO_PINCHO = 15
    ALTO_PINCHO = 10 

    for i in range(NUM_PLAT_HORIZONTALES):
        
        OFFSET_X = POSICION_INICIO_HORIZONTALES_X + i * ESPACIO_X
        Y_POS = POSICIONES_Y_FIJAS[i]
        # Posición de la plataforma:
        PLAT_IZQ = OFFSET_X
        PLAT_TOP = Y_POS
        PLAT_BOT = Y_POS + ALTO_PLAT
        PINCHO_CENTRO_X = PLAT_IZQ + (LARGO_PLAT // 2) - (ANCHO_PINCHO // 2)
        # 1. Pinchos apuntando HACIA ABAJO 
        spike_down_y = PLAT_TOP 
        spikes.add(Spike(PINCHO_CENTRO_X, spike_down_y, ANCHO_PINCHO, ALTO_PINCHO))
        # 2. Pinchos apuntando HACIA ARRIBA 
        spike_up_y = PLAT_BOT - ALTO_PINCHO 
        spikes.add(Spike(PINCHO_CENTRO_X, spike_up_y, ANCHO_PINCHO, ALTO_PINCHO))

    #-------BUCLE DE PINCHOS DE PLATAFORMAS FINALES
    for i in range(43):
        spikes.add(Spike(42800 + i*40, 170,direction="up"))

    for i in range(70):
        spikes.add(Spike(44700 + i*40, 50,direction="up"))

    #--------------------ADICIÓN DE JUMP PADS------------------ 

    pad_elevado = JumpPad(1400, 380, w=40, h=10)
    pad_elevado2 = JumpPad(6970, 380, w=40, h=10)
    pad_elevado3 = JumpPad(7600, 268, w=40, h=10)
    jump_pads.add(pad_elevado)
    all_sprites.add(pad_elevado)
    jump_pads.add(pad_elevado2)
    all_sprites.add(pad_elevado2)
    jump_pads.add(pad_elevado3)
    all_sprites.add(pad_elevado3)

    #-------------ALL_SPRITES Y JUGADOR-------------------

    all_sprites.add(platforms)
    all_sprites.add(spikes)
    P1 = Player()
    all_sprites.add(P1)


    # --------------------------- BUCLE PRINCIPAL ---------------------------
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not P1.modo_cohete:#Logica de salto
                        P1.salto() 
            
        if not nivel_terminado:#Movimiento del jugador
            P1.move()
            P1.update()

        for platform in platforms:
            collision = platform.check_collision(P1.rect)
        
            if collision == "platform":
                if P1.vel.y > 0:  # solo si cae
                    P1.vel.y = 0
                    P1.rect.bottom = platform.rect.top
                    P1.saltable = True
            elif collision == "spike_left":
                # Bloquear que atraviese la izquierda
                P1.rect.left = platform.left_spike.right

        jump_pad_hit = pygame.sprite.spritecollideany(P1, jump_pads)
        
        if jump_pad_hit:
            # Solo aplica si es el cubo en gravedad normal
            if not P1.modo_cohete and not P1.inverted:
                P1.vel.y = -10
                P1.saltable = False 
        
        gravity_hit = pygame.sprite.spritecollideany(P1, gravity_blocks)
        
        if gravity_hit and not P1.modo_cohete:
            # Invierte el estado de gravedad del jugador (True -> False o False -> True)
            P1.inverted = not P1.inverted 
            # Detiene la aceleración y restablece la velocidad vertical a cero
            P1.vel.y = 0 
            #Evita que la gravedad se invierta varias veces por un solo toque
            gravity_hit.kill() 
            
        # Lógica de Muerte
        if pygame.sprite.spritecollide(P1, spikes, False):
            # Reinicia la posición del jugador
            P1.pos = vec(10, 385) 
            P1.vel = vec(0,0) 
            P1.inverted = False # Vuelve a la gravedad normal
            P1.modo_cohete = False 

            #Restaura los bloques inversores
            if not any(isinstance(s, GravityBlock) for s in all_sprites):
                reinversor = GravityBlock(12500, 180)
                gravity_blocks.add(reinversor)
                all_sprites.add(reinversor)
                reinversor2 = GravityBlock(15700, 170)
                gravity_blocks.add(reinversor2)
                all_sprites.add(reinversor2)

            #Restaura el Portal Cohete
            if not any(isinstance(s, portal_cohete) for s in portales_cohete):
                portal_cohete_nuevo = portal_cohete(16870, 240, 40, 40)
                portales_cohete.add(portal_cohete_nuevo)
                all_sprites.add(portal_cohete_nuevo)

            #Restaura el Portal Cubo
            if not any(isinstance(s, portal_cubo) for s in portales_cubo):
                portal_cubo_salida = portal_cubo(32800, 300, 40, 40) 
                portales_cubo.add(portal_cubo_salida)
                all_sprites.add(portal_cubo_salida)

            pygame.mixer.music.play(0)#Reinicio de musica

        #Lógica de meta
        if not nivel_terminado:
            if pygame.sprite.spritecollideany(P1, meta_group):
                print("¡Nivel completado!")
                nivel_terminado = True
                P1.vel = vec(0,0)#Jugador detenido
                P1.pos.y = meta_final.rect.top

        #Cámara
        camera_offset_x = P1.pos.x - WIDTH // 2

        #Fondo estático
        if fondo_ok:
            displaysurface.blit(fondo, (0, 0))
        else:
            displaysurface.fill((135, 206, 250))

        # Dibujar sprites con offset de cámara
        for entity in all_sprites:
            displaysurface.blit(entity.surf, (entity.rect.x - camera_offset_x, entity.rect.y))

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    el_nivel_2(config)