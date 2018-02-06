import pygame
import numpy as np
from ... import gradient
from .simple_button import simple_button
from .normal_button import normal_button
from .box_button import box_button

# TODO rounded button
# TODO slanted button

def create_button_image(color, style, rect, gradient_style=None, effects=None):
    if not gradient_style:
        gradient_style = gradient.hsl_by_value

    error_message = 'Error: Color in wrong format.'
    default_style = gradient.hsl_by_value
    default_color = (False, 2, 'dodgerblue', 15, 6, True)
    disabled_color = (False, 2, 'gray40', 15, 6, True)

    if gradient_style in [gradient.hsl_by_value, gradient.hsv_by_value, gradient.rgb_by_value]:
        if len(color) not in [5, 6]:
            print(error_message, color)
            if style == 'normal':
                return normal_button(default_style, default_color, disabled_color, rect)
            elif style == 'box':
                return box_button(default_style, default_color, disabled_color, rect)
            else:
                return simple_button(default_style, default_color, disabled_color)

    if style == 'simple':
        if isinstance(color, (str, np.ndarray, pygame.Color)):
            return simple_button(color, disabled_color, gradient_style)
        elif isinstance(color, (tuple, list)):
            if isinstance(color[0], (tuple, list)):
                return simple_button(gradient_style, *color)
            else:
                return simple_button(gradient_style, color, disabled_color)
        else:
            print(error_message, color)
            return simple_button(default_style, default_color, disabled_color)
    elif style == 'normal':
        if isinstance(color, (str, np.ndarray, pygame.Color)):
            return normal_button(color, disabled_color, gradient_style)
        elif isinstance(color, (tuple, list)):
            if isinstance(color[0], (tuple, list)):
                return normal_button(gradient_style, *color)
            else:
                return normal_button(gradient_style, color, disabled_color)
        else:
            print(error_message, color)
            return normal_button(default_style, default_color, disabled_color)
    else:
        print('Error: Style is not available.', style)
        return simple_button(default_style, default_color, disabled_color)
