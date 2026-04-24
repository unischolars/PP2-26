import pygame, sys
from pygame.locals import *
import random, time
import os

# --- PATH HANDLING ---
# This ensures the game looks for files in the same folder as this script
FOLDER = os.path.dirname(os.path.abspath(__file__))

def get_path(name):
    return os.path.join(FOLDER, name)

# Initializing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

sfx = pygame.mixer.Sound(r"C:\Users\rozao\Pop\work\Practice-10\racer\lose.mp3")

# Setting up Fonts
font_small = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 60)

# Create Screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer - Coin Collector")

# Load Background (Using the absolute path)
background = pygame.image.load(get_path("AnimatedStreet.png"))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Load enemy image using the absolute path
        self.image = pygame.image.load(get_path("Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a 30x30 pixel transparent surface for the coin
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # Draw a yellow circle (Color: 255, 223, 0) in the center
        # (surface, color, center_coordinates, radius)
        pygame.draw.circle(self.image, (255, 223, 0), (15, 15), 12)
        
        # Optional: Add a black border to make the circle "pop" against the road
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 12, 2)
        
        self.rect = self.image.get_rect()
        self.spawn()
        self.weight=random.randrange(1,5)

    def spawn(self):
        """Randomly places the coin at the top of the screen"""
        # We use -50 so it starts off-screen and falls into view
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def move(self):
        global COINS_COLLECTED
        self.rect.move_ip(0, SPEED)
        # If the player misses the coin, it respawns at the top
        if (self.rect.top > 600):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Load player image using the absolute path
        self.image = pygame.image.load(get_path("Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Setup Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Adding a new User event to increase speed over time
INC_SPEED = pygame.USEREVENT + 1

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw Background
    DISPLAYSURF.blit(background, (0,0))

    # Render Score (Top Left) and Coins (Top Right)
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_count = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    
    DISPLAYSURF.blit(scores, (10, 10))
    # Positioning coin count at the top right
    DISPLAYSURF.blit(coin_count, (SCREEN_WIDTH - 110, 10))

    # Move and Draw all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check for Coin Collection
    if pygame.sprite.spritecollide(P1, coins, False):
        COINS_COLLECTED += random.randrange(1,5)
        
        SPEED =5+ (COINS_COLLECTED // 5)
        # pygame.mixer.Sound(get_path('coin_sound.wav')).play()
        C1.spawn() # Respawn the coin at the top

    # Check for Enemy Collision
    if pygame.sprite.spritecollideany(P1, enemies):
        sfx.play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        msg = game_over_font.render("GAME OVER", True, BLACK)
        DISPLAYSURF.blit(msg, (30, 250))
        pygame.display.update()
        
        # Kill all sprites and wait before closing
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
         
    pygame.display.update()
    FramePerSec.tick(FPS)