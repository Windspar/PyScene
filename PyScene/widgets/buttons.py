import pygame
import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
from .widget import Widget, WidgetImage
from PyScene.tool import gradient, twist
from PyScene.tool.point import Vector, Point
from .text import Text

def simple_button(color, disabled_color):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color)

    return WidgetImage(
        gradient.vertical(dim),
        gradient.vertical(bright),
        gradient.vertical(dark),
        gradient.vertical(dcolor))

def box_button(color, disabled_color, alpha, objrect):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.5, False, False)
    rect = pygame.Rect(0,0,*objrect.size)
    rect.inflate_ip(-6, -6)

    def overlay(fg, bg, rect, objrect, alpha):
        if isinstance(bg, Vector):
            surface = pygame.Surface(objrect.size)
            surface = surface.convert_alpha()
            surface.fill((*bg.tup_cast(), alpha))
        else:
            gsurface = gradient.vertical(bg, objrect.size[0], alpha)
            surface = pygame.transform.scale(gsurface, objrect.size)

        pygame.draw.rect(surface, fg.tup_cast(), rect, 1)
        return surface

    return WidgetImage(
        overlay(dim[0], bright[0], rect, objrect, alpha),
        overlay(bright[0], bright[0], rect, objrect, alpha),
        overlay(dark[0], bright[0], rect, objrect, alpha),
        overlay(dcolor[0], dcolor, rect, objrect, alpha))

def normal_button(color, disabled_color, rect):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.5, False, False)
    brightr, dimr, darkr, dcolorr = twist.gkey(color, disabled_color, 0.5, True, False)

    def overlay(fg, bg, rect):
        back = gradient.horizontal(bg, rect.w)
        front = gradient.horizontal(fg, rect.w - 6)
        back = pygame.transform.scale(back, rect.size)
        w, h = rect.size
        rect = pygame.Rect(3,3,w - 6, h - 6)
        front = pygame.transform.scale(front, rect.size)
        back.blit(front, rect)
        rect.inflate_ip(2,2)
        pygame.draw.rect(back, (0,0,0), rect, 1)
        return back

    return WidgetImage(
        overlay(dim, dimr, rect),
        overlay(bright, dimr, rect),
        overlay(dark, dimr, rect),
        overlay(dcolor, dcolorr, rect))

class Button(Widget):
    # text = PyScene.widgets.text.Text or string
    def __init__(self, parent, text, rect, callback, pydata=None, image='dodgerblue', group=None, style='simple', allow_bindings=True):
        Widget.__init__(self, parent, rect, 'Button', group, allow_bindings)
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
            self.text = Text(parent, text, *self._rect.center, allow_bindings=False)

        if allow_bindings:
            parent.bind_event(pygame.MOUSEBUTTONUP, self._key + 'up__', self.event_mousebuttonup)
            parent.bind_blit(self._key + 'blit__', self.blit)

    def _make_button(self, color, style):
        if style == 'simple':
            if isinstance(color, (str, Vector)):
                self._image = simple_button(color, 'gray40')
            elif len(color) == 1:
                self._image = simple_button(color[0], 'gray40')
            elif len(color) == 2:
                self._image = simple_button(color[0], color[1])
            else:
                print('Error: color in wrong format', color)
                self._image = simple_button('dodgerblue', 'gray40')
        elif style == 'normal':
            if isinstance(color, (str, Vector)):
                self._image = normal_button(color, 'gray40', self._rect)
            elif len(color) == 1:
                self._image = normal_button(color[0], 'gray40', self._rect)
            elif len(color) == 2:
                self._image = normal_button(color[0], color[1], self._rect)
            else:
                print('Error: color in wrong format', color)
                self._image = normal_button('dodgerblue', 'gray40', self._rect)
        elif style == 'box':
            if isinstance(color, (str, Vector)):
                self._image = box_button(color, 'gray40', 70, self._rect)
            elif len(color) == 1:
                self._image = box_button(color[0], 'gray40', 70, self._rect)
            elif len(color) == 2:
                self._image = box_button(color[0], color[1], 70, self._rect)
            elif len(color) == 3:
                self._image = box_button(color[0], color[1], color[2], self._rect)
            else:
                print('Error: color in wrong format', color)
                self._image = box_button('dodgerblue', 'gray40', 70, self._rect)

        self._image.scale(self._rect.size)

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
        if event.button == 1:
            self._toggle = False
            if self._hover and self.enable:
                if self.callback:
                    self.callback(self, self.pydata)

class ToggleButton(Button):
    def __init__(self, parent, text, rect, callback, pydata=None, image='blue', group=None, style='simple', allow_bindings=True):
        Button.__init__(self, parent, text, rect, callback, pydata, image, group, style, allow_bindings)

        if self._group is None:
            self.allow_toggle = True

        if allow_bindings:
            parent.unbind_event(pygame.MOUSEBUTTONUP, self._key + 'up__')

    def event_mousebuttondown(self, event, key, pydata):
        Widget.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1:
            if self.callback and self._hover:
                self.callback(self, self.pydata)
