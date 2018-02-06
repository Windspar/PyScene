import os
import pygame
from random import choice, shuffle
from pyscene_importer import pyscene
from pyscene import Scene, gradient
from pyscene.objects import Button, Text
from pyscene.objects.styles import BoxStyle
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene

class Puzzle(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'Puzzle', grid.position(8,1), self.font.large, 'mediumorchid1',
            anchor=Anchor.CENTER)

        # image artist
        Text(self, 'artwork by Kenny', grid.position(4,14), self.font.basic, 'mediumorchid1',
            anchor=Anchor.CENTER)
        Text(self, 'www.kenney.nl', grid.position(12,14), self.font.basic, 'mediumorchid1',
            anchor=Anchor.CENTER)

        box = Grid(self._rect.inflate(-10,-10), (19, 17), (2,2))
        Button(self, 'Back', box.align(0,0,3,1), 'mediumorchid1', self.push_back)
        Button(self, 'New Game', box.align(0,1,3,1), 'mediumorchid1', self.push_newgame)

        self.grab_images()
        width = 288
        height = 288
        gx = (self._rect.w - width) / 2
        gy = (self._rect.h - height) / 2
        self.board_grid = Grid((gx, gy, width, height), (4,4), (1,1))
        self.board = []
        self.board_rect = []
        for j in range(4):
            for i in range(4):
                rect = self.board_grid.rect(i,j)
                clip_rect = rect.copy()
                clip_rect.x -= i * 2 + self.board_grid._rect.x + 1
                clip_rect.y -= j * 2 + self.board_grid._rect.y + 1
                self.board.append(clip_rect)
                self.board_rect.append(rect)

        self.board[-1] = None
        self.push_newgame(None, None)

    def grab_images(self):
        filepath = os.path.join('images', 'PNG')
        self.images_file = []
        items = os.listdir(filepath)
        for item in items:
            if item.endswith('.png'):
                filename = os.path.join(filepath, item)
                self.images_file.append(filename)

    def load_image(self):
        filename = choice(self.images_file)
        self.image = pygame.image.load(filename)
        self.image = self.image.convert_alpha()
        self.shadow_image = pygame.transform.scale(self.image, (60,60))
        self.image = pygame.transform.scale(self.image, self.board_grid.get_size())

    def push_newgame(self, button, pydata):
        self.load_image()
        shuffle(self.board)

    def push_back(self, button, pydata):
        self.set_scene('SimpleGames')

    def blit(self, surface):
        surface.fill((40,0,40))
        surface.blit(self.shadow_image, self.board_grid.rect(5,1))
        for clip_rect, rect in zip(self.board, self.board_rect):
            if clip_rect:
                surface.blit(self.image.subsurface(clip_rect), rect)

    def event(self, event):
        QuitScene.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = self.board_grid.location(*event.pos)
                if x is None or y is None:
                    return

                if 0 <= x < 4 and 0 <= y < 4:
                    pos = y * 4 + x
                    if self.board[pos] is None:
                        return

                    def setboard(npos):
                        if self.board[npos] is None:
                            self.board[npos] = self.board[pos]
                            self.board[pos] = None

                    if pos + 4 < 16:
                        setboard(pos + 4)
                    if pos - 4 >= 0:
                        setboard(pos - 4)
                    if pos % 4 + 1 < 4:
                        setboard(pos + 1)
                    if pos % 4 - 1 >= 0:
                        setboard(pos - 1)
