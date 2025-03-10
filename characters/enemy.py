import pygame
import random
import constants

# Clase de enemigo
class Enemy:
    def __init__(self):
        # Tamaño del enemigo
        self.radius = 10
        # Velocidad y dirección
        self.speed = random.randint(3, 3)
        self.direction = random.choice([-1, 1])
        # Color del enemigo
        self.color = (255, 0, 0)

        # Posición inicial
        # Desde la derecha
        if self.direction == -1:
            self.x = constants.WIDTH_WINDOW + self.radius
        # Desde la izquierda
        else:
            self.x = -self.radius

        # Posición vertical aleatoria
        self.y = random.randint(100, constants.HEIGHT_WINDOW - 100)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    # Mover el enemigo
    def move(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Reaparecer en el lado opuesto
        if self.direction == -1 and self.x < -self.radius:
            self.x = constants.WIDTH_WINDOW + self.radius
        elif self.direction == 1 and self.x > constants.WIDTH_WINDOW + self.radius:
            self.x = -self.radius

    # Dibujar el enemigo
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    # Verificar colisión con el jugador
    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
