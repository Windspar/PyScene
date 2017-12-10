import os
import pygame
import PyScene.tick_timer as tick_timer
pygame.init()

class Font:
	@staticmethod
	def load(fontname, size=None):
		if size is None:
			return pygame.font.Font(None, fontname)
		else:
			return pygame.font.Font(fontname, size)

class Bindings:
	def __init__(self):
		self.events = {}
		self.blits = {}
		self.group = {}
		self.pid = 0

# Scene flipping
class Scene:
	def __init__(self):
		self._bindings = Bindings()
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

	def _event(self, event):
		if self._bindings.events.get(event.type, None):
			for key, (callback, pydata) in self._bindings.events[event.type].items():
				callback(event, key, pydata)

	def _blit(self, surface):
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

# static
class Screen:
	set_scene = None
	running = False
	scenes = {}

	def center():
		os.environ['SDL_VIDEO_CENTERED'] = '1'

	# static
	def init(caption, size, flags=0, depth=0):
		Screen.size = size
		Screen.current_scene = Scene()
		pygame.display.set_caption(caption)
		Screen.surface = pygame.display.set_mode(size, flags, depth)
		Screen.clock = pygame.time.Clock()

	#static
	def loop(start_scene=None, fps=60):
		Screen.fps = fps
		Screen.running = True
		Screen.set_scene = start_scene

		while Screen.running:
			if Screen.set_scene:
				Screen.current_scene.timer._stop()
				Screen.current_scene.drop()
				Screen.current_scene = Screen.scenes[Screen.set_scene]
				for key, (callback, pydata) in Screen.current_scene._bindings.events[pygame.MOUSEMOTION].items():
					callback(None, key, pydata)
				Screen.current_scene.entrance()
				Screen.current_scene.timer._time_elaspe()
				Screen.set_scene = None

			for event in pygame.event.get():
				Screen.current_scene._event(event)
				Screen.current_scene.event(event)

			Screen.current_scene.timer._update(pygame.time.get_ticks())
			Screen.current_scene.blit(Screen.surface)
			Screen.current_scene._blit(Screen.surface)

			pygame.display.flip()
			Screen.clock.tick(Screen.fps)

		pygame.quit()
