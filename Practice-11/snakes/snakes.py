import pygame

from pygame.locals import *

import random
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))

def get_path(name):
    return os.path.join(FOLDER, name)

def ran60(bad):
    while True:
        num = random.randrange(0, 601, 10)
        if num != bad:
            return num
def ran40(bad):
    while True:
        num = random.randrange(0, 401, 10)
        if num != bad:
            return num
pygame.init()

screen = pygame.display.set_mode((600,400))


running = True

x = 50
y = 50

fruit_color = (200,120,0)

snake_color = (50,200,50)


segments = [[50,50],[60,50],[70,50],[80,50]]

dir ="r"

fruit = [ran60(segments[-1][0]),ran40(segments[-1][1]),random.randrange(1,5)]
eaten = 0
clock=pygame.time.Clock()
last_update = pygame.time.get_ticks()
level=int(eaten/3)

image_lib = {}


def load_image(path):
    loaded_image = image_lib.get(path)
    if loaded_image == None:
        
        original_image = pygame.image.load(path)
        loaded_image = pygame.transform.scale(original_image, (600, 400))
        image_lib[path] = loaded_image
    return loaded_image

pygame.mixer.music.load(get_path("mus.mp3"))
pygame.mixer.music.play()

sfx_lib = {}

def load_sfx(path):
    sfx = sfx_lib.get(path)
    if sfx == None:
        sfx = pygame.mixer.Sound(path)
        sfx_lib[path] = sfx
    return sfx


while running:
    level=int(eaten/3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            snake_color = (255,0,0)
            load_sfx(get_path("gc.wav")).play()
    current_time = pygame.time.get_ticks()
    

    klava = pygame.key.get_pressed()
    if klava[K_UP]: dir = "u"
    elif klava[K_DOWN]: dir = "d"
    elif klava[K_LEFT]: dir = "l"
    elif klava[K_RIGHT]: dir = "r"

    # Calculate where the head WILL be
    head_x = segments[-1][0]
    head_y = segments[-1][1]

    if dir == "r": head_x += 10
    elif dir == "l": head_x -= 10
    elif dir == "u": head_y -= 10
    elif dir == "d": head_y += 10 

    screen.fill((255,255,255))
    
    #Draw background
    screen.blit(load_image(get_path("wall.png")), (0, 0))

    font = pygame.font.SysFont("times new roman", 20)
    text = font.render("High score:" + str(int(eaten))+"level:"+str(int(level)), True, (250,250,250))
    lose = font.render("You lose, your score:" + str(int(eaten))+" your level:"+str(int(level)), True, (250,250,250))

    if head_x >= 600 or head_x < 0 or head_y >= 400 or head_y < 0:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 600, 400))
        screen.blit(lose, (150, 180))
        pygame.display.flip()
        pygame.time.delay(1000)
        running = False 
    else:
        # Move logic
        pygame.draw.rect(screen, fruit_color, pygame.Rect(fruit[0], fruit[1], 9, 9))
        segments.append([head_x, head_y])
        if head_x == fruit[0] and head_y == fruit[1]:
            eaten +=fruit[2]
            fruit = [ran60(segments[-1][0]),ran40(segments[-1][1]),random.randrange(1,5)]
        elif current_time - last_update >= 20000:
            fruit = [ran60(segments[-1][0]),ran40(segments[-1][1]),random.randrange(1,5)]
            last_update=current_time
        else:
            segments.pop(0)

        #Draw the Snake
        for segment in segments:
            pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0], segment[1], 9, 9))
        
        screen.blit(text, (200, 0))

    pygame.time.Clock().tick(3 + level*2)
    pygame.display.flip()
 