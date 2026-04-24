import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser")
    clock = pygame.time.Clock()

    # stores all finished shapes
    shapes = []
    current_shape = None

    drawing = False
    start_pos = (0, 0)

    radius = 15
    color = (0, 0, 255)  # default color
    mode = 'brush'       # current tool

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # color selection
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)

                # tool selection
                elif event.key == pygame.K_1: mode = 'brush'
                elif event.key == pygame.K_2: mode = 'rect'
                elif event.key == pygame.K_3: mode = 'circle'
                elif event.key == pygame.K_4: mode = 'eraser'
                elif event.key == pygame.K_5: mode = 'square'
                elif event.key == pygame.K_6: mode = 'right_tri'
                elif event.key == pygame.K_7: mode = 'equiltarian_tri'
                elif event.key == pygame.K_8: mode = 'rhombulus'

                # clear screen
                elif event.key == pygame.K_SPACE:
                    shapes = []

            # mouse pressed → start drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

                # brush/eraser need list of points
                if mode in ['brush', 'eraser']:
                    current_shape = {
                        "type": mode,
                        "points": [start_pos],
                        "color": color if mode != 'eraser' else (0, 0, 0),
                        "width": radius
                    }
                else:
                    # other shapes defined by start/end
                    current_shape = {
                        "type": mode,
                        "start": start_pos,
                        "end": start_pos,
                        "color": color,
                        "width": radius
                    }

                # mouse wheel (resize brush)
                if event.button == 4:
                    radius = min(100, radius + 2)
                if event.button == 5:
                    radius = max(2, radius - 2)

            # mouse moving while drawing
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode in ['brush', 'eraser']:
                    current_shape["points"].append(event.pos)
                else:
                    # update shape size dynamically
                    current_shape["end"] = event.pos

            # mouse released → save shape
            if event.type == pygame.MOUSEBUTTONUP:
                if current_shape:
                    shapes.append(current_shape)
                current_shape = None
                drawing = False

        screen.fill((0, 0, 0))

        # draw everything (including current preview)
        for s in shapes + ([current_shape] if current_shape else []):

            # brush / eraser drawing
            if s['type'] in ['brush', 'eraser']:
                if len(s['points']) > 1:
                    for i in range(len(s['points']) - 1):
                        draw_smooth_line(screen, s['points'][i], s['points'][i+1], s['width'], s['color'])

            # rectangle
            elif s['type'] == 'rect':
                rect_coords = get_rect_points(s['start'], s['end'])
                pygame.draw.rect(screen, s['color'], rect_coords, 2)

            # square (force equal sides)
            elif s['type'] == 'square':
                sx, sy = s['start']
                ex, ey = s['end']

                side = min(abs(ex - sx), abs(ey - sy))

                # handle direction so square draws correctly
                x = sx if ex >= sx else sx - side
                y = sy if ey >= sy else sy - side

                pygame.draw.rect(screen, s['color'], (x, y, side, side), 2)

            # circle
            elif s['type'] == 'circle':
                dx = s['start'][0] - s['end'][0]
                dy = s['start'][1] - s['end'][1]
                dist = int((dx*dx + dy*dy) ** 0.5)

                pygame.draw.circle(screen, s['color'], s['start'], dist, 2)

            # right triangle (simple axis-aligned)
            elif s['type'] == 'right_tri':
                sx, sy = s['start']
                ex, ey = s['end']

                points = [
                    (sx, sy),
                    (ex, sy),
                    (sx, ey)
                ]

                pygame.draw.polygon(screen, s['color'], points, 2)

            # equilateral triangle (based on geometry)
            elif s['type'] == 'equiltarian_tri':
                sx, sy = s['start']
                ex, ey = s['end']

                side = abs(ex - sx)
                height = int((math.sqrt(3) / 2) * side)

                points = [
                    (sx, sy),
                    (sx + side, sy),
                    (sx + side // 2, sy - height)
                ]

                pygame.draw.polygon(screen, s['color'], points, 2)

            # rhombus (diamond shape)
            elif s['type'] == 'rhombulus':
                sx, sy = s['start']
                ex, ey = s['end']

                mid_x = (sx + ex) // 2
                mid_y = (sy + ey) // 2

                points = [
                    (mid_x, sy),
                    (ex, mid_y),
                    (mid_x, ey),
                    (sx, mid_y)
                ]

                pygame.draw.polygon(screen, s['color'], points, 2)

        pygame.display.flip()
        clock.tick(60)


# smoother brush drawing (fills gaps between points)
def draw_smooth_line(screen, start, end, width, color):
    dx, dy = end[0] - start[0], end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps):
        p = i / steps
        x = int(start[0] + p * dx)
        y = int(start[1] + p * dy)
        pygame.draw.circle(screen, color, (x, y), width)


# helper to normalize rectangle coordinates
def get_rect_points(start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    return (x, y, w, h)


main()