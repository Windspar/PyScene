import pygame
import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
from pyscene.tool import Point

class PySceneImage:
    def __init__(self, base, hover, toggle, disabled):
        self.base = base
        self.hover = hover
        self.toggle = toggle
        self.disabled = disabled

    def scale(self, size):
            self.base = pygame.transform.scale(self.base, size)
            self.hover = pygame.transform.scale(self.hover, size)
            self.toggle = pygame.transform.scale(self.toggle, size)
            self.disabled = pygame.transform.scale(self.disabled, size)

class PySceneObject:
    CENTER = 0
    LEFT = 1
    TOPLEFT = 2

    def __init__(self, parent, rect, classname, group, allow_bindings):
        self.allow_toggle = False
        self.enable = True
        self._parent = parent
        self._group = group
        self._toggle = False
        self._hover = False
        self._key = '__object_{0}_{1}__'.format(classname, parent._get_pid())

        if group:
            parent._bind_group(self._group, self._key, self)

        if isinstance(rect, pygame.Rect):
            self._rect = rect
        elif len(rect) == 2:
            self._rect = pygame.Rect(*rect, 1, 1)
        else:
            self._rect = pygame.Rect(*rect)

        self._position = Point(self._rect.topleft)
        self._anchor = PySceneObject.TOPLEFT

        if allow_bindings:
            parent.bind_event(pygame.MOUSEMOTION, self._key + 'm_motion__', self.event_mousemotion)
            parent.bind_event(pygame.MOUSEBUTTONDOWN, self._key + 'b_down__', self.event_mousebuttondown)

    def set_focus(self):
        if self._group:
            if self._parent._bindings.group[self._group]['focus']:
                if self._parent._bindings.group[self._group]['focus'] != self:
                    self._parent._bindings.group[self._group]['focus']._toggle = False
            self._parent._bindings.group[self._group]['focus'] = self
            self._parent._bindings.group[self._group]['focus']._toggle = True

    def event_mousemotion(self, event, key, pydata):
        if event is None:
            self._hover = False
        elif self.enable:
            self._hover =  self._rect.collidepoint(event.pos)

    def event_mousebuttondown(self, event, key, pydata):
        if event.button == 1:
            if self._hover and self.enable:
                if self.allow_toggle:
                    self._toggle = not self._toggle
                else:
                    self._toggle = True

                if self._toggle and self._group:
                    self.set_focus()

    def get_key(self):
        return self._key

    def set_position(self, x, y=None):
        if y is None:
            if isinstance(x, Point):
                self._position = x
            elif x:
                self._position = Point(x)
        else:
            self._position = Point(x, y)

        self._anchor_position()

    def set_center(self, x=None, y=None):
        self._anchor = PySceneObject.CENTER
        self.set_position(x,y)
        return self

    def set_topleft(self, x=None, y=None):
        self._anchor = PySceneObject.TOPLEFT
        self.set_position(x,y)
        return self

    def set_left(self, x=None, y=None):
        self._anchor = PySceneObject.LEFT
        self.set_position(x,y)
        return self

    def _anchor_position(self, rect=None):
        if rect is None:
            rect = self._rect

        if self._anchor == PySceneObject.CENTER:
            rect.center = self._position.tup_cast()
        elif self._anchor == PySceneObject.TOPLEFT:
            rect.topleft = self._position.tup_cast()
        elif self._anchor == PySceneObject.LEFT:
            rect.x = int(self._position.x)
            rect.centery = int(self._position.y)
