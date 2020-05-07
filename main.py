import pygame
import random
import math
from pygame import mixer

pygame.init()
icon = pygame.image.load('spaceship.png')
bg_image = pygame.image.load('2myiG0.jpg')

enemy_image_list = []
enemy_x_list = []
enemy_y_list = []
e_x_change_factor_list = []
e_y_change_factor_list = []
number_of_enemies = 6
enemy_image = pygame.image.load('enemy.png')
bullet_image = pygame.image.load('bullet.png')
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Veeha's Space Invaders")
e_x_change_factor = 4
e_y_change_factor = 10
x_change_factor = 5
running = True
px, py = 370, 480
by = 480
ex, ey = random.randint(0, 800), random.randint(50, 150)
bullet_state = "ready"
by_change_factor = 8
bx = 0
playerX_change = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_value = 0
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

mixer.music.load('background.wav')
mixer.music.play(-1)

for m in range(number_of_enemies):
    enemy_image_list.append(pygame.image.load('enemy.png'))
    enemy_x_list.append(random.randint(0, 736))
    enemy_y_list.append(random.randint(50, 150))
    e_x_change_factor_list.append(e_x_change_factor)
    e_y_change_factor_list.append(e_y_change_factor)


def render_score(x, y):
    score = font.render("Score: {}".format(score_value), True, (255, 100, 0))
    screen.blit(score, (x, y))


def enemy(x, y, k):
    screen.blit(enemy_image_list[k], (x, y))


def player(x, y):
    screen.blit(icon, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 13, y - 10))


def is_collision_detected(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))
    if distance < 27:
        return True
    return False


def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 100, 0))
    screen.blit(game_over, (250, 200))


while running:
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bx = px
                    bullet(bx, by)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    px = px + playerX_change
    if px < 0:
        px = 0
    elif px > 736:
        px = 736

    for i in range(number_of_enemies):
        if enemy_y_list[i] >= 440:
            for j in range(number_of_enemies):
                enemy_y_list[j] = 2000
            game_over_text()
            break

        enemy_x_list[i] += e_x_change_factor_list[i]

        if enemy_x_list[i] <= 0:
            e_x_change_factor_list[i] = 5
            enemy_y_list[i] = enemy_y_list[i] + e_y_change_factor
        elif enemy_x_list[i] >= 750:
            e_x_change_factor_list[i] = -5
            enemy_y_list[i] = enemy_y_list[i] + e_y_change_factor

        if is_collision_detected(bx, by, enemy_x_list[i], enemy_y_list[i]):
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            score_value += 1
            by = 480
            bullet_state = "ready"
            enemy_x_list[i] = random.randint(300, 800)
            enemy_y_list[i] = random.randint(50, 150)

        enemy(enemy_x_list[i], enemy_y_list[i], i)

    if bullet_state is "fire":
        bullet(bx, by)
        by -= by_change_factor
    if by <= 50:
        by = 480
        bullet_state = "ready"

    player(px, py)
    render_score(10, 10)
    pygame.display.update()
