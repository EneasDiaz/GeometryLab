import pygame
from pygame.locals import *
import sys

pygame.init()
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 900
ACC = 0.5
FRIC = -0.12
FPS = 60

def el_nivel_3(config):

    pausado = False
    nivel_terminado = False
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/Lvl3/Hopes_and_Dreams.mp3")
    pygame.mixer.music.set_volume(config.get("volumen", 100) / 100)


    sonido_muerte = pygame.mixer.Sound("assets/sounds/muerte/candidato_muerte.wav")

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    fondo = pygame.image.load("assets/img/fondos/3er_lvl.jpg").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    #para abajo clases y funciones de player
    class linea_meta(pygame.sprite.Sprite):   
        def __init__(self, x, y, w=20, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/Metas_paredes/linea_meta.jpg").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class ProgresoBarra:
        def __init__(self, screen, total_distance, width=300, height=15, color=(0, 255, 0), position=(20, 20), show_text=True):
            self.screen = screen
            self.total_distance = total_distance
            self.width = width
            self.height = height
            self.color = color
            self.position = position
            self.show_text = show_text
            self.bg_color = (50, 50, 50)  
            self.current_width = 0          
            self.progress_percent = 0       
            self.font = pygame.font.Font(None, 24)

        def update(self, player_x):
            progress_ratio = min(player_x / self.total_distance, 1)
            self.current_width = int(self.width * progress_ratio)
            self.progress_percent = int(progress_ratio * 100)

        def draw(self):
            # fondo
            pygame.draw.rect(self.screen, self.bg_color, (*self.position, self.width, self.height))
            # barra de progreso
            pygame.draw.rect(self.screen, self.color, (*self.position, self.current_width, self.height))
            # porcentaje
            if self.show_text:
                text = self.font.render(f"{self.progress_percent}%", True, (255, 255, 255))
                text_x = self.position[0] + self.width + 10
                text_y = self.position[1] - 2
                self.screen.blit(text, (text_x, text_y))
    class portal_cubo(pygame.sprite.Sprite):    
        def __init__(self, x, y, w=20, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/portal_cubo.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class portal_UFO(pygame.sprite.Sprite):
        def __init__(self, x, y, w=20, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/portal_ufo.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class pregunta(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,0))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/pregunta.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class cruz(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,0))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/cruz_roja.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class tick(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,0))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/tick_blaco.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class portal_cohete(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/portal_cohete.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class platf_amarilla(pygame.sprite.Sprite):
        def __init__(self, x, y, w=30, h=20):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/plataforma_salto.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (60, 40))

    class orbe_amarilla(pygame.sprite.Sprite):
        def __init__(self, x, y, w=22, h=22):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((0, 0, 255)) 
            self.rect = self.surf.get_rect(topleft=(x, y)) 
            self.usado=False
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/orbe_amarilla.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (30, 30))

            
    class Spike(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255, 255, 0)) 
            self.rect = self.surf.get_rect(topleft=(x, y))   
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/pincho.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w+5, h+5))


    class SpikePlataforma(pygame.sprite.Sprite):
        def __init__(self, x, y, w=30, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255, 255, 255)) 
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf.set_alpha(0)
            


    class platform(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,0))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/plataforma_final.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class platformBase(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/piso_base.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class platformGrande(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/set_piso_grande.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class platfpalo(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/pared.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
    class palocostado(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255, 255, 0)) 
            self.rect = self.surf.get_rect(topleft=(x, y))  
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/pincho.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.original_surf = pygame.image.load("assets/img/obstaculos_jugador/cubo_jugador_3.jpg").convert_alpha()
            self.original_surf = pygame.transform.scale(self.original_surf, (35, 35))

            self.surf = self.original_surf.copy()

            self.rect = self.surf.get_rect(center = (10, 420))


            self.pos = vec((110, 400))
            self.vel = vec(0,0)
            self.acc = vec(0,0)

            self.angulo = False
            self.saltable = False
            self.modo_cohete = False
            self.modo_ufo = False
            self.cohete_img = pygame.Surface((50, 25)) 
            self.cohete_img.fill((255, 150, 0))

        def move(self):
            self.vel.x=8
            self.vel.y+=0.23
            self.pos += self.vel 
            self.rect.midbottom = self.pos 

            if self.modo_cohete:
                mouse = pygame.mouse.get_pressed()
                keys = pygame.key.get_pressed()
                for i in range(3):
                    if mouse[0]:        
                        if self.vel.y > -5:
                            self.vel.y -= 0.18
            if self.modo_ufo:
                self.saltable=True
                
        def update(self):
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if P1.vel.y > 0 and hits:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.saltable=True
            else:
                self.saltable=False
            self.angulo = False
            if not self.saltable:
                self.angulo += (abs(self.vel.y) * 3)
                self.angulo %= 360
                self.surf = pygame.transform.rotate(self.original_surf, self.angulo)
                self.rect = self.surf.get_rect(center=self.rect.center)
            else:
                self.surf = self.original_surf.copy()
                self.rect = self.surf.get_rect(center=self.rect.center)
            for orbe in orbes_amarillas: 
                if not orbe.usado and pygame.sprite.spritecollide(self, [orbe], False): 
                    self.saltable=True 
            for platf_amarilla in plataformas_amarillas:
                if pygame.sprite.spritecollide(self, [platf_amarilla], False): 
                    self.vel.y=-10
            for portal in portales_cohete:
                if pygame.sprite.spritecollide(self, [portal], False):
                    self.modo_cohete=True
                    self.modo_ufo=False
            for portal in portales_ufo:
                if pygame.sprite.spritecollide(self, [portal], False):
                    self.modo_ufo=True
                    self.modo_cohete=False
            for portal in portales_cubo:
                if pygame.sprite.spritecollide(self, [portal], False):
                    self.modo_ufo=False
                    self.modo_cohete=False

        def salto(self):
            if self.saltable:
                self.vel.y=-5
                self.saltable=False
            elif self.modo_ufo:
                self.vel.y=-4.3
            for orbe in orbes_amarillas:
                if pygame.sprite.spritecollide(self, [orbe], False):
                    orbe.usado = True
            
    

    #para arriba clases y funciones
    #para abajo estructuras y musica

    font = pygame.font.SysFont(None, 30)    
    imagenes = pygame.sprite.Group()
    palos=pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    plataformasGrandes = pygame.sprite.Group()
    portales_cohete = pygame.sprite.Group()
    plataformas_amarillas = pygame.sprite.Group()
    portales_ufo=pygame.sprite.Group()
    lineas_meta=pygame.sprite.Group()
    for i in range(60):
        plat = platformBase(i * 201, HEIGHT - 20, 200, 20)
        platforms.add(plat)

    progress_bar = ProgresoBarra(displaysurface, total_distance=37800, width=300, height=15, color=(0, 255, 0), position=(20, 20))
    P1 = Player()
    all_sprites = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    orbes_amarillas = pygame.sprite.Group()
    portales_cubo = pygame.sprite.Group()
    pygame.mixer.music.play(-1)
    for i in range(50):
        spikes.add(Spike(483 + i*40, 405, 30, 30))
    for i in range(36):
        spikes.add(Spike(3200 + i*40, 405, 30, 30))
    for i in range(100):
        palos.add(palocostado(10000 + i*250, 10, 250, 10))
        spikes.add(SpikePlataforma(10000 + i*250, 10, 250, 5))

        palos.add(palocostado(12000 + i*250, 440, 250, 10))
        spikes.add(SpikePlataforma(12000 + i*250, 430, 250, 5))
    #1er platf
    platforms.add(platform(500, 380, 100, 20))
    spikes.add(SpikePlataforma(500, 383, 30, 25)) 
    #2daplatf
    platforms.add(platform(800, 350, 100, 20))
    spikes.add(SpikePlataforma(783, 353, 30, 25)) 
    #3ra platf
    platforms.add(platform(1000, 380, 100, 20))
    #4ta platf
    platforms.add(platform(1350, 355, 30, 20))
    spikes.add(SpikePlataforma(1350, 358, 30, 25))
    #5ta platf
    platforms.add(platform(1500, 380, 200, 20))
    spikes.add(SpikePlataforma(1500, 384, 30, 25))
    #6ta platf
    platforms.add(platform(600, -40, 30000, 20))
    #7ma platf
    platforms.add(platform(1820, 400, 650, 20))
    spikes.add(Spike(2140, 380, 30, 25))
    spikes.add(Spike(2175, 380, 30, 25))
    spikes.add(Spike(2210, 380, 30, 25))
    spikes.add(Spike(2245, 380, 30, 25))
    #8va platf
    platforms.add(platform(2900, 380, 150, 20))
    spikes.add(SpikePlataforma(2890, 383, 30, 10))
    #9na platf
    platforms.add(platform(3230, 360, 200, 20))
    spikes.add(SpikePlataforma(3220, 363, 30, 10))
    #10ma platf
    platforms.add(platform(3560, 340, 470, 20))
    spikes.add(SpikePlataforma(3560, 343, 30, 10))
    #11ma platf
    orbes_amarillas.add(orbe_amarilla(4150, 300, 20, 20))
    #12ma platf
    platforms.add(platform(4460, 300, 40, 10))
    spikes.add(SpikePlataforma(4450, 305, 10, 10))
    #13 pincho
    spikes.add(Spike(4880, 405, 30, 25))
    spikes.add(Spike(4920, 405, 30, 25))
    spikes.add(Spike(4960, 405, 30, 25))
    spikes.add(Spike(5000, 405, 30, 25))
    #14 orbe
    orbes_amarillas.add(orbe_amarilla(5350, 380))

    #15 pincho
    spikes.add(Spike(5470, 400, 30, 25))
    spikes.add(Spike(5470, 380, 30, 25))
    spikes.add(Spike(5500, 400, 30, 25))
    spikes.add(Spike(5500, 380, 30, 25))
    spikes.add(Spike(5530, 400, 30, 25))
    spikes.add(Spike(5530, 380, 30, 25))
    #16 orbe
    orbes_amarillas.add(orbe_amarilla(5700, 360))
    #17 pinchos
    spikes.add(Spike(5690, 405, 30, 25))
    spikes.add(Spike(5730, 405, 30, 25))
    spikes.add(Spike(5770, 405, 30, 25))
    spikes.add(Spike(5810, 405, 30, 25))
    spikes.add(Spike(5850, 405, 30, 25))
    #18 platf
    platforms.add(platform(6166, 375, 100, 10))
    for i in range(3):
        spikes.add(Spike(6160 + i*40, 355, 25, 25))
    #19 pincho
    spikes.add(Spike(6343, 408, 25, 25))
    spikes.add(Spike(6400, 408, 30, 25))
    spikes.add(Spike(6460, 408, 30, 25))
    #20 platf
    spikes.add(Spike(7050, 410, 30, 25))
    platforms.add(platform(7100, 380, 200, 10))
    spikes.add(SpikePlataforma(7100, 383, 20, 10))
    spikes.add(Spike(7280, 360, 30, 25))
    #21 platf
    platforms.add(platform(7500, 350, 200, 10))
    spikes.add(SpikePlataforma(7500, 353, 20, 10))
    #22 orbe
    orbes_amarillas.add(orbe_amarilla(7900, 320))
    #23 pinchos
    for i in range(10):
        spikes.add(Spike(7700 + i*40, 400, 30, 25))
    #24 orbe fake
    orbes_amarillas.add(orbe_amarilla(8250, 320))
    #25 platf
    platforms.add(platform(8430, 370, 260, 20))
    for i in range(7):
        spikes.add(SpikePlataforma(8430 + i*40, 373, 10, 10))
        spikes.add(Spike(8430 + i*40, 363, 10, 10))
    #26 platf amarilla salto
    plataformas_amarillas.add(platf_amarilla(8780, 410))
    #27 platf
    platforms.add(platform(9250, 250, 280, 20))
    #28 spikes
    for i in range(40):
        spikes.add(Spike(8950 + i*40, 400, 30, 30))
    #29 orbes
    orbes_amarillas.add(orbe_amarilla(9690, 300))
    orbes_amarillas.add(orbe_amarilla(9720, 300))
    orbes_amarillas.add(orbe_amarilla(9750, 300))
    #30 platf
    platforms.add(platform(10000, 350, 350, 15))
    #31
    plataformas_amarillas.add(platf_amarilla(10260, 330))
    #32 spike
    spikes.add(Spike(10300, 320, 30, 30))
    #33 portal cohete 
    portales_cohete.add(portal_cohete(10500, 60, 30, 80))


    #34 platf grande abajo
    plataformasGrandes.add(platformGrande(11000, 380, 500, 150))
    spikes.add(SpikePlataforma(11000, 380, 10, 500))
    spikes.add(SpikePlataforma(11000, 380, 500, 10))
    spikes.add(SpikePlataforma(11500, 380, 10, 500)) 
    #34 platf grande arriba
    plataformasGrandes.add(platformGrande(11000, 120, 500, 150))
    spikes.add(SpikePlataforma(11000, 110, 500, 10))
    spikes.add(SpikePlataforma(11000, 270, 500, 10))
    spikes.add(SpikePlataforma(11010, 110, 10, 170))
    spikes.add(SpikePlataforma(11500, 110, 10, 170))
    #35 platfs palos
    palos.add(platfpalo(13000, 300, 20, 150))
    spikes.add(SpikePlataforma(13000, 300, 20, 150))
    palos.add(platfpalo(13000, 0, 20, 200))
    spikes.add(SpikePlataforma(13000, 0, 20, 200))
    #36 platfs palos
    palos.add(platfpalo(13250, 0, 20, 300))
    spikes.add(SpikePlataforma(13250, 0, 20, 300))
    palos.add(platfpalo(13250, 380, 20, 70))
    spikes.add(SpikePlataforma(13250, 380, 20, 70))
    #37 platfs palos
    palos.add(platfpalo(12600, 200, 20, 150))
    spikes.add(SpikePlataforma(12600, 200, 20, 150))

    #38 platfs
    plataformasGrandes.add(platformGrande(13700, 350, 300, 200))
    spikes.add(SpikePlataforma(13700, 350, 300, 10))
    spikes.add(SpikePlataforma(13700, 350, 10, 200))



    plataformasGrandes.add(platformGrande(14000, 200, 300, 300))
    spikes.add(SpikePlataforma(14000, 200, 300, 10))
    spikes.add(SpikePlataforma(14000, 200, 10, 300))

    plataformasGrandes.add(platformGrande(14300, 140, 300, 410))
    spikes.add(SpikePlataforma(14300, 140, 300, 10))
    spikes.add(SpikePlataforma(14300, 140, 10, 410))

    for i in range(11):
        spikes.add(Spike(14300 + i*25, 120, 30, 25 ))

    #39 platfs
    palos.add(platfpalo(15400, 20, 20, 330))
    spikes.add(SpikePlataforma(15400, 20, 20, 330))
    palos.add(palocostado(15400, 340, 500, 20))
    spikes.add(SpikePlataforma(15400, 340, 500, 20))
    palos.add(platfpalo(15900, 20, 20, 330))
    spikes.add(SpikePlataforma(15900, 20, 20, 330))
    platforms.add(platform(15750, 410, 250, 25))
    spikes.add(SpikePlataforma(15750, 412, 30, 10))
    plataformas_amarillas.add(platf_amarilla(15980, 380, 20, 20))

    #40 palo
    palos.add(platfpalo(16200, 235, 20, 340))
    spikes.add(SpikePlataforma(16200, 235, 20, 340))
    palos.add(platfpalo(16200, 0, 20, 140))
    spikes.add(SpikePlataforma(16200, 0, 20, 140))

    #41 palo
    palos.add(platfpalo(16650, 0, 20, 215))
    spikes.add(SpikePlataforma(16650, 0, 20, 215))

    palos.add(platfpalo(16550, 300, 20, 300))
    spikes.add(SpikePlataforma(16550, 300, 20, 300))


        
    palos.add(platfpalo(17400, 0, 20, 450))
    imagenes.add(cruz(17300, 60, 80, 80))
    spikes.add(SpikePlataforma(17400, 0, 20, 170))
    imagenes.add(tick(17300, 200, 80, 80))

    imagenes.add(cruz(17300, 360, 80, 80))
    spikes.add(SpikePlataforma(17400, 340, 20, 90))

    palos.add(platfpalo(18000, 0, 20, 450))
    imagenes.add(cruz(17900, 60, 80, 80))
    imagenes.add(cruz(17900, 200, 80, 80))
    spikes.add(SpikePlataforma(18000, 0, 20, 320))
    imagenes.add(tick(17900, 360, 80, 80))

    palos.add(platfpalo(18600, 0, 20, 450))
    imagenes.add(cruz(18500, 60, 80, 80))
    imagenes.add(cruz(18500, 200, 80, 80))
    spikes.add(SpikePlataforma(18600, 0, 20, 320))
    imagenes.add(tick(18500, 360, 80, 80))

    palos.add(platfpalo(19200, 0, 20, 450))
    imagenes.add(tick(19100, 60, 80, 80))
    imagenes.add(cruz(19100, 200, 80, 80))
    imagenes.add(cruz(19100, 360, 80, 80))
    spikes.add(SpikePlataforma(19200, 170, 20, 280))

    imagenes.add(pregunta(19700, 150, 200, 200))

    palos.add(platfpalo(20300, 0, 20, 450))
    imagenes.add(pregunta(20200, 60, 80, 80))
    spikes.add(SpikePlataforma(20300, 0, 20, 170))
    imagenes.add(pregunta(20200, 200, 80, 80))

    imagenes.add(pregunta(20200, 360, 80, 80))
    spikes.add(SpikePlataforma(20300, 320, 20, 130))

    palos.add(platfpalo(20900, 0, 20, 450))
    imagenes.add(pregunta(20800, 60, 80, 80))
    imagenes.add(pregunta(20800, 200, 80, 80))
    imagenes.add(pregunta(20800, 360, 80, 80))
    spikes.add(SpikePlataforma(20900, 0, 20, 320))

    palos.add(platfpalo(21400, 0, 20, 450))
    imagenes.add(pregunta(21300, 60, 80, 80))
    imagenes.add(pregunta(21300, 200, 80, 80))
    imagenes.add(pregunta(21300, 360, 80, 80))
    spikes.add(SpikePlataforma(21400, 0, 20, 320))

    palos.add(platfpalo(22000, 0, 20, 450))
    imagenes.add(pregunta(21900, 60, 80, 80))
    imagenes.add(pregunta(21900, 200, 80, 80))
    imagenes.add(pregunta(21900, 360, 80, 80))
    spikes.add(SpikePlataforma(22000, 170, 20, 280))


    portales_ufo.add(portal_UFO(22600, 240, 40, 80))
    palos.add(platfpalo(22600, 0, 20, 200))
    spikes.add(SpikePlataforma(22600, 0, 20, 200))
    palos.add(platfpalo(22600, 350, 20, 100))
    spikes.add(SpikePlataforma(22600, 350, 20, 100))
    ########## primer seccion

    palos.add(platfpalo(23000, 0, 20, 280))
    spikes.add(SpikePlataforma(23000, 0, 20, 300))
    palos.add(platfpalo(23000, 400, 20, 50))
    spikes.add(SpikePlataforma(23000, 400, 20, 50))

    palos.add(platfpalo(23230, 0, 20, 200))
    spikes.add(SpikePlataforma(23230, 0, 20, 200))
    palos.add(platfpalo(23230, 300, 20, 150))
    spikes.add(SpikePlataforma(23230, 300, 20, 150))

    palos.add(platfpalo(23370, 0, 20, 80))
    spikes.add(SpikePlataforma(23370, 0, 20, 80))
    palos.add(platfpalo(23370, 250, 20, 250))
    spikes.add(SpikePlataforma(23370, 250, 20, 250))
    ###################################### 
    #segunda seccion
    palos.add(platfpalo(23970, 0, 20, 315))
    spikes.add(SpikePlataforma(23970, 0, 20, 330))
    palos.add(platfpalo(23970, 400, 20, 50))
    spikes.add(SpikePlataforma(23970, 400, 20, 50))

    palos.add(platfpalo(24150, 0, 20, 260))
    spikes.add(SpikePlataforma(24150, 0, 20, 260))
    palos.add(platfpalo(24150, 360, 20, 90))
    spikes.add(SpikePlataforma(24150, 360, 20, 90))

    palos.add(platfpalo(24400, 0, 20, 150))
    spikes.add(SpikePlataforma(24400, 0, 20, 150))
    palos.add(platfpalo(24400, 250, 20, 200))
    spikes.add(SpikePlataforma(24400, 250, 20, 200))

    palos.add(platfpalo(24600, 0, 20, 80))
    spikes.add(SpikePlataforma(24600, 0, 20,80))
    palos.add(platfpalo(24600, 190, 20, 260))
    spikes.add(SpikePlataforma(24600, 190, 20, 260))



    palos.add(platfpalo(25200, 0, 20, 200))
    spikes.add(SpikePlataforma(25200, 0, 20, 200))
    palos.add(platfpalo(25200, 300, 20, 150))
    spikes.add(SpikePlataforma(25200, 300, 20, 150))

    portales_cohete.add(portal_cohete(25200, 210, 30, 80))

    palos.add(platfpalo(25690, 0, 20, 240))
    spikes.add(SpikePlataforma(25690, 0, 20, 240))
    palos.add(platfpalo(25690, 350, 20, 100))
    spikes.add(SpikePlataforma(25690, 350, 20, 100))

    palos.add(palocostado(25700, 250, 1000, 20))
    spikes.add(SpikePlataforma(25700, 250, 1000, 20))
    palos.add(palocostado(25700, 330, 1000, 20))
    spikes.add(SpikePlataforma(25700, 330, 1000, 20))

    palos.add(palocostado(26800, 255, 300, 20))
    spikes.add(SpikePlataforma(26800, 250, 300, 15))
    palos.add(palocostado(26800, 325, 300, 20))
    spikes.add(SpikePlataforma(26800, 330, 300, 15))

    palos.add(platfpalo(27700, 0, 20, 150))
    spikes.add(SpikePlataforma(27700, 0, 20, 150))
    palos.add(palocostado(27700, 300, 500, 20))
    spikes.add(SpikePlataforma(27700, 300, 500, 20))
    palos.add(palocostado(27700, 200, 500, 20))
    spikes.add(SpikePlataforma(27700, 200, 500, 20))
    palos.add(platfpalo(27700, 350, 20, 100))
    spikes.add(SpikePlataforma(27700, 350, 20, 100))


    palos.add(palocostado(28200, 280, 300, 20))
    spikes.add(SpikePlataforma(28200, 280, 300, 20))
    palos.add(palocostado(28200, 180, 300, 20))
    spikes.add(SpikePlataforma(28200, 180, 300, 20))

    palos.add(palocostado(28500, 260, 200, 20))
    spikes.add(SpikePlataforma(28500, 260, 200, 20))
    palos.add(palocostado(28500, 160, 200, 20))
    spikes.add(SpikePlataforma(28500, 160, 200, 20))

    palos.add(palocostado(28700, 240, 150, 20))
    spikes.add(SpikePlataforma(28700, 240, 150, 20))
    palos.add(palocostado(28700, 140, 150, 20))
    spikes.add(SpikePlataforma(28700, 140, 150, 20))

    palos.add(palocostado(28850, 250, 200, 20))
    spikes.add(SpikePlataforma(28850, 250, 200, 20))
    palos.add(palocostado(28850, 150, 200, 20))
    spikes.add(SpikePlataforma(28850, 150, 200, 20))


    palos.add(palocostado(29000, 260, 250, 20))
    spikes.add(SpikePlataforma(29000, 260, 250, 20))
    palos.add(palocostado(29000, 160, 250, 20))
    spikes.add(SpikePlataforma(29000, 160, 250, 20))

    palos.add(palocostado(29250, 270, 300, 20))
    spikes.add(SpikePlataforma(29250, 270, 300, 20))
    palos.add(palocostado(29250, 170, 300, 20))
    spikes.add(SpikePlataforma(29250, 170, 300, 20))

    portales_ufo.add(portal_UFO(29550, 180, 30, 80))

    palos.add(palocostado(29700, 190, 1000, 20))
    spikes.add(SpikePlataforma(29700, 190, 1000, 20))
    palos.add(palocostado(29700, 305, 1000, 20))
    spikes.add(SpikePlataforma(29700, 305, 1000, 20))

    portales_cohete.add(portal_cohete(30700, 210, 30, 80))



    for i in range(7):
        palos.add(platfpalo(31000 + 80*i, 0, 20, 250-20*i))
        spikes.add(SpikePlataforma(31000 + 80*i, 0, 20, 250-20*i))
        palos.add(platfpalo(31000 + 80*i, 350-20*i, 20, 450-(350-20*i)))
        spikes.add(SpikePlataforma(31000 + 80*i, 350-20*i, 20, 450-(350-20*i)))
        palos.add(platfpalo(31450 + 115*i, 0, 20, 150+20*i))
        spikes.add(SpikePlataforma(31450 + 115*i, 0, 20, 150+20*i))
        palos.add(platfpalo(31450 + 115*i, 250+15*i, 20, 450+(250+15*i)))
        spikes.add(SpikePlataforma(31450 + 115*i, 250+15*i, 20, 450+(250+15*i)))
    palos.add(palocostado(32800, 240, 600, 20))
    spikes.add(SpikePlataforma(32600, 240, 600, 20))

    palos.add(platfpalo(32550, 0, 30, 250))
    spikes.add(SpikePlataforma(32550, 0, 30, 250))
    portales_cubo.add(portal_cubo(32500, 260, 30, 110))


    platforms.add(platform(32600, 400, 1500, 20))

    spikes.add(Spike(33000, 370, 30, 30))
    spikes.add(Spike(33040, 370, 30, 30))
    spikes.add(Spike(33080, 370, 30, 30))
    spikes.add(Spike(33120, 370, 30, 30))

    plataformas_amarillas.add(platf_amarilla(33400, 380, 20, 20))
    plataformas_amarillas.add(platf_amarilla(33800, 380, 20, 20))

    plataformas_amarillas.add(platf_amarilla(33980, 380, 20, 20))
    spikes.add(Spike(34090, 370, 10, 30))
    palos.add(palocostado(33300, 250, 700, 20))
    spikes.add(SpikePlataforma(33300, 250, 700, 20))

    portales_cohete.add(portal_cohete(34150, 180, 30, 80))
    palos.add(palocostado(34150, 10, 1000, 20))
    spikes.add(SpikePlataforma(34150, 10, 1000, 20))
    palos.add(palocostado(34150, 440, 1000, 20))
    spikes.add(SpikePlataforma(34150, 430, 1000, 20))

    palos.add(palocostado(35150, 10, 1000, 20))
    spikes.add(SpikePlataforma(35150, 10, 1000, 20))
    palos.add(palocostado(35150, 440, 1000, 20))
    spikes.add(SpikePlataforma(35150, 430, 1000, 20))

    palos.add(palocostado(36150, 10, 1000, 20))
    spikes.add(SpikePlataforma(36150, 10, 1000, 20))
    palos.add(palocostado(36150, 440, 1000, 20))
    spikes.add(SpikePlataforma(36150, 440, 1000, 20))

    palos.add(platfpalo(34500, 100, 20, 60))
    spikes.add(SpikePlataforma(34500, 100, 20, 60))
    palos.add(platfpalo(34550, 300, 20, 60))
    spikes.add(SpikePlataforma(34550, 300, 20, 60))
    palos.add(platfpalo(34650, 430, 20, 60))
    spikes.add(SpikePlataforma(34650, 430, 20, 60))
    palos.add(platfpalo(34780, 200, 20, 60))
    spikes.add(SpikePlataforma(34780, 200, 20, 60))
    palos.add(platfpalo(34910, 10, 20, 60))
    spikes.add(SpikePlataforma(34910, 10, 20, 60))
    palos.add(platfpalo(35240, 400, 20, 60))
    spikes.add(SpikePlataforma(35240, 400, 20, 60))
    palos.add(platfpalo(35370, 150, 20, 60))
    spikes.add(SpikePlataforma(35370, 150, 20, 60))

    palos.add(platfpalo(35770, 0, 20, 100))
    spikes.add(SpikePlataforma(35770, 0, 20, 100))
    palos.add(platfpalo(35770, 250, 20, 200))
    spikes.add(SpikePlataforma(35770, 250, 20, 200))

    palos.add(platfpalo(36100, 80, 20, 60))
    spikes.add(SpikePlataforma(36100, 80, 20, 60))
    palos.add(platfpalo(36230, 320, 20, 60))
    spikes.add(SpikePlataforma(36230, 320, 20, 60))
    palos.add(platfpalo(36360, 150, 20, 60))
    spikes.add(SpikePlataforma(36360, 150, 20, 60))
    palos.add(platfpalo(36500, 400, 20, 60))
    spikes.add(SpikePlataforma(36500, 400, 20, 60))
    palos.add(platfpalo(36630, 40, 20, 60))
    spikes.add(SpikePlataforma(36630, 40, 20, 60))
    palos.add(platfpalo(36760, 300, 20, 60))
    spikes.add(SpikePlataforma(36760, 300, 20, 60))

    palos.add(platfpalo(36900, 0, 20, 250))
    spikes.add(SpikePlataforma(36900, 0, 20, 250))
    palos.add(platfpalo(36900, 350, 20, 100))
    spikes.add(SpikePlataforma(36900, 350, 20, 100))
    portales_cubo.add(portal_cubo(36910, 260, 30, 90))


    platforms.add(platform(37000, 400, 1500, 20))
    lineas_meta.add(linea_meta(37800, -10000, 30, 10000))
    lineas_meta.add(linea_meta(37800, 0, 30, 450))

    all_sprites.add(lineas_meta)
    all_sprites.add(portales_cubo)
    all_sprites.add(imagenes)
    all_sprites.add(platforms)
    all_sprites.add(P1)
    all_sprites.add(orbes_amarillas)
    all_sprites.add(portales_cohete)
    all_sprites.add(plataformas_amarillas)
    all_sprites.add(palos)
    all_sprites.add(plataformasGrandes)
    all_sprites.add(spikes)
    all_sprites.add(portales_ufo)
    #para arriba, estructuras y musica
    #para abajo ejecucion de juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausado = not pausado
                    if pausado:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    P1.salto()
            
        screen.blit(fondo, (0, 0))
        progress_bar.update(P1.pos.x)
        progress_bar.draw()
        teclas = pygame.key.get_pressed()
        camera_offset_x = P1.pos.x - WIDTH // 2
        



        if pausado:
    
            pausar_overlay = pygame.Surface((WIDTH, HEIGHT))
            pausar_overlay.set_alpha(150)     
            pausar_overlay.fill((0, 0, 0))    
            screen.blit(pausar_overlay, (0, 0))

        
            font1 = pygame.font.Font(None, 80)
            font2 = pygame.font.Font(None, 40)
            texto = font1.render("PAUSA", True, (255, 255, 255))
            screen.blit(texto, (350, 150))
            texto = font2.render("Continuar: 'escape' ", True, (255, 255, 255))
            screen.blit(texto, (100, 300))
            texto = font2.render("Salir: 'enter'", True, (255, 255, 255))
            screen.blit(texto, (580, 300))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from menu_niveles import niveles
                    niveles(config)
                        
            pygame.display.update()
            continue  

            
        P1.move()
        P1.update()
        if pygame.sprite.spritecollide(P1, spikes, False):
            sonido_muerte.play()
            P1.pos=vec(100, 400)
            P1.vel=vec(0,0)
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)
            for orbe in orbes_amarillas: 
                orbe.usado = False
            P1.modo_cohete=False
            P1.modo_ufo=False

        if not nivel_terminado and pygame.sprite.spritecollide(P1, lineas_meta, False):
            nivel_terminado=True

        if nivel_terminado:
            pausar_overlay = pygame.Surface((WIDTH, HEIGHT))
            pausar_overlay.set_alpha(150)     
            pausar_overlay.fill((0, 0, 0))    
            screen.blit(pausar_overlay, (0, 0))
            font1 = pygame.font.Font(None, 80)
            font2 = pygame.font.Font(None, 40)
            texto = font1.render("¡COMPLETADO!", True, (255, 255, 255))
            screen.blit(texto, (260, 150))
            texto = font2.render("Volver: 'enter'", True, (255, 255, 255))
            screen.blit(texto, (350, 300))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from menu_niveles import niveles
                    niveles(config)
            pygame.display.update()
            continue
        camera_offset_x = P1.pos.x - WIDTH // 2

        for entity in all_sprites:
            displaysurface.blit(entity.surf, (entity.rect.x - camera_offset_x, entity.rect.y))
        
        
    
        pygame.display.update()
        FramePerSec.tick(FPS)



if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    el_nivel_3(config)