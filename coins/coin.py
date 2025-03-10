import pygame
import random
import constants

# Clase de moneda
class Coin:
    def __init__(self, x=None, y=None):
        self.image = pygame.image.load("assets/image/Coin/coin.png")
        # Ajusta el tamaño de la moneda
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Generar posición segura
        while True:
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(50, constants.WIDTH_WINDOW - 50)

            # Evita que quede en el suelo
            self.rect.y = random.randint(50, constants.HEIGHT_WINDOW - 200)

            # Verificar que no esté en el suelo ni plataformas
            if not self.rect.colliderect(pygame.Rect(0, constants.HEIGHT_WINDOW - 50, constants.WIDTH_WINDOW, 50)):
                break  # Solo sale del bucle si la posición es válida

    # Dibujar la moneda
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Verificar colisión con el jugador
    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
