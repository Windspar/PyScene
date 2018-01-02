import pygame
from pyscene.objects import PySceneObject, PySceneImage
from pyscene.text import Text
from pyscene.tool import gradient, twist
import numpy as np

def simple_button(color, disabled_color, grad):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color)

    return PySceneImage(
        grad[0](grad[1], dim, inverse=grad[2]),
        grad[0](grad[1], bright, inverse=grad[2]),
        grad[0](grad[1], dark, inverse=grad[2]),
        grad[0](grad[1], dcolor, inverse=grad[2]))

def box_button(color, disabled_color, alpha, objrect, grad):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.5, False, False)
    rect = pygame.Rect(0,0,*objrect.size)
    rect.inflate_ip(-6, -6)

    def overlay(fg, bg, rect, objrect, alpha, grad):
        if isinstance(bg, np.ndarray):
            surface = pygame.Surface(objrect.size)
            surface = surface.convert_alpha()
            bg[3] = alpha
            bg = bg.astype(int).tolist()
            surface.fill(bg)
        else:
            gsurface = grad[0](grad[1], bg, objrect.size[0], grad[2])
            surface = pygame.transform.scale(gsurface, objrect.size)

        pygame.draw.rect(surface, fg.astype(int).tolist(), rect, 1)
        return surface

    return PySceneImage(
        overlay(dim[0], bright[0], rect, objrect, alpha, grad),
        overlay(bright[1], bright[0], rect, objrect, alpha, grad),
        overlay(dark[0], bright[0], rect, objrect, alpha, grad),
        overlay(dcolor[0], dcolor, rect, objrect, alpha, grad))

def normal_button(color, disabled_color, rect, grad):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.5, False, False)
    brightr, dimr, darkr, dcolorr = twist.gkey(color, disabled_color, 0.5, True, False)

    def overlay(fg, bg, rect, grad):
        back = grad[0](grad[1], bg, rect.w, grad[2])
        front = grad[0](grad[1], fg, rect.w - 6, grad[2])
        back = pygame.transform.scale(back, rect.size)
        w, h = rect.size
        rect = pygame.Rect(3,3,w - 6, h - 6)
        front = pygame.transform.scale(front, rect.size)
        back.blit(front, rect)
        rect.inflate_ip(2,2)
        pygame.draw.rect(back, (0,0,0), rect, 1)
        return back

    return PySceneImage(
        overlay(dim, dimr, rect, grad),
        overlay(bright, dimr, rect, grad),
        overlay(dark, dimr, rect, grad),
        overlay(dcolor, dcolorr, rect, grad))

class Button(PySceneObject):
    def __init__(self, parent, text, rect, callback, pydata=None, image='dodgerblue', group=None, style='simple', allow_bindings=True):
        PySceneObject.__init__(self, parent, rect, 'Button', group, allow_bindings)
        self.callback = callback
        self.pydata = pydata

        if isinstance(image, (str, tuple, list, np.ndarray)):
            self._make_button(image, style)
        else:
            self._image = image
            self._image.scale(self._rect.size)

        drect = self._draw_rect(self._rect, self._parent.get_position())
        if isinstance(text, Text):
            self.text = text
            self.text.set_position(drect.center)
            self.text.anchor('center', 'center')
        else:
            self.text = Text(parent, text, drect.center, allow_bindings=False)
            self.text.anchor('center', 'center')

        if allow_bindings:
            parent.bind_event(pygame.MOUSEBUTTONUP, self._key + 'up__', self.event_mousebuttonup)
            parent.bind_blit(self._key + 'blit__', self.blit)

    def _make_button(self, color, style):
        if color[0] in ['v-rgb', 'h-rgb', 'v-hsl', 'v-hsli', 'h-hsl', 'h-hsli']:
            grad = (
                [gradient.hsl, gradient.rgb][color[0][2:5] == 'rgb'],
                color[0][0] == 'h',
                color[0][-1] == 'i' )
        else:
            grad = (gradient.rgb, False, False)

        if style == 'simple':
            if isinstance(color, (str, np.ndarray)):
                self._image = simple_button(color, 'gray40', grad)
            elif isinstance(color[0], (str, int, float, np.ndarray)):
                self._image = simple_button(color, 'gray40')
            elif isinstance(color[0], (tuple, list)):
                if len(color) == 1:
                    self._image = simple_button(color[0], 'gray40', grad)
                elif len(color) == 2:
                    self._image = simple_button(color[0], color[1], grad)
                else:
                    print('Error: color in wrong format', color)
                    self._image = simple_button('dodgerblue', 'gray40', grad)
            else:
                print('Error: color in wrong format', color)
                self._image = simple_button('dodgerblue', 'gray40', grad)
        elif style == 'normal':
            if isinstance(color, (str, np.ndarray)):
                self._image = normal_button(color, 'gray40', self._rect, grad)
            elif isinstance(color[0], (str, int, float, np.ndarray)):
                self._image = normal_button(color, 'gray40', grad)
            elif isinstance(color[0], (tuple, list)):
                if len(color) == 1:
                    self._image = normal_button(color[0], 'gray40', self._rect, grad)
                elif len(color) == 2:
                    self._image = normal_button(color[0], color[1], self._rect, grad)
                else:
                    print('Error: color in wrong format', color)
                    self._image = normal_button('dodgerblue', 'gray40', self._rect, grad)
            else:
                print('Error: color in wrong format', color)
                self._image = normal_button('dodgerblue', 'gray40', self._rect, grad)
        elif style == 'box':
            if isinstance(color, (str, np.ndarray)):
                self._image = box_button(color, 'gray40', 70, self._rect, grad)
            elif isinstance(color[0], (str, int, float, np.ndarray)):
                self._image = box_button(color, 'gray40', grad)
            elif isinstance(color[0], (tuple, list)):
                if len(color) == 1:
                    self._image = box_button(color[0], 'gray40', 70, self._rect, grad)
                elif len(color) == 2:
                    self._image = box_button(color[0], color[1], 70, self._rect, grad)
                elif len(color) == 3:
                    self._image = box_button(color[0], color[1], color[2], self._rect, grad)
                else:
                    print('Error: color in wrong format', color)
                    self._image = box_button('dodgerblue', 'gray40', 70, self._rect, grad)
            else:
                print('Error: color in wrong format', color)
                self._image = box_button('dodgerblue', 'gray40', 70, self._rect, grad)

        self._image.scale(self._rect.size)

    def blit(self, surface, position=None):
        rect = self._draw_rect(self._rect, position)

        if self.enable:
            if self._toggle:
                surface.blit(self._image.toggle, rect)
            elif self._hover:
                surface.blit(self._image.hover, rect)
            else:
                surface.blit(self._image.base, rect)
        else:
            surface.blit(self._image.disabled, rect)

        self.text.blit(surface, position)

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
        PySceneObject.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1:
            if self.callback and self._hover:
                self.callback(self, self.pydata)
