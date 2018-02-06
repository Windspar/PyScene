import pygame
from .base import BaseEffect

class Blink(BaseEffect):
    def __init__(self, parent, color, time_interval=1400, interval=700, alpha=None):
        BaseEffect.__init__(self, parent, color, alpha)
        self.time_interval = time_interval
        self.interval = interval
        self.alpha = alpha
        self.blink = False

        self.parent._parent.timer.add(self.parent._key + 'blink_timer__', self.interval,
        self._blink, 'time')

    def _blink(self, info):
        if info.pydata == 'time':
            self.blink = False
            info.pydata = 'blink'
            info.interval = self.time_interval
        else:
            self.blink = True
            info.pydata = 'time'
            info.interval = self.interval

    def blit(self, surface, clip_rect=None):
        if self.color:
            BaseEffect.blit(self, surface, clip_rect)

    def destroy(self):
        self.parent._parent.timer.pop(self.parent._key + 'blink_timer__')
