import pygame
import numpy as np
from ..layout import Anchor
from .styles import ButtonStyle, SimpleButtonStyle
from .objects import PySceneObject
from .text import Text

class Button(PySceneObject):
    def __init__(self, parent,
            text = 'Button',
            rect =(0,0,100,34),
            image=None,
            callback = None,        # (callback, pydata)
            group=None,
            allow_bindings=True,
            text_kw = {'color':'white'},
            anchor=Anchor.LEFT):

        PySceneObject.__init__(self, parent, rect, 'Button', group, allow_bindings, anchor)
        if isinstance(callback, (tuple, list)):
            self.callback = callback[0]
            self.pydata = callback[1]
        else:
            self.callback = callback
            self.pydata = None

        self.set_image(image)

        if isinstance(text, Text):
            self.text = text
            self.text.set_position(rect.center)
            self.text.anchor(Anchor.CENTER)
        else:
            self.text = Text(parent, text, rect.center,
            **text_kw,
            allow_bindings = False,
            anchor = Anchor.CENTER)

        if allow_bindings:
            parent.bind_event(pygame.MOUSEBUTTONUP, self._key + 'up__', self.event_mousebuttonup)
            parent.bind_blit(self._key + 'blit__', self.blit)

    def blit(self, surface, position=None):
        if self.enable:
            if self._toggle:
                surface.blit(self._image.toggle, self._rect)
            elif self._hover:
                surface.blit(self._image.hover, self._rect)
            else:
                surface.blit(self._image.base, self._rect)
        else:
            surface.blit(self._image.disabled, self._rect)

        self.text.blit(surface, position)

    def event_mousebuttonup(self, event, key, pydata):
        if event.button == 1 and self.enable:
            self._toggle = False
            if self._hover:
                if self.callback:
                    self.callback(self, self.pydata)

    def set_image(self, image):
        self._image_data = image
        if image is None:
            simple = SimpleButtonStyle('dodgerblue','gray40', [False, 2, 20, 0, True])
            self._image = simple.get_image(self._rect)
        elif isinstance(image, str):
            simple = SimpleButtonStyle(image,'gray40', [False, 2, 20, 0, True])
            self._image = simple.get_image(self._rect)
        elif isinstance(image, pygame.Surface):
            self._image = image
            self._image.scale(self._rect.size, self._rect)
        elif isinstance(image, ButtonStyle):
            self._image = image.get_image(self._rect)
        else:
            print('Error: wrong data for button', image)
            simple = SimpleButtonStyle('dodgerblue','gray40', [False, 2, 20, 0, True])
            self._image = simple.get_image(self._rect)

class ToggleButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)

        if self._group is None:
            self.allow_toggle = True

        if len(args) > 7:
            allow_bindings = args[7]
        elif kwargs.get('allow_bindings', False):
            allow_bindings = kwargs['allow_bindings']
        else:
            allow_bindings = True

        if allow_bindings:
            args[0].unbind_event(pygame.MOUSEBUTTONUP, self._key + 'up__')

    def event_mousebuttondown(self, event, key, pydata):
        PySceneObject.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1 and self.enable:
            if self.callback and self._hover:
                self.callback(self, self.pydata)
