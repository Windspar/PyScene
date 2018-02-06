import pygame
from pyscene_importer import pyscene
from pyscene.objects import Button, Text
from pyscene import Screen, Scene
from pyscene import gradient
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene
from builtin_color_scene import ColorBuiltin
from text_scenes import GroupExample, TextEffects

class Intro(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        caption = 'PyScene'
        text_grid = Grid(self._rect.inflate(-10,-10), (16, 15), (3,3))
        grid = Grid(self._rect.inflate(-10,-10), (17, 15), (3,3))
        color_surface = gradient.by_letter(self.font.super, caption, ('dodgerblue', 'dodgerblue', 'snow'))
        Text(self, caption, text_grid.position(8, 1), self.font.super, color_surface,
            reflection = (1, 'down', (45, 'down')),
            anchor = Anchor.CENTER
        )

        Button(self, 'Text Group', grid.align(1, 5, 3, 1), None,
            (self.push_button, 'GroupExample'))
        Button(self, 'Text Effects', grid.align(1, 6, 3, 1), None,
            (self.push_button, 'TextEffects'))

        Button(self, 'Pygame Builtin Color', grid.align(6, 5, 5, 1), 'steelblue',
            (self.push_button, "ColorBuiltin"))

    def push_button(self, button, data):
        self.set_scene(data)

    def blit(self, surface):
        surface.fill((0,0,40))

if __name__ == '__main__':
    Screen.center()
    Screen.open('Introduction', (800, 600))
    # quick fonts
    Scene.font.basic = pygame.font.Font(None, 24)
    Scene.font.large = pygame.font.Font(None, 36)
    Scene.font.big = pygame.font.Font(None, 48)
    Scene.font.super = pygame.font.Font(None, 72)
    # add scenes
    Screen.add_scene(Intro)
    Screen.add_scene(ColorBuiltin)
    Screen.add_scene(GroupExample)
    Screen.add_scene(TextEffects)
    # start loop and active first scene
    Screen.loop('Intro', 30)
