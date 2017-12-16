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
	def resize(cls, size, flags=0, depth=0):
		# this area needs more work
		cls.rect.size = size
		cls.surface = pygame.display.set_mode(cls.rect.size, flags, depth)

	@classmethod
	def open(cls, caption, size, flags=0, depth=0):
		pygame.init()
		cls.rect = pygame.Rect(0,0,*size)
		cls.current_scene = Scene()
		pygame.display.set_caption(caption)
		cls.surface = pygame.display.set_mode(cls.rect.size, flags, depth)
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
		self.scenery = {}
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

	# When it switch to scene
	def entrance(self):
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
	# Items that only upate but not on pause
	def update(self):
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
		self.timer._start()

	def screen_drop(self):
		self.timer._stop()
		self.drop()

	def screen_event(self, event):
		allow_event = True
		for scenery in self._bindings.scenery.values():
			if scenery.show:
				scenery.screen_event(event)
				if scenery._hover or scenery.allow_event is False:
					allow_event = False

		if allow_event:
			self.event(event)
			if self._bindings.events.get(event.type, None):
				for key, (callback, pydata) in self._bindings.events[event.type].items():
					callback(event, key, pydata)

	def screen_update(self):
		self.timer._update(pygame.time.get_ticks())
		self.update()

	def screen_blit(self, surface, update=True):
		allow_update = True
		draw_scenery = []
		for key, scenery in self._bindings.scenery.items():
			if scenery.show:
				allow_update = False
				draw_scenery.append(key)

		if update and allow_update:
			self.timer._start()
			self.screen_update()
		else:
			self.timer._stop()

		self.blit(surface)
		for key, callback in self._bindings.blits.items():
			callback(surface)

		for key in draw_scenery:
			self._bindings.scenery[key].screen_blit(surface)

	def bind_event(self, event, key, callback, pydata=None):
		self._bindings.events[event] = self._bindings.events.get(event, {})
		self._bindings.events[event][key] = callback, pydata

	def unbind_event(self, event, key):
		del self._bindings.events[event][key]

	def bind_blit(self, key, callback):
		self._bindings.blits[key] = callback

	def unbind_blit(self, key):
		del self._bindings.blits[key]

	def get_position(self):
		return Scene.screen.rect.topleft

	def get_size(self):
		return Scene.screen.rect.size

	def get_rect(self):
		return Scene.screen.rect.copy()

	def get_center(self):
		return Scene.screen.rect.center

	def get_centerx(self):
		return Scene.screen.rect.centerx

	def get_centery(self):
		return Scene.screen.rect.centery

	def add_scene(self, scene, name=None):
		Scene.screen.add_scene(scene, name)

	def close_screen(self):
		Scene.screen.running = False

	def set_scene(self, scene):
		Scene.screen.set_scene = scene

	def del_scene(self, scene):
		del Scene.screen.scenes[scene]

	def add_scenery(self, scenery, scenery_name=None):
		if scenery_name is None:
			scenery_name = type(scenery).__name__
		self._bindings.scenery[scenery_name] = scenery

	def show_scenery(self, scenery_name, show=True):
		self._bindings.scenery[scenery_name].show = show

	def del_scenery(self, scenery_name):
		del self._bindings.scenery[scenery_name]

# under construction
class Scenery(Scene):
	def __init__(self, position, size, show, allow_event):
		Scene.__init__(self)
		self._screen_rect = pygame.Rect(*position, *size)
		self._surface = pygame.Surface(size)
		self._rect = pygame.Rect(0, 0, *size)
		self._hover = False
		self.allow_event = allow_event
		self.show = show

	def screen_event(self, event):
		if event.type == pygame.MOUSEMOTION:
			self._hover = self._screen_rect.collidepoint(event.pos)

		if self._hover:
			self.event(event)
			if self._bindings.events.get(event.type, None):
				for key, (callback, pydata) in self._bindings.events[event.type].items():
					callback(event, key, pydata)

	def screen_blit(self, surface, update=True):
		if update:
			self.screen_update()

		self.blit(self._surface)
		for callback in self._bindings.blits.values():
			callback(self._surface, self._screen_rect.topleft)

		surface.blit(self._surface, self._screen_rect)

	def get_position(self):
		return self._screen_rect.topleft

	def get_size(self, screen=False):
		if screen:
			return self._screen_rect.size
		return self._rect.size

	def get_rect(self, screen=False):
		if screen:
			return self._screen_rect.copy()
		return self._rect.copy()

	def get_center(self, screen=False):
		if screen:
			return self._screen_rect.center
		return self._rect.center

	def get_centerx(self, screen=False):
		if screen:
			return self._screen_rect.centerx
		return self._rect.centerx

	def get_centery(self, screen=False):
		if screen:
			return self._screen_rect.centery
		return self._rect.centery
