import pygame
from pyscene_importer import pyscene
from pyscene.objects import Button, Text
from pyscene import Screen, Scene
from pyscene import gradient
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene
from random import choice

class ColorBuiltin(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        self.page = 1
        text_grid = Grid(self._rect.inflate(-10,-10), (16, 15), (3,3))
        grid = Grid(self._rect.inflate(-10,-10), (17, 15), (3,3))

        self.keys = [key for key in list(pygame.color.THECOLORS.keys())
            if key[:4] not in ['gray', 'grey']]
        self.max_page = int(len(self.keys) / 60) + 1
        self.keys.sort()
        self.keys_group = []
        for x in range(5):
            for y in range(12):
                self.keys_group.append(
                    Text(self, "None", text_grid.position(2 + x * 3, 2 + y), self.font.basic,
                        anchor=Anchor.MID_TOP)
                )
        self.update_colors()

        title = 'Pygame Builtin Colors {0}'.format(self.page)
        color_option = self.keys[:]
        color_option.remove('black')
        colors = []
        for i in range(len(title)):
            color_choice = choice(color_option)
            colors.append(color_choice)
            color_option.remove(color_choice)

        color_surface = gradient.by_letter(self.font.large, title, colors, True)
        self.intro = Text(self, title, text_grid.position(8,1), self.font.large,
            color_surface, anchor=Anchor.CENTER)

        Button(self, 'Prev', grid.align(5,14,2,1), 'aliceblue', self.prev_page)
        Button(self, 'Next', grid.align(10,14,2,1), 'aliceblue', self.next_page)
        Button(self, 'Back', grid.align(0,0,2,1), 'aliceblue', self.push_back)

    def update_colors(self):
        self.rects = []
        keys = self.keys[60 * (self.page - 1): 60 * self.page]
        for enum, key in enumerate(keys):
            self.keys_group[enum].set_text(key)
            self.keys_group[enum].set_color(key)
            color =  pygame.Color(key)
            if color.r < 30 and color.g < 30 and color.b < 30:
                self.rects.append(self.keys_group[enum]._rect)

        if len(keys) < 60:
            for n in range(enum + 1, 60):
                self.keys_group[n].set_text(" ")

    def prev_page(self, button, pydata):
        if self.page > 1:
            self.page -= 1
            self.update_colors()
            self.intro.set_text('Pygame Builtin Colors {0}'.format(self.page))

    def next_page(self, button, pydata):
        if self.page < self.max_page:
            self.page += 1
            self.update_colors()
            self.intro.set_text('Pygame Builtin Colors {0}'.format(self.page))

    def push_back(self, button, pydata):
        self.set_scene("Intro")

    def blit(self, surface):
        surface.fill((0,0,0))
        for rect in self.rects:
            surface.fill(pygame.Color('grey15'), rect)
