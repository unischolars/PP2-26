

import sys
import pygame
from datetime import datetime

from tools import (
    PencilTool, EraserTool, ShapeTool,
    FillTool, ColorPickerTool, TextTool,
)

# ─────────────────────── constants ──────────────────────────────────────────

WIN_W, WIN_H   = 1100, 700
TOOLBAR_W      = 160
CANVAS_X       = TOOLBAR_W
CANVAS_Y       = 0
CANVAS_W       = WIN_W - TOOLBAR_W
CANVAS_H       = WIN_H

BG_DARK   = (28,  30,  36)
BG_MID    = (38,  41,  50)
BG_PANEL  = (45,  48,  58)
ACCENT    = (99, 179, 237)        # sky-blue
ACCENT2   = (246, 173,  85)       # amber
TEXT_CLR  = (220, 224, 235)
DIVIDER   = (60,  64,  78)
WHITE     = (255, 255, 255)

SIZE_MAP  = {1: 2, 2: 5, 3: 10}  # key → px

PALETTE = [
    (0,   0,   0),   (255, 255, 255), (192, 192, 192), (128, 128, 128),
    (255,   0,   0), (200,   0,   0), (255, 128,   0), (255, 200,   0),
    (255, 255,   0), (128, 255,   0), (0,  200,   0),  (0,  255, 128),
    (0,  255, 255),  (0,  128, 255),  (0,    0, 255),  (128,   0, 255),
    (255,   0, 255), (255,   0, 128), (180,  90,  40),  (90,  40,  10),
]

# ─────────────────────── toolbar definition ─────────────────────────────────

TOOL_DEFS = [
    # (label, tool-object or factory, keyboard shortcut hint)
    ("Pencil",     "pencil",             "P"),
    ("Line",       "line",               "L"),
    ("Rectangle",  "rectangle",          "R"),
    ("Circle",     "circle",             "C"),
    ("Square",     "square",             "Q"),
    ("Rt.Tri",     "right_triangle",     "T"),
    ("Eq.Tri",     "equilateral_triangle","E"),
    ("Rhombus",    "rhombus",            "H"),
    ("Fill",       "fill",               "F"),
    ("Eraser",     "eraser",             "X"),
    ("Eyedrop",    "color_picker",       "I"),
    ("Text",       "text",               "A"),
]


def build_tools():
    return {
        "pencil":               PencilTool(),
        "line":                 ShapeTool("line"),
        "rectangle":            ShapeTool("rectangle"),
        "circle":               ShapeTool("circle"),
        "square":               ShapeTool("square"),
        "right_triangle":       ShapeTool("right_triangle"),
        "equilateral_triangle": ShapeTool("equilateral_triangle"),
        "rhombus":              ShapeTool("rhombus"),
        "fill":                 FillTool(),
        "eraser":               EraserTool(),
        "color_picker":         ColorPickerTool(),
        "text":                 TextTool(),
    }


# ─────────────────────── UI helpers ─────────────────────────────────────────

def draw_toolbar(surface, font_sm, font_xs,
                 active_tool, active_size, active_color,
                 tool_rects, size_rects, palette_rects):
    """Render the left toolbar panel."""
    pygame.draw.rect(surface, BG_PANEL, (0, 0, TOOLBAR_W, WIN_H))
    pygame.draw.line(surface, DIVIDER, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, WIN_H), 2)

    # ── title ────────────────────────────────────────────────────────────────
    title = font_sm.render("🎨 Paint", True, ACCENT)
    surface.blit(title, (12, 10))

    y = 42
    # ── tool buttons ─────────────────────────────────────────────────────────
    lbl = font_xs.render("TOOLS", True, (130, 135, 155))
    surface.blit(lbl, (12, y));  y += 16

    for idx, (label, key, _shortcut) in enumerate(TOOL_DEFS):
        rect = pygame.Rect(8, y, TOOLBAR_W - 16, 26)
        tool_rects[key] = rect
        is_active = (active_tool == key)
        color = ACCENT if is_active else BG_MID
        pygame.draw.rect(surface, color, rect, border_radius=5)
        if is_active:
            pygame.draw.rect(surface, ACCENT, rect, 1, border_radius=5)
        txt_clr = BG_DARK if is_active else TEXT_CLR
        t = font_xs.render(label, True, txt_clr)
        surface.blit(t, (rect.x + 8, rect.y + 5))
        y += 30

    y += 6
    # ── brush size ────────────────────────────────────────────────────────────
    lbl = font_xs.render("BRUSH SIZE", True, (130, 135, 155))
    surface.blit(lbl, (12, y));  y += 16

    size_labels = {1: "S (1)", 2: "M (2)", 3: "L (3)"}
    for sz in (1, 2, 3):
        rect = pygame.Rect(8, y, TOOLBAR_W - 16, 24)
        size_rects[sz] = rect
        is_active = (active_size == sz)
        color = ACCENT2 if is_active else BG_MID
        pygame.draw.rect(surface, color, rect, border_radius=5)
        txt_clr = BG_DARK if is_active else TEXT_CLR
        t = font_xs.render(size_labels[sz], True, txt_clr)
        surface.blit(t, (rect.x + 8, rect.y + 4))
        y += 28

    y += 6
    # ── colour palette ────────────────────────────────────────────────────────
    lbl = font_xs.render("PALETTE", True, (130, 135, 155))
    surface.blit(lbl, (12, y));  y += 16

    cols = 5
    sw   = (TOOLBAR_W - 16) // cols
    for i, clr in enumerate(PALETTE):
        cx = 8 + (i % cols) * sw
        cy = y + (i // cols) * sw
        rect = pygame.Rect(cx, cy, sw - 2, sw - 2)
        palette_rects[i] = (rect, clr)
        pygame.draw.rect(surface, clr, rect, border_radius=3)
        if clr == active_color:
            pygame.draw.rect(surface, WHITE, rect, 2, border_radius=3)

    rows = (len(PALETTE) + cols - 1) // cols
    y += rows * sw + 6

    # ── active colour swatch ──────────────────────────────────────────────────
    lbl = font_xs.render("ACTIVE COLOR", True, (130, 135, 155))
    surface.blit(lbl, (12, y));  y += 16
    swatch_rect = pygame.Rect(8, y, TOOLBAR_W - 16, 28)
    pygame.draw.rect(surface, active_color, swatch_rect, border_radius=5)
    pygame.draw.rect(surface, WHITE, swatch_rect, 1, border_radius=5)


def draw_status_bar(surface, font_xs, active_tool, active_size, mouse_pos):
    bar_rect = pygame.Rect(CANVAS_X, WIN_H - 22, CANVAS_W, 22)
    pygame.draw.rect(surface, BG_PANEL, bar_rect)
    pygame.draw.line(surface, DIVIDER,
                     (CANVAS_X, WIN_H - 22), (WIN_W, WIN_H - 22), 1)
    cx = mouse_pos[0] - CANVAS_X
    cy = mouse_pos[1]
    info = (f"  Tool: {active_tool.replace('_',' ').title()}  |  "
            f"Size: {SIZE_MAP[active_size]}px  |  "
            f"Cursor: ({max(cx,0)}, {cy})  |  Ctrl+S to save")
    t = font_xs.render(info, True, (130, 135, 155))
    surface.blit(t, (CANVAS_X + 6, WIN_H - 18))


# ─────────────────────── main ────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.display.set_caption("Paint – TSIS 2")
    screen  = pygame.display.set_mode((WIN_W, WIN_H))
    clock   = pygame.time.Clock()

    font_sm = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_xs = pygame.font.SysFont("Segoe UI", 13)

    # Canvas surface (white background)
    canvas = pygame.Surface((CANVAS_W, CANVAS_H - 22))
    canvas.fill(WHITE)

    tools        = build_tools()
    active_tool  = "pencil"
    active_size  = 1          # 1=small, 2=med, 3=large
    active_color = (0, 0, 0)

    tool_rects    = {}
    size_rects    = {}
    palette_rects = {}

    def on_canvas(pos):
        x, y = pos
        return CANVAS_X <= x < WIN_W and 0 <= y < WIN_H - 22

    def canvas_pos(pos):
        return (pos[0] - CANVAS_X, pos[1])

    def set_color(c):
        nonlocal active_color
        active_color = c

    # ── keyboard shortcuts for tools ─────────────────────────────────────────
    key_tool_map = {
        pygame.K_p: "pencil",
        pygame.K_l: "line",
        pygame.K_r: "rectangle",
        pygame.K_c: "circle",
        pygame.K_q: "square",
        pygame.K_t: "right_triangle",
        pygame.K_e: "equilateral_triangle",
        pygame.K_h: "rhombus",
        pygame.K_f: "fill",
        pygame.K_x: "eraser",
        pygame.K_i: "color_picker",
        pygame.K_a: "text",
    }

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Translate events for the active tool
        state = {
            "color":     active_color,
            "size":      SIZE_MAP[active_size],
            "on_canvas": on_canvas,
            "set_color": set_color,
        }

        # Build translated events (shift coords into canvas space)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── global keyboard ───────────────────────────────────────────────
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                # Ctrl+S — save
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{ts}.png"
                    pygame.image.save(canvas, filename)
                    pygame.display.set_caption(f"Paint – saved {filename}")
                    continue

                # Brush size 1/2/3
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    active_size = event.key - pygame.K_0
                    continue

                # Tool shortcuts (but not when text tool is typing)
                if active_tool != "text" or not tools["text"].active:
                    if event.key in key_tool_map:
                        active_tool = key_tool_map[event.key]
                        continue

            # ── toolbar clicks ────────────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Tool buttons
                for key, rect in tool_rects.items():
                    if rect.collidepoint(event.pos):
                        active_tool = key
                        break
                else:
                    # Size buttons
                    for sz, rect in size_rects.items():
                        if rect.collidepoint(event.pos):
                            active_size = sz
                            break
                    else:
                        # Palette
                        for _i, (rect, clr) in palette_rects.items():
                            if rect.collidepoint(event.pos):
                                active_color = clr
                                break

            # ── forward canvas events to active tool ──────────────────────────
            # Translate mouse coords to canvas-local for tools that need it,
            # but we keep global coords and offset the blit; tool on_canvas
            # already checks CANVAS_X boundary.

            if on_canvas(mouse_pos) or event.type in (pygame.MOUSEBUTTONUP, pygame.KEYDOWN):
                # Translate event position into canvas surface coords
                translated = translate_event(event, CANVAS_X, 0)
                tools[active_tool].handle_event(translated, canvas, state)

        # ── draw ─────────────────────────────────────────────────────────────
        screen.fill(BG_DARK)

        # Canvas
        screen.blit(canvas, (CANVAS_X, 0))

        # Tool preview overlay (drawn on a copy so canvas stays clean)
        preview_surf = canvas.copy()
        tools[active_tool].draw_preview(preview_surf, state)
        screen.blit(preview_surf, (CANVAS_X, 0))

        # Toolbar
        draw_toolbar(screen, font_sm, font_xs,
                     active_tool, active_size, active_color,
                     tool_rects, size_rects, palette_rects)

        # Status bar
        draw_status_bar(screen, font_xs, active_tool, active_size, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def translate_event(event, dx, dy):
    """Reconstruct a pygame.event.Event with mouse positions shifted by (-dx, -dy).
    pygame events cannot be copied with copy.copy, so we build a new one via
    pygame.event.Event(type, dict) using the event's __dict__ attributes.
    """
    attrs = event.__dict__.copy()          # plain dict — always picklable
    if "pos" in attrs:
        x, y = attrs["pos"]
        attrs["pos"] = (x - dx, y - dy)
    return pygame.event.Event(event.type, attrs)


if __name__ == "__main__":
    main()