import pygame
from pygame.locals import *
import sys

pygame.init()
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 900
FPS = 60

def el_nivel_2(config):
    pausado = False
    nivel_terminado = False
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.mixer.music.load("assets/sounds/Lvl2/ASGORE.mp3") 
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nivel 2")

    fondo = pygame.image.load("assets/img/fondos/2do_nivel.jpg").convert() 
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    class linea_meta(pygame.sprite.Sprite):   
        
        def __init__(self, x, y, w=20, h=30):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/Metas_paredes/linea_meta.jpg").convert_alpha() #cambiar esta linea de meta
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

    class portal_cohete(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((120, 120, 120))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/portal_cohete.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class GravityBlock(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=40):
            super().__init__()
            self.surf = pygame.image.load("assets/img/plataformas_signos/diamante.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))
            self.rect = self.surf.get_rect(topleft=(x, y))

    class Spike(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h, orientacion = 'up'):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255, 255, 0)) 
            self.rect = self.surf.get_rect(topleft=(x, y))   
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/pincho.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w+5, h+5))

            if orientacion == 'down':
                self.surf = pygame.transform.rotate(self.surf, 180)
                self.rect = self.surf.get_rect(bottomleft=(x, y + h))
            else:
                self.rect = self.surf.get_rect(topleft=(x, y))
            

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
            self.surf = pygame.image.load("assets/img/obstaculos_jugador/plataforma_2.jpg").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    #class platformBase(pygame.sprite.Sprite):
        #def __init__(self, x, y, w, h):
            #super().__init__()
            #self.surf = pygame.Surface((w, h))
            #self.surf.fill((255,0,255))
            #self.rect = self.surf.get_rect(topleft=(x, y))
            #self.surf = pygame.image.load("assets_nivel1/plataforma.jpg").convert_alpha()#assets/img/plataformas_signos/piso_base.png
            #self.surf = pygame.transform.scale(self.surf, (w, h))


    class plataformamuro(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((255,0,255))
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.surf = pygame.image.load("assets/img/plataformas_signos/muro.jpg").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (w, h))

    class JumpPad(pygame.sprite.Sprite):
        def __init__(self, x, y, w=40, h=10):
            super().__init__()
            self.surf = pygame.Surface((w, h))
            self.surf.fill((0, 0, 255)) # Color Azul
            self.rect = self.surf.get_rect(topleft=(x, y))


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.original_surf = pygame.image.load("assets/img/obstaculos_jugador/cubo_jugador_2.jpg").convert_alpha()
            self.original_surf = pygame.transform.scale(self.original_surf, (35, 35))

            self.surf = self.original_surf.copy()

            self.rect = self.surf.get_rect(center = (10, 420))


            self.pos = vec((110, 400))
            self.vel = vec(0,0)
            self.acc = vec(0,0)

            self.angulo = False
            self.saltable = False
            self.modo_cohete = False
            # self.modo_ufo = False 
            self.inverted = False
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
                    # self.modo_ufo=False 
            
            # Portal UFO eliminado
            # for portal in portales_ufo: 
            #     if pygame.sprite.spritecollide(self, [portal], False):
            #         self.modo_ufo=True 
            #         self.modo_cohete=False 
            
            for portal in portales_cubo:
                if pygame.sprite.spritecollide(self, [portal], False):
                    # self.modo_ufo=False 
                    self.modo_cohete=False

        def salto(self):
            if self.saltable:
                self.vel.y=-5
                self.saltable=False
            # elif self.modo_ufo: 
            #     self.vel.y=-4.3 
            for orbe in orbes_amarillas:
                if pygame.sprite.spritecollide(self, [orbe], False):
                    orbe.usado = True

        def reset(self):
            self.pos = vec((110, 400))
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.saltable = False
            self.modo_cohete = False
            self.inverted = False # Asegúrate de que esto esté definido en __init__

    font = pygame.font.SysFont(None, 30)    
    imagenes = pygame.sprite.Group()
    palos=pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    portales_cohete = pygame.sprite.Group()
    plataformas_amarillas = pygame.sprite.Group()
    lineas_meta=pygame.sprite.Group()

    #for i in range(60):
        #plat = platformBase(i * 201, HEIGHT - 20, 200, 20)
        #platforms.add(plat)
    progress_bar = ProgresoBarra(displaysurface, total_distance=51600, width=300, height=15, color=(0, 255, 0), position=(20, 20))


    P1 = Player()
    all_sprites = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    orbes_amarillas = pygame.sprite.Group()
    jump_pads = pygame.sprite.Group() 
    gravity_blocks = pygame.sprite.Group()
    portales_cubo = pygame.sprite.Group()

    spikes.add(SpikePlataforma(0, -40, 51000, 20))
    spikes.add(SpikePlataforma(0, 480, 51000, 20))
    for i in range(50):
        spikes.add(Spike(483 + i*40, 405, 30, 30))
    for i in range(12):
        spikes.add(Spike(3200 + i*40, 350, 30, 30))
    platforms.add(platform(0, HEIGHT - 20, 4900, 20))
    for i in range(315):
        spikes.add(Spike(4400 + i*40, 415, 40, 40))
    #1
    platforms.add(platform(600, 380, 100, 20))
    #2
    platforms.add(platform(900, 350, 340, 20))
    spikes.add(Spike(1040, 320, 40, 40))
    #3
    platforms.add(platform(1300, 380, 100, 20))
    #4
    platforms.add(platform(1800, 180, 60, 20))
    #5
    platforms.add(platform(2120, 300, 60, 20))
    #6
    platforms.add(platform(2420, 380, 60, 20))
    #7
    platforms.add(platform(2900, 365, 60, 20))
    spikes.add(Spike(2910, 325, 40, 40)) 
    #8
    platforms.add(platform(3200, 365, 470, 20))
    #9
    platforms.add(platform(3900, 385, 470, 20))
    #10
    platforms.add(platform(4400, 350, 520, 20))
    spikes.add(Spike(4650, 310, 40, 40))  # Encima
    #for i in range(185):
        #spikes.add(Spike(4900 + i*40, 420, 40, 40))
    #11
    platforms.add(platform(5200, 330, 150, 20))
    #12
    platforms.add(platform(5600, 330, 150, 20))
    #13
    platforms.add(platform(6000, 330, 150, 20))
    #14
    platforms.add(platform(6400, 330, 150, 20))
    #15
    platforms.add(platform(6800, 330, 130, 20))
    spikes.add(Spike(6800, 320, 15, 10))
    spikes.add(Spike(6820, 320, 15, 10))
    spikes.add(Spike(6840, 320, 15, 10))
    spikes.add(Spike(6860, 320, 15, 10))
    spikes.add(Spike(6880, 320, 15, 10))
    spikes.add(Spike(6900, 320, 15, 10))
    #16
    platforms.add(platform(6700, 385, 300, 20))
    #17
    platforms.add(platform(7500, 270, 150, 20))
    #18
    platforms.add(platform(8150, 180, 50, 20))
    #19
    platforms.add(platform(8300, 210, 50, 20))
    #20
    platforms.add(platform(8450, 240, 50, 20))
    #21
    platforms.add(platform(8600, 270, 90, 20))
    #22
    platforms.add(platform(8750, 300, 60, 20))
    spikes.add(Spike(8750, 290, 15, 10))
    spikes.add(Spike(8770, 290, 15, 10))
    spikes.add(Spike(8790, 290, 15, 10))
    spikes.add(Spike(8810, 290, 15, 10))
    #23
    platforms.add(platform(8900, 270, 1100, 20))
    spikes.add(Spike(9200, 240, 40, 40))
    spikes.add(Spike(9225, 240, 40, 40))
    spikes.add(Spike(9600, 240, 40, 40))
    spikes.add(Spike(9625, 240, 40, 40))
    #24
    platforms.add(platform(10200, 320, 50, 20))
    #25
    platforms.add(platform(10500, 280, 50, 20))
    #26
    platforms.add(platform(10800, 240, 50, 20))
    #27
    platforms.add(platform(11100, 200, 400, 20))
    #28
    platforms.add(platform(11600, 260, 400, 20))
    #spikes.add(Spike(12200, 200, 40, 40))
    #29
    platforms.add(platform(12100, 200, 400, 20))
    #30
    platforms.add(platform(12600, 150, 600, 20))
    spikes.add(Spike(12850, 130, 40, 40))

    platforms.add(platform(13300, 140, 400, 20))#31
    platforms.add(platform(13800, 170, 600, 20))#32
    #platforms.add(platform(13800, 250, 400, 20))#32
    platforms.add(platform(14600, 220, 50, 20))#33
    platforms.add(platform(14800, 270, 50, 20))#34
    platforms.add(platform(15000, 330, 50, 20))#35
    platforms.add(platform(15500, 350, 500, 20))#36
    platforms.add(platform(16300, 310, 50, 20))#37
    platforms.add(platform(16600, 270, 200, 20))#38

    #Pasillo
    platforms.add(platform(17000, 100, 2400, 20,))
    for x in range(17000, 17000 + 2400, 40):  
        spikes.add(Spike(x, 120, 20, 20, orientacion='down'))  
    platforms.add(platform(17000, 380, 2400, 20))
    for x in range(17000, 17000 + 2400, 40):
        spikes.add(Spike(x, 360, 20, 20))

    # Primera W superior
    platforms.add(platform(20450, 160, 100, 20))  # Base izquierda
    platforms.add(platform(20550, 120, 100, 20))  # Pico izquierdo
    platforms.add(platform(20650, 80, 100, 20))  # Base central
    platforms.add(platform(20750, 120, 100, 20))  # Pico derecho
    platforms.add(platform(20850, 160, 100, 20))  # Base derecha
    spikes.add(Spike(20450, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(20490, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(20550, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(20590, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(20650, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(20690, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(20750, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(20790, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(20850, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(20890, 160, 40, 40, orientacion='down'))

    # Primera W inferior 
    platforms.add(platform(20450, 400, 100, 20))  # Base izquierda
    platforms.add(platform(20550, 360, 100, 20))  # Pico izquierdo
    platforms.add(platform(20650, 320, 100, 20))  # Base central
    platforms.add(platform(20750, 360, 100, 20))  # Pico derecho
    platforms.add(platform(20850, 400, 100, 20))  # Base derecha
    spikes.add(Spike(20450, 380, 40, 40))
    spikes.add(Spike(20490, 380, 40, 40))
    spikes.add(Spike(20550, 340, 40, 40))
    spikes.add(Spike(20590, 340, 40, 40))
    spikes.add(Spike(20650, 300, 40, 40))
    spikes.add(Spike(20690, 300, 40, 40))
    spikes.add(Spike(20750, 340, 40, 40))
    spikes.add(Spike(20790, 340, 40, 40))
    spikes.add(Spike(20850, 380, 40, 40))
    spikes.add(Spike(20890, 380, 40, 40))

    # Segunda W superior
    platforms.add(platform(20950, 160, 100, 20))  # Base izquierda
    platforms.add(platform(21050, 120, 100, 20))  # Pico izquierdo
    platforms.add(platform(21150, 80, 100, 20))  # Base central
    platforms.add(platform(21250, 120, 100, 20))  # Pico derecho
    platforms.add(platform(21350, 160, 100, 20))  # Base derecha
    spikes.add(Spike(20950, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(20990, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21050, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21090, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21150, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(21190, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(21250, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21290, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21350, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21390, 160, 40, 40, orientacion='down'))

    # Segunda W inferior 
    platforms.add(platform(20950, 400, 100, 20))  # Base izquierda
    platforms.add(platform(21050, 360, 100, 20))  # Pico izquierdo
    platforms.add(platform(21150, 320, 100, 20))  # Base central
    platforms.add(platform(21250, 360, 100, 20))  # Pico derecho
    platforms.add(platform(21350, 400, 100, 20))  # Base derecha
    spikes.add(Spike(20950, 380, 40, 40))
    spikes.add(Spike(20990, 380, 40, 40))
    spikes.add(Spike(21050, 340, 40, 40))
    spikes.add(Spike(21090, 340, 40, 40))
    spikes.add(Spike(21150, 300, 40, 40))
    spikes.add(Spike(21190, 300, 40, 40))
    spikes.add(Spike(21250, 340, 40, 40))
    spikes.add(Spike(21290, 340, 40, 40))
    spikes.add(Spike(21350, 380, 40, 40))
    spikes.add(Spike(21390, 380, 40, 40))

    # Tercera W superior
    platforms.add(platform(21450, 160, 100, 20))  # Base izquierda
    platforms.add(platform(21550, 120, 100, 20))  # Pico izquierdo
    platforms.add(platform(21650, 80, 100, 20))  # Base central
    platforms.add(platform(21750, 120, 100, 20))  # Pico derecho
    platforms.add(platform(21850, 160, 100, 20))  # Base derecha
    spikes.add(Spike(21450, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21490, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21550, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21590, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21650, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(21690, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(21750, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21790, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(21850, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21890, 160, 40, 40, orientacion='down'))

    # Tercera W inferior 
    platforms.add(platform(21450, 400, 100, 20))  # Base izquierda
    platforms.add(platform(21550, 360, 100, 20))  # Pico izquierdo
    platforms.add(platform(21650, 320, 100, 20))  # Base central
    platforms.add(platform(21750, 360, 100, 20))  # Pico derecho
    platforms.add(platform(21850, 400, 100, 20))  # Base derecha
    spikes.add(Spike(21450, 380, 40, 40))
    spikes.add(Spike(21490, 380, 40, 40))
    spikes.add(Spike(21550, 340, 40, 40))
    spikes.add(Spike(21590, 340, 40, 40))
    spikes.add(Spike(21650, 300, 40, 40))
    spikes.add(Spike(21690, 300, 40, 40))
    spikes.add(Spike(21750, 340, 40, 40))
    spikes.add(Spike(21790, 340, 40, 40))
    spikes.add(Spike(21850, 380, 40, 40))
    spikes.add(Spike(21890, 380, 40, 40))

    # Cuarta W superior
    platforms.add(platform(21950, 160, 100, 20))  # Base izquierda
    platforms.add(platform(22050, 120, 100, 20))  # Pico izquierdo
    platforms.add(platform(22150, 80, 100, 20))  # Base central
    platforms.add(platform(22250, 120, 100, 20))  # Pico derecho
    platforms.add(platform(22350, 160, 100, 20))  # Base derecha
    spikes.add(Spike(21950, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(21990, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(22050, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(22090, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(22150, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(22190, 80, 40, 40, orientacion='down'))
    spikes.add(Spike(22250, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(22290, 120, 40, 40, orientacion='down'))
    spikes.add(Spike(22350, 160, 40, 40, orientacion='down'))
    spikes.add(Spike(22390, 160, 40, 40, orientacion='down'))

    # Cuarta W inferior 
    platforms.add(platform(21950, 400, 100, 20))  # Base izquierda
    platforms.add(platform(22050, 360, 100, 20))  # Pico izquierdo
    platforms.add(platform(22150, 320, 100, 20))  # Base central
    platforms.add(platform(22250, 360, 100, 20))  # Pico derecho
    platforms.add(platform(22350, 400, 100, 20))  # Base derecha
    spikes.add(Spike(21950, 380, 40, 40))
    spikes.add(Spike(21990, 380, 40, 40))
    spikes.add(Spike(22050, 340, 40, 40))
    spikes.add(Spike(22090, 340, 40, 40))
    spikes.add(Spike(22150, 300, 40, 40))
    spikes.add(Spike(22190, 300, 40, 40))
    spikes.add(Spike(22250, 340, 40, 40))
    spikes.add(Spike(22290, 340, 40, 40))
    spikes.add(Spike(22350, 380, 40, 40))
    spikes.add(Spike(22390, 380, 40, 40))

    #Pilares
    platforms.add(platform(24500, 0, 60, 80))      # techo
    platforms.add(platform(24620, 330, 60, 120))   # suelo
    spikes.add(Spike(24620, 310, 40, 40))

    platforms.add(platform(24740, 0, 60, 150))     # techo
    platforms.add(platform(24860, 300, 60, 150))   # suelo
    spikes.add(Spike(24860, 280, 40, 40))

    platforms.add(platform(24980, 0, 60, 120))     # techo
    platforms.add(platform(25100, 370, 60, 80))    # suelo
    spikes.add(Spike(25100, 350, 40, 40))

    platforms.add(platform(25220, 0, 60, 80))# techo
    platforms.add(platform(25340, 330, 60, 120))   # suelo
    spikes.add(Spike(25340, 310, 40, 40))

    platforms.add(platform(25460, 0, 60, 150))     # techo
    platforms.add(platform(25580, 300, 60, 150))   # suelo
    spikes.add(Spike(25580, 280, 40, 40))

    platforms.add(platform(25700, 0, 60, 120))     # techo
    platforms.add(platform(25820, 370, 60, 80))    # suelo
    spikes.add(Spike(25820, 350, 40, 40))

    platforms.add(platform(25940, 0, 60, 80))      # techo
    platforms.add(platform(26060, 330, 60, 120))   # suelo
    spikes.add(Spike(26060, 310, 40, 40))

    platforms.add(platform(26180, 0, 60, 150))     # techo
    platforms.add(platform(26300, 300, 60, 150))   # suelo
    spikes.add(Spike(26300, 280, 40, 40))

    platforms.add(platform(26420, 0, 60, 120))     # techo
    platforms.add(platform(26540, 370, 60, 80))    # suelo
    spikes.add(Spike(26540, 350, 40, 40))

    platforms.add(platform(26660, 0, 60, 80))      # techo
    platforms.add(platform(26780, 330, 60, 120))   # suelo
    spikes.add(Spike(26780, 310, 40, 40))

    platforms.add(platform(26900, 0, 60, 80))      # techo
    platforms.add(platform(27020, 330, 60, 120))   # suelo
    spikes.add(Spike(27020, 310, 40, 40))

    platforms.add(platform(27140, 0, 60, 150))     # techo
    platforms.add(platform(27260, 300, 60, 150))   # suelo
    spikes.add(Spike(27260, 280, 40, 40))

    platforms.add(platform(27380, 0, 60, 120))     # techo
    platforms.add(platform(27500, 370, 60, 80))    # suelo
    spikes.add(Spike(27500, 350, 40, 40))

    platforms.add(platform(27620, 0, 60, 80))      # techo
    platforms.add(platform(27740, 330, 60, 120))   # suelo
    spikes.add(Spike(27740, 310, 40, 40))

    platforms.add(platform(27860, 0, 60, 150))     # techo
    platforms.add(platform(27980, 300, 60, 150))   # suelo
    spikes.add(Spike(27980, 280, 40, 40))

    platforms.add(platform(28100, 0, 60, 120))     # techo
    platforms.add(platform(28220, 370, 60, 80))    # suelo
    spikes.add(Spike(28220, 350, 40, 40)) 

    #plataformas horizontales
    platforms.add(platform(29300, 100, 50, 20))
    spikes.add(Spike(29300, 80, 40, 40))
    platforms.add(platform(29450, 270, 50, 20))
    spikes.add(Spike(29450, 250, 40, 40))
    platforms.add(platform(29600, 350, 50, 20))
    spikes.add(Spike(29600, 330, 40, 40))
    platforms.add(platform(29750, 180, 50, 20))
    spikes.add(Spike(29750, 160, 40, 40))
    platforms.add(platform(29900, 100, 50, 20))
    spikes.add(Spike(29900, 80, 40, 40))
    platforms.add(platform(30050, 350, 50, 20))
    spikes.add(Spike(30050, 330, 40, 40))
    platforms.add(platform(30200, 270, 50, 20))
    spikes.add(Spike(30200, 250, 40, 40))
    platforms.add(platform(30350, 100, 50, 20))
    spikes.add(Spike(30350, 80, 40, 40))
    platforms.add(platform(30500, 180, 50, 20))
    spikes.add(Spike(30500, 160, 40, 40))
    platforms.add(platform(30650, 350, 50, 20))
    spikes.add(Spike(30650, 330, 40, 40))
    platforms.add(platform(30800, 100, 50, 20))
    spikes.add(Spike(30800, 80, 40, 40))
    platforms.add(platform(30950, 270, 50, 20))
    spikes.add(Spike(30950, 250, 40, 40))
    platforms.add(platform(31100, 180, 50, 20))
    spikes.add(Spike(31100, 160, 40, 40))
    platforms.add(platform(31250, 350, 50, 20))
    spikes.add(Spike(31250, 320, 40, 40))
    platforms.add(platform(31400, 100, 50, 20))
    spikes.add(Spike(31400, 80, 40, 40))
    platforms.add(platform(31550, 270, 50, 20))
    spikes.add(Spike(31550, 250, 40, 40))
    platforms.add(platform(31700, 180, 50, 20))
    spikes.add(Spike(31700, 160, 40, 40))
    platforms.add(platform(31850, 350, 50, 20))
    spikes.add(Spike(31850, 330, 40, 40))
    platforms.add(platform(32000, 270, 50, 20))
    spikes.add(Spike(32000, 250, 40, 40))
    platforms.add(platform(32150, 100, 50, 20))
    spikes.add(Spike(32150, 80, 40, 40))

    platforms.add(platform(32750, 380, 700, 20))#39
    for i in range(315):
        spikes.add(Spike(32750 + i*40, 415, 40, 40))
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
    platforms.add(platform(38100, 240, 80, 20))#53: Caída 3 
    platforms.add(platform(38550, 310, 70, 20))#54
    platforms.add(platform(39000, 380, 100, 20))#56
    platforms.add(platform(39300, 330, 100, 20))#57
    platforms.add(platform(39600, 280, 100, 20))#58
    platforms.add(platform(39900, 250, 400, 20))#59 
    platforms.add(platform(40400, 220, 200, 20))#60
    platforms.add(platform(40800, 190, 200, 20))#61
    platforms.add(platform(41200, 160, 500, 20))#62
    platforms.add(platform(41900, 200, 5700, 20))#63
    for i in range(43):
        spikes.add(Spike(42800 + i*40, 170, 40, 40))
    spikes.add(Spike(42500, 180, 40, 40))
    spikes.add(Spike(43200, 100, 40, 40))
    spikes.add(Spike(43600, 100, 40, 40))
    spikes.add(Spike(44100, 100, 40, 40))
    platforms.add(platform(42800, 140, 1700, 20))#64
    spikes.add(Spike(45000, 170, 40, 40))
    spikes.add(Spike(45400, 170, 40, 40))
    spikes.add(Spike(45800, 170, 40, 40))
    spikes.add(Spike(46200, 170, 40, 40))
    spikes.add(Spike(46600, 170, 40, 40))
    spikes.add(Spike(47000, 170, 40, 40))
    spikes.add(Spike(47400, 170, 40, 40))

    platforms.add(platform(44700, 70, 2800, 20))#65
    spikes.add(Spike(45200, 90, 40, 40, orientacion='down'))
    spikes.add(Spike(45600, 90, 40, 40, orientacion='down'))
    spikes.add(Spike(46000, 90, 40, 40, orientacion='down'))
    spikes.add(Spike(46400, 90, 40, 40, orientacion='down'))
    spikes.add(Spike(46800, 90, 40, 40, orientacion='down'))
    platforms.add(platform(47800, 150, 200, 20))#66
    platforms.add(platform(48300, 170, 200, 20))#67
    platforms.add(platform(48700, 190, 400, 20))#68
    platforms.add(platform(49300, 270, 1400, 20))#69
    spikes.add(Spike(49800, 230, 40, 40))
    platforms.add(platform(50900, 310, 300, 20))#70
    spikes.add(Spike(50300, 230, 40, 40))
    spikes.add(Spike(51300, 280,40, 40))
    spikes.add(Spike(51300, 180, 40, 40, orientacion='down'))

    portal_cohete_nuevo = portal_cohete(16870, 240, 40, 40) 
    portales_cohete.add(portal_cohete_nuevo)
    all_sprites.add(portal_cohete_nuevo)

    portal_cubo_salida = portal_cubo(32800, 300, 40, 40) 
    portales_cubo.add(portal_cubo_salida)
    all_sprites.add(portal_cubo_salida)


    pygame.mixer.music.play(-1)


    pad_elevado = JumpPad(1400, 380, w=40, h=10)
    pad_elevado2 = JumpPad(6970, 380, w=40, h=10)
    pad_elevado3 = JumpPad(7600, 268, w=40, h=10)
    pad_elevado4 = JumpPad(15000, 320, w=40, h=10)
    jump_pads.add(pad_elevado)
    all_sprites.add(pad_elevado)
    jump_pads.add(pad_elevado2)
    all_sprites.add(pad_elevado2)
    jump_pads.add(pad_elevado3)
    all_sprites.add(pad_elevado3)
    jump_pads.add(pad_elevado4)
    all_sprites.add(pad_elevado4)
    all_sprites.add(lineas_meta)
    all_sprites.add(portales_cubo)
    all_sprites.add(imagenes)
    all_sprites.add(platforms)
    all_sprites.add(P1)
    all_sprites.add(orbes_amarillas)
    all_sprites.add(portales_cohete)
    all_sprites.add(plataformas_amarillas)
    all_sprites.add(palos)
    all_sprites.add(spikes)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausado = not pausado
                    if pausado:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    P1.salto()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
            P1.reset()
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)
            gravity_blocks.empty() 

            for orbe in orbes_amarillas: 
                orbe.usado = False
            P1.modo_cohete=False
            P1.modo_ufo=False
        
        jump_pad_hit = pygame.sprite.spritecollideany(P1, jump_pads)
        
        if jump_pad_hit:
            if not P1.modo_cohete and not P1.inverted:
                P1.vel.y = -10
                P1.saltable = False 
        
        gravity_hit = pygame.sprite.spritecollideany(P1, gravity_blocks)
        
        if gravity_hit and not P1.modo_cohete:

            P1.inverted = not P1.inverted 
            P1.vel.y = 0 
            gravity_hit.kill() 

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
        
        brillo = config.get("brillo", 100)
        oscuridad = 200 - int(200 * (brillo / 100))
        filtro = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, oscuridad))
        screen.blit(filtro, (0, 0))

        pygame.display.update()
        FramePerSec.tick(FPS)



if __name__ == "__main__":
    config = {"brillo": 100, "volumen": 100}
    el_nivel_2(config)