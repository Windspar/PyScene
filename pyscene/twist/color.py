import pygame
import numpy as np

def color(color):    
    if isinstance(color, pygame.Color):
        return color
    elif isinstance(color, str):
        return pygame.Color(color)
    elif isinstance(color, np.ndarray):
        return pygame.Color(*color.tolist())
    elif isinstance(color, (tuple, list)):
        return pygame.Color(*color)
    elif isinstance(color, pygame.Surface):
        return color.convert_alpha()
    else:
        print("Twist.color. Wrong format !", color)
        return pygame.Color('white')
