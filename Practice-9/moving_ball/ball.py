class Ball:
    def __init__(self, x: int, y: int, radius: int = 25,
                 color: tuple = (220, 40, 40)):
        self.x      = x
        self.y      = y
        self.radius = radius
        self.color  = color

    def move(self, dx: int, dy: int,
             screen_width: int, screen_height: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        if self._within_bounds(new_x, new_y, screen_width, screen_height):
            self.x = new_x
            self.y = new_y

    def _within_bounds(self, x: int, y: int,
                       width: int, height: int) -> bool:
        return (self.radius <= x <= width  - self.radius and
                self.radius <= y <= height - self.radius)

    def draw(self, surface) -> None:
        import pygame
        outline_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.circle(surface, outline_color, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(surface, self.color,    (self.x, self.y), self.radius)