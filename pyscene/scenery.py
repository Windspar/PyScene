import pygame
from .scene import Scene
from .arrays import Point

# under construction
# Scene within a Scene
class Scenery(Scene):
    @classmethod
    def init_center(cls, self, parent, size, show, allow_event):
        # shrink it from parent scene
        size = Point(size) - Point(parent._scene_surface_rect.size)
        rect = parent._scene_surface_rect.inflate(*size.tup())
        cls.__init__(self, rect, show, allow_event)

    def __init__(self, rect, show, allow_event):
        Scene.__init__(self, pygame.Rect(*rect))
        self.allow_event = allow_event
        self._hover = False
        self.show = show

    def screen_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self._screen_rect.collidepoint(event.pos)

        if self._hover:
            self.event(event)
            if self._scene_bindings.events.get(event.type, None):
                for key, (callback, pydata) in self._scene_bindings.events[event.type].items():
                    callback(event, key, pydata)
