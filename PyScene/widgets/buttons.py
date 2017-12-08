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

        if isinstance(image, (str, tuple, list, Vector)):
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
        _, gray_bright, gray_dark, _ = self.make_color('gray')
        self._image = WidgetImage(
            vertical((dark, bright, bright, dark)),
            vertical((dark + light, bright + dull, bright + dull, dark + light)),
            vertical((bright, dark, dark, bright)),
            vertical((gray_dark, gray_bright, gray_bright, gray_dark)))

        self._image.scale(self._rect.size)

    def box_button(self, color):
        bright, dark, lighten = self.make_color(color)[1:]
        gray_bright = self.make_color('gray60')[1]
        rect = pygame.Rect(0,0,*self._rect.size)
        rect.inflate_ip(-6, -6)

        def overlay(fg, rect):
            surface = pygame.Surface(self._rect.size)
            surface = surface.convert_alpha()
            surface.fill((*fg.tup(), 80))
            pygame.draw.rect(surface, fg.tup(), rect, 1)
            return surface

        self._image = WidgetImage(
            overlay(bright, rect),
            overlay(bright + lighten, rect),
            overlay(dark, rect),
            overlay(gray_bright, rect))

    def normal_button(self, color):
        dimmer, bright, dark, lighten = self.make_color(color)
        gray_bright, gray_dark = self.make_color('gray60')[1:3]

        def overlay(bg, fg, back):
            front = horizontal((fg, bg), self._rect.w - 6)
            back = pygame.transform.scale(back, self._rect.size)
            w, h = self._rect.size
            rect = pygame.Rect(3,3,w - 6, h - 6)
            front = pygame.transform.scale(front, rect.size)
            back.blit(front, rect)
            rect.inflate_ip(2,2)
            pygame.draw.rect(back, (0,0,0), rect, 1)
            return back

        back = horizontal((dark, bright), self._rect.w)
        gray_back = horizontal((gray_dark, gray_bright), self._rect.w)
        self._image = WidgetImage(
            overlay(dark, bright, back),
            overlay(dark + lighten, bright + dimmer, back),
            overlay(bright, dark, back),
            overlay(gray_dark, gray_bright, gray_back))

    def make_color(self, color):
        color = Vector(color).cast()
        dimmer = (color * 0.20).cast()
        bright = color - dimmer
        dark = (bright * 0.5).cast()
        lighten = (dark * 0.20).cast()
        return dimmer, bright, dark, lighten

    def _make_button(self, color, style):
        if style == 'simple':
            self.simple_button(color)
        elif style == 'normal':
            self.normal_button(color)
        elif style == 'box':
            self.box_button(color)

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
