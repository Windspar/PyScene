import pygame
from pyscene_importer import pyscene
from pyscene import Screen, Scene, gradient
from pyscene.objects import Text
from pyscene.layout import Anchor, Grid
from quit_scene import QuitScene
from tictactoe import TicTacToe
from mastermind import MasterMind
from floodit import FloodIt
from memory import Memory
from puzzle import Puzzle

class SimpleGames(QuitScene):
    def __init__(self):
        QuitScene.__init__(self)
        grid = Grid(self._rect, (16,15), (3,3))
        Text(self, 'Simple Games', grid.position(8,1), self.font.large, 'dodgerblue',
            anchor=Anchor.CENTER)

        Text(self, 'TicTacToe', grid.position(8,4), self.font.large, 'wheat4',
            callback = (self.push_game, 'TicTacToe'),
            hilight = 'burlywood',
            anchor = Anchor.CENTER)

        Text(self, 'MasterMind', grid.position(8,5), self.font.large, 'wheat4',
            callback = (self.push_game, 'MasterMind'),
            hilight = 'burlywood',
            anchor = Anchor.CENTER)

        Text(self, 'FloodIt', grid.position(8,6), self.font.large, 'wheat4',
            callback = (self.push_game, 'FloodIt'),
            hilight = 'burlywood',
            anchor = Anchor.CENTER)

        Text(self, 'Memory', grid.position(8,7), self.font.large, 'wheat4',
            callback = (self.push_game, 'Memory'),
            hilight = 'burlywood',
            anchor = Anchor.CENTER)

        Text(self, 'Puzzle', grid.position(8,8), self.font.large, 'wheat4',
            callback = (self.push_game, 'Puzzle'),
            hilight = 'burlywood',
            anchor = Anchor.CENTER)

    def push_game(self, button, data):
        if data:
            self.set_scene(data)

    def blit(self, surface):
        surface.fill((0,0,0))

def main():
    Screen.center()
    Screen.open("Simple Games", (800, 600))

    Scene.font.basic = pygame.font.Font(None, 24)
    Scene.font.large = pygame.font.Font(None, 36)

    Screen.add_scene(SimpleGames)
    Screen.add_scene(TicTacToe)
    Screen.add_scene(MasterMind)
    Screen.add_scene(FloodIt)
    Screen.add_scene(Memory)
    Screen.add_scene(Puzzle)
    Screen.loop('SimpleGames', 30)

if __name__ == '__main__':
    main()
