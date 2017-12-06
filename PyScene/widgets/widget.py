import pygame

class WidgetImage:
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

class Widget:
    group = {}
    pid = 0

    def __init__(self, parent, rect, classname, group):
        self.allow_toggle = False
        self.enable = True
        self._group = group
        self._toggle = False
        self._hover = False
        self._key = '__widget_{0}_{1}__'.format(classname, Widget.pid)
        Widget.pid += 1

        if group:
            Widget.group[self._group] = Widget.group.get(self._group, {'focus':None})
            Widget.group[self._group][self._key] = self

        if rect is None:
            self._rect = rect
        elif isinstance(rect, pygame.Rect):
            self._rect = rect
        else:
            self._rect = pygame.Rect(*rect)

        if parent:
            parent.bind_event(pygame.MOUSEMOTION, self._key + 'm_motion__', self.event_mousemotion)
            parent.bind_event(pygame.MOUSEBUTTONDOWN, self._key + 'b_down__', self.event_mousebuttondown)

    def set_focus(self):
        if self._group:
            if Widget.group[self._group]['focus']:
                if Widget.group[self._group]['focus'] != self:
                    Widget.group[self._group]['focus']._toggle = False
            Widget.group[self._group]['focus'] = self
            Widget.group[self._group]['focus']._toggle = True

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
