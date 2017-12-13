import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import pygame
from widgets.widget import Widget, WidgetImage
from widgets.text import Text
from pyscene.tool import twist, gradient, Vector
#import pyscene.tool.gradient as gradient

def simple_textbox(color, disabled_color, objrect):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.7, False, False)
    brightr, dimr, darkr, dcolorr = twist.gkey(color, disabled_color, 0.7, True, False)
    rect = pygame.Rect(0,0,*objrect.size)
    rect.inflate_ip(-8, -8)
    def overlay(fg, bg, rect, objrect):
        gsurface = gradient.horizontal(bg)
        back = pygame.transform.scale(gsurface, objrect.size)
        gsurface = gradient.horizontal(fg)
        front = pygame.transform.scale(gsurface, rect.size)
        back.blit(front, (4,4))
        return back

    return WidgetImage(
        overlay(dim, dimr, rect, objrect),
        overlay(dim, brightr, rect, objrect),
        overlay(dim, dimr, rect, objrect),
        overlay(dcolor, dcolorr, rect, objrect))

def box_textbox(color , disabled_color, alpha, objrect):
    bright, dim, dark, dcolor = twist.gkey(color, disabled_color, 0.7, False, False)
    rect = pygame.Rect(0,0,*objrect.size)
    rect.inflate_ip(-2, -2)

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
        self.position = [x, int(y - (h / 2))]

class Textbox(Widget):
    def __init__(self, parent, rect, font=None, color='white', callback=None, image='steelblue', style='simple', allow_bindings=True):
        Widget.__init__(self, parent, rect, 'Textbox', None, allow_bindings)
        x = self._rect.x + 6
        y = self._rect.centery
        self.text = Text(parent, "Textbox", x, y, font, color, allow_bindings=False)
        self.text.set_left()
        twist.ghost(self.text._info['base'].image, 60)
        self._buffer = []
        self.callback = callback
        self._carrot = Carrot(self.text._font, x, y, color)
        self._ghost = 'Textbox'
        self._ghost_alpha = 60

        if isinstance(image, (str, tuple, list)):
            self.make_button(image, style)
        else:
            self._image = image

        if allow_bindings:
            parent.bind_event(pygame.KEYDOWN, self._key + 'keydown__', self.event_keydown)
            parent.bind_blit(self._key + 'blit__', self.blit)

    # alpha 0 - 255 , expensive operation
    def set_ghost(self, text, alpha):
        self._ghost = text
        if len(self._buffer) == 0:
            self.text.set_text(self._ghost)
            twist.ghost(self.text._info['base'].image, self._ghost_alpha)

    def set_text(self, text):
        self._buffer = list(text)
        self.update_text()

    def make_button(self, color, style):
        if style == 'simple':
            if isinstance(color, (str, Vector)):
                self._image = simple_textbox(color, 'gray40', self._rect)
            elif isinstance(color[0], (str, int, float, Vector)):
                self._image = simple_textbox(color, 'gray40', self._rect)
            elif isinstance(color[0], (tuple, list)):
                if len(color) == 1:
                    self._image = simple_textbox(color[0], 'gray40', self._rect)
                elif len(color) == 2:
                    self._image = simple_textbox(color[0], color[1], self._rect)
                else:
                    print('Error: color in wrong format', color)
                    self._image = simple_textbox('dodgerblue', 'gray40')
            else:
                print('Error: color in wrong format', color)
                self._image = simple_textbox('dodgerblue', 'gray40')
        elif style == 'box':
            if isinstance(color, (str, Vector)):
                self._image = box_textbox(color, 'gray40', 70, self._rect)
            elif isinstance(color[0], (str, int, float, Vector)):
                self._image = box_textbox(color, 'gray40', 70, self._rect)
            elif isinstance(color[0], (tuple, list)):
                if len(color) == 1:
                    self._image = box_textbox(color[0], 'gray40', 70, self._rect)
                elif len(color) == 2:
                    self._image = box_textbox(color[0], color[1], 70, self._rect)
                elif len(color) == 3:
                    self._image = box_textbox(color[0], color[1], color[2], self._rect)
                else:
                    print('Error: color in wrong format', color)
                    self._image = box_textbox('dodgerblue', 'gray40', 70, self._rect)
            else:
                print('Error: color in wrong format', color)
                self._image = box_textbox('dodgerblue', 'gray40', 70, self._rect)

    def blit(self, surface):
        if not self.enable:
            surface.blit(self._image.disabled, self._rect)
        elif self._hover and not self._toggle:
            surface.blit(self._image.hover, self._rect)
        else:
            surface.blit(self._image.base, self._rect)

        self.text.blit(surface)
        if self._toggle:
            surface.blit(self._carrot.image, self._carrot.position)

    def update_text(self):
        text = ''.join(self._buffer)
        length = len(text)
        font = self.text._font
        if length == 0:
            self.text.set_text('')
            if self.text._anchor == Widget.CENTER:
                self._carrot.position[0] = self.text._rect.centerx
            elif self.text._anchor in (Widget.TOPLEFT, Widget.LEFT):
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
            if self.text._anchor == Widget.CENTER:
                x = self.text._rect.centerx
                # Text is Center so adjust for it
                x -= (font.size(text[left:right])[0] / 2)
                self._carrot.position[0] = x + font.size(text[left:self._carrot.pos])[0]
            elif self.text._anchor in (Widget.TOPLEFT, Widget.LEFT):
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
                if self._toggle:
                    if self.callback:
                        self.callback(self, ''.join(self._buffer))
                self._toggle = False
                if len(self._buffer) == 0:
                    self.text.set_text(self._ghost)
                    twist.ghost(self.text._info['base'].image, self._ghost_alpha)

                pygame.key.set_repeat()

    def set_position(self, x, y=None):
        Widget.set_position(self, x, y)
        if self.text._anchor == Widget.CENTER:
            self.text.set_position(self._rect.center)
        elif self.text._anchor == Widget.TOPLEFT:
            self.text.set_position(self._rect.topleft)
        elif self.text._anchor == Widget.LEFT:
            self.text.set_position(self._rect.x, self._rect.centery)

    def text_center(self):
        self.text.set_center(self._rect.center)

    def text_topleft(self):
        self.text.set_topleft(self._rect.topleft)

    def text_left(self):
        self.text.set_left(self._rect.x, self._rect.centery)
