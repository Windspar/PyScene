import pygame
from widgets.widget import Widget, WidgetImage
from widgets.text import Text

class Carrot:
    def __init__(self, font, rect, color):
        h = font.size("Ay")[1]
        self.image = pygame.Surface((2, h))
        if isinstance(color, str):
            self.image.fill(pygame.Color(color))
        else:
            self.image.fill(pygame.Color(*color))
        self.pos = 0
        self.position = [rect.centerx, int(rect.y - ((rect.h - h) / 2))]

class Textbox(Widget):
    def __init__(self, parent, rect, font=None, color='white', callback=None, image='blue', style='plain', allow_bindings=True):
        Widget.__init__(self, parent, rect, 'Textbox', None, allow_bindings)
        self.text = Text(parent, "Textbox", *self._rect.center, font, color, allow_bindings=False)
        self._alpha(0.3)
        self._buffer = []
        self.callback = callback
        self._carrot = Carrot(self.text._font, self.text._rect, color)
        self._ghost = 'Textbox'
        self._ghost_alpha = 0.3

        if isinstance(image, (str, tuple, list)):
            self.make_button(image, style)
        else:
            self._image = image

        if allow_bindings:
            parent.bind_event(pygame.KEYDOWN, self._key + 'keydown__', self.event_keydown)
            parent.bind_blit(self._key + 'blit__', self.blit)

    # alpha 0 - 255 , expensive operation
    def set_ghost(self, text, alpha):
        self._ghost_alpha = alpha / 255.0
        self._ghost = text
        if len(self._buffer) == 0:
            self.text.set_text(self._ghost)
            self._alpha(self._ghost_alpha)

    def make_button(self, color, style):
        self._image = pygame.Surface(self._rect.size)
        if isinstance(color, str):
            self._image.fill(pygame.Color(color))
        else:
            self._image.fill(pygame.Color(*color))

    def blit(self, surface):
        surface.blit(self._image, self._rect)
        self.text.blit(surface)
        if self._toggle:
            surface.blit(self._carrot.image, self._carrot.position)

    def update_text(self):
        text = ''.join(self._buffer)
        length = len(text)
        font = self.text._font
        if length == 0:
            self.text.set_text('')
            self._carrot.position[0] = self.text._rect.centerx
        else:
            left, right = 0 , length
            while font.size(text[left:right])[0] > self._rect.w - 10:
                if self._carrot.pos - left > right - self._carrot.pos:
                    left += 1
                elif self._carrot.pos - left < right - self._carrot.pos:
                    right -= 1
                else:
                    left += 1
                    right -= 1

            self.text.set_text(text[left:right])
            x = self.text._rect.centerx
            # Text is Center so adjust for it
            x -= (font.size(text[left:right])[0] / 2)
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
                    self.callback(self, ''.join(self._buffer))

            self.update_text()

    # expensive operation
    def _alpha(self, pyfloat):
        rect = self.text._info['base'].image.get_rect()
        for x in range(rect.w):
            for y in range(rect.h):
                color = self.text._info['base'].image.get_at((x, y))
                color.a = int(color.a * pyfloat)
                self.text._info['base'].image.set_at((x,y), color)

    def event_mousebuttondown(self, event, key, pydata):
        if event.button == 1:
            if self._hover and self.enable:
                if len(self._buffer) == 0:
                    self.text.set_text('')
                self._toggle = True
                pygame.key.set_repeat(80,80)
            else:
                self._toggle = False
                if len(self._buffer) == 0:
                    self.text.set_text(self._ghost)
                    self._alpha(self._ghost_alpha)

                pygame.key.set_repeat()
