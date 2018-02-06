import pygame
from ... import twist
from ... import gradient

class BaseEffect:
    def __init__(self, parent, color, alpha):
        self.parent = parent
        self.alpha = alpha
        self.image = None
        self.rotation_image = None
        self.rotation_rect = None
        self.clip_rect = None
        self.set_color(color)
        self.render()

    def set_color(self, color):
        self.color = twist.color(color)

    def do_effects(self, image, effects=None):
        if not effects:
            effects = self.parent._effects

        if effects['fade']:
            twist.fade(image, effects['fade'])

        if effects['shift']:
            self.image = twist.shift(image, *effects['shift'])

        if effects['angle']:
            angle_image = pygame.transform.rotate(image, effects['angle'])
            self.rotation_rect = angle_image.get_rect()
            self.rotation_rect.topleft = self.parent._rect.topleft
            self.build_rotation_image(None, True)

    def do_rect(self):
        self.parent._rect = self.image.get_rect()
        self.parent._anchor_position()

    def render(self, allow_effects=True):
        if isinstance(self.color, pygame.Surface):
            surface = self.parent._font.render(self.parent._text, 1, (255,255,255))
        else:
            surface = self.parent._font.render(self.parent._text, 1, self.color)

        if isinstance(self.color, pygame.Surface):
            self.image = gradient.apply_surface(surface, self.color)
            if self.alpha:
                twist.ghost(self.image, self.alpha)
        else:
            self.image = surface
            if self.alpha:
                twist.ghost(self.image, self.alpha)

        if allow_effects:
            self.do_effects(self.image)

    def build_rotation_image(self, clip_rect, force=False):
        if self.clip_rect != clip_rect or force:
            self.clip_rect = clip_rect
            if clip_rect:
                image_clip = self.image.subsurface(clip_rect)
            else:
                image_clip = self.image

            self.rotation_image = pygame.transform.rotate(image_clip, self.parent._effects['angle'])

    def blit(self, surface, clip_rect=None):
        if self.rotation_image:
            self.build_rotation_image(clip_rect)
            surface.blit(self.rotation_image, self.rotation_rect, clip_rect)
        else:
            surface.blit(self.image, self.parent._rect, clip_rect)
