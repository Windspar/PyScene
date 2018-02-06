import pygame
from pyscene_importer import pyscene
from pyscene.objects import Button, Text
from pyscene import Screen, Scene
from pyscene import gradient
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene

class GroupExample(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect.inflate(-10,-10), (16, 15), (3,3))
        Text(self, 'Text Group Example', grid.position(8,1), self.font.basic,
            'orange', anchor=Anchor.CENTER)
        self.back = Button(self, 'Back', grid.align(0,0,2,1), 'orange', self.back_push)
        text_args = (self.font.basic, 'wheat4', None, 'me_group')
        text_kargs = {'anchor':Anchor.CENTER, 'hilight':'burlywood', 'toggle':'wheat'}
        self.texts = [
            Text(self, 'Me First', grid.position(8,4), *text_args, **text_kargs),
            Text(self, 'Pick Me', grid.position(8,5), *text_args, **text_kargs),
            Text(self, 'Click Me', grid.position(8,6), *text_args, **text_kargs)
        ]

    def blit(self, surface):
        surface.fill((30,30,30))

    def back_push(self, button, pydata):
        self.set_scene("Intro")

    # when you enter the scene
    def entrance(self, *args):
        self.texts[0].set_focus()

class TextEffects(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect.inflate(-10,-10), (16, 15), (3,3))
        self.back = Button(self, 'Back', grid.align(0,0,2,1), 'darkolivegreen3', self.back_push)
        Text(self, 'Text Effects', grid.position(8,1), self.font.big,
            'darkolivegreen3', anchor=Anchor.CENTER)

        Text(self, 'Shifted Text', grid.position(1,4), self.font.large, 'darkolivegreen4',
            shift=(45, 'top'))

        Text(self, 'Fading Text', grid.position(1,5), self.font.large, 'darkolivegreen4',
            fade='right')

        Text(self, 'Reflection Text', grid.position(8,3), self.font.large, 'darkolivegreen4',
            reflection=(1, 'down'), anchor=Anchor.CENTER)

        Text(self, 'Shadow Trail Text', grid.position(11,4), self.font.large, 'darkolivegreen4',
            shadow=('darkolivegreen', (5,5), True))

        Text(self, 'Shadow Text', grid.position(12,5), self.font.large, 'darkolivegreen4',
            shadow=('darkolivegreen', (3,3)))

        Text(self, 'Blinking Text', grid.position(8,6), self.font.large, 'darkolivegreen4',
            blink=((30,30,30), 1500, 700), anchor=Anchor.CENTER)

        self.type_text = Text(self, 'TypeWriter Text', grid.position(8,8), self.font.large,
            'darkolivegreen4', typewriter=(333, self.writer_finish), anchor=Anchor.CENTER)

        self.timer.add('TypeWriter', 2000, self.timer_retype)
        self.timer.stop('TypeWriter')

    def writer_finish(self, writer, data):
        self.timer.start('TypeWriter')

    def timer_retype(self, timer):
        self.timer.stop('TypeWriter')
        self.type_text.effect('typewriter').reset()

    def blit(self, surface):
        surface.fill((30,30,30))

    def back_push(self, button, pydata):
        self.set_scene("Intro")
