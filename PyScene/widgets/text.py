import pygame
import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
from widgets.widget import Widget
from tool.point import Point
from tool.gradient import apply_surface

# Text are static. Can be transform in Text Click.
# Text can have a hilight color.
# Text can have colorful text

class TextInfo:
    def __init__(self, color):
        self.image = None
        self.r_image = None
        self.set_color(color)

    def set_color(self, color):
        if isinstance(color, str):
            self.color = pygame.Color(color)
        elif isinstance(color, (tuple, list)):
            self.color = pygame.Color(*color)
        elif isinstance(color, pygame.Surface):
            self.color = color.convert_alpha()

# color takes pygame.Color args or pygame.Surface
class Text(Widget):
    def __init__(self, parent, text, x, y, font=None, color='white', group=None, callback=None, pydata=None, allow_bindings=True):
        Widget.__init__(self, parent, None, 'Text', group, allow_bindings)
        if font is None:
            self._font = pygame.font.Font(None, 24)
        else:
            self._font = font

        self._text = text
        self._anchor = 'center'
        self._position = Point(x, y)
        self._info = TextInfo(color)
        self._hover_info = None
        self._toggle_info = None
        self._angle = None
        self._r_rect = None
        self._render(self._info)
        self.callback = callback
        self.pydata = pydata

        if allow_bindings:
            parent.bind_blit(self._key, self.blit)

    def set_callback(self, callback, pydata=None):
        self.callback = callback
        self.pydata = pydata

    def event_mousebuttondown(self, event, key, pydata):
        Widget.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1:
            if self.callback and self._hover:
                self.callback(self, self.pydata)

    def set_hilight(self, color):
        if self._hover_info is None:
            self._hover_info = TextInfo(color)
        else:
            self._hover_info.set_color(color)
        self._render(self._hover_info)

    def set_toggle(self, color):
        if self._toggle_info is None:
            self._toggle_info = TextInfo(color)
        else:
            self._toggle_info.set_color(color)
        self._render(self._toggle_info)

    def _render(self, info):
        if isinstance(info.color, pygame.Surface):
            surface = self._font.render(self._text, 1, (255,255,255))
        else:
            surface = self._font.render(self._text, 1, info.color)
        self._rect = surface.get_rect()
        self._do_anchor()

        if isinstance(info.color, pygame.Surface):
            info.image = apply_surface(surface, info.color)
            if self._angle is not None:
                info.r_image = pygame.transform.rotate(info.image, self._angle)
                self._r_rect = info.r_image.get_rect()
                self._r_rect.center = self._rect.center
        else:
            info.image = surface
            if self._angle is not None:
                info.r_image = pygame.transform.rotate(info.image, self._angle)
                self._r_rect = info.r_image.get_rect()
                self._r_rect.center = self._rect.center

    def blit(self, surface):
        if self._angle is None:
            if self._hover_info:
                if self._group and self._toggle:
                    surface.blit(self._toggle_info.image, self._rect)
                elif self._hover:
                    surface.blit(self._hover_info.image, self._rect)
                else:
                    surface.blit(self._info.image, self._rect)
            else:
                surface.blit(self._info.image, self._rect)
        else:
            if self._hover_info:
                if self._group and self._toggle:
                    surface.blit(self._toggle_info.r_image, self._r_rect)
                elif self._hover:
                    surface.blit(self._hover_info.r_image, self._r_rect)
                else:
                    surface.blit(self._info.r_image, self._r_rect)
            else:
                surface.blit(self._info.r_image, self._r_rect)

    def _do_render(self):
        self._render(self._info)
        if self._hover_info:
            self._render(self._hover_info)
        if self._toggle_info:
            self._render(self._toggle_info)

    def set_font(self, font):
        self._font = font
        self._do_render()

    def set_text(self, text):
        self._text = text
        self._do_render()

    def set_color(self, color):
        self._info.set_color(color)
        self._render(self._info)

    # handles Point, tuple, list, (x, y)
    def set_position(self, point, y=None):
        if y is None:
            if isinstance(point, (tuple, list)):
                self._position = Point(*point)
            elif isinstance(point, Point):
                self._position = point
        self.position = Point(point, y)
        self._do_anchor()

    def set_angle(self, angle):
        self._angle = angle
        self._do_render()

    def set_anchor(self, pystr):
        self._anchor = pystr
        self._do_anchor()

    def _do_anchor(self):
        if self._anchor == 'center':
            self._rect.center = self._position.tup()
        elif self_anchor == 'left':
            self._rect.left = self._position.x
            self._rect.centery = self._position.y

    def __repr__(self):
        return "Text({0})".format(self._text)
