import sys
import pygame
from player import MusicPlayer

WINDOW_TITLE   = "Pygame Music Player"
WINDOW_WIDTH   = 500
WINDOW_HEIGHT  = 340
FPS            = 30
MUSIC_DIR      = "music"

BG_COLOR       = ( 20,  20,  30)
PANEL_COLOR    = ( 35,  35,  55)
ACCENT_COLOR   = ( 90, 180, 255)
TEXT_PRIMARY   = (230, 230, 240)
TEXT_SECONDARY = (140, 140, 160)
TEXT_PLAYING   = ( 80, 220, 120)
TEXT_STOPPED   = (200,  80,  80)

MARGIN         = 30
KEY_HINT_Y_START = 220


def draw_ui(screen, player, fonts):
    font_large, font_medium, font_small = fonts
    screen.fill(BG_COLOR)

    panel_rect = pygame.Rect(MARGIN, 20, WINDOW_WIDTH - 2 * MARGIN, 170)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=12)
    pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, width=1, border_radius=12)

    screen.blit(font_large.render("♪  Music Player", True, ACCENT_COLOR), (MARGIN + 16, 34))
    screen.blit(font_medium.render(player.current_track_name, True, TEXT_PRIMARY), (MARGIN + 16, 82))
    screen.blit(font_small.render(player.playlist_info, True, TEXT_SECONDARY), (MARGIN + 16, 116))

    status_color = TEXT_PLAYING if player.playing else TEXT_STOPPED
    screen.blit(font_medium.render(f"● {player.status_label}", True, status_color), (MARGIN + 16, 142))

    bindings = [
        ("[P]  Play",           TEXT_PLAYING),
        ("[S]  Stop",           TEXT_STOPPED),
        ("[N]  Next track",     TEXT_SECONDARY),
        ("[B]  Previous track", TEXT_SECONDARY),
        ("[Q]  Quit",           TEXT_SECONDARY),
    ]
    y = KEY_HINT_Y_START
    screen.blit(font_small.render("Keyboard controls:", True, ACCENT_COLOR), (MARGIN, y))
    y += 28
    for label, color in bindings:
        screen.blit(font_small.render(label, True, color), (MARGIN, y))
        y += 22

    pygame.display.flip()


def main():
    pygame.init()
    screen     = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    tick_clock = pygame.time.Clock()

    fonts = (
        pygame.font.SysFont(None, 32),
        pygame.font.SysFont(None, 24),
        pygame.font.SysFont(None, 20),
    )

    player = MusicPlayer(MUSIC_DIR)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_p: player.play()
                elif event.key == pygame.K_s: player.stop()
                elif event.key == pygame.K_n: player.next_track()
                elif event.key == pygame.K_b: player.prev_track()
                elif event.key == pygame.K_q:
                    player.stop()
                    pygame.quit()
                    sys.exit()

        player.update_playing_status()
        draw_ui(screen, player, fonts)
        tick_clock.tick(FPS)


if __name__ == "__main__":
    main()