import sys
import pygame
from ball import Ball

WINDOW_TITLE  = "Moving Ball"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480
FPS           = 60
BG_COLOR      = (255, 255, 255)
BALL_RADIUS   = 25
BALL_COLOR    = (220, 40, 40)
STEP          = 20


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont(None, 22)

    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_RADIUS, BALL_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_UP:    ball.move( 0,    -STEP, WINDOW_WIDTH, WINDOW_HEIGHT)
                elif event.key == pygame.K_DOWN:  ball.move( 0,    +STEP, WINDOW_WIDTH, WINDOW_HEIGHT)
                elif event.key == pygame.K_LEFT:  ball.move(-STEP,  0,    WINDOW_WIDTH, WINDOW_HEIGHT)
                elif event.key == pygame.K_RIGHT: ball.move(+STEP,  0,    WINDOW_WIDTH, WINDOW_HEIGHT)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)
        ball.draw(screen)

        info = font.render(
            f"Position: ({ball.x}, {ball.y})   |   Press Q to quit",
            True, (120, 120, 120)
        )
        screen.blit(info, (8, WINDOW_HEIGHT - 24))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()