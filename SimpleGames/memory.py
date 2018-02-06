import os
import pygame
from random import choice
from pyscene_importer import pyscene
from pyscene import Scene, gradient
from pyscene.objects import Button, Text
from pyscene.objects.styles import BoxStyle
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene

class Card:
    images = []
    color = pygame.Color('snow')

    @classmethod
    def load_images(cls):
        filepath = os.path.join('images', 'PNG')
        cls.images = []
        items = os.listdir(filepath)
        for item in items:
            if item.endswith('.png'):
                filename = os.path.join(filepath, item)
                image = pygame.image.load(filename)
                image = image.convert_alpha()
                image = pygame.transform.scale(image, (50,50))
                cls.images.append(image)

    def __init__(self, rect, item):
        self.item = item
        self.rect = pygame.Rect(rect)
        self.show = False

    def blit(self, surface):
        if self.show:
            image = Card.images[self.item]
            rect = image.get_rect()
            rect.center = self.rect.center
            surface.blit(image, rect)
        else:
            surface.fill(Card.color, self.rect)

class Memory(QuitScene):
    def __init__(self):
        Card.load_images()
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'Memory', grid.position(8,1), self.font.large, 'orange',
            anchor=Anchor.CENTER)

        self.move_text = Text(self, 'Moves: 0', grid.position(8, 3), self.font.basic,
            'orange', anchor=Anchor.CENTER)

        # image artist
        Text(self, 'artwork by Kenny', grid.position(4,14), self.font.basic, 'orange',
            anchor=Anchor.CENTER)
        Text(self, 'www.kenney.nl', grid.position(12,14), self.font.basic, 'orange',
            anchor=Anchor.CENTER)

        box = Grid(self._rect.inflate(-10,-10), (19, 17), (2,2))
        Button(self, 'Back', box.align(0,0,3,1), 'orange', callback=self.push_back)
        Button(self, 'New Game', box.align(0,1,3,1), 'orange', callback=self.push_newgame)

        gx = (self._rect.w - 700) / 2
        gy = (self._rect.h - 360) / 2 + 30
        self.grid = Grid((gx,gy,700,360), (10,6), (5,5))
        self.push_newgame(None, None)

    def push_newgame(self, button, data):
        self.cards = []
        self.move_text.set_text('Moves: 0')
        objects = list(range(30)) + list(range(30))
        for across in range(10):
            self.cards.append([])
            for down in range(6):
                pick = choice(objects)
                objects.remove(pick)
                self.cards[across].append(Card(self.grid.rect(across,down),pick))

        self.last_pick = []
        self.move_count = 0

    def push_back(self, button, data):
        self.set_scene('SimpleGames')

    def blit(self, surface):
        surface.fill((30,30,30))
        for item in self.cards:
            for card in item:
                card.blit(surface)

    def event(self, event):
        QuitScene.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = self.grid.location(*event.pos)
                if x == None or y == None:
                    return

                if 0 <= x < 10 and 0 <= y < 6:
                    if self.cards[x][y].show == True:
                        return

                    self.cards[x][y].show = True
                    if len(self.last_pick) == 0:
                        self.last_pick = [(x, y)]
                    elif len(self.last_pick) == 1:
                        cx, cy = self.last_pick[0]
                        if self.cards[x][y].item == self.cards[cx][cy].item:
                            self.last_pick = []
                        else:
                            self.last_pick.append((x,y))
                            self.move_count += 1
                            self.move_text.set_text('Moves: {0}'.format(self.move_count))
                    else:
                        for cx,cy in self.last_pick:
                            self.cards[cx][cy].show = False
                        self.last_pick = [(x, y)]
