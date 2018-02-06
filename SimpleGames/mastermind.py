import pygame
from random import choice
from pyscene_importer import pyscene
from pyscene import Scene, gradient
from pyscene.objects import Button, Text
from pyscene.objects.styles import BoxStyle
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene

class Slot:
    def __init__(self, rect, color=(0,0,0)):
        self.rect = rect
        self.color = color

class MasterMind(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'MasterMind', grid.position(8,1), self.font.large, 'forestgreen',
            anchor=Anchor.CENTER)

        self.outcome = Text(self, "", grid.position(8,12), self.font.basic, 'forestgreen',
            anchor=Anchor.CENTER)

        box = Grid(self._rect.inflate(-10,-10), (19, 17), (2,2))
        Button(self, 'Check', box.align(2,9,4,1,(28,0)), 'forestgreen', self.push_check)
        Button(self, 'Back', box.align(0,0,3,1), 'forestgreen', self.push_back)
        Button(self, 'New Game', box.align(0,1,3,1), 'forestgreen', self.push_newgame)


        self.colors = ('gold', 'darkred', 'royalblue', 'honeydew2',
            'wheat4', 'orange', 'green3', 'purple')
        self.colors = tuple(map(pygame.Color, self.colors))
        grid = Grid((124, 208, 96, 92), (2, 4), (4,3))
        self.color_picker = []
        for j in range(4):
            self.color_picker.append([])
            for i in range(2):
                self.color_picker[j].append(Slot(grid.rect(i,j), self.colors[i * 4 + j]))

        self.push_newgame(None, None)

    def push_newgame(self, button, data):
        grid = Grid((300, 150, 200, 260), (4, 10), (4,3))
        self.board = []
        for j in range(10):
            self.board.append([])
            for i in range(4):
                self.board[j].append(Slot(grid.rect(i, 9 - j)))

        self.code = [choice(self.colors) for i in range(4)]
        self.code_slots = []
        for i in range(4):
            self.code_slots.append(Slot(grid.rect(i, -2), self.code[i]))

        grid = Grid((530, 150, 70, 260), (4, 10), (3,8))
        self.check_blocks = []
        for j in range(10):
            self.check_blocks.append([])
            for i in range(4):
                self.check_blocks[j].append(Slot(grid.rect(i, 9 - j)))

        self.current_row = 0
        self.current_pos = 0
        self.outcome.set_text("")

    def push_check(self, button, data):
        if self.current_row > 9:
            return

        blocks = []
        colorcode = self.code[:]
        colors = [item.color for item in self.board[self.current_row]]
        for enum, slot in enumerate(self.board[self.current_row]):
            if slot.color == (0,0,0):
                return
            elif slot.color == self.code[enum]:
                blocks.append('green3')
                colors.remove(slot.color)
                colorcode.remove(slot.color)

        for color in colors:
            if color in colorcode:
                colorcode.remove(color)
                blocks.append('honeydew2')

        blocks.sort()
        data = []
        for enum, color in enumerate(blocks):
            self.check_blocks[self.current_row][enum].color = pygame.Color(color)

        self.current_row += 1
        self.current_pos = 0

        if blocks == ['green3','green3','green3','green3']:
            self.current_row = 10
            self.outcome.set_text('Winner!')
            self.outcome.set_color('green')
        elif self.current_row > 9:
            pass
            self.outcome.set_text('You Lose ! Please Try Again.')
            self.outcome.set_color('red')

    def push_back(self, button, data):
        self.set_scene('SimpleGames')

    def blit(self, surface):
        surface.fill((0,40,0))
        for row in self.board:
            for item in row:
                surface.fill(item.color, item.rect)

        if self.current_row > 0:
            for row in self.check_blocks[:self.current_row]:
                for item in row:
                    surface.fill(item.color, item.rect)

        for row in self.color_picker:
            for item in row:
                surface.fill(item.color, item.rect)

        if self.current_row > 9:
            for item in self.code_slots:
                surface.fill(item.color, item.rect)

    def event(self, event):
        QuitScene.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_row < 10:
                if event.button == 1 and self.current_pos < 4:
                    for row in self.color_picker:
                        for item in row:
                            if item.rect.collidepoint(event.pos):
                                self.board[self.current_row][self.current_pos].color = item.color
                                self.current_pos += 1
                if event.button == 3 and self.current_pos > 0:
                    self.current_pos -= 1
                    self.board[self.current_row][self.current_pos].color = (0,0,0)
