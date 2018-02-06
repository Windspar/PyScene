import pygame
from pyscene_importer import pyscene
from pyscene import Scene, gradient
from pyscene.objects import Button, Text
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene
from random import choice

class Dot:
    def __init__(self, colors, rect, pos):
        self.color = choice(colors)
        self.rect = pygame.Rect(rect)
        self.choosen = False
        self.ignore_me = False
        self.pos = pos

    def disturbance(self, board, color, match=0):
        if self.ignore_me:
            return 0

        x, y = self.pos
        self.ignore_me = True
        def domove(mx, my, board, color):
            if board[x + mx][y + my].choosen:
                return board[x + mx][y + my].disturbance(board, color, 0)
            elif board[x + mx][y + my].color == color:
                board[x + mx][y + my].choosen = True
                return board[x + mx][y + my].disturbance(board, color, 1)
            return 0

        if x > 0:
            match += domove(-1,0, board, color)
        if x < 13:
            match += domove(1,0, board, color)
        if y > 0:
            match += domove(0,-1, board, color)
        if y < 13:
            match += domove(0,1, board, color)

        return match

class FloodIt(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'FloodIt', grid.position(8,1), self.font.large, 'royalblue',
            anchor=Anchor.CENTER)

        self.turn_text = Text(self, 'Turn: 0', grid.position(8,14), self.font.basic,
            'wheat4', anchor=Anchor.CENTER)

        box = Grid(self._rect.inflate(-10,-10), (19, 17), (2,2))
        Button(self, 'Back', box.align(0,0,3,1), 'royalblue', self.push_back)
        Button(self, 'New Game', box.align(0,1,3,1), 'royalblue', self.push_newgame)

        self.colors = tuple(map(pygame.Color,
            ['dodgerblue', 'gold', 'firebrick1', 'darkslateblue',
             'forestgreen', 'darkorange', 'mediumorchid'] ))

        self.board_grid = Grid((190,100,420,420), (14,14), (1,1))
        self.push_newgame(None, None)

    def push_newgame(self, button, data):
        self.board = []
        for j in range(14):
            self.board.append([])
            for i in range(14):
                self.board[j].append(Dot(self.colors, self.board_grid.rect(i,j), (j,i)))

        self.board[0][0].choosen = True
        self.board[0][0].disturbance(self.board, self.board[0][0].color)
        for item in self.board:
            for dot in item:
                dot.ignore_me = False

        self.count = 0
        self.turn_text.set_text("Turn: 0")

    def push_back(self, button, data):
        self.set_scene('SimpleGames')

    def blit(self, surface):
        surface.fill((10,10,20))

        for row in self.board:
            for dot in row:
                surface.fill(dot.color, dot.rect)

    def event(self, event):
        QuitScene.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = self.board_grid.location(*event.pos)
                if x is None or y is None:
                    return

                if 0 <= x < 14 and 0 <= y < 14:
                    color = self.board[y][x].color
                    match = self.board[0][0].disturbance(self.board, color)
                    if match > 0:
                        self.count += 1
                        self.turn_text.set_text('Turn: ' + str(self.count))
                        for item in self.board:
                            for dot in item:
                                dot.ignore_me = False
                                if dot.choosen:
                                    dot.color = color
                    else:
                        for item in self.board:
                            for dot in item:
                                dot.ignore_me = False
