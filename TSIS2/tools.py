"""
tools.py — Drawing tool implementations for the Paint application (TSIS 2).
Each tool class exposes handle_event(event, canvas, state) and draw_preview(surface, state).
"""

import pygame
from collections import deque


# ─────────────────────────────── helpers ────────────────────────────────────

def draw_shape(surface, tool_name, color, size, start, end):
    """Unified shape renderer used by both preview and final commit."""
    x1, y1 = start
    x2, y2 = end
    left   = min(x1, x2)
    top    = min(y1, y2)
    width  = abs(x2 - x1)
    height = abs(y2 - y1)

    if tool_name == "rectangle":
        pygame.draw.rect(surface, color, (left, top, width, height), size)

    elif tool_name == "circle":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        rx = max(1, width // 2)
        ry = max(1, height // 2)
        rect = pygame.Rect(cx - rx, cy - ry, rx * 2, ry * 2)
        pygame.draw.ellipse(surface, color, rect, size)

    elif tool_name == "square":
        side = min(width, height)
        pygame.draw.rect(surface, color, (left, top, side, side), size)

    elif tool_name == "right_triangle":
        pts = [(x1, y2), (x1, y1), (x2, y2)]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool_name == "equilateral_triangle":
        import math
        base   = abs(x2 - x1)
        height_eq = int(base * math.sqrt(3) / 2)
        pts = [
            (left, top + height_eq),
            (left + base, top + height_eq),
            (left + base // 2, top),
        ]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool_name == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        pts = [(cx, top), (x2, cy), (cx, top + height), (left, cy)]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool_name == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif tool_name == "eraser":
        # Eraser draws a white filled rect centred on the cursor
        r = size * 4
        pygame.draw.rect(surface, (255, 255, 255), (x2 - r, y2 - r, r * 2, r * 2))


# ─────────────────────────────── pencil ─────────────────────────────────────

class PencilTool:
    name = "pencil"

    def __init__(self):
        self.last_pos = None

    def handle_event(self, event, canvas, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                self.last_pos = event.pos
                pygame.draw.circle(canvas, state["color"], event.pos, state["size"] // 2)

        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if state["on_canvas"](event.pos) and self.last_pos:
                pygame.draw.line(canvas, state["color"],
                                 self.last_pos, event.pos, state["size"])
                self.last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            self.last_pos = None

    def draw_preview(self, surface, state):
        pass  # no preview needed for pencil


# ──────────────────────────────── eraser ────────────────────────────────────

class EraserTool:
    name = "eraser"

    def __init__(self):
        self.last_pos = None

    def handle_event(self, event, canvas, state):
        r = state["size"] * 4

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                self.last_pos = event.pos
                pygame.draw.rect(canvas, (255, 255, 255),
                                 (event.pos[0] - r, event.pos[1] - r, r * 2, r * 2))

        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if state["on_canvas"](event.pos):
                pygame.draw.rect(canvas, (255, 255, 255),
                                 (event.pos[0] - r, event.pos[1] - r, r * 2, r * 2))
                self.last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            self.last_pos = None

    def draw_preview(self, surface, state):
        pos = pygame.mouse.get_pos()
        if state["on_canvas"](pos):
            r = state["size"] * 4
            pygame.draw.rect(surface, (200, 200, 200),
                             (pos[0] - r, pos[1] - r, r * 2, r * 2), 1)


# ───────────────────────── generic shape tool ────────────────────────────────

class ShapeTool:
    """Handles rectangle, circle, square, right_triangle, equilateral_triangle, rhombus, line."""

    def __init__(self, shape_name):
        self.name = shape_name
        self.start = None
        self.dragging = False

    def handle_event(self, event, canvas, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                self.start = event.pos
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging and self.start:
                if state["on_canvas"](event.pos):
                    draw_shape(canvas, self.name,
                               state["color"], state["size"],
                               self.start, event.pos)
            self.start = None
            self.dragging = False

    def draw_preview(self, surface, state):
        if self.dragging and self.start:
            pos = pygame.mouse.get_pos()
            # Semi-transparent overlay
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            r, g, b = state["color"]
            draw_shape(overlay, self.name,
                       (r, g, b, 160), state["size"],
                       self.start, pos)
            surface.blit(overlay, (0, 0))


# ──────────────────────────── flood fill ─────────────────────────────────────

class FillTool:
    name = "fill"

    def handle_event(self, event, canvas, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                flood_fill(canvas, event.pos, state["color"])

    def draw_preview(self, surface, state):
        pass


def flood_fill(surface, start_pos, fill_color):
    """BFS flood fill directly on a pygame surface."""
    sw, sh = surface.get_size()
    sx, sy = int(start_pos[0]), int(start_pos[1])

    if not (0 <= sx < sw and 0 <= sy < sh):
        return

    target_color = surface.get_at((sx, sy))[:3]
    fill_rgb      = fill_color[:3] if len(fill_color) > 3 else fill_color

    if target_color == fill_rgb:
        return

    visited = set()
    queue   = deque([(sx, sy)])
    visited.add((sx, sy))

    surface.lock()
    try:
        while queue:
            x, y = queue.popleft()
            surface.set_at((x, y), fill_rgb)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if (0 <= nx < sw and 0 <= ny < sh
                        and (nx, ny) not in visited
                        and surface.get_at((nx, ny))[:3] == target_color):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    finally:
        surface.unlock()


# ─────────────────────────── color picker ────────────────────────────────────

class ColorPickerTool:
    name = "color_picker"

    def handle_event(self, event, canvas, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                picked = canvas.get_at(event.pos)[:3]
                state["set_color"](picked)

    def draw_preview(self, surface, state):
        pass


# ──────────────────────────── text tool ─────────────────────────────────────

class TextTool:
    name = "text"

    def __init__(self):
        self.active   = False
        self.position = (0, 0)
        self.buffer   = ""
        self.font     = None

    def _get_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("Arial", 24)
        return self.font

    def handle_event(self, event, canvas, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["on_canvas"](event.pos):
                self.active   = True
                self.position = event.pos
                self.buffer   = ""

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # Commit text to canvas
                font    = self._get_font()
                rendered = font.render(self.buffer, True, state["color"])
                canvas.blit(rendered, self.position)
                self.active = False
                self.buffer = ""

            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.buffer = ""

            elif event.key == pygame.K_BACKSPACE:
                self.buffer = self.buffer[:-1]

            else:
                if event.unicode and event.unicode.isprintable():
                    self.buffer += event.unicode

    def draw_preview(self, surface, state):
        if not self.active:
            return
        font     = self._get_font()
        text_surf = font.render(self.buffer + "|", True, state["color"])
        # Light background behind cursor area
        bg = pygame.Surface(
            (text_surf.get_width() + 4, text_surf.get_height() + 4),
            pygame.SRCALPHA
        )
        bg.fill((255, 255, 255, 180))
        surface.blit(bg,        (self.position[0] - 2, self.position[1] - 2))
        surface.blit(text_surf,  self.position)