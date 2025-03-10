import pygame
import constants
from characters.personaje import Personaje
from coins.coin import Coin
from characters.enemy import Enemy
from utils.helpers import scale_image

pygame.init()

# Inicializar ventana
window = pygame.display.set_mode((constants.WIDTH_WINDOW, constants.HEIGHT_WINDOW))
pygame.display.set_caption("El principe de la noche")

# Fuentes para los mensajes
font_big = pygame.font.Font("assets/fonts/LGGothic.ttf", 60)
font_small = pygame.font.Font("assets/fonts/LGGothic.ttf", 30)

# Cargar imágenes de corazones
full_heart = scale_image(pygame.image.load("assets/image/Heart/full_heart.png"), 0.3)
empty_heart = scale_image(pygame.image.load("assets/image/Heart/empty_heart.png"), 0.3)

# Cargar animaciones del personaje
animations = [scale_image(pygame.image.load(f"assets/image/Player/Walk/Walk-{i}.png"), constants.SCALE_PLAYER) for i in
              range(1, 8)]
image_default = scale_image(pygame.image.load("assets/image/Player/Idle/Idle-0.png"), constants.SCALE_PLAYER)
animations.insert(0, image_default)

animations_attack = [
    [scale_image(pygame.image.load(f"assets/image/Player/Attack/Attack_0/Attack_{i}.png"), constants.SCALE_PLAYER) for i
     in range(5)],
    [scale_image(pygame.image.load(f"assets/image/Player/Attack/Attack_1/Attack1_{i}.png"), constants.SCALE_PLAYER) for
     i in range(3)],
    [scale_image(pygame.image.load(f"assets/image/Player/Attack/Attack_2/Attack2_{i}.png"), constants.SCALE_PLAYER) for
     i in range(4)]
]

# Inicializar personaje
player = Personaje(constants.WIDTH_WINDOW // 2, constants.HEIGHT_WINDOW - 100, animations, animations_attack)
player.gravity = 0
player.on_ground = True
player.lives = 3

move_left = move_right = False

floor = pygame.Rect(0, constants.HEIGHT_WINDOW - 50, constants.WIDTH_WINDOW, 50)

platforms = [pygame.Rect(100, 420, 150, 20), pygame.Rect(350, 320, 180, 20), pygame.Rect(620, 220, 200, 20),
             pygame.Rect(430, 120, 160, 20), pygame.Rect(750, 90, 130, 20)]

# Generar monedas
coins = []
for _ in range(12):
    while True:
        new_coin = Coin()
        if not any(new_coin.rect.colliderect(obj) for obj in platforms + [floor]):
            coins.append(new_coin)
            break

# Enemigos
enemies = []
enemy_spawn_delay = 200
enemy_timer = 0

reloj = pygame.time.Clock()
score = 0
modal_active = False
modal_message = ""

# Indica si el modal es de victoria o derrota
modal_won = False


def show_modal(window, message, won):
    #Muestra el modal con estilos diferentes si ganas o pierdes.
    overlay = pygame.Surface((constants.WIDTH_WINDOW, constants.HEIGHT_WINDOW))
    overlay.set_alpha(180)

    if won:
        overlay.fill((34, 177, 76))
        text_color = (255, 255, 255)
        border_color = (0, 200, 0)
        msg = "¡Felicidades!"
    else:
        overlay.fill((150, 0, 0))
        text_color = (255, 255, 255)
        border_color = (200, 0, 0)
        msg = "¡No te rindas!"

    # Dibujar el modal
    window.blit(overlay, (0, 0))
    pygame.draw.rect(window, border_color, (100, 200, constants.WIDTH_WINDOW - 200, 250), border_radius=15)

    # Dibujar el texto
    title_text = font_big.render(msg, True, text_color)
    window.blit(title_text, (constants.WIDTH_WINDOW // 2 - title_text.get_width() // 2, 220))

    # Dibujar el mensaje
    body_text = font_small.render(message, True, text_color)
    window.blit(body_text, (constants.WIDTH_WINDOW // 2 - body_text.get_width() // 2, 280))

    # Dibujar el mensaje de salida
    exit_text = font_small.render("Presiona ENTER para continuar", True, text_color)
    window.blit(exit_text, (constants.WIDTH_WINDOW // 2 - exit_text.get_width() // 2, 350))

while constants.RUN:
    # Limitar la velocidad de la pantalla
    reloj.tick(constants.FPS)

    # Mostrar modal
    if modal_active:
        show_modal(window, modal_message, modal_won)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constants.RUN = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                constants.RUN = False  # Salir del juego
        continue

    # Dibujar elementos
    window.fill(constants.COLOR_BG)

    # Mover y dibujar personaje
    deltaX = constants.SPEED * (move_right - move_left)
    if not player.on_ground:
        player.gravity += 1
        player.shape.y += player.gravity

    # Verificar colisiones con plataformas
    player.on_ground = any(player.shape.colliderect(platform) and player.gravity > 0 for platform in
                           platforms) or player.shape.colliderect(floor)

    # Ajustar la posición del jugador si está en el suelo
    if player.on_ground:
        player.gravity = 0
        player.shape.bottom = min(platform.top for platform in platforms if player.shape.colliderect(platform)) if any(
            player.shape.colliderect(platform) for platform in platforms) else floor.top

    # Mover al jugador
    player.movePlayer(deltaX, 0)
    player.update()
    player.draw(window)

    # Dibujar plataformas
    pygame.draw.rect(window, (34, 139, 34), floor)
    for platform in platforms:
        pygame.draw.rect(window, (100, 100, 100), platform)

    # Dibujar monedas
    for coin in coins[:]:
        coin.draw(window)
        if coin.check_collision(player.shape):
            coins.remove(coin)
            score += 1

    # Enemigos aparecen
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_delay:
        enemies.append(Enemy())
        enemy_timer = 0

    # Colisión con enemigos
    attack_hitbox = player.get_attack_hitbox()
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw(window)

        # Verificar colisión con el jugador
        if attack_hitbox and enemy.rect.colliderect(attack_hitbox):
            enemies.remove(enemy)
        elif enemy.check_collision(player.shape) and not player.is_attacking:
            player.lives -= 1
            enemies.remove(enemy)
            if player.lives == 0:
                modal_active = True
                modal_won = False
                modal_message = f"Recogiste {score} monedas. ¡Vuelve a intentarlo!"

    # Mostrar corazones
    for i in range(3):
        x_pos = 10 + i * (full_heart.get_width() + 5)
        window.blit(full_heart if i < player.lives else empty_heart, (x_pos, 10))

    # Mostrar puntuación
    window.blit(font_small.render(f"Puntuación: {score}", True, (255, 255, 255)), (10, 50))

    # Mostrar mensaje de victoria
    if not coins:
        modal_active = True
        modal_won = True
        modal_message = f"Has recogido todas las monedas. ¡Gran trabajo!"

    # Actualizar pantalla
    for event in pygame.event.get():
        # Salir del juego
        if event.type == pygame.QUIT:
            constants.RUN = False

        # Movimiento del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: move_left = True
            if event.key == pygame.K_d: move_right = True
            if event.key == pygame.K_SPACE and player.on_ground: player.gravity = -18
            if event.key == pygame.K_f: player.attack("F")
            if event.key == pygame.K_h: player.attack("H")

        # Detener movimiento
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: move_left = False
            if event.key == pygame.K_d: move_right = False

    # Actualizar pantalla
    pygame.display.update()

pygame.quit()
