import pygame
from random import choice
from pyscene_importer import pyscene
from pyscene import Scene, gradient
from pyscene.objects import Button, Text
from pyscene.objects.styles import BoxStyle
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene

class TicTacToe(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'TicTacToe', grid.position(8,1), self.font.large, 'dodgerblue',
            anchor=Anchor.CENTER)

        self.wins_text = Text(self, 'Wins: 0', grid.position(2,3), self.font.basic,
            'forestgreen', anchor=Anchor.CENTER)

        self.cats_text = Text(self, 'Cats: 0', grid.position(8,3), self.font.basic,
            'dodgerblue', anchor=Anchor.CENTER)

        self.lost_text = Text(self, 'Lost: 0',  grid.position(13,3), self.font.basic,
            'firebrick', anchor=Anchor.CENTER)

        self.winner_text = Text(self, '',  grid.position(8,12), self.font.basic,
            'dodgerblue', anchor=Anchor.CENTER)

        box = Grid(self._rect.inflate(-10,-10), (19, 17), (2,2))
        Button(self, 'Back', box.align(0,0,3,1), 'dodgerblue', callback=self.push_back)
        Button(self, 'New Game', box.align(0,1,3,1), 'dodgerblue', callback=self.push_newgame)

        self.x_style = BoxStyle('dodgerblue3', 'dodgerblue3')
        self.o_style = BoxStyle('firebrick1', 'firebrick1')
        self.box_style = BoxStyle('aquamarine4', 'aquamarine4')
        box = Grid(self._rect.inflate(-530,-330), (3,3), (3,3))
        self.buttons = []
        for y in range(3):
            for x in range(3):
                self.buttons.append(
                    Button(self, '', box.rect(x, y), self.box_style,
                        callback=(self.push_button, x + y * 3))
                )

        self.game_data()
        self.win_pattern = ((0,1,2), (3,4,5), (6,7,8), # across
                            (0,3,6), (1,4,7), (2,5,8), # down
                            (0,4,8), (2,4,6))

        self.ai_pattern  = {0:((1,2), (3,6), (4,8)), 1:((1,2), (4,7)),
                            2:((0,1), (5,8), (4,6)), 3:((0,6), (4,5)),
                            4:((1,7), (3,5), (0,8), (2,6)), 5:((2,8), (3,4)),
                            6:((0,3), (4,2), (7,8)), 7:((1,4), (6,8)),
                            8:((6,7),(0,4),(2,5)) }

    def push_newgame(self, button, data):
        self.winner_text.set_text(' ')
        if self.count < 9:
            self.lost += 1
            self.lost_text.set_text('Lost {0}'.format(self.lost))

        self.state = self.state_reset()

    def game_data(self):
        self.board = ['','','' ,'','','' ,'','','']
        self.count = 0
        self.win = 0
        self.lost = 0
        self.cats = 0
        self.state = None
        self.state_data = None

    def push_back(self, button, data):
        self.set_scene('SimpleGames')

    def push_button(self, button, data):
        if self.board[data] == '':
            self.state = self.state_human_play
            self.state_data = button, data
        #print(data)

    def state_human_play(self):
        button, data = self.state_data
        if self.board[data] == '':
            self.board[data] = 'x'
            #button.enable = False
            button.text.set_text('X')
            button.set_image(self.x_style)
            if self.check_win('x'):
                self.win += 1
                self.wins_text.set_text('Wins {0}'.format(self.win))
                self.count = 10
                self.state = None
                self.winner_text.set_text('Winner X')
            elif self.count == 9:
                self.cats += 1
                self.cats_text.set_text('Cats {0}'.format(self.cats))
                self.count = 10
                self.state = None
                self.winner_text.set_text('Cats Game')
            else:
                self.state = self.state_computer_play
                self.state_data = None

    def state_computer_play(self):
        self.computer()
        if self.check_win('o'):
            self.lost += 1
            self.lost_text.set_text('Lost {0}'.format(self.lost))
            self.count = 10
            self.state = None
            self.winner_text.set_text('Winner O')
        elif self.count == 9:
            self.cats += 1
            self.cats_text.set_text('Cats {0}'.format(self.cats))
            self.count = 10
            self.state = None
            self.winner_text.set_text('Cats Game')
        else:
            self.state = None

    def computer(self):
        plays = {}
        can_win = None
        for i in range(9):
            if self.board[i] == '':
                for x, y in self.ai_pattern[i]:
                    if self.board[x] == 'o' and self.board[y] == 'o':
                        can_win = i
                    plays[i] = plays.get(i, 0)
                    total = (self.board[x] == 'x') + (self.board[y] == 'x')
                    if total > plays[i]:
                        plays[i] = total

        if can_win is None:
            value = max(plays.values())
            keys = [k for k, v in plays.items() if v == value]
            place = choice(keys)
        else:
            place = can_win

        self.board[place] = 'o'
        #self.buttons[place].enable = False
        self.buttons[place].text.set_text('O')
        self.buttons[place].set_image(self.o_style)

    def check_win(self, letter):
        self.count += 1
        b = self.board
        for x,y,z in self.win_pattern:
            if b[x] == b[y] == b[z] == letter:
                return True
        return False

    def state_reset(self):
        #print('Reset')
        self.state = None
        self.state_data = None
        self.count = 0
        self.board = ['','','' ,'','','' ,'','','']
        for button in self.buttons:
            #button.enable = True
            button.set_image(self.box_style)
            button.text.set_text(' ')

    def blit(self, surface):
        surface.fill((0,0,30))
        if self.state:
            self.state()
