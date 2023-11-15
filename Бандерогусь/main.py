import random                                              #підключення випадкових чисел
import os


import pygame                                              #імпорт бібліотеки
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT         #імпортування вихід, клавіши вниз, вверх, вліво, вправо


pygame.init()                                              #ініціалізування гри


FPS = pygame.time.Clock()                                  #постійний такт строрення константи


HEIGHT = 800                                               #розмір екрана для гри висота, а те ща написано капсом вважається константой їх можно не змінювати
WIDTH = 1400                                               #ширина екрана


FONT = pygame.font.SysFont('Verdana', 20)


COLOR_WHITE = (255, 255, 255)                              #константа кольору, білий
COLOR_BLACK = (0, 0, 0)     
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 1, 1)


main_display = pygame.display.set_mode((WIDTH, HEIGHT))    #встановлення основного екрана в розміри наших констант((тапл)) 


bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3


IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


player_size = (20, 20)                                     #розміри гравця
player = pygame.image.load('player.png').convert_alpha()   # pygame.Surface(player_size)                #гравець
                                                          # player.fill(COLOR_BLACK)                   #кольор гравця
player_rect = player.get_rect(midleft=(0, 300))            #рект(прямокутник) поверне координати на 0 0
                                                          #player_speed = [1, 1]                       #швидкість змінной
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]




def create_enemy():
   #enemy_size = (30, 30)
   enemy = pygame.image.load('enemy.png').convert_alpha() # pygame.Surface(enemy_size)
   # enemy.fill(COLOR_BLUE)
   enemy_size = enemy.get_size()
   enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT - enemy.get_height()), *enemy.get_size())
   enemy_move = [random.randint(-8, -4), 0]
   return [enemy, enemy_rect, enemy_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)


enemies = []


score = 0


image_index = 0


def create_bonus():
   #bonus_size = (15, 15)
   bonus = pygame.image.load('bonus.png').convert_alpha() # pygame.Surface(bonus_size)
   bonus_size = bonus.get_size()
   # bonus.fill(COLOR_RED)
   bonus_rect = pygame.Rect(random.randint(bonus.get_width(), WIDTH - bonus.get_width()), -bonus.get_height(), *bonus.get_size())
   bonus_move = [0, random.randint(4, 8)]
   return [bonus, bonus_rect, bonus_move]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)


bonuses = []




playing = True                                             #поки грає то да
while playing:                                             #початок цикла (функція віділяється тіла 4 пробіла)
   FPS.tick(240)                                          #встановлення фпс
   for event in pygame.event.get():
       if event.type == QUIT:
           playing = False
       if event.type == CREATE_ENEMY:
           enemies.append(create_enemy())
       if event.type == CREATE_BONUS:
           bonuses.append(create_bonus())                 #якщо цикл закінчився то закрити
       if event.type == CHANGE_IMAGE:
           player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
           image_index += 1
           if image_index >= len(PLAYER_IMAGES):
               image_index = 0  
  
                                                          # main_display.fill(COLOR_BLACK)   #замальювання дисплея після його руху
  
   bg_X1 -= bg_move
   bg_X2 -= bg_move


   if bg_X1 < -bg.get_width():
       bg_X1 = bg.get_width()


   if bg_X2 < -bg.get_width():
       bg_X2 = bg.get_width()   


   main_display.blit(bg, (bg_X1, 0))
   main_display.blit(bg, (bg_X2, 0))


   keys = pygame.key.get_pressed()  


   if keys[K_DOWN] and player_rect.bottom < HEIGHT:
       player_rect = player_rect.move(player_move_down)


   if keys[K_RIGHT] and player_rect.right < WIDTH:
       player_rect = player_rect.move(player_move_right)       
  
   if keys[K_UP] and player_rect.top > 0:
       player_rect = player_rect.move(player_move_up)       
   
   if keys[K_LEFT] and player_rect.left > 0:
       player_rect = player_rect.move(player_move_left)


   for enemy in enemies:
       enemy[1] = enemy[1].move(enemy[2])
       main_display.blit(enemy[0], enemy[1])


       if player_rect.colliderect(enemy[1]):
           playing = False


   for bonus in bonuses:
       bonus[1] = bonus[1].move(bonus[2])
       main_display.blit(bonus[0], bonus[1])


       if player_rect.colliderect(bonus[1]):
           score += 1
           bonuses.pop(bonuses.index(bonus)) 


                                                           #  enemy_rect = enemy_rect.move(enemy_move)
 


   # if player_rect.bottom >= HEIGHT:                      #змінювання руху його по висоті
   #     player_speed = random.choice(([1, -1], [-1, -1])) #чоіс вибір руху рандомно або вліво або вправо


   # if player_rect.right >= WIDTH:                        #відбиття від правої частини
   #     player_speed = random.choice(([-1, -1], [-1, 1]))


   # if player_rect.top <= 0:                              #верхня частина відбиття
   #     player_speed = random.choice(([-1, 1], [1, 1]))
      
   # if player_rect.left < 0:                              #відбиття від лівої стінки
   #     player_speed = random.choice(([1, 1], [1, -1]))


   main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
   main_display.blit(player, player_rect)                  #розташування гравця на полі




                                                           #  main_display.blit(enemy, enemy_rect)


   # player_rect = player_rect.move(player_speed)          #передає значення руху гравця і швидкості


   pygame.display.flip()                                   #оновлення гравця


   for enemy in enemies:
       if enemy[1].right < 0:
           enemies.pop(enemies.index(enemy))


   for bonus in bonuses:
       if bonus[1].top > HEIGHT:
           bonuses.pop(bonuses.index(bonus))

