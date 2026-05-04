

import pygame
from ui import MainMenu, SettingsScreen, LeaderboardScreen, GameOverScreen, UsernameScreen
from racer import Game
from persistence import load_settings, save_settings, load_leaderboard, save_score

def main():
    pygame.init()
    pygame.mixer.init()

    # ── Window setup ──────────────────────────────────────────────────────────
    SCREEN_W, SCREEN_H = 500, 700
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("TSIS 3 Racer")
    clock = pygame.time.Clock()

    # ── Load persisted settings ───────────────────────────────────────────────
    settings = load_settings()

    # ── State machine ─────────────────────────────────────────────────────────
    state = "main_menu"   # current screen / game state
    username = ""
    last_result = None    # result dict returned by Game after a run

    while True:
        if state == "main_menu":
            action = MainMenu(screen, clock).run()
            if action == "play":
                state = "username"
            elif action == "leaderboard":
                state = "leaderboard"
            elif action == "settings":
                state = "settings"
            elif action == "quit":
                break

        elif state == "username":
            name = UsernameScreen(screen, clock).run()
            if name is None:          # player pressed Back
                state = "main_menu"
            else:
                username = name or "Player"
                state = "game"

        elif state == "game":
            # Run a full game session; returns a result dict on finish
            result = Game(screen, clock, settings, username).run()
            last_result = result
            if result:
                # Persist the score
                save_score(username, result["score"], result["distance"], result["coins"])
            state = "game_over"

        elif state == "game_over":
            action = GameOverScreen(screen, clock, last_result).run()
            if action == "retry":
                state = "game"
            else:
                state = "main_menu"

        elif state == "leaderboard":
            entries = load_leaderboard()
            action = LeaderboardScreen(screen, clock, entries).run()
            state = "main_menu"

        elif state == "settings":
            new_settings = SettingsScreen(screen, clock, settings).run()
            if new_settings:
                settings = new_settings
                save_settings(settings)
            state = "main_menu"

    pygame.quit()

if __name__ == "__main__":
    main()