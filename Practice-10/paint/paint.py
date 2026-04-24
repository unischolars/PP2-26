import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser")
    clock = pygame.time.Clock()

    # App State
    shapes = []  # List to store finished drawings
    current_shape = None
    drawing = False
    start_pos = (0, 0)
    
    radius = 15
    color = (0, 0, 255) # Default Blue
    mode = 'brush' # brush, rect, circle, eraser

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Color Selection
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)
                elif event.key == pygame.K_1: mode = 'brush'
                elif event.key == pygame.K_2: mode = 'rect'
                elif event.key == pygame.K_3: mode = 'circle'
                elif event.key == pygame.K_4: mode = 'eraser'
                elif event.key == pygame.K_SPACE: shapes = []

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if mode == 'brush' or mode == 'eraser':
                    current_shape = {"type": mode, "points": [start_pos], "color": color if mode != 'eraser' else (0,0,0), "width": radius}

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'brush' or mode == 'eraser':
                    current_shape["points"].append(event.pos)
                else:
                    # For Rect/Circle, we just track the current stretch
                    current_shape = {"type": mode, "start": start_pos, "end": event.pos, "color": color, "width": radius}

            if event.type == pygame.MOUSEBUTTONUP:
                if current_shape:
                    shapes.append(current_shape)
                current_shape = None
                drawing = False

            # Radius adjustment with scroll wheel
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: radius = min(100, radius + 2)
                if event.button == 5: radius = max(2, radius - 2)

        screen.fill((0, 0, 0))

        # Draw all saved shapes
        for s in shapes + ([current_shape] if current_shape else []):
            if s['type'] in ['brush', 'eraser']:
                if len(s['points']) > 1:
                    for i in range(len(s['points']) - 1):
                        draw_smooth_line(screen, s['points'][i], s['points'][i+1], s['width'], s['color'])
            elif s['type'] == 'rect':
                rect_coords = get_rect_points(s['start'], s['end'])
                pygame.draw.rect(screen, s['color'], rect_coords, 2)
            elif s['type'] == 'circle':
                dist = int(((s['start'][0] - s['end'][0])**2 + (s['start'][1] - s['end'][1])**2)**0.5)
                pygame.draw.circle(screen, s['color'], s['start'], dist, 2)

        pygame.display.flip()
        clock.tick(60)

def draw_smooth_line(screen, start, end, width, color):
    dx, dy = end[0] - start[0], end[1] - start[1]
    steps = max(abs(dx), abs(dy))
    for i in range(steps):
        p = i / steps
        x = int(start[0] + p * dx)
        y = int(start[1] + p * dy)
        pygame.draw.circle(screen, color, (x, y), width)

def get_rect_points(start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    return (x, y, w, h)

main()