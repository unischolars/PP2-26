"""
racer.py — Core gameplay module for TSIS 3 Racer.

Implements:
  - Lane-based scrolling road with lane markings
  - Player car with keyboard control
  - Weighted coin spawning (Practice 11)
  - Traffic cars that end the run on collision (3.2)
  - Road obstacles: oil spills, potholes, speed bumps (3.2)
  - Lane hazard zones and nitro boost strips (3.1)
  - Three power-ups: Nitro, Shield, Repair (3.3)
  - Score = coins × value + distance bonus (3.4)
  - Difficulty scaling (3.2 / 3.4)
  - HUD: coins, score, distance, power-up timer (3.4)
  - Shield visual and invincibility flash
"""

import pygame
import random
import math

# ── Colours ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GRAY       = (100, 100, 100)
DARK_GRAY  = (50,  50,  50)
ROAD_COLOR = (60,  60,  60)
LINE_COLOR = (220, 220, 220)
GRASS_COLOR= (34,  139, 34)

RED        = (220, 50,  50)
BLUE       = (50,  100, 220)
GREEN      = (50,  200, 80)
YELLOW     = (255, 220, 0)
ORANGE     = (255, 140, 0)
CYAN       = (0,   220, 220)
PURPLE     = (160, 32,  240)
PINK       = (255, 105, 180)

# ── Car colour map (settings → RGB) ──────────────────────────────────────────
CAR_COLORS = {
    "red":    RED,
    "blue":   BLUE,
    "green":  GREEN,
    "yellow": YELLOW,
}

# ── Difficulty presets ────────────────────────────────────────────────────────
DIFFICULTY = {
    "easy":   {"base_speed": 4,  "traffic_interval": 120, "obstacle_interval": 180, "coin_speed_thresh": 20},
    "normal": {"base_speed": 5,  "traffic_interval": 90,  "obstacle_interval": 130, "coin_speed_thresh": 15},
    "hard":   {"base_speed": 7,  "traffic_interval": 60,  "obstacle_interval": 90,  "coin_speed_thresh": 10},
}

# ── Road geometry ─────────────────────────────────────────────────────────────
ROAD_LEFT   = 80    # x where road begins
ROAD_RIGHT  = 420   # x where road ends
ROAD_WIDTH  = ROAD_RIGHT - ROAD_LEFT
NUM_LANES   = 3
LANE_WIDTH  = ROAD_WIDTH // NUM_LANES


def lane_center(lane: int) -> int:
    """Return the x-centre pixel of lane 0/1/2."""
    return ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: PlayerCar
# ─────────────────────────────────────────────────────────────────────────────
class PlayerCar(pygame.sprite.Sprite):
    """Player-controlled car. Moves left/right between lanes."""

    WIDTH, HEIGHT = 40, 70

    def __init__(self, color: tuple, screen_h: int):
        super().__init__()
        self.lane       = 1          # start in centre lane
        self.color      = color
        self.screen_h   = screen_h
        self.y          = screen_h - 120
        self.x          = float(lane_center(self.lane))
        self.target_x   = self.x
        self.speed_x    = 8          # lateral slide speed (px/frame)
        self.shielded   = False      # Shield power-up active
        self.shield_hits = 0         # number of hits absorbed
        self.image      = self._draw()
        self.rect       = self.image.get_rect(center=(int(self.x), self.y))

    def _draw(self) -> pygame.Surface:
        """Render the car body onto a surface."""
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(surf, self.color, (5, 10, 30, 50), border_radius=6)
        # Windscreen
        pygame.draw.rect(surf, CYAN, (9, 14, 22, 14), border_radius=3)
        # Rear window
        pygame.draw.rect(surf, CYAN, (9, 42, 22, 10), border_radius=3)
        # Wheels
        for wx, wy in [(2, 12), (self.WIDTH-10, 12), (2, 46), (self.WIDTH-10, 46)]:
            pygame.draw.rect(surf, BLACK, (wx, wy, 8, 14), border_radius=3)
        # Shield glow
        if self.shielded:
            pygame.draw.ellipse(surf, (*CYAN, 80),
                                (-6, -6, self.WIDTH+12, self.HEIGHT+12))
        return surf

    def handle_input(self, keys):
        """Move to an adjacent lane on key press (once per press)."""
        if keys[pygame.K_LEFT] and self.lane > 0:
            self.lane -= 1
            self.target_x = float(lane_center(self.lane))
        if keys[pygame.K_RIGHT] and self.lane < NUM_LANES - 1:
            self.lane += 1
            self.target_x = float(lane_center(self.lane))

    def update(self):
        """Slide horizontally toward target lane."""
        dx = self.target_x - self.x
        if abs(dx) < self.speed_x:
            self.x = self.target_x
        else:
            self.x += math.copysign(self.speed_x, dx)
        self.image = self._draw()
        self.rect  = self.image.get_rect(center=(int(self.x), self.y))

    def absorb_hit(self) -> bool:
        """Try to absorb a collision with the shield. Returns True if absorbed."""
        if self.shielded:
            self.shielded = False
            return True
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: TrafficCar
# ─────────────────────────────────────────────────────────────────────────────
class TrafficCar(pygame.sprite.Sprite):
    """Enemy vehicle that scrolls down the screen."""

    WIDTH, HEIGHT = 40, 70

    def __init__(self, lane: int, speed: float):
        super().__init__()
        self.lane  = lane
        self.speed = speed
        self.color = random.choice([RED, BLUE, ORANGE, PURPLE, PINK])
        self.image = self._draw()
        start_y    = -self.HEIGHT - random.randint(0, 60)
        self.rect  = self.image.get_rect(center=(lane_center(lane), start_y))

    def _draw(self) -> pygame.Surface:
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (5, 10, 30, 50), border_radius=6)
        pygame.draw.rect(surf, CYAN, (9, 14, 22, 14), border_radius=3)
        pygame.draw.rect(surf, CYAN, (9, 42, 22, 10), border_radius=3)
        for wx, wy in [(2, 12), (self.WIDTH-10, 12), (2, 46), (self.WIDTH-10, 46)]:
            pygame.draw.rect(surf, BLACK, (wx, wy, 8, 14), border_radius=3)
        return surf

    def update(self, scroll_speed: float):
        self.rect.y += int(self.speed + scroll_speed)

    def off_screen(self, screen_h: int) -> bool:
        return self.rect.top > screen_h


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: Coin
# ─────────────────────────────────────────────────────────────────────────────
COIN_WEIGHTS = {1: 0.60, 3: 0.25, 5: 0.10, 10: 0.05}   # value: probability

class Coin(pygame.sprite.Sprite):
    """Weighted coin that scrolls down and awards different values."""

    def __init__(self):
        super().__init__()
        self.value = random.choices(
            list(COIN_WEIGHTS.keys()),
            weights=list(COIN_WEIGHTS.values())
        )[0]
        # Colour by value
        colors = {1: YELLOW, 3: ORANGE, 5: CYAN, 10: WHITE}
        self.color = colors[self.value]
        self.image = self._draw()
        lane = random.randint(0, NUM_LANES - 1)
        self.rect  = self.image.get_rect(center=(lane_center(lane), -20))

    def _draw(self) -> pygame.Surface:
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (12, 12), 12)
        pygame.draw.circle(surf, BLACK,      (12, 12), 12, 2)
        font = pygame.font.SysFont("Arial", 10, bold=True)
        txt  = font.render(str(self.value), True, BLACK)
        surf.blit(txt, txt.get_rect(center=(12, 12)))
        return surf

    def update(self, scroll_speed: float):
        self.rect.y += int(scroll_speed)

    def off_screen(self, screen_h: int) -> bool:
        return self.rect.top > screen_h


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: Obstacle  (oil spill, pothole, speed bump)
# ─────────────────────────────────────────────────────────────────────────────
OBSTACLE_TYPES = ["oil", "pothole", "bump"]

class Obstacle(pygame.sprite.Sprite):
    """Static road hazard the player must avoid."""

    def __init__(self):
        super().__init__()
        self.kind  = random.choice(OBSTACLE_TYPES)
        self.lane  = random.randint(0, NUM_LANES - 1)
        self.image = self._draw()
        self.rect  = self.image.get_rect(center=(lane_center(self.lane), -30))

    def _draw(self) -> pygame.Surface:
        if self.kind == "oil":
            surf = pygame.Surface((50, 26), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (20, 20, 80, 180), (0, 0, 50, 26))
            pygame.draw.ellipse(surf, (80, 80, 255, 80),  (5, 5, 40, 16))
        elif self.kind == "pothole":
            surf = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, DARK_GRAY, (0, 0, 36, 36))
            pygame.draw.ellipse(surf, BLACK,     (4, 4, 28, 28))
        else:  # bump
            surf = pygame.Surface((LANE_WIDTH - 10, 14), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 140, 0), (0, 0, LANE_WIDTH-10, 14), border_radius=4)
            pygame.draw.rect(surf, YELLOW, (0, 0, LANE_WIDTH-10, 14), 2, border_radius=4)
        return surf

    def update(self, scroll_speed: float):
        self.rect.y += int(scroll_speed)

    def off_screen(self, screen_h: int) -> bool:
        return self.rect.top > screen_h


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: LaneEvent  (nitro strip or slow zone)
# ─────────────────────────────────────────────────────────────────────────────
class LaneEvent(pygame.sprite.Sprite):
    """Full-lane event: nitro boost strip or slow-down zone."""

    def __init__(self, kind: str = None):
        super().__init__()
        self.kind  = kind or random.choice(["nitro", "slow"])
        self.lane  = random.randint(0, NUM_LANES - 1)
        self.active_timer = 0    # frames the effect lasts when player enters
        self.image = self._draw()
        self.rect  = self.image.get_rect(
            center=(lane_center(self.lane), -40))

    def _draw(self) -> pygame.Surface:
        surf = pygame.Surface((LANE_WIDTH - 4, 60), pygame.SRCALPHA)
        if self.kind == "nitro":
            color = (255, 100, 0, 140)
            label = "NITRO"
        else:
            color = (0, 100, 200, 140)
            label = "SLOW"
        pygame.draw.rect(surf, color, (0, 0, LANE_WIDTH-4, 60), border_radius=6)
        font = pygame.font.SysFont("Arial", 14, bold=True)
        txt  = font.render(label, True, WHITE)
        surf.blit(txt, txt.get_rect(center=(surf.get_width()//2, 30)))
        return surf

    def update(self, scroll_speed: float):
        self.rect.y += int(scroll_speed)

    def off_screen(self, screen_h: int) -> bool:
        return self.rect.top > screen_h


# ─────────────────────────────────────────────────────────────────────────────
# Sprite: PowerUp
# ─────────────────────────────────────────────────────────────────────────────
POWERUP_TYPES = ["nitro", "shield", "repair"]

class PowerUp(pygame.sprite.Sprite):
    """Collectible power-up. Disappears after TIMEOUT frames if not collected."""

    TIMEOUT = 300   # frames (~5 s at 60 fps) before auto-removal

    def __init__(self):
        super().__init__()
        self.kind  = random.choice(POWERUP_TYPES)
        self.lane  = random.randint(0, NUM_LANES - 1)
        self.timer = self.TIMEOUT
        self.image = self._draw()
        self.rect  = self.image.get_rect(center=(lane_center(self.lane), -30))

    def _draw(self) -> pygame.Surface:
        icons   = {"nitro": "⚡", "shield": "🛡", "repair": "🔧"}
        bg_cols = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
        surf    = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(surf, bg_cols[self.kind], (18, 18), 18)
        pygame.draw.circle(surf, WHITE, (18, 18), 18, 2)
        font = pygame.font.SysFont("Segoe UI Emoji", 18)
        txt  = font.render(icons[self.kind], True, WHITE)
        surf.blit(txt, txt.get_rect(center=(18, 18)))
        return surf

    def update(self, scroll_speed: float):
        self.rect.y += int(scroll_speed)
        self.timer  -= 1

    def expired(self) -> bool:
        return self.timer <= 0

    def off_screen(self, screen_h: int) -> bool:
        return self.rect.top > screen_h


# ─────────────────────────────────────────────────────────────────────────────
# Road renderer (scrolling stripes)
# ─────────────────────────────────────────────────────────────────────────────
class Road:
    """Draws the scrolling road background."""

    STRIPE_H = 40    # height of one dashed-line segment
    STRIPE_GAP = 20  # gap between segments

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w  = screen_w
        self.screen_h  = screen_h
        self.scroll_y  = 0.0

    def update(self, scroll_speed: float):
        self.scroll_y = (self.scroll_y + scroll_speed) % (self.STRIPE_H + self.STRIPE_GAP)

    def draw(self, surface: pygame.Surface):
        # Grass sides
        pygame.draw.rect(surface, GRASS_COLOR, (0, 0, ROAD_LEFT, self.screen_h))
        pygame.draw.rect(surface, GRASS_COLOR, (ROAD_RIGHT, 0,
                                                self.screen_w - ROAD_RIGHT, self.screen_h))
        # Road surface
        pygame.draw.rect(surface, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, self.screen_h))

        # Lane dividers (dashed white lines)
        for lane in range(1, NUM_LANES):
            x = ROAD_LEFT + lane * LANE_WIDTH
            y = -self.STRIPE_GAP + self.scroll_y
            while y < self.screen_h:
                pygame.draw.rect(surface, LINE_COLOR, (x - 2, int(y), 4, self.STRIPE_H))
                y += self.STRIPE_H + self.STRIPE_GAP

        # Road borders
        pygame.draw.rect(surface, WHITE, (ROAD_LEFT,  0, 4, self.screen_h))
        pygame.draw.rect(surface, WHITE, (ROAD_RIGHT - 4, 0, 4, self.screen_h))


# ─────────────────────────────────────────────────────────────────────────────
# Main Game class
# ─────────────────────────────────────────────────────────────────────────────
class Game:
    """Runs one full play session and returns a result dict."""

    FINISH_DISTANCE = 2000   # metres to reach finish line

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 settings: dict, username: str):
        self.screen   = screen
        self.clock    = clock
        self.settings = settings
        self.username = username
        self.W, self.H = screen.get_size()

        # Difficulty config
        diff_key = settings.get("difficulty", "normal")
        diff      = DIFFICULTY.get(diff_key, DIFFICULTY["normal"])
        self.base_speed          = diff["base_speed"]
        self.traffic_interval    = diff["traffic_interval"]
        self.obstacle_interval   = diff["obstacle_interval"]
        self.coin_speed_thresh   = diff["coin_speed_thresh"]

        # Road
        self.road = Road(self.W, self.H)

        # Player
        car_color = CAR_COLORS.get(settings.get("car_color", "red"), RED)
        self.player = PlayerCar(car_color, self.H)

        # Sprite groups
        self.traffic_group   = pygame.sprite.Group()
        self.coin_group      = pygame.sprite.Group()
        self.obstacle_group  = pygame.sprite.Group()
        self.powerup_group   = pygame.sprite.Group()
        self.lane_event_group= pygame.sprite.Group()

        # Timers / counters
        self.traffic_timer   = 0
        self.coin_timer      = 0
        self.obstacle_timer  = 0
        self.powerup_timer   = 0
        self.lane_event_timer= 0

        # Game state
        self.coins_collected  = 0
        self.coin_value_total = 0    # sum of coin values for score
        self.scroll_speed     = float(self.base_speed)
        self.distance         = 0.0  # metres driven
        self.frame            = 0
        self.running          = True

        # Active power-up state
        self.active_powerup        = None   # "nitro" | "shield" | "repair" | None
        self.powerup_remaining     = 0      # frames remaining
        self.nitro_boost           = 0.0    # extra speed from nitro

        # Invincibility flash frames after shield absorbs hit
        self.invincible_frames = 0

        # Font
        self.font_sm = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_md = pygame.font.SysFont("Arial", 24, bold=True)

        # Key state guard (prevent lane-sliding every frame)
        self._prev_keys = pygame.key.get_pressed()

    # ── Spawning helpers ──────────────────────────────────────────────────────

    def _player_lane(self) -> int:
        return self.player.lane

    def _safe_lane(self, exclude_lane: int = -1) -> int:
        """Pick a random lane different from the exclude lane."""
        choices = [l for l in range(NUM_LANES) if l != exclude_lane]
        return random.choice(choices) if choices else random.randint(0, NUM_LANES-1)

    def _spawn_traffic(self):
        """Spawn a traffic car, never in the player's lane if player is near top."""
        lane = self._safe_lane(self._player_lane())
        speed = self.scroll_speed * random.uniform(0.3, 0.8)
        car = TrafficCar(lane, speed)
        # ensure we don't overlap existing traffic
        for existing in self.traffic_group:
            if existing.lane == lane and existing.rect.top < 80:
                return
        self.traffic_group.add(car)

    def _spawn_coin(self):
        self.coin_group.add(Coin())

    def _spawn_obstacle(self):
        obs = Obstacle()
        # Don't spawn directly at player's lane if player is at bottom
        if obs.lane == self._player_lane():
            obs.lane = self._safe_lane(self._player_lane())
            obs.rect.centerx = lane_center(obs.lane)
        self.obstacle_group.add(obs)

    def _spawn_powerup(self):
        if len(self.powerup_group) == 0:   # only one at a time on road
            self.powerup_group.add(PowerUp())

    def _spawn_lane_event(self):
        self.lane_event_group.add(LaneEvent())

    # ── Power-up activation ───────────────────────────────────────────────────

    def _activate_powerup(self, kind: str):
        """Apply a power-up effect (only one active at a time)."""
        self.active_powerup = kind
        if kind == "nitro":
            self.powerup_remaining = 60 * 4   # 4 seconds
            self.nitro_boost = 3.0
        elif kind == "shield":
            self.powerup_remaining = 0         # shield lasts until hit
            self.player.shielded = True
        elif kind == "repair":
            self.powerup_remaining = 1         # instant; clears nearest obstacle
            # Remove the closest obstacle to the player
            closest = None
            best_dist = 9999
            for obs in self.obstacle_group:
                d = abs(obs.rect.centery - self.player.rect.centery)
                if d < best_dist:
                    best_dist = d
                    closest = obs
            if closest:
                closest.kill()
            self.active_powerup = None

    def _tick_powerup(self):
        if self.active_powerup == "nitro":
            self.powerup_remaining -= 1
            if self.powerup_remaining <= 0:
                self.active_powerup = None
                self.nitro_boost    = 0.0
        elif self.active_powerup == "shield":
            # Shield removed when a collision is absorbed (in collision check)
            if not self.player.shielded:
                self.active_powerup = None

    # ── Difficulty scaling ────────────────────────────────────────────────────

    def _scale_difficulty(self):
        """Increase speed and spawn rates as distance grows."""
        # Every 200 m travelled, bump speed by 0.3 (capped at base+5)
        bonus = min((self.distance // 200) * 0.3, 5.0)
        self.scroll_speed = self.base_speed + bonus + self.nitro_boost

        # Also increase traffic density (shorter interval)
        traffic_reduction = int(self.distance // 300) * 5
        self.traffic_interval = max(
            30,
            DIFFICULTY.get(self.settings.get("difficulty","normal"),
                           DIFFICULTY["normal"])["traffic_interval"] - traffic_reduction
        )

        # Increase speed when enough coins collected (Practice 11)
        if self.coins_collected >= self.coin_speed_thresh:
            self.scroll_speed += 1.0

    # ── Score calculation ─────────────────────────────────────────────────────

    def _calc_score(self) -> int:
        distance_bonus = int(self.distance * 2)
        coin_bonus     = self.coin_value_total * 10
        return coin_bonus + distance_bonus

    # ── HUD drawing ───────────────────────────────────────────────────────────

    def _draw_hud(self):
        """Render on-screen info: coins, score, distance, speed, power-up."""
        # Semi-transparent banner at top
        hud = pygame.Surface((self.W, 44), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 140))
        self.screen.blit(hud, (0, 0))

        # Coins (top-right)
        coin_txt = self.font_sm.render(f"🪙 {self.coins_collected}", True, YELLOW)
        self.screen.blit(coin_txt, (self.W - coin_txt.get_width() - 10, 10))

        # Score
        score_txt = self.font_sm.render(f"Score: {self._calc_score()}", True, WHITE)
        self.screen.blit(score_txt, (10, 10))

        # Distance meter
        dist_m   = int(self.distance)
        remain_m = max(0, self.FINISH_DISTANCE - dist_m)
        dist_txt = self.font_sm.render(f"{dist_m} m  |  {remain_m} m left", True, LINE_COLOR)
        self.screen.blit(dist_txt, (self.W//2 - dist_txt.get_width()//2, 10))

        # Progress bar (below banner)
        bar_w = self.W - 20
        pct   = min(self.distance / self.FINISH_DISTANCE, 1.0)
        pygame.draw.rect(self.screen, DARK_GRAY, (10, 44, bar_w, 6))
        pygame.draw.rect(self.screen, GREEN,     (10, 44, int(bar_w * pct), 6))

        # Active power-up (bottom-left)
        if self.active_powerup == "nitro":
            secs = self.powerup_remaining // 60
            pu_txt = self.font_sm.render(f"⚡ Nitro {secs}s", True, ORANGE)
            self.screen.blit(pu_txt, (10, self.H - 34))
        elif self.active_powerup == "shield":
            pu_txt = self.font_sm.render("🛡 Shield", True, CYAN)
            self.screen.blit(pu_txt, (10, self.H - 34))

        # Username
        name_txt = self.font_sm.render(self.username, True, GRAY)
        self.screen.blit(name_txt, (10, 54))

    # ── Main run loop ─────────────────────────────────────────────────────────

    def run(self) -> dict:
        """Run the game loop; return a result dict when session ends."""
        key_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False}

        while self.running:
            self.frame += 1

            # ── Events ────────────────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.player.lane > 0:
                            self.player.lane   -= 1
                            self.player.target_x = float(lane_center(self.player.lane))
                    if event.key == pygame.K_RIGHT:
                        if self.player.lane < NUM_LANES - 1:
                            self.player.lane   += 1
                            self.player.target_x = float(lane_center(self.player.lane))
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # ── Difficulty / speed scaling ────────────────────────────────────
            self._scale_difficulty()

            # ── Spawn timers ─────────────────────────────────────────────────
            self.traffic_timer   += 1
            self.coin_timer      += 1
            self.obstacle_timer  += 1
            self.powerup_timer   += 1
            self.lane_event_timer+= 1

            if self.traffic_timer   >= self.traffic_interval:
                self._spawn_traffic();    self.traffic_timer   = 0
            if self.coin_timer      >= 60:
                self._spawn_coin();       self.coin_timer      = 0
            if self.obstacle_timer  >= self.obstacle_interval:
                self._spawn_obstacle();   self.obstacle_timer  = 0
            if self.powerup_timer   >= 240:
                self._spawn_powerup();    self.powerup_timer   = 0
            if self.lane_event_timer>= 400:
                self._spawn_lane_event(); self.lane_event_timer= 0

            # ── Updates ───────────────────────────────────────────────────────
            self.road.update(self.scroll_speed)
            self.player.update()

            for car in self.traffic_group:
                car.update(self.scroll_speed)
            for coin in self.coin_group:
                coin.update(self.scroll_speed)
            for obs in self.obstacle_group:
                obs.update(self.scroll_speed)
            for pu in self.powerup_group:
                pu.update(self.scroll_speed)
            for ev in self.lane_event_group:
                ev.update(self.scroll_speed)

            # Distance increases with scroll
            self.distance += self.scroll_speed * 0.05

            # ── Collisions: coins ─────────────────────────────────────────────
            hit_coins = pygame.sprite.spritecollide(
                self.player, self.coin_group, True,
                pygame.sprite.collide_rect)
            for coin in hit_coins:
                self.coins_collected  += 1
                self.coin_value_total += coin.value

            # ── Collisions: power-ups ─────────────────────────────────────────
            hit_pus = pygame.sprite.spritecollide(
                self.player, self.powerup_group, True,
                pygame.sprite.collide_rect)
            for pu in hit_pus:
                self._activate_powerup(pu.kind)

            # ── Collisions: obstacles ─────────────────────────────────────────
            hit_obs = pygame.sprite.spritecollide(
                self.player, self.obstacle_group, False,
                pygame.sprite.collide_mask if hasattr(pygame.sprite, 'collide_mask')
                else pygame.sprite.collide_rect)
            for obs in hit_obs:
                if self.invincible_frames > 0:
                    continue
                if obs.kind == "oil":
                    # Oil: slides player to random adjacent lane for 60 frames
                    # (just force a random lane)
                    other = self._safe_lane(self.player.lane)
                    self.player.lane    = other
                    self.player.target_x= float(lane_center(other))
                    obs.kill()
                elif obs.kind == "bump":
                    # Bump: brief slowdown
                    self.scroll_speed = max(2, self.scroll_speed - 2)
                    obs.kill()
                else:  # pothole — end run or absorb with shield
                    if not self.player.absorb_hit():
                        self.running = False
                    else:
                        self.invincible_frames = 60
                    obs.kill()

            # ── Collisions: traffic cars ──────────────────────────────────────
            hit_traffic = pygame.sprite.spritecollide(
                self.player, self.traffic_group, False,
                pygame.sprite.collide_rect)
            for car in hit_traffic:
                if self.invincible_frames > 0:
                    continue
                if not self.player.absorb_hit():
                    self.running = False
                else:
                    self.invincible_frames = 90
                car.kill()

            # ── Lane events (nitro strip / slow zone) ─────────────────────────
            hit_evs = pygame.sprite.spritecollide(
                self.player, self.lane_event_group, False,
                pygame.sprite.collide_rect)
            for ev in hit_evs:
                if ev.kind == "nitro" and self.active_powerup != "nitro":
                    self._activate_powerup("nitro")
                elif ev.kind == "slow":
                    self.scroll_speed = max(2, self.scroll_speed - 1.5)
                ev.kill()

            # ── Power-up tick ──────────────────────────────────────────────────
            self._tick_powerup()

            # ── Invincibility countdown ───────────────────────────────────────
            if self.invincible_frames > 0:
                self.invincible_frames -= 1

            # ── Remove off-screen sprites ─────────────────────────────────────
            for car in list(self.traffic_group):
                if car.off_screen(self.H):
                    car.kill()
            for coin in list(self.coin_group):
                if coin.off_screen(self.H):
                    coin.kill()
            for obs in list(self.obstacle_group):
                if obs.off_screen(self.H):
                    obs.kill()
            for pu in list(self.powerup_group):
                if pu.off_screen(self.H) or pu.expired():
                    pu.kill()
            for ev in list(self.lane_event_group):
                if ev.off_screen(self.H):
                    ev.kill()

            # ── Finish line ───────────────────────────────────────────────────
            if self.distance >= self.FINISH_DISTANCE:
                self.running = False

            # ── Draw ──────────────────────────────────────────────────────────
            self.screen.fill(BLACK)
            self.road.draw(self.screen)

            self.lane_event_group.draw(self.screen)
            self.obstacle_group.draw(self.screen)
            self.coin_group.draw(self.screen)
            self.powerup_group.draw(self.screen)
            self.traffic_group.draw(self.screen)

            # Player (flash when invincible)
            if self.invincible_frames == 0 or (self.frame % 6 < 3):
                self.screen.blit(self.player.image, self.player.rect)

            self._draw_hud()

            pygame.display.flip()
            self.clock.tick(60)

        # ── Return run result ─────────────────────────────────────────────────
        return {
            "score":    self._calc_score(),
            "distance": self.distance,
            "coins":    self.coins_collected,
        }