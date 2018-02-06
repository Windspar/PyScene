import pygame
from .screen import Screen
from . import tick_timer

class Font:
    pass

class Bindings:
    def __init__(self):
        self.scenery = {}
        self.events = {}
        self.blits = {}
        self.group = {}
        self.pid = 0

# Scene flipping
class Scene:
    # store all fonts in Scene
    font = Font()
    # instance of Screen incase it not imported
    screen = Screen

    def __init__(self, rect=None):
        # Scene use
        self._scene_bindings = Bindings()
        if rect is None:
            self._scene_surface_rect = Screen.rect
        else:
            self._scene_surface_rect = rect

        self._scene_rect = pygame.Rect(0,0,*self._scene_surface_rect.size)
        self._scene_surface = pygame.Surface(self._scene_surface_rect.size)
        self._scene_surface = self._scene_surface.convert_alpha()
        self._scene_surface.fill((0,0,0,0))
        # builtins
        self.font = Scene.font
        self.timer = tick_timer.TickTimer(pygame.time.get_ticks())

    # When it switch to scene
    def entrance(self, *args):
        pass
    # When scene is being switch
    def drop(self):
        pass
    # pygame draw code goes here
    def blit(self, surface):
        pass
    # pygame events go here
    def event(self, event):
        pass
    # Items that always need to be updated. Even when inactive
    def update(self):
        pass

    def _bind_group(self, group, key, data):
        self._scene_bindings.group[group] = self._scene_bindings.group.get(group, {'focus': None})
        self._scene_bindings.group[group][key] = data

    def _get_pid(self):
        self._scene_bindings.pid += 1
        return self._scene_bindings.pid

    # does all setup
    def screen_entrance(self, *args):
        if self._scene_bindings.events.get(pygame.MOUSEMOTION, False):
            for key, (callback, pydata) in self._scene_bindings.events[pygame.MOUSEMOTION].items():
                callback(None, key, pydata)

        self.entrance(args)
        self.timer._start()

    def screen_drop(self):
        self.timer._stop()
        self.drop()

    # handles all events
    def screen_event(self, event):
        allow_event = True
        for scenery in self._scene_bindings.scenery.values():
            if scenery.show:
                scenery.screen_event(event)
                if scenery._hover or scenery.allow_event is False:
                    allow_event = False

        if allow_event:
            self.event(event)
            if self._scene_bindings.events.get(event.type, None):
                for key, (callback, pydata) in self._scene_bindings.events[event.type].items():
                    callback(event, key, pydata)

    def screen_update(self):
        self.timer._update(pygame.time.get_ticks())
        self.update()

    # handles all blitting
    def screen_blit(self, surface, update=True):
        allow_update = True
        draw_scenery = []
        for key, scenery in self._scene_bindings.scenery.items():
            if scenery.show:
                allow_update = False
                draw_scenery.append(key)

        if update and allow_update:
            self.timer._start()
            self.screen_update()
        else:
            self.timer._stop()

        self.blit(self._scene_surface)
        for key, callback in self._scene_bindings.blits.items():
            callback(self._scene_surface)

        for key in draw_scenery:
            self._scene_bindings.scenery[key].screen_blit(self._scene_surface)

        surface.blit(self._scene_surface, self._scene_surface_rect)

    def bind_event(self, event, key, callback, pydata=None):
        self._scene_bindings.events[event] = self._scene_bindings.events.get(event, {})
        self._scene_bindings.events[event][key] = callback, pydata

    def unbind_event(self, event, key):
        del self._scene_bindings.events[event][key]

    def bind_blit(self, key, callback):
        self._scene_bindings.blits[key] = callback

    def unbind_blit(self, key):
        del self._scene_bindings.blits[key]

    def draw_scene(self, scene_name, surface):
        Scene.screen.scenes[scene_name].screen_blit(surface)

    def add_scene(self, scene, name=None):
        Scene.screen.add_scene(scene, name)

    def close_screen(self):
        Scene.screen.running = False

    def set_scene(self, scene_name, *args):
        Scene.screen.set_scene(scene_name, args)

    def del_scene(self, scene_name):
        del Scene.screen.scenes[scene_name]

    def add_scenery(self, scenery, scenery_name=None):
        if scenery_name is None:
            scenery_name = type(scenery).__name__
        self._scene_bindings.scenery[scenery_name] = scenery

    def show_scenery(self, scenery_name, show=True):
        self._scene_bindings.scenery[scenery_name].show = show

    def del_scenery(self, scenery_name):
        del self._scene_bindings.scenery[scenery_name]

    @property
    def screen_position(self):
        return self._scene_surface_rect.topleft

    #readonly
    @property
    def _rect(self):
        return self._scene_rect

    #readonly
    @property
    def _screen_rect(self):
        return Scene.screen.rect
