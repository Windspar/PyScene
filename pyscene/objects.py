import pygame
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

class AnchorX:
    CENTER = 'center'
    LEFT = 'left'
    RIGHT = 'right'

class AnchorY:
    CENTER = 'center'
    TOP = 'top'
    BOTTOM = 'bottom'

class PySceneObject:
    def __init__(self, parent, rect, classname, group, allow_bindings, anchorx='left', anchory='top'):
        self.allow_toggle = False
        self.enable = True
        self._parent = parent
        self._group = group
        self._toggle = False
        self._hover = False
        self._key = '__object_{0}_{1}__'.format(classname, parent._get_pid())

        if group:
            parent._bind_group(self._group, self._key, self)

        if rect is None:
            self._rect = pygame.Rect(0,0,1,1)
        if isinstance(rect, pygame.Rect):
            self._rect = rect
        elif len(rect) == 2:
            self._rect = pygame.Rect(*rect, 1, 1)
        else:
            self._rect = pygame.Rect(*rect)

        self._rect_offset()
        self._position = Point(self._rect.topleft)
        self._anchorx = anchorx
        self._anchory = anchory

        if allow_bindings:
            parent.bind_event(pygame.MOUSEMOTION, self._key + 'm_motion__', self.event_mousemotion)
            parent.bind_event(pygame.MOUSEBUTTONDOWN, self._key + 'b_down__', self.event_mousebuttondown)

    def _anchor_rect(self, rect):
        if self._anchorx == AnchorX.CENTER:
            self._position.x = rect.centerx
        else:
            self._position.x = rect.x

        if self._anchory == AnchorY.CENTER:
            self._position.y = rect.centery
        else:
            self._position.y = rect.y

    # private
    def _anchor_position(self, rect=None):
        if rect is None:
            rect = self._rect

        if self._anchorx == AnchorX.CENTER:
            rect.centerx = int(self._position.x)
        elif self._anchorx == AnchorX.RIGHT:
            rect.right = int(self._position.x)
        else:
            rect.x = int(self._position.x)

        if self._anchory == AnchorY.CENTER:
            rect.centery = int(self._position.y)
        elif self._anchory == AnchorY.BOTTOM:
            rect.bottom = int(self._position.y)
        else:
            rect.y = int(self._position.y)

    # private
    def _draw_rect(self, rect, position):
        if position is None:
            return rect
        else:
            nrect = rect.copy()
            nrect.x -= position[0]
            nrect.y -= position[1]
            return nrect

    # private
    def _rect_offset(self):
        position = self._parent.get_position()
        self._rect.x += position[0]
        self._rect.y += position[1]

    def anchor(self, x, y):
        self._anchorx = x
        self._anchory = y
        self._anchor_position()
        return self

    def anchorx(self, x):
        self._anchorx = x
        self._anchor_position()
        return self

    def anchory(self, y):
        self._anchory = y
        self._anchor_position()
        return self

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
            self._position = Point((x, y))

        self._rect_offset()
        self._anchor_position()
        return self
