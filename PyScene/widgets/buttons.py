import pygame
import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
from widgets.widget import Widget, WidgetImage
from tool.gradient import horizontal, vertical
from tool.point import Vector, Point
from widgets.text import Text

class Button(Widget):
    # text = PyScene.widgets.text.Text or string
    def __init__(self, parent, text, rect, callback, pydata=None, image='blue', group=None, style='simple'):
        Widget.__init__(self, parent, rect, 'Button', group)
        self.callback = callback
        self.pydata = pydata

        if isinstance(image, (str, tuple, list)):
            self._make_button(image, style)
        else:
            self._image = image
            self._image.scale(self._rect.size)

        if isinstance(text, Text):
            self.text = text
            self.text.set_position(self._rect.center)
        else:
            self.text = Text(None, text, *self._rect.center)

        if parent:
            parent.bind_event(pygame.MOUSEBUTTONUP, self._key + 'up__', self.event_mousebuttonup)
            parent.bind_blit(self._key + 'blit__', self.blit)

    def simple_button(self, color):
        dull, bright, dark, light = self.make_color(color)
        _, bdis, ddis, _ = self.make_color('gray')
        self._image = WidgetImage(
            vertical((dark, bright, bright, dark)),
            vertical((dark + light, bright + dull, bright + dull, dark + light)),
            vertical((bright, dark, dark, bright)),
            vertical((ddis, bdis, bdis, ddis)))

        self._image.scale(self._rect.size)

    def normal_mix(self, dark, bright, dimmer, fill):
        w, h = (Point(*self._rect.size) / 10).tup()
        top = pygame.transform.scale(horizontal((bright + dimmer, bright)), (self._rect.w + 1, h))
        left = pygame.transform.scale(vertical((bright + dimmer, bright)), (w, self._rect.h + 1))
        right = pygame.transform.scale(vertical((bright, dark)), (w, self._rect.h + 1))
        bottom = pygame.transform.scale(horizontal((bright, dark)), (self._rect.w + 1, h))
        surface = pygame.Surface(self._rect.size)
        surface.fill(tuple(map(int, fill.tup())))
        surface.blit(top,(0,0))
        surface.blit(left, (0,0))
        surface.blit(bottom, (0, self._rect.h - h))
        surface.blit(right, (self._rect.w - w, 0))

        return surface

    def normal_button(self, color):
        dimmer, bright, dark, light = self.make_color(color)
        dimmer_off, off, dark_off, _ = self.make_color('gray')
        self._image = WidgetImage(
            self.normal_mix(dark - light, bright - dimmer, dimmer, bright - dimmer),
            self.normal_mix(dark, bright, dimmer, bright),
            self.normal_mix(bright - dimmer, dark - light, light, bright - dimmer),
            self.normal_mix(dark_off, off, dimmer_off, off)
        )

    def make_color(self, color):
        if isinstance(color, str):
            pycolor = pygame.Color(color)
        elif isinstance(color, (tuple, list)):
            pycolor = pygame.Color(*color)
        elif isinstance(color, Vector):
            pycolor = pygame.Color(*color.tup())

        color = Vector(pycolor.r, pycolor.g, pycolor.b)
        dimmer = color * 0.25
        bright = color - dimmer
        dark = bright * 0.5
        light = dark * 0.25
        return dimmer, bright, dark, light

    def _make_button(self, color, style):
        if style == 'simple':
            self.simple_button(color)
        elif style == 'normal':
            self.normal_button(color)

    def blit(self, surface):
        if self.enable:
            if self._toggle:
                surface.blit(self._image.toggle, self._rect)
            elif self._hover:
                surface.blit(self._image.hover, self._rect)
            else:
                surface.blit(self._image.base, self._rect)
        else:
            surface.blit(self._image.disabled, self._rect)

        self.text.blit(surface)

    def event_mousebuttonup(self, event, key, pydata):
        self._toggle = False
        if self._hover and self.enable:
            if self.callback:
                self.callback(self, self.pydata)
