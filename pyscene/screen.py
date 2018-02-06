import os
import pygame

class SceneData:
    def __init__(self, scene, name, alive, track, *args):
        if name is None:
            name = scene.__name__

        if alive:
            self.scene = scene(*args)
        else:
            self.scene = scene

        self.name = name
        self.alive = alive  # Scene stay loaded
        self.track = track  # Keep track of last scene
        self.args = args
        self.entrance_args = args

    def grab(self):
        if self.alive:
            return self.scene
        else:
            return self.scene(*self.args)

class Screen:
    next_scene_name = None
    current_scene = None
    track_scenes = []
    last_scene = None
    running = False
    scenes = {}

    clear_color = (0,0,0)

    @classmethod
    def add_scene(cls, scene, name=None, alive=False, track=False, *args):
        scene_data = SceneData(scene, name, alive, track, *args)
        cls.scenes[scene_data.name] = scene_data

    @classmethod
    def set_scene(cls, name, *args):
        cls.scenes[name].entrance_args = args
        cls.next_scene_name = name
        if cls.scenes[name].track:
            if cls.current_scene:
                cls.track_scenes.append(cls.current_scene)
        else:
            cls.track_scenes = []

    @classmethod
    def set_last_scene(cls):
        cls.last_scene = cls.track_scenes[-1]
        if len(cls.track_scenes) < 2:
            cls.track_scenes = []
        else:
            cls.track_scenes = cls.track_scenes[:-1]

    @staticmethod
    def center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @classmethod
    def resize(cls, size, flags=0, depth=0):
        # this area needs more work
        cls.rect.size = size
        cls.surface = pygame.display.set_mode(cls.rect.size, flags, depth)

    @classmethod
    def open(cls, caption, size, flags=0, depth=0):
        pygame.init()
        cls.rect = pygame.Rect(0,0,*size)
        pygame.display.set_caption(caption)
        cls.surface = pygame.display.set_mode(cls.rect.size, flags, depth)
        cls.clock = pygame.time.Clock()
        cls.running = False

    @classmethod
    def close(cls):
        cls.running = False

    @classmethod
    def loop(cls, start_scene, fps=60):
        cls.fps = fps
        cls.running = True

        next_scene = cls.scenes[start_scene]
        cls.current_scene = next_scene.grab()
        cls.current_scene.screen_entrance(*next_scene.entrance_args)

        while cls.running:
            # run all events first before changing scene
            # Went to poll events. Sometimes you just want to clear events.
            while True:
                event = pygame.event.poll()
                if event.type == pygame.NOEVENT:
                    break
                else:
                    cls.current_scene.screen_event(event)

            # change scene
            if cls.next_scene_name:
                cls.current_scene.screen_drop()
                next_scene = cls.scenes[cls.next_scene_name]
                cls.current_scene = next_scene.grab()
                cls.current_scene.screen_entrance(*next_scene.entrance_args)
                cls.next_scene_name = None

            if cls.last_scene:
                cls.current_scene.screen_drop()
                cls.current_scene = cls.last_scene
                cls.current_scene.screen_entrance()
                cls.last_scene = None

            # blit current scene
            cls.surface.fill(cls.clear_color)
            cls.current_scene.screen_blit(cls.surface)
            pygame.display.flip()
            cls.clock.tick(Screen.fps)

        pygame.quit()
