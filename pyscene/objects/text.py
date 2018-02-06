import pygame
from .objects import PySceneObject
from .text_effects import BaseEffect, Blink, Reflection, Shadow, TypeWriter
from ..layout import Anchor

# Text are static. Can be transform in Text Click.
# Text can have a hilight color.
# Text can have colorful text

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
                fade=None,        # 'up', 'down', 'left', 'right'
                shift=None,       # (value, direction)
                hilight=None,     # (color, alpha=None)
                toggle=None,      # (color, alpha=None)
                blink=None,       # (color, time_interval, interval, alpha=None)
                shadow=None,      # (color, offset=(1,1), trail=False, step=1, alpha=None)
                typewriter=None,  # (interval, callback, pydata)
                reflection=None,  # (distance=0, fades=None, shifts=None, color=None)
                angle=None,
                anchor=Anchor.LEFT):

        PySceneObject.__init__(self, parent, pos, 'Text', group, allow_bindings, anchor)
        if font is None:
            self._font = pygame.font.Font(None, 24)
        else:
            self._font = font

        self._effects = {
            'angle': angle,
            'shift': shift,
            'fade': fade
        }
        self._text = text
        self._info = {'base': BaseEffect(self, color, alpha)}
        self._info['base'].do_rect()
        self._build(self.set_callback, callback, True)
        self._build(self.effect_toggle, toggle)
        self._build(self.effect_hilight, hilight)
        self._build(self.effect_blink, blink)
        self._build(self.effect_shadow, shadow)
        self._build(self.effect_typewriter, typewriter)
        self._build(self.effect_reflection, reflection)

        if allow_bindings:
            parent.bind_blit(self._key + 'blit__', self.blit)

    def _build(self, method, data, allow=False):
        if data or allow:
            if isinstance(data, (tuple, list)):
                method(*data)
            else:
                method(data)

    def _do_render(self):
        for key in self._info.keys():
            self._info[key].render()
        self._info['base'].do_rect()

    def blit(self, surface, position=None):
        clip_rect = None
        if self._info.get('typewriter', False):
            if not self._info['typewriter'].finish:
                clip_rect = self._info['typewriter'].clip_rect

        if self._info.get('shadow', False):
            self._info['shadow'].blit(surface, clip_rect)

        if self._info.get('toggle', False) and self._toggle:
            self._info['toggle'].blit(surface, clip_rect)
        elif self._info.get('hover', False) and self._hover:
            self._info['hover'].blit(surface, clip_rect)
        elif self._info.get('blink', False) and self._info['blink'].blink:
            self._info['blink'].blit(surface, clip_rect)
        else:
            self._info['base'].blit(surface, clip_rect)

        if self._info.get('reflection', False):
            self._info['reflection'].blit(surface)

    def event_mousemotion(self, event, key, pydata):
        if event is None:
            self._hover = False
            if self._info.get('blink', False):
                if self._parent.timer[self._key + 'blink_timer__'].stop:
                    self._parent.timer.start(self._key + 'blink_timer__')
        elif self.enable:
            self._hover = self._rect.collidepoint(event.pos)
            if self._info.get('hover', False) and self._hover:
                if self._info.get('blink', False):
                    self._parent.timer.stop(self._key + 'blink_timer__')
            else:
                if self._info.get('blink', False):
                    if self._parent.timer[self._key + 'blink_timer__'].stop:
                        self._parent.timer.start(self._key + 'blink_timer__')

    def event_mousebuttondown(self, event, key, pydata):
        PySceneObject.event_mousebuttondown(self, event, key, pydata)

        if event.button == 1:
            if self.callback and self._hover:
                self.callback(self, self.pydata)

    def effect_blink(self, color=None, time_interval=1400, interval=700, alpha=None):
        self._info['blink']= Blink(self, color, time_interval, interval, alpha)

    def effect_blink_destroy(self):
        self._info['blink'].destroy()
        del self._info['blink']

    def effect_hilight(self, color=None, alpha=None):
        if color is None:
            if self._info.get('hover', False):
                del self._info['hover']
        else:
            self._info['hover'] = BaseEffect(self, color, alpha)

    def effect_shadow(self, color=None, offset=(1,1), trail=False, step=1, alpha=None):
        if color is None:
            if self._info.get('shadow', False):
                del self._info['shadow']
        else:
            self._info['shadow'] = Shadow(self, color, offset, trail, step, alpha)

    def effect_typewriter(self, interval=50, callback=None, pydata=None):
        self._info['typewriter'] = TypeWriter(self, interval, callback, pydata)

    def effect_toggle(self, color=None, alpha=None):
        if color is None:
            self.allow_toggle = False
            if self._info.get('toggle', False):
                del self._info['toggle']
            return
        else:
            self._info['toggle'] = BaseEffect(self, color, alpha)

        if self._group is None:
            self.allow_toggle = True

    def effect_reflection(self, distance=0, fades=None, shifts=None, color=None):
        if color is None:
            color = self._info['base'].color

        self._info['reflection'] = Reflection(self, distance, fades, shifts, color)

    def effect_reflection_destroy(self):
        del self._info['reflection']

    def set_angle(self, angle):
        self._effects['angle'] = angle
        self._do_render()

    def set_callback(self, callback, pydata=None):
        self.callback = callback
        self.pydata = pydata

    def set_color(self, color, alpha=None):
        self._info['base'].set_color(color)
        self._info['base'].alpha = alpha
        self._info['base'].render()

    def set_font(self, font):
        self._font = font
        self._do_render()

    def set_text(self, text):
        self._text = text
        self._do_render()

    def set_position(self, x, y=None):
        PySceneObject.set_position(self, x, y)
        #self._do_render()

    def effect(self, key):
        return self._info[key]

    def __repr__(self):
        return "Text({0})".format(self._text)
