import sys
import math
import pygame
from clock import get_current_time, get_hand_angle

WINDOW_TITLE  = "Mickey's Clock"
WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600
BG_COLOR      = (255, 255, 255)
FPS           = 30
PIVOT_X       = WINDOW_WIDTH  // 2
PIVOT_Y       = WINDOW_HEIGHT // 2
HAND_IMAGE_PATH  = "images/mickey_hand.png"
FALLBACK_WIDTH   = 20
FALLBACK_HEIGHT  = 120
MINUTES_COLOR    = (255, 80, 80)
SECONDS_COLOR    = (80, 80, 255)
FONT_SIZE        = 48
FONT_COLOR       = (30, 30, 30)

def draw_hand(surface, hand_img, angle_deg, pivot):
    if hand_img is not None:
        rotated = pygame.transform.rotate(hand_img, -angle_deg + 90)
        rect = rotated.get_rect(center=pivot)
        surface.blit(rotated, rect)

def load_hand_image(path):
    try:
        mirrored = pygame.image.load(path).convert_alpha()
        image = pygame.transform.flip(mirrored, True, False)
        return image, mirrored
    except (pygame.error, FileNotFoundError):
        print(f"Error: Could not load image at {path}")
        return None, None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    minutes_img, seconds_img = load_hand_image(HAND_IMAGE_PATH)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        minutes, seconds = get_current_time()
        min_angle = get_hand_angle(minutes + seconds / 60, 60)
        sec_angle = get_hand_angle(seconds, 60)

        screen.fill(BG_COLOR)
        pivot = (PIVOT_X, PIVOT_Y)

        draw_hand(screen, seconds_img, sec_angle, pivot)
        draw_hand(screen, minutes_img, min_angle, pivot)

        pygame.draw.circle(screen, (0, 0, 0), pivot, 10)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()