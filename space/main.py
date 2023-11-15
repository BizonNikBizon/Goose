import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение констант
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
ASTEROID_SIZE = 50
ASTEROID_SPEED = 2

# Определение цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра с астероидами")

# Создание игрока
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)

# Создание списков для астероидов и пуль
asteroids = []
bullets = []

# Функция для создания астероида
def create_asteroid():
    x = random.randint(0, WIDTH - ASTEROID_SIZE)
    y = random.randint(-ASTEROID_SIZE, 0)
    asteroid = pygame.Rect(x, y, ASTEROID_SIZE, ASTEROID_SIZE)
    asteroids.append(asteroid)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Создание пули
                bullet = pygame.Rect(player.centerx, player.top, 5, 10)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += PLAYER_SPEED

    # Движение астероидов
    for asteroid in asteroids:
        asteroid.y += ASTEROID_SPEED

        # Проверка столкновения астероида с игроком
        if asteroid.colliderect(player):
            running = False

    # Удаление астероидов, которые вышли за границу экрана
    asteroids = [asteroid for asteroid in asteroids if asteroid.y < HEIGHT]

    # Движение пуль
    bullets = [bullet for bullet in bullets if bullet.y > 0]
    for bullet in bullets:
        bullet.y -= 10

    # Создание новых астероидов
    if random.random() < 0.02:
        create_asteroid()

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player)
    for asteroid in asteroids:
        pygame.draw.rect(screen, WHITE, asteroid)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    pygame.display.update()
    clock.tick(60)

# Завершение игры
pygame.quit()
