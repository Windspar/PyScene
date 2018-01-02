import pygame
from pyscene.objects import PySceneObject
from pyscene.tool import gradient, twist

# Text are static. Can be transform in Text Click.
# Text can have a hilight color.
# Text can have colorful text

class TextInfo:
    def __init__(self, color, alpha):
        self.alpha = alpha
        self.image = None
        self.r_image = None
        self.color = twist.colorx(color)

    def set_color(self, color):
        self.color = twist.colorx(color)

# color takes pygame.Color args or pygame.Surface
class Text(PySceneObject):

    def __init__(self, parent,
                text='Text',
                pos=(0,0),
                font=None,
                color='white',
                alpha=None,
                group=None,
                callback=None,    # (callback, pydata=None)
                allow_bindings=True,
                hilight=None,     # (color, alpha=None)
                toggle=None,      # (color, alpha=None)
                blink=None,       # (color, time_interval, interval, alpha=None)
                angle=None,
                anchorx='left',
                anchory='top'):

        PySceneObject.__init__(self, parent, pos, 'Text', group, allow_bindings, anchorx, anchory)
        if font is None:
            self._font = pygame.font.Font(None, 24)
        else:
            self._font = font
        self._info = {'base': TextInfo(color, alpha)}
        self._text = text
        self._angle = angle
        self._rot_rect = None
        self._render(self._info['base'])
        self._build(self.set_callback, callback)
        self._build(self.set_toggle, toggle)
        self._build(self.set_hilight, hilight)
        self._build(self.set_blink, blink)

        if allow_bindings:
            parent.bind_blit(self._key + 'blit__', self.blit)

    def _build(self, method, data):
        if isinstance(data, (tuple, list)):
            method(*data)
        else:
            method(data)

    def _do_render(self):
        for key in self._info.keys():
            self._render(self._info[key])

    def _render(self, info):
        if isinstance(info.color, pygame.Surface):
            surface = self._font.render(self._text, 1, (255,255,255))
        else:
            surface = self._font.render(self._text, 1, info.color)
        self._rect = surface.get_rect()
        self._anchor_position()

        if isinstance(info.color, pygame.Surface):
            info.image = gradient.apply_surface(surface, info.color)
            if self._angle is not None:
                info.r_image = pygame.transform.rotate(info.image, self._angle)
                self._rot_rect = info.r_image.get_rect()
                self._rot_rect.center = self._rect.center
        else:
            info.image = surface
            if info.alpha:
                twist.ghost(info.image, info.alpha)

            if self._angle is not None:
                info.r_image = pygame.transform.rotate(info.image, self._angle)
                self._rot_rect = info.r_image.get_rect()
                self._rot_rect.center = self._rect.center

    def blit(self, surface, position=None):
        rect = [self._rot_rect, self._rect][self._angle is None]
        rect = self._draw_rect(rect, position)
        attr = ['r_image', 'image'][self._angle is None]

        if self._info.get('toggle', False) and self._toggle:
            surface.blit(getattr(self._info['toggle'], attr), rect)
        elif self._info.get('hover', False) and self._hover:
            surface.blit(getattr(self._info['hover'], attr), rect)
        elif self._info.get('blink', False) and self._info['blink'].blink:
            surface.blit(getattr(self._info['blink'], attr), rect)
        else:
            surface.blit(getattr(self._info['base'], attr), rect)

    def event_mousemotion(self, event, key, pydata):
        if event is None:
            self._hover = False
            if self._info.get('blink', False):
                if self._parent.timer[self._key + 'timer__'].stop:
                    self._parent.timer.start(self._key + 'timer__')
        elif self.enable:
            self._hover = self._rect.collidepoint(event.pos)
            if self._info.get('hover', False) and self._hover:
                if self._info.get('blink', False):
                    self._parent.timer.stop(self._key + 'timer__')
            else:
                if self._info.get('blink', False):
                    if self._parent.timer[self._key + 'timer__'].stop:
                        self._parent.timer.start(self._key + 'timer__')

    def event_mousebuttondown(self, event, key, pydata):
        PySceneObject.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1:
            if self.callback and self._hover:
                self.callback(self, self.pydata)

    def _timer_blink(self, info):
        if info.pydata == 'time':
            self._info['blink'].blink = False
            info.pydata = 'blink'
            info.interval = self._info['blink'].time_interval
        else:
            self._info['blink'].blink = True
            info.pydata = 'time'
            info.interval = self._info['blink'].interval

    def set_blink(self, color, time_interval=1400, interval=700, alpha=None):
        if color is None:
            if self._info.get('blink', False):
                self._parent.timer.pop(self._key + 'timer__')
                del self._info['blink']
            return

        if self._info.get('blink', False):
            self._info['blink'].set_color(color)
            self._info['blink'].alpha = alpha
        else:
            self._info['blink'] = TextInfo(color, alpha)

        self._info['blink'].interval = interval
        self._info['blink'].time_interval = time_interval
        self._info['blink'].blink = False
        self._parent.timer.add(self._key + 'timer__', interval, self._timer_blink, 'time')
        self._render(self._info['blink'])
        return self

    def set_angle(self, angle):
        self._angle = angle
        self._do_render()
        return self

    def set_callback(self, callback, pydata=None):
        self.callback = callback
        self.pydata = pydata
        return self

    def set_color(self, color, alpha=None):
        self._info['base'].set_color(color)
        self._info['base'].alpha = alpha
        self._render(self._info['base'])
        return self

    def set_hilight(self, color, alpha=None):
        if color is None:
            if self._info.get('hover', False):
                del self._info['hover']
            return
        elif self._info.get('hover', False):
            self._info['hover'].set_color(color)
            self._info['hover'].alpha = alpha
        else:
            self._info['hover'] = TextInfo(color, alpha)
        self._render(self._info['hover'])
        return self

    def set_font(self, font):
        self._font = font
        self._do_render()
        return self

    def set_text(self, text):
        self._text = text
        self._do_render()
        return self

    def set_toggle(self, color, alpha=None):
        if color is None:
            self.allow_toggle = False
            if self._info.get('toggle', False):
                del self._info['toggle']
            return

        if self._group is None:
            self.allow_toggle = True

        if self._info.get('toggle', False):
            self._info['toggle'].set_color(color)
            self._info['toggle'].alpha = alpha
        else:
            self._info['toggle'] = TextInfo(color, alpha)
        self._render(self._info['toggle'])
        return self

    def set_position(self, x, y=None):
        PySceneObject.set_position(self, x, y)
        if self._rot_rect:
            self._anchor_position(self._rot_rect)
        return self

    def __repr__(self):
        return "Text({0})".format(self._text)
