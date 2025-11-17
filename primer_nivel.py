import pygame
from pygame.locals import *
import sys

pygame.init()
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 900
FPS = 60



def el_nivel_1(config):

    pausado = False
    nivel_terminado = False
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    

    sonido_muerte = pygame.mixer.Sound("assets/sounds/muerte/candidato_muerte.wav")

    pygame.mixer.music.load("assets/sounds/Lvl1/Ruder_Buster.mp3")
    volumen = config.get("volumen", 100)/100
    pygame.mixer.music.set_volume(volumen)
    sonido_muerte.set_volume(volumen)



    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 1")


    fondo = pygame.image.load("assets/img/fondos/1er_lvl.png").convert()   
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))


    #clases
    class portal_cubo(pygame.sprite.Sprite):        
        def __init__(self, x, y, w=20, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/portal_cubo.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
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

            self.bg_color = (50, 50, 50)   # fondo gris
            self.current_width = 0          # progreso actual
            self.progress_percent = 0       # porcentaje inicial
            self.font = pygame.font.Font(None, 24)  # fuente para texto

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
            self.surf.fill((255, 0, 0)) 
            self.rect = self.surf.get_rect(topleft=(x, y)) 
            self.surf.set_alpha(0)
            

    class platform(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,0))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/plat.jpg").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class platformBase(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/piso_lvl1.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))


    class platformGrande(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/plat_grande.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class platfpalo(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/palo.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
            


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.original_surf = pygame.image.load("assets/img/obstaculos_jugador/cubo_jugador_1.png").convert_alpha()
            self.original_surf = pygame.transform.scale(self.original_surf, (35, 35))

            self.surf = self.original_surf.copy()
            self.rect = self.surf.get_rect(center = (10, 420))

            self.pos = vec((80, 300))  
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
                    if mouse[0] or keys[pygame.K_SPACE]:        
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
            
    

    font = pygame.font.SysFont(None, 30)    
    imagenes = pygame.sprite.Group()
    palos=pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    plataformasGrandes = pygame.sprite.Group()
    portales_cohete = pygame.sprite.Group()
    plataformas_amarillas = pygame.sprite.Group()
    portales_ufo=pygame.sprite.Group()
    lineas_meta=pygame.sprite.Group()
    for i in range(300):
        plat = platformBase(i * 201, HEIGHT - 20, 200, 20)
        platforms.add(plat)

    for i in range(300):
        plat = platformBase(i * 201, 0, 200, 20)
        platforms.add(plat)    



    progress_bar = ProgresoBarra(displaysurface, total_distance=20930, width=300, height=15, color=(0, 255, 0), position=(20, 20))
    P1 = Player()
    all_sprites = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    orbes_amarillas = pygame.sprite.Group()
    portales_cubo = pygame.sprite.Group()
    pygame.mixer.music.play(-1)


    #spikes para el techo
    for i in range(300):
        spikes.add(SpikePlataforma(i * 201, 0))




    #obstaculos
    platforms.add(platform(600, 380, 100, 20))
    spikes.add(SpikePlataforma(600, 383)) 

    spikes.add(Spike(760, 400, 30, 30))
    spikes.add(Spike(800, 400, 30, 30))
    spikes.add(Spike(840, 400, 30, 30))
    spikes.add(Spike(880, 400, 30, 30))
    spikes.add(Spike(920, 400, 30, 30))
    spikes.add(Spike(960, 400, 30, 30))


    platforms.add(platform(1000, 380, 100, 20))
    spikes.add(SpikePlataforma(1000, 383))

    spikes.add(Spike(1110, 400, 30, 30))
    spikes.add(Spike(1150, 400, 30, 30))
    spikes.add(Spike(1190, 400, 30, 30))
    spikes.add(Spike(1230, 400, 30, 30))
    spikes.add(Spike(1270, 400, 30, 30))


    platforms.add(platform(1300, 350, 80, 20))
    spikes.add(SpikePlataforma(1300, 353))

    spikes.add(Spike(1390, 400, 30, 30))
    spikes.add(Spike(1430, 400, 30, 30))
    spikes.add(Spike(1470, 400, 30, 30))
    spikes.add(Spike(1510, 400, 30, 30))
    spikes.add(Spike(1550, 400, 30, 30))
    spikes.add(Spike(1590, 400, 30, 30))
    spikes.add(Spike(1630, 400, 30, 30))

    platforms.add(platform(1690, 350, 80, 20))
    spikes.add(SpikePlataforma(1690, 353))

    spikes.add(Spike(1780, 400, 30, 30))
    spikes.add(Spike(1820, 400, 30, 30))
    spikes.add(Spike(1860, 400, 30, 30))
    spikes.add(Spike(1900, 400, 30, 30))
    spikes.add(Spike(1940, 400, 30, 30))
    spikes.add(Spike(1980, 400, 30, 30))

    platforms.add(platform(1980, 320, 50, 20))
    spikes.add(SpikePlataforma(1980, 323))

    platforms.add(platform(2170, 350, 80, 20))
    spikes.add(SpikePlataforma(2170, 353))

    platforms.add(platform(2350, 380, 80, 20))
    spikes.add(SpikePlataforma(2350, 383))

    spikes.add(Spike(2450, 400, 30, 30))
    spikes.add(Spike(2490, 400, 30, 30))
    spikes.add(Spike(2530, 400, 30, 30))
    spikes.add(Spike(2570, 400, 30, 30))
    spikes.add(Spike(2610, 400, 30, 30))

    platforms.add(platform(2700, 350, 70, 20))
    spikes.add(SpikePlataforma(2700, 353))

    platforms.add(platform(3020, 310, 100, 20))
    spikes.add(SpikePlataforma(3000, 313))

    spikes.add(Spike(3270, 400, 30, 30))
    spikes.add(Spike(3310, 400, 30, 30))
    spikes.add(Spike(3350, 400, 30, 30))
    spikes.add(Spike(3390, 400, 30, 30))
    spikes.add(Spike(3430, 400, 30, 30))
    spikes.add(Spike(3470, 400, 30, 30))

    #plat salto
    plataformas_amarillas.add(platf_amarilla(3570, 410))

    #spikes
    for i in range(18):
        spikes.add(Spike(3670 + i*40, 405, 30, 30))


    platforms.add(platform(4000, 250, 200, 20))
    spikes.add(SpikePlataforma(4000, 253))

    #orbe 1
    orbes_amarillas.add(orbe_amarilla(4370, 300, 20, 20))

    platforms.add(platform(4550, 280, 200, 20))
    spikes.add(SpikePlataforma(4550, 283))

    for i in range(5):
        spikes.add(Spike(4570 + i*40, 405, 30, 30))


    #plat fake
    platforms.add(platform(4840, 200, 150, 20))
    spikes.add(SpikePlataforma(4840, 203))
    spikes.add(Spike(4860, 170, 30, 30))
    spikes.add(Spike(4900, 170, 30, 30))
    spikes.add(Spike(4940, 170, 30, 30))

    #plat debajo 
    platforms.add(platform(4840, 340, 150, 20))
    spikes.add(SpikePlataforma(4840, 343))

    #orbes pegadas 2
    orbes_amarillas.add(orbe_amarilla(5400, 360, 20, 20))
    orbes_amarillas.add(orbe_amarilla(5430, 360, 20, 20))
    orbes_amarillas.add(orbe_amarilla(5460, 360, 20, 20))

    spikes.add(Spike(5560, 400, 30, 30))
    spikes.add(Spike(5600, 400, 30, 30))
    spikes.add(Spike(5640, 400, 30, 30))
    spikes.add(Spike(5680, 400, 30, 30))

    #plat salto
    plataformas_amarillas.add(platf_amarilla(5900, 410))

    #spikes
    for i in range(5):
        spikes.add(Spike(6000 + i*40, 405, 30, 30))

    #plat
    platforms.add(platform(6370, 240, 220, 20))
    spikes.add(SpikePlataforma(6370, 343))
    spikes.add(Spike(6560, 210, 30, 30))

    #spikes
    for i in range(5):
        spikes.add(Spike(6370 + i*40, 405, 30, 30))


    #portal cohete
    portales_cohete.add(portal_cohete(7000, 330, 30, 80))


    #plat grande abajo
    plataformasGrandes.add(platformGrande(7300, 380, 500, 150))
    spikes.add(SpikePlataforma(7300, 380, 10, 500))
    spikes.add(SpikePlataforma(7310, 380, 500, 10))
    spikes.add(SpikePlataforma(7800, 380, 10, 500)) 

    #platf grande arriba
    plataformasGrandes.add(platformGrande(7300, 80, 500, 150))
    spikes.add(SpikePlataforma(7300, 70, 500, 10))
    spikes.add(SpikePlataforma(7300, 230, 500, 10))
    spikes.add(SpikePlataforma(7310, 70, 10, 170))
    spikes.add(SpikePlataforma(7800, 70, 10, 170))


    #palos
    palos.add(platfpalo(8000, 330, 20, 120)) #abajo 
    spikes.add(SpikePlataforma(8000, 330, 20, 120))
    palos.add(platfpalo(8000, 0, 20, 120)) #arriba
    spikes.add(SpikePlataforma(8000, 0, 20, 120))

    palos.add(platfpalo(8350, 300, 20, 150)) #abajo 
    spikes.add(SpikePlataforma(8350, 300, 20, 150))
    palos.add(platfpalo(8350, 0, 20, 200)) #arriba 
    spikes.add(SpikePlataforma(8350, 0, 20, 200))

    palos.add(platfpalo(8700, 380, 20, 180)) #abajo 
    spikes.add(SpikePlataforma(8700, 380, 20, 180))
    palos.add(platfpalo(8710, 10, 20, 200)) #arriba 
    spikes.add(SpikePlataforma(8710, 10, 20, 200))

    palos.add(platfpalo(9050, 340, 20, 180)) #abajo 
    spikes.add(SpikePlataforma(9050, 340, 20, 180))
    palos.add(platfpalo(9070, 20, 20, 150)) #arriba 
    spikes.add(SpikePlataforma(9070, 20, 20, 150))

    palos.add(platfpalo(9300, 230, 20, 100)) #medio 
    spikes.add(SpikePlataforma(9300, 230, 20, 100))

    palos.add(platfpalo(9550, 45, 20, 150)) #medio 
    spikes.add(SpikePlataforma(9550, 45, 20, 150))

    palos.add(platfpalo(9780, 350, 20, 140)) #medio 
    spikes.add(SpikePlataforma(9780, 350, 20, 140))

    palos.add(platfpalo(10080, 230, 20, 200)) #medio 
    spikes.add(SpikePlataforma(10080, 230, 20, 200))

    palos.add(platfpalo(10280, 340, 20, 220)) #abajo 
    spikes.add(SpikePlataforma(10280, 340, 20, 220))
    palos.add(platfpalo(10280, 0, 20, 130)) #arriba 
    spikes.add(SpikePlataforma(10280, 0, 20, 130))

    palos.add(platfpalo(10580, 50, 20, 240)) #medio 
    spikes.add(SpikePlataforma(10580, 50, 20, 240))

    palos.add(platfpalo(10800, 350, 20, 240)) #medio 
    spikes.add(SpikePlataforma(10800, 350, 20, 240))

    palos.add(platfpalo(11100, 50, 20, 140)) 
    spikes.add(SpikePlataforma(11100, 50, 20, 140))

    palos.add(platfpalo(11320, 350, 20, 160))  
    spikes.add(SpikePlataforma(11320, 350, 20, 100))

    palos.add(platfpalo(11590, 290, 20, 200))  
    spikes.add(SpikePlataforma(11590, 290, 20, 200))

    palos.add(platfpalo(11880, 210, 20, 210))  
    spikes.add(SpikePlataforma(11880, 210, 20, 210))

    palos.add(platfpalo(12050, 170, 20, 250))  
    spikes.add(SpikePlataforma(12050, 170, 20, 250))


    #pasillo de palos
    for i in range(12):
        palos.add(platfpalo(12300 + i*140, 140, 20, 290))  
        spikes.add(SpikePlataforma(12300 + i*140, 140, 20, 290))


    #tilde
    palos.add(platfpalo(14500, 0, 20, 450))
    imagenes.add(cruz(14400, 60, 80, 80))
    spikes.add(SpikePlataforma(14500, 0, 20, 170))
    imagenes.add(tick(14400, 200, 80, 80))
    imagenes.add(cruz(14400, 360, 80, 80))
    spikes.add(SpikePlataforma(14500, 340, 20, 90))    


    palos.add(platfpalo(14900, 0, 20, 450))
    imagenes.add(cruz(14800, 60, 80, 80))
    imagenes.add(cruz(14800, 200, 80, 80))
    spikes.add(SpikePlataforma(14900, 0, 20, 320))
    imagenes.add(tick(14800, 360, 80, 80))


    palos.add(platfpalo(15400, 0, 20, 450))
    imagenes.add(tick(15300, 60, 80, 80))
    imagenes.add(cruz(15300, 200, 80, 80))
    imagenes.add(cruz(15300, 360, 80, 80))
    spikes.add(SpikePlataforma(15400, 170, 20, 280))



    #tunel
    #plat grande abajo dsp de ticks
    plataformasGrandes.add(platformGrande(16200, 280, 500, 150))
    spikes.add(SpikePlataforma(16200, 280, 10, 500))
    spikes.add(SpikePlataforma(16210, 280, 500, 10))
    spikes.add(SpikePlataforma(16310, 280, 10, 500)) 

    #platf grande arriba dsp de ticks
    plataformasGrandes.add(platformGrande(16200, 0, 500, 150))
    spikes.add(SpikePlataforma(16200, 0, 500, 10))
    spikes.add(SpikePlataforma(16200, 0, 500, 10))
    spikes.add(SpikePlataforma(16210, 0, 10, 170))
    spikes.add(SpikePlataforma(16310, 0, 10, 170))

    portales_cubo.add(portal_cubo(16730, 150, 30, 80))


    #ultima fase 
    #plat salto
    plataformas_amarillas.add(platf_amarilla(17500, 410))
    #spike
    for i in range(11):
        spikes.add(Spike(17600 + i*40, 405, 30, 30))



    plataformas_amarillas.add(platf_amarilla(18100, 300))
    #spike
    for i in range(11):
        spikes.add(Spike(18200 + i*40, 405, 30, 30))


    plataformas_amarillas.add(platf_amarilla(18800, 300))
    for i in range(10):
        spikes.add(Spike(18950 + i*40, 405, 30, 30))


    #orbes
    orbes_amarillas.add(orbe_amarilla(19550, 360, 20, 20))
    orbes_amarillas.add(orbe_amarilla(19580, 360, 20, 20))
    orbes_amarillas.add(orbe_amarilla(19610, 360, 20, 20))

    for i in range(3):
        spikes.add(Spike(19660 + i*40, 405, 30, 30))

    orbes_amarillas.add(orbe_amarilla(19810, 340, 20, 20))
    orbes_amarillas.add(orbe_amarilla(19840, 340, 20, 20))
    orbes_amarillas.add(orbe_amarilla(19870, 340, 20, 20))


    #plat
    platforms.add(platform(20060, 330, 180, 20))
    spikes.add(SpikePlataforma(20060, 333))

    for i in range(3):
        spikes.add(Spike(20100 + i*40, 405, 30, 30))

    platforms.add(platform(20500, 380, 180, 20))
    spikes.add(SpikePlataforma(20500, 383))


    #palo arriba
    palos.add(platfpalo(20920, 0, 20, 270))
    spikes.add(SpikePlataforma(20920, 0, 20, 270))
    #portal final
    portales_cubo.add(portal_cubo(20900, 330, 30, 80))
    lineas_meta.add(linea_meta(21200, 0, 30, 450))


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


    #loop principal de mi nivel
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                P1.salto()

        screen.blit(fondo, (0, 0))
        
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
            texto = font2.render("Continuar: 'Escape' ", True, (255, 255, 255))
            screen.blit(texto, (100, 300))
            texto = font2.render("Salir: 'Enter'", True, (255, 255, 255))
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
            P1.pos=vec(10, 385)
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
            texto = font2.render("Volver: 'Enter'", True, (255, 255, 255))
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
        

        progress_bar.update(P1.pos.x)
        progress_bar.draw()
    
        brillo = config.get("brillo", 100)
        oscuridad = 200 - int(200 * (brillo / 100))
        filtro = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        screen.blit(filtro, (0, 0))

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    el_nivel_1(config)