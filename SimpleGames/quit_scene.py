import pygame
from pyscene_importer import pyscene
from pyscene import Scenery, Scene
from pyscene.objects import Button, Text
from pyscene.layout import Anchor, Grid

class QuitScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.add_scenery(QuitScenery(self), 'Quit')

    def event(self, event):
        if event.type == pygame.QUIT:
            self.show_scenery('Quit')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_scenery('Quit')

class QuitScenery(Scenery):
    def __init__(self, parent):
        # init Scenery through init_center method
        Scenery.init_center(self, parent, (170, 80), False, False)
        grid = Grid(self._rect, (6, 8), (10, 5))
        Text(self, 'Confirm Quit', grid.position(3,1), self.font.basic, 'gray60',
            anchor = Anchor.MID_TOP
        )
        Button(self, 'Yes', grid.align(0,4,3,4,(2,4)), 'red', (self.push_confirm, True))
        Button(self, 'No', grid.align(3,4,3,4,(2,4)), 'green', (self.push_confirm, False))

        self.position = grid.position(2,0)
        self.image = self.font.basic.render('Test', 1, (0,200,0))

    def push_confirm(self, button, pydata):
        if pydata:
            self.close_screen()
        else:
            self.show = False

    def blit(self, surface):
        surface.fill(pygame.Color('gray20'))
        pygame.draw.rect(surface, pygame.Color('gray40'), self._rect.inflate(-4,-4), 1)
        pygame.draw.rect(surface, pygame.Color('gray30'), self._rect.inflate(-8,-8), 1)
