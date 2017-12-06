import pygame
from PyScene import scene
from PyScene.widgets import Button, Text, Textbox
from random import choice

class Quit:
    def event(self, event):
        if event.type == pygame.QUIT:
            scene.Screen.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                scene.Screen.running = False

class Intro(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        Text(self, 'Welcome To Simple Games', mid, 20, scene.Font.basic, 'blue')
        text = Text(self, 'TicTacToe', mid, 200, scene.Font.basic, 'wheat4')
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('TicTacToe', TicTacToe))
        text = Text(self, 'MasterMind', mid, 250, scene.Font.basic, 'wheat4')
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('MasterMind', MasterMind))
        text = Text(self, 'FloodIt', mid, 300, scene.Font.basic, 'wheat4')
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('FloodIt', FloodIt))
        self.last_scene = None

    def entrance(self):
        if self.last_scene:
            del scene.Screen.scenes[self.last_scene]

    def start_game(self, text, pydata):
        self.last_scene = pydata[0]
        scene.Screen.scenes[pydata[0]] = pydata[1]()
        scene.Screen.set_scene = pydata[0]

    def blit(self, surface):
        surface.fill((0,0,30))

class TicTacToe(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        Text(self, 'TicTacToe', mid, 20, scene.Font.basic, 'blue')
        button = Button(self, 'Back', (10,10,100,30), self.push_back)
        self.board = ['','','' ,'','','' ,'','','']
        self.buttons = []
        for i in range(9):
            x = int((i % 3) * 55 + scene.Screen.size[0] / 2 - (55 + 55 / 2))
            y = int(i / 3) * 55 + 200
            self.buttons.append(Button(self, '', (x, y, 50, 50), self.push, i))

        self.wins_text = Text(self, 'Wins: 0', 100, 100, scene.Font.basic, 'green')
        self.cats_text = Text(self, 'Cats: 0', mid, 100, scene.Font.basic, 'blue')
        x = scene.Screen.size[0] - 150
        self.lost_text = Text(self, 'Lost: 0', x, 100, scene.Font.basic, 'red')
        self.count = 0
        self.win = 0
        self.lost = 0
        self.cats = 0
        self.win_pattern = ((0,1,2), (3,4,5), (6,7,8), # across
                            (0,3,6), (1,4,7), (2,5,8), # down
                            (0,4,8), (2,4,6))

        self.ai_pattern  = {0:((1,2), (3,6), (4,8)), 1:((1,2), (4,7)),
                            2:((0,1), (5,8), (4,6)), 3:((0,6), (4,5)),
                            4:((1,7), (3,5), (0,8), (2,6)), 5:((2,8), (3,4)),
                            6:((0,3), (4,2), (7,8)), 7:((1,4), (6,8)),
                            8:((6,7),(0,4),(2,5)) }

    def push(self, button, pydata):
        if self.board[pydata] == '':
            self.board[pydata] = 'x'
            button.text.set_text('X')
            if self.check_win('x'):
                self.win += 1
                self.wins_text.set_text('Wins: ' + str(self.win))
                self.reset()
            elif self.count == 9:
                self.cats += 1
                self.cats_text.set_text('Cats: ' + str(self.cats))
                self.reset()
            self.computer()
            if self.check_win('o'):
                self.lost += 1
                self.lost_text.set_text('Lost: ' + str(self.lost))
                self.reset()
            elif self.count == 9:
                self.cats += 1
                self.cats_text.set_text('Cats: ' + str(self.cats))
                self.reset()

    def computer(self):
        plays = {}
        can_win = None
        #better = [1, 3, 4, 5, 7]
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
        self.buttons[place].text.set_text('O')

    def check_win(self, letter):
        self.count += 1
        b = self.board
        for x,y,z in self.win_pattern:
            if b[x] == b[y] == b[z] == letter:
                return True
        return False

    def reset(self):
        self.count = 0
        self.board = ['','','' ,'','','' ,'','','']
        for button in self.buttons:
            button.text.set_text("")

    def push_back(self, button, pydata):
        scene.Screen.set_scene = 'Intro'

    def blit(self, surface):
        surface.fill((0,0,40))

class Slot:
    def __init__(self, rect, color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.color = color

class MasterMind(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        Text(self, 'MasterMind', mid, 20, scene.Font.basic, 'green')
        Button(self, 'Check', (mid - 50, 475, 100, 32), self.check, None, 'green')
        Button(self, 'Back', (10, 10, 100, 30), self.push_back, None, 'orange')
        Button(self, 'New Game', (10, 50, 100, 30), self.push_newgame, None, 'green')
        self.colors = ('yellow', 'red', 'blue', 'white', 'wheat4', 'orange', 'green', 'purple')
        self.colors = tuple(map(pygame.Color, self.colors))
        self.picker = [pygame.Rect(150, i * 30 + 180, 40, 20) for i in range(8)]
        self.outcome = Text(self, "", mid, 550, scene.Font.basic, 'green')
        self.push_newgame(None, None)

    def push_back(self, button, pydata):
        scene.Screen.set_scene = 'Intro'

    def push_newgame(self, button, pydata):
        self.board = []
        for j in range(10):
            self.board.append([])
            for i in range(4):
                self.board[j].append(Slot((i * 50 + 305, (9 - j) * 30 + 150, 40, 20)))
        self.check_blocks = []

        self.code = [choice(self.colors) for i in range(4)]
        self.current_row = 0
        self.current_pos = 0
        self.outcome.set_text("")

    def check(self, button, pydata):
        if self.current_row > 9:
            return

        blocks = []
        colorcode = self.code[:]
        colors = [item.color for item in self.board[self.current_row]]
        for enum, slot in enumerate(self.board[self.current_row]):
            if slot.color == (0,0,0):
                return
            elif slot.color == self.code[enum]:
                blocks.append('green')
                colors.remove(slot.color)
                colorcode.remove(slot.color)

        for color in colors:
            if color in colorcode:
                colorcode.remove(color)
                blocks.append('white')

        blocks.sort()
        while len(blocks) < 4:
            blocks.append('black')
        data = []
        for enum, color in enumerate(blocks):
            y = (9 - self.current_row) * 30 + 160
            data.append(Slot((enum * 15 + 505, y, 10,10), pygame.Color(color)))

        self.check_blocks.append(data)
        self.current_row += 1
        self.current_pos = 0

        if blocks == ['green','green','green','green']:
            self.current_row = 10
            self.outcome.set_text('Winner')
            self.outcome.set_color('green')
        elif self.current_row > 9:
            self.outcome.set_text('You Lose ! Please Try Again.')
            self.outcome.set_color('red')

    def blit(self, surface):
        surface.fill((0,40,0))
        for color, rect in zip(self.colors, self.picker):
            surface.fill(color, rect)

        for row in self.board:
            for slot in row:
                surface.fill(slot.color, slot.rect)

        for row in self.check_blocks:
            for slot in row:
                surface.fill(slot.color, slot.rect)

        if self.current_row > 9:
            for enum, color in enumerate(self.code):
                rect = pygame.Rect(enum * 50 + 305, 100, 40, 20)
                surface.fill(color, rect)

    def event(self, event):
        Quit.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_row < 10:
                if event.button == 1 and self.current_pos < 4:
                    for enum, rect in enumerate(self.picker):
                        if rect.collidepoint(event.pos):
                            self.board[self.current_row][self.current_pos].color = self.colors[enum]
                            self.current_pos += 1
                if event.button == 3 and self.current_pos > 0:
                    self.current_pos -= 1
                    self.board[self.current_row][self.current_pos].color = (0,0,0)

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

class FloodIt(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        Text(self, 'FloodIt', mid, 20, scene.Font.basic, 'dodgerblue')
        Button(self, 'Back', (10,10,100,30), self.push_back, None, 'dodgerblue')
        Button(self, 'New Game', (10,50,100,30), self.push_newgame, None, 'dodgerblue')
        self.colors = tuple(map(pygame.Color,
            ['dodgerblue', 'gold', 'firebrick1', 'darkslateblue',
             'forestgreen', 'darkorange', 'mediumorchid'] ))

        self.turn_text = Text(self, 'Turn: 0', mid, 560, scene.Font.basic, 'wheat4')
        self.push_newgame(None, None)

    def push_back(self, button, pydata):
        scene.Screen.set_scene = 'Intro'

    def push_newgame(self, button, pydata):
        self.board = []
        for j in range(14):
            self.board.append([])
            for i in range(14):
                self.board[j].append(Dot(self.colors, (i * 30 + 190, j * 30 + 100 , 29,29), (j,i)))

        self.board[0][0].choosen = True
        self.board[0][0].disturbance(self.board, self.board[0][0].color)
        for item in self.board:
            for dot in item:
                dot.ignore_me = False

        self.count = 0
        self.turn_text.set_text("Turn: 0")

    def blit(self, surface):
        surface.fill((0,0,40))

        for row in self.board:
            for dot in row:
                surface.fill(dot.color, dot.rect)

    def event(self, event):
        Quit.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                if 190 <= mx < 610 and 100 < my < 520:
                    x = int((mx - 190) / 30)
                    y = int((my - 100) / 30)
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

def main():
    scene.Screen.center()
    scene.Screen.init('Simple Games', (800, 600))
    scene.Font.basic = pygame.font.Font(None, 36)

    scene.Screen.scenes['Intro'] = Intro()

    scene.Screen.loop('Intro', 30)
    pygame.quit()

if __name__ == '__main__':
    main()
