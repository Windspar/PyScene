import pygame
import numpy as np
from ..layout.anchor import Anchor, AnchorX, AnchorY
from .styles import TextboxStyle, SimpleTextboxStyle
from .objects import PySceneObject, PySceneImage
from .text import Text
from .. import twist

class Carrot:
    def __init__(self, font, x, y, color):
        h = font.get_height()
        color = twist.color(color)
        if isinstance(color, pygame.Color):
            self.image = pygame.Surface((2, h))
            self.image.fill(color)
        else:
            self.image = pygame.transform.scale(color, (2,h))
        self.pos = 0
        self.position = [x, int(y - (h / 2)), 2, h]

class Textbox(PySceneObject):
    def __init__(self, parent,
            rect = (0,0,200,40),
            font=None,
            color='white',
            image=None,
            callback=None,
            allow_bindings=True,
            anchor = Anchor.LEFT,
            ghost_kw = {'text':"Textbox", 'color':'white', 'alpha':60},
            text_kw = {}):
        PySceneObject.__init__(self, parent, rect, 'Textbox', None, allow_bindings)
        self._anchor_position()
        x = self._rect.x + 6
        y = self._rect.centery
        self.text = Text(parent, "", (x, y), font, color,
            anchor = Anchor.MID_LEFT,
            allow_bindings=False,
            **text_kw)
        self._buffer = []
        self.callback = callback
        self._carrot = Carrot(self.text._font, x, y, color)
        x = self._rect.centerx
        if ghost_kw.get('font', False) is False:
            ghost_kw['font'] = font

        self.ghost_text = Text(parent,
            pos = (x, y),
            allow_bindings = False,
            anchor = Anchor.CENTER,
            **ghost_kw)

        self._image_data = image
        if image == None:
            simple = SimpleTextboxStyle('dodgerblue','gray40')
            self._image = simple.get_image(self._rect)
        elif isinstance(image, pygame.Surface):
            self._image = image
            self._image.scale(self._rect.size, self._rect)
        elif isinstance(image, TextboxStyle):
            self._image = image.get_image(self._rect)
        else:
            print('Error: wrong data for textbox', image)

        if allow_bindings:
            parent.bind_event(pygame.KEYDOWN, self._key + 'keydown__', self.event_keydown)
            parent.bind_blit(self._key + 'blit__', self.blit)

    def set_ghost(self, text, color, alpha=60):
        self.ghost_text.set_color(color, alpha)
        self.ghost_text.set_text(text)
        return self

    def set_text(self, text):
        self._buffer = list(text)
        self.update_text()

    def blit(self, surface, position=None):
        if not self.enable:
            surface.blit(self._image.disabled, self._rect)
        elif self._hover and not self._toggle:
            surface.blit(self._image.hover, self._rect)
        else:
            surface.blit(self._image.base, self._rect)

        self.text.blit(surface, position)
        if self._toggle:
            surface.blit(self._carrot.image, self._carrot.position)
        elif len(self._buffer) == 0:
            self.ghost_text.blit(surface)

    def update_text(self):
        text = ''.join(self._buffer)
        length = len(text)
        font = self.text._font
        if length == 0:
            self.text.set_text('')
            if self.text._anchor.x == AnchorX.CENTER:
                self._carrot.position[0] = self.text._rect.centerx
            elif self.text._anchor.x == AnchorX.LEFT:
                self._carrot.position[0] = self.text._rect.x
        else:
            left, right = 0 , length
            while font.size(text[left:right])[0] > self._rect.w - 10:
                if self._carrot.pos - left > right - self._carrot.pos:
                    left += 1
                elif self._carrot.pos - left < right - self._carrot.pos + 1:
                    right -= 1
                else:
                    left += 1
                    right -= 1

            self.text.set_text(text[left:right])
            if self.text._anchor.x == AnchorX.CENTER:
                x = self.text._rect.centerx
                # Text is Center so adjust for it
                x -= (font.size(text[left:right])[0] / 2)
                self._carrot.position[0] = x + font.size(text[left:self._carrot.pos])[0]
            elif self.text._anchor.x == AnchorX.LEFT:
                x = self.text._rect.x
                self._carrot.position[0] = x + font.size(text[left:self._carrot.pos])[0]

    def event_keydown(self, event, key, pydata):
        if pygame.key.get_repeat() == (0,0):
            pygame.key.set_repeat(80,80)
        if self._toggle:
            if 32 <= event.key < 123:
                self._buffer.insert(self._carrot.pos, str(event.unicode))
                self._carrot.pos += 1
            elif event.key == pygame.K_DELETE:
                self._buffer = []
                self._carrot.pos = 0
            elif event.key == pygame.K_BACKSPACE:
                if len(self._buffer) > 1:
                    if self._carrot.pos > 0:
                        self._buffer = self._buffer[:self._carrot.pos - 1] + self._buffer[self._carrot.pos:]
                        self._carrot.pos -= 1
                else:
                    self._buffer = []
                    self._carrot.pos = 0
            elif event.key == pygame.K_LEFT:
                if self._carrot.pos > 0:
                    self._carrot.pos -= 1
            elif  event.key == pygame.K_RIGHT:
                if self._carrot.pos < len(self._buffer):
                    self._carrot.pos += 1
            elif event.key == pygame.K_END:
                self._carrot.pos = len(self._buffer)
            elif event.key == pygame.K_HOME:
                self._carrot.pos = 0
            elif event.key == pygame.K_RETURN:
                if self.callback:
                    self._toggle = False
                    self.callback(self, ''.join(self._buffer))

            self.update_text()

    def event_mousebuttondown(self, event, key, pydata):
        if event.button == 1:
            if self._hover and self.enable:
                if len(self._buffer) == 0:
                    self.text.set_text('')
                self._toggle = True
                pygame.key.set_repeat(80,80)
            else:
                self._toggle = False
                if len(self._buffer):
                    if self.callback:
                        self.callback(self, ''.join(self._buffer))

                pygame.key.set_repeat()

    def set_position(self, x, y=None):
        PySceneObject.set_position(self, x, y)
        self.text._anchor_rect(self._rect)

    def text_center(self):
        self.text.set_position(self._rect.center)
        self.text.anchor(Anchor.CENTER)

    def text_topleft(self):
        self.text.set_position(self._rect.topleft)
        self.text.anchor(Anchor.LEFT)

    def text_left(self):
        self.text.set_position(self._rect.x, self._rect.centery)
        self.text.anchor(Anchor.MID_LEFT)
