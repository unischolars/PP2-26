import datetime
import math


def get_current_time():
    now = datetime.datetime.now()
    return now.minute, now.second


def get_hand_angle(value, max_value):
    return (value / max_value) * 360


def pygame_rotate(image, angle):
    import pygame
    return pygame.transform.rotate(image, angle)


def rotate_point(point, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    x, y = point
    new_x = x * cos_a + y * sin_a
    new_y = -x * sin_a + y * cos_a
    return new_x, new_y