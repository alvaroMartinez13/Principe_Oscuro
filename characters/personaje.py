import pygame

# Clase de personaje
class Personaje:
    def __init__(self, x, y, animations, animations_attack):
        self.flip = False
        self.animations = animations
        self.animations_attack = animations_attack
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]

        # Obtener el tamaño real de la imagen para que la colisión sea precisa
        img_width, img_height = self.image.get_size()

        # Definir el rectángulo de colisión con el mismo tamaño que la imagen
        self.shape = pygame.Rect(0, 0, img_width, img_height)

        # Centrar el rectángulo en la posición inicial del personaje
        self.shape.center = (x, y)

        # Estado del personaje
        self.is_moving = False
        self.is_attacking = False
        self.attack_phase = -1
        self.attack_chain_requested = False

    # Actualizar animaciones
    def update(self):
        cooldown_animation = 100

        # Actualizar animaciones de ataque
        if self.is_attacking and 0 <= self.attack_phase < len(self.animations_attack):
            # Actualizar la imagen actual
            if 0 <= self.frame_index < len(self.animations_attack[self.attack_phase]):
                self.image = self.animations_attack[self.attack_phase][self.frame_index]
            # Actualizar el índice de la imagen
            if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
                self.update_time = pygame.time.get_ticks()
                # Cambiar a la siguiente imagen
                if self.frame_index < len(self.animations_attack[self.attack_phase]) - 1:
                    self.frame_index += 1
                # Cambiar de fase de ataque
                else:
                    if self.attack_phase == 0:
                        self.attack_phase = 1
                        self.frame_index = 0
                    elif self.attack_phase == 1 and self.attack_chain_requested:
                        self.attack_phase = 2
                        self.frame_index = 0
                    else:
                        self.is_attacking = False
                        self.attack_phase = -1
                        self.frame_index = 0
                        self.attack_chain_requested = False

            return

        if self.is_moving:
            if 0 <= self.frame_index < len(self.animations):
                self.image = self.animations[self.frame_index]

            if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            if self.frame_index >= len(self.animations):
                self.frame_index = 1
        else:
            self.frame_index = 0

        if not self.is_attacking and 0 <= self.frame_index < len(self.animations):
            self.image = self.animations[self.frame_index]

    def attack(self, attack_type):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_phase = 0  # Se pone en posición inicial del ataque
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        elif self.attack_phase == 1 and attack_type == "H":
            if len(self.animations_attack) > 2:
                self.attack_chain_requested = True

    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interface.blit(image_flip, self.shape)

    def movePlayer(self, delta_x, delta_y):
        if self.is_attacking:
            return
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.is_moving = delta_x != 0 or delta_y != 0
        self.shape.x += delta_x
        self.shape.y += delta_y

    def get_attack_hitbox(self):
        if not self.is_attacking or self.attack_phase < 1:
            return None  # No hay hitbox si no está atacando

        # Definir el área de impacto frente al personaje
        # Ajusta según el alcance del ataque
        attack_width = 50
        # Mitad de la altura del personaje
        attack_height = self.shape.height // 2
        # Ajuste basado en la dirección
        offset_x = 20 if not self.flip else -attack_width - 20

        # Crear y devolver el rectángulo de colisión
        return pygame.Rect(
            self.shape.centerx + offset_x,
            self.shape.centery - attack_height // 2,
            attack_width,
            attack_height
        )
