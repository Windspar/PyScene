import os
import pygame
import pyscene.tick_timer as tick_timer

class Screen:
	set_scene = None
	running = False
	scenes = {}

	@classmethod
	def add_scene(cls, scene, name=None):
		if name is None:
			name = type(scene).__name__
		cls.scenes[name] = scene

	@staticmethod
	def center():
		os.environ['SDL_VIDEO_CENTERED'] = '1'

	@classmethod
	def open(cls, caption, size, flags=0, depth=0):
		pygame.init()
		cls.size = size
		cls.current_scene = Scene()
		pygame.display.set_caption(caption)
		cls.surface = pygame.display.set_mode(size, flags, depth)
		cls.clock = pygame.time.Clock()
		cls.running = False

	@classmethod
	def close(cls):
		cls.running = False

	@classmethod
	def loop(cls, start_scene=None, fps=60):
		cls.fps = fps
		cls.running = True
		cls.set_scene = start_scene

		while cls.running:
			if cls.set_scene:
				cls.current_scene.screen_drop()
				cls.current_scene = cls.scenes[cls.set_scene]
				cls.current_scene.screen_entrance()
				cls.set_scene = None

			for event in pygame.event.get():
				cls.current_scene.screen_event(event)

			cls.current_scene.screen_blit(cls.surface)

			pygame.display.flip()
			cls.clock.tick(Screen.fps)

		pygame.quit()

class Font:
	pass

class Bindings:
	def __init__(self):
		self.events = {}
		self.blits = {}
		self.group = {}
		self.pid = 0

# Scene flipping
class Scene:
	font = Font()
	screen = Screen

	def __init__(self):
		self._bindings = Bindings()
		# builtins
		self.font = Scene.font
		self.timer = tick_timer.TickTimer(pygame.time.get_ticks())

	def entrance(self):
		pass
	def drop(self):
		pass
	def blit(self, surface):
		pass
	def event(self, event):
		pass

	def _bind_group(self, group, key, data):
		self._bindings.group[group] = self._bindings.group.get(group, {'focus': None})
		self._bindings.group[group][key] = data

	def _get_pid(self):
		self._bindings.pid += 1
		return self._bindings.pid

	def screen_entrance(self):
		if self._bindings.events.get(pygame.MOUSEMOTION, False):
			for key, (callback, pydata) in self._bindings.events[pygame.MOUSEMOTION].items():
				callback(None, key, pydata)

		self.entrance()
		self.timer._time_elaspe()

	def screen_drop(self):
		self.timer._stop()
		self.drop()

	def screen_event(self, event):
		self.event(event)
		if self._bindings.events.get(event.type, None):
			for key, (callback, pydata) in self._bindings.events[event.type].items():
				callback(event, key, pydata)

		self.timer._update(pygame.time.get_ticks())

	def screen_blit(self, surface):
		self.blit(surface)
		for key, callback in self._bindings.blits.items():
			callback(surface)

	def bind_event(self, event, key, callback, pydata=None):
		self._bindings.events[event] = self._bindings.events.get(event, {})
		self._bindings.events[event][key] = callback, pydata

	def unbind_event(self, event, key):
		del self._bindings.events[event][key]

	def bind_blit(self, key, callback):
		self._bindings.blits[key] = callback

	def unbind_blit(self, key):
		del self._bindings.blits[key]

	def add_scene(self, scene, name=None):
		Scene.screen.add_scene(scene, name)

	def close_screen(self):
		Scene.screen.running = False

	def set_scene(self, scene):
		Scene.screen.set_scene = scene
