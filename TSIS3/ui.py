
import pygame
import sys

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = (18,  18,  28)
PANEL       = (30,  30,  50)
ACCENT      = (255, 200,  0)
ACCENT2     = (0,   200, 255)
WHITE       = (255, 255, 255)
GRAY        = (160, 160, 160)
DARK        = (10,  10,  20)
RED_HL      = (220,  60,  60)
GREEN_HL    = (60,  200,  80)
BTN_IDLE    = (50,  50,  80)
BTN_HOVER   = (80,  80, 130)
BTN_BORDER  = (100, 100, 160)

CAR_COLOR_OPTIONS = ["red", "blue", "green", "yellow"]
DIFFICULTY_OPTIONS = ["easy", "normal", "hard"]

CAR_PREVIEW = {
    "red":    (220,  50,  50),
    "blue":   ( 50, 100, 220),
    "green":  ( 50, 200,  80),
    "yellow": (240, 200,   0),
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def draw_button(surface: pygame.Surface, rect: pygame.Rect,
                text: str, font: pygame.font.Font,
                hover: bool = False) -> None:
    """Draw a rounded rectangle button with label."""
    color = BTN_HOVER if hover else BTN_IDLE
    pygame.draw.rect(surface, color,      rect, border_radius=10)
    pygame.draw.rect(surface, BTN_BORDER, rect, 2, border_radius=10)
    txt = font.render(text, True, WHITE)
    surface.blit(txt, txt.get_rect(center=rect.center))


def draw_title(surface: pygame.Surface, text: str,
               font: pygame.font.Font, y: int, color=ACCENT) -> None:
    """Draw centred title text."""
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(centerx=surface.get_width()//2, top=y))


def draw_bg(surface: pygame.Surface):
    """Gradient-ish background."""
    surface.fill(BG)
    # Subtle horizontal bands
    for i in range(0, surface.get_height(), 4):
        alpha = max(0, 10 - i // 40)
        pygame.draw.line(surface, (255, 255, 255), (0, i), (surface.get_width(), i))


# ─────────────────────────────────────────────────────────────────────────────
# MainMenu
# ─────────────────────────────────────────────────────────────────────────────
class MainMenu:
    """Shows Play / Leaderboard / Settings / Quit buttons."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.W, self.H = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_sub   = pygame.font.SysFont("Arial", 20)
        self.font_btn   = pygame.font.SysFont("Arial", 26, bold=True)

        bw, bh = 260, 54
        cx = self.W // 2
        labels = ["Play", "Leaderboard", "Settings", "Quit"]
        actions = ["play", "leaderboard", "settings", "quit"]
        self.buttons = []
        for i, (lbl, act) in enumerate(zip(labels, actions)):
            r = pygame.Rect(0, 0, bw, bh)
            r.center = (cx, 280 + i * 72)
            self.buttons.append((r, lbl, act))

    def run(self) -> str:
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for r, lbl, act in self.buttons:
                        if r.collidepoint(mx, my):
                            return act

            draw_bg(self.screen)

            # Title
            draw_title(self.screen, "🏎  RACER", self.font_title, 80, ACCENT)
            draw_title(self.screen, "TSIS 3  |  Arcade Edition",
                       self.font_sub, 148, ACCENT2)

            # Road decoration
            pygame.draw.rect(self.screen, (40, 40, 40), (160, 190, 180, 60), border_radius=6)
            for x in [195, 240, 285]:
                pygame.draw.rect(self.screen, WHITE, (x, 205, 30, 8), border_radius=3)

            for r, lbl, act in self.buttons:
                draw_button(self.screen, r, lbl, self.font_btn,
                            hover=r.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
# UsernameScreen
# ─────────────────────────────────────────────────────────────────────────────
class UsernameScreen:
    """Simple text-input screen for entering the player's name."""

    MAX_LEN = 16

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.W, self.H = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_input = pygame.font.SysFont("Arial", 32)
        self.font_btn   = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_hint  = pygame.font.SysFont("Arial", 18)
        self.text = ""

        cx = self.W // 2
        self.ok_rect   = pygame.Rect(cx - 130, 420, 120, 48)
        self.back_rect = pygame.Rect(cx +  10, 420, 120, 48)
        self.input_rect= pygame.Rect(cx - 150, 310, 300, 52)

    def run(self):
        cursor_tick = 0
        while True:
            cursor_tick += 1
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.text or "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif len(self.text) < self.MAX_LEN and event.unicode.isprintable():
                        self.text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.ok_rect.collidepoint(mx, my):
                        return self.text or "Player"
                    if self.back_rect.collidepoint(mx, my):
                        return None

            draw_bg(self.screen)
            draw_title(self.screen, "Enter Your Name", self.font_title, 200, ACCENT)

            # Input box
            pygame.draw.rect(self.screen, PANEL, self.input_rect, border_radius=8)
            pygame.draw.rect(self.screen, ACCENT2, self.input_rect, 2, border_radius=8)
            display = self.text
            if cursor_tick % 60 < 30:
                display += "|"
            txt = self.font_input.render(display, True, WHITE)
            self.screen.blit(txt, txt.get_rect(midleft=(self.input_rect.x + 12,
                                                         self.input_rect.centery)))

            hint = self.font_hint.render("Press Enter or click OK", True, GRAY)
            self.screen.blit(hint, hint.get_rect(centerx=self.W//2, top=370))

            draw_button(self.screen, self.ok_rect,   "OK",   self.font_btn,
                        hover=self.ok_rect.collidepoint(mx, my))
            draw_button(self.screen, self.back_rect, "Back", self.font_btn,
                        hover=self.back_rect.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
# SettingsScreen
# ─────────────────────────────────────────────────────────────────────────────
class SettingsScreen:
    """Toggle sound, pick car color, pick difficulty; returns updated settings."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 settings: dict):
        self.screen   = screen
        self.clock    = clock
        self.settings = dict(settings)   # work on a copy
        self.W, self.H = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_lbl   = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_btn   = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_sm    = pygame.font.SysFont("Arial", 17)

        cx = self.W // 2
        # Sound toggle button
        self.sound_rect = pygame.Rect(cx - 60, 190, 120, 42)
        # Car color buttons
        self.color_rects = []
        for i, col in enumerate(CAR_COLOR_OPTIONS):
            r = pygame.Rect(60 + i * 100, 310, 80, 42)
            self.color_rects.append((r, col))
        # Difficulty buttons
        self.diff_rects = []
        for i, d in enumerate(DIFFICULTY_OPTIONS):
            r = pygame.Rect(60 + i * 130, 420, 110, 42)
            self.diff_rects.append((r, d))
        # Save / Back
        self.save_rect = pygame.Rect(cx - 130, 530, 120, 48)
        self.back_rect = pygame.Rect(cx +  10, 530, 120, 48)

    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.sound_rect.collidepoint(mx, my):
                        self.settings["sound"] = not self.settings["sound"]
                    for r, col in self.color_rects:
                        if r.collidepoint(mx, my):
                            self.settings["car_color"] = col
                    for r, d in self.diff_rects:
                        if r.collidepoint(mx, my):
                            self.settings["difficulty"] = d
                    if self.save_rect.collidepoint(mx, my):
                        return self.settings
                    if self.back_rect.collidepoint(mx, my):
                        return None

            draw_bg(self.screen)
            draw_title(self.screen, "Settings", self.font_title, 100, ACCENT)

            # ── Sound toggle ───────────────────────────────────────────────────
            lbl = self.font_lbl.render("Sound:", True, WHITE)
            self.screen.blit(lbl, (60, 196))
            snd_lbl = "ON 🔊" if self.settings["sound"] else "OFF 🔇"
            draw_button(self.screen, self.sound_rect, snd_lbl, self.font_btn,
                        hover=self.sound_rect.collidepoint(mx, my))

            # ── Car colour ─────────────────────────────────────────────────────
            lbl2 = self.font_lbl.render("Car Colour:", True, WHITE)
            self.screen.blit(lbl2, (60, 272))
            for r, col in self.color_rects:
                selected = self.settings["car_color"] == col
                pygame.draw.rect(self.screen,
                                 (*CAR_PREVIEW[col],), r, border_radius=8)
                border_col = ACCENT if selected else BTN_BORDER
                pygame.draw.rect(self.screen, border_col, r, 3 if selected else 1,
                                 border_radius=8)
                name_txt = self.font_sm.render(col.capitalize(), True, WHITE)
                self.screen.blit(name_txt, name_txt.get_rect(centerx=r.centerx,
                                                              top=r.bottom + 4))

            # ── Difficulty ─────────────────────────────────────────────────────
            lbl3 = self.font_lbl.render("Difficulty:", True, WHITE)
            self.screen.blit(lbl3, (60, 385))
            for r, d in self.diff_rects:
                selected = self.settings["difficulty"] == d
                col = GREEN_HL if d == "easy" else (ACCENT if d == "normal" else RED_HL)
                bg  = (*col, 180) if selected else BTN_IDLE
                pygame.draw.rect(self.screen, bg, r, border_radius=8)
                border = col if selected else BTN_BORDER
                pygame.draw.rect(self.screen, border, r, 2, border_radius=8)
                dtxt = self.font_btn.render(d.capitalize(), True, WHITE)
                self.screen.blit(dtxt, dtxt.get_rect(center=r.center))

            # ── Buttons ────────────────────────────────────────────────────────
            draw_button(self.screen, self.save_rect, "Save", self.font_btn,
                        hover=self.save_rect.collidepoint(mx, my))
            draw_button(self.screen, self.back_rect, "Back", self.font_btn,
                        hover=self.back_rect.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
# LeaderboardScreen
# ─────────────────────────────────────────────────────────────────────────────
class LeaderboardScreen:
    """Display top-10 saved scores in a table."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 entries: list):
        self.screen  = screen
        self.clock   = clock
        self.entries = entries
        self.W, self.H = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_hdr   = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_row   = pygame.font.SysFont("Arial", 17)
        self.font_btn   = pygame.font.SysFont("Arial", 24, bold=True)
        self.back_rect  = pygame.Rect(self.W//2 - 70, self.H - 70, 140, 46)

    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (
                        pygame.K_ESCAPE, pygame.K_RETURN):
                    return "back"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(mx, my):
                        return "back"

            draw_bg(self.screen)
            draw_title(self.screen, "🏆 Leaderboard", self.font_title, 50, ACCENT)

            # Table header
            cols = [("#", 40), ("Name", 130), ("Score", 250), ("Dist m", 360), ("Coins", 440)]
            y0 = 120
            pygame.draw.rect(self.screen, PANEL, (30, y0 - 6, self.W - 60, 30), border_radius=6)
            for label, x in cols:
                hdr = self.font_hdr.render(label, True, ACCENT2)
                self.screen.blit(hdr, (x, y0))

            # Rows
            medals = {0: "🥇", 1: "🥈", 2: "🥉"}
            for i, entry in enumerate(self.entries[:10]):
                y = y0 + 36 + i * 34
                row_bg = (35, 35, 58) if i % 2 == 0 else (28, 28, 48)
                pygame.draw.rect(self.screen, row_bg, (30, y - 4, self.W - 60, 30), border_radius=4)
                rank_str = medals.get(i, str(i + 1))
                cells = [
                    (rank_str,                 40),
                    (entry.get("name", "?"),  130),
                    (str(entry.get("score",0)),250),
                    (str(entry.get("distance", 0)), 360),
                    (str(entry.get("coins", 0)), 440),
                ]
                for text, x in cells:
                    col = ACCENT if i == 0 else WHITE
                    txt = self.font_row.render(text, True, col)
                    self.screen.blit(txt, (x, y))

            if not self.entries:
                no_txt = self.font_hdr.render("No scores yet — be the first!", True, GRAY)
                self.screen.blit(no_txt, no_txt.get_rect(centerx=self.W//2, top=200))

            draw_button(self.screen, self.back_rect, "Back", self.font_btn,
                        hover=self.back_rect.collidepoint(mx, my))
            pygame.display.flip()
            self.clock.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
# GameOverScreen
# ─────────────────────────────────────────────────────────────────────────────
class GameOverScreen:
    """Show run results + Retry / Main Menu buttons."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 result: dict):
        self.screen = screen
        self.clock  = clock
        self.result = result or {}
        self.W, self.H = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_stat  = pygame.font.SysFont("Arial", 24)
        self.font_btn   = pygame.font.SysFont("Arial", 26, bold=True)

        cx = self.W // 2
        self.retry_rect = pygame.Rect(cx - 140, 490, 130, 50)
        self.menu_rect  = pygame.Rect(cx +  10, 490, 130, 50)

    def run(self) -> str:
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "retry"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.retry_rect.collidepoint(mx, my):
                        return "retry"
                    if self.menu_rect.collidepoint(mx, my):
                        return "menu"

            draw_bg(self.screen)

            # Title
            draw_title(self.screen, "GAME OVER", self.font_title, 120, RED_HL)

            # Stats panel
            panel = pygame.Rect(80, 220, self.W - 160, 240)
            pygame.draw.rect(self.screen, PANEL, panel, border_radius=12)
            pygame.draw.rect(self.screen, BTN_BORDER, panel, 2, border_radius=12)

            stats = [
                ("Score",    str(self.result.get("score",    0)), ACCENT),
                ("Distance", f"{int(self.result.get('distance', 0))} m", ACCENT2),
                ("Coins",    str(self.result.get("coins",    0)), (255, 220, 0)),
            ]
            for i, (label, value, col) in enumerate(stats):
                y = 240 + i * 64
                lbl_txt = self.font_stat.render(label + ":", True, GRAY)
                val_txt = self.font_stat.render(value,       True, col)
                self.screen.blit(lbl_txt, (120, y))
                self.screen.blit(val_txt, (self.W - 120 - val_txt.get_width(), y))

            hint = pygame.font.SysFont("Arial", 17).render(
                "Press R to retry or Esc for menu", True, GRAY)
            self.screen.blit(hint, hint.get_rect(centerx=self.W//2, top=474))

            draw_button(self.screen, self.retry_rect, "Retry",     self.font_btn,
                        hover=self.retry_rect.collidepoint(mx, my))
            draw_button(self.screen, self.menu_rect,  "Main Menu", self.font_btn,
                        hover=self.menu_rect.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)