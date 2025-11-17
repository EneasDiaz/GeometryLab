import pygame

class ProgresoBarra:
        def __init__(self, screen, total_distance, width=300, height=15, color=(0, 255, 0), position=(20, 20), show_text=True):
            """
            screen: superficie de pygame donde se dibuja la barra
            total_distance: distancia total del nivel (posición X del final del mapa)
            width, height: tamaño de la barra
            color: color del progreso (RGB)
            position: (x, y) posición en pantalla
            show_text: si True, muestra el porcentaje numérico
            """
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
            """
            Actualiza el ancho de la barra según la posición del jugador.
            """
            progress_ratio = min(player_x / self.total_distance, 1)
            self.current_width = int(self.width * progress_ratio)
            self.progress_percent = int(progress_ratio * 100)

        def draw(self):
            """
            Dibuja la barra en pantalla.
            """
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