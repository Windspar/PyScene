import pygame
from pyscene import Scene, Screen, Font
from pyscene import Button, Text, Textbox
from pyscene import Point, Vector, gradient
from random import choice, shuffle

class Quit:
    def event(self, event):
        if event.type == pygame.QUIT:
            Screen.set_scene = 'QuitScene'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Screen.set_scene = 'QuitScene'

class QuitScene(Scene):
    last_scene = None

    def __init__(self):
        Scene.__init__(self)
        midx, midy = self.get_center()
        Text(self, "Do you really want to leave ?", midx, midy - 50, self.font.basic, 'mediumorchid1').set_center()
        Button(self, 'Yes', (midx - 150, midy, 100, 30), self.push, True, 'red')
        Button(self, 'No', (midx + 50, midy, 100, 30), self.push, False, 'green')
        self.rect = pygame.Rect(midx - 175, midy - 80, 355, 120)

    def push(self, button, pydata):
        if pydata:
            self.close_screen()
        else:
            self.set_scene(QuitScene.last_scene)

    def blit(self, surface):
        if QuitScene.last_scene:
            Screen.scenes[QuitScene.last_scene].screen_blit(surface)
        else:
            surface.fill((40,0,0))

        surface.fill(pygame.Color('mediumorchid4'), self.rect)

class Intro(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'Welcome To Simple Games', mid, 20, Scene.font.basic, 'blue').set_center()
        text = Text(self, 'TicTacToe', mid, 200, Scene.font.basic, 'wheat4')
        text.set_center()
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('TicTacToe', TicTacToe))

        text = Text(self, 'MasterMind', mid, 250, Scene.font.basic, 'wheat4')
        text.set_center()
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('MasterMind', MasterMind))

        text = Text(self, 'FloodIt', mid, 300, Scene.font.basic, 'wheat4')
        text.set_center()
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('FloodIt', FloodIt))

        text = Text(self, 'Memory', mid, 350, Scene.font.basic, 'wheat4')
        text.set_center()
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('Memory', Memory))

        text = Text(self, 'Puzzle', mid, 400, Scene.font.basic, 'wheat4')
        text.set_center()
        text.set_hilight('burlywood')
        text.set_callback(self.start_game, ('Puzzle', Puzzle))
        self.last_scene = None

    def entrance(self):
        QuitScene.last_scene = 'Intro'
        if self.last_scene:
            del Screen.scenes[self.last_scene]
            self.last_scene = None

    def start_game(self, text, pydata):
        self.last_scene = pydata[0]
        Screen.scenes[pydata[0]] = pydata[1]()
        Screen.set_scene = pydata[0]

    def blit(self, surface):
        surface.fill((0,0,30))

class TicTacToe(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'TicTacToe', mid, 20, Scene.font.basic, 'blue').set_center()
        button = Button(self, 'Back', (10,10,100,30), self.push_back)
        self.board = ['','','' ,'','','' ,'','','']
        self.buttons = []
        for i in range(9):
            x = int((i % 3) * 55 + self.get_centerx() - (55 + 55 / 2))
            y = int(i / 3) * 55 + 200
            self.buttons.append(Button(self, '', (x, y, 50, 50), self.push, i))

        self.wins_text = Text(self, 'Wins: 0', 100, 100, Scene.font.basic, 'green').set_center()
        self.cats_text = Text(self, 'Cats: 0', mid, 100, Scene.font.basic, 'blue').set_center()
        x = self.get_size()[0] - 150
        self.lost_text = Text(self, 'Lost: 0', x, 100, Scene.font.basic, 'red').set_center()
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

    def entrance(self):
        QuitScene.last_scene = "TicTacToe"

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
        Screen.set_scene = 'Intro'

    def blit(self, surface):
        surface.fill((0,0,40))

class Slot:
    def __init__(self, rect, color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.color = color

class MasterMind(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'MasterMind', mid, 20, Scene.font.basic, 'green').set_center()
        Button(self, 'Check', (mid - 50, 475, 100, 32), self.check, None, 'green')
        Button(self, 'Back', (10, 10, 100, 30), self.push_back, None, 'green')
        Button(self, 'New Game', (10, 50, 100, 30), self.push_newgame, None, 'green')
        self.colors = ('yellow', 'red', 'blue', 'white', 'wheat4', 'orange', 'green', 'purple')
        self.colors = tuple(map(pygame.Color, self.colors))
        self.picker = [pygame.Rect(150, i * 30 + 180, 40, 20) for i in range(8)]
        self.outcome = Text(self, "", mid, 550, Scene.font.basic, 'green')
        self.push_newgame(None, None)

    def entrance(self):
        QuitScene.last_scene = 'MasterMind'

    def push_back(self, button, pydata):
        Screen.set_scene = 'Intro'

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

class FloodIt(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'FloodIt', mid, 20, Scene.font.basic, 'dodgerblue').set_center()
        Button(self, 'Back', (10,10,100,30), self.push_back, None, 'dodgerblue')
        Button(self, 'New Game', (10,50,100,30), self.push_newgame, None, 'dodgerblue')
        self.colors = tuple(map(pygame.Color,
            ['dodgerblue', 'gold', 'firebrick1', 'darkslateblue',
             'forestgreen', 'darkorange', 'mediumorchid'] ))

        self.turn_text = Text(self, 'Turn: 0', mid, 560, Scene.font.basic, 'wheat4').set_center()
        self.push_newgame(None, None)

    def entrance(self):
        QuitScene.last_scene = 'FloodIt'

    def push_back(self, button, pydata):
        Screen.set_scene = 'Intro'

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

class Card:
    def __init__(self, rect, item):
        self.item = item
        self.image = self.draw()
        self.rect = pygame.Rect(rect)
        self.show = False

    def draw(self):
        surface = pygame.Surface((30,30))
        surface = surface.convert_alpha()
        surface.fill((0,0,0,0))
        rect = pygame.Rect(0,0,30,30)

        if self.item in [0,1,2,3]:
            colors_list = ['deepskyblue1','firebrick1','limegreen','lightgoldenrod']
            foreground = pygame.Color(colors_list[self.item % 4])
            surface.fill(foreground, rect)
            r = pygame.Rect(5,5,5,5)
            pygame.draw.rect(surface, (0,0,0), r)
            r.move_ip(15, 0)
            pygame.draw.rect(surface, (0,0,0), r)
            r = pygame.Rect(11,15,8,8)
            pygame.draw.rect(surface, (0,0,0), r)
        elif self.item in [4,5,6,7,8]:
            colors_list = ['dodgerblue','indianred','mediumseagreen','mediumpurple','khaki']
            fg = pygame.Color(colors_list[self.item % 5])
            bg = (Vector(fg) * 0.6).tup_cast()
            colors = [fg, bg]
            for i in range(3):
                for j in range(3):
                    irect = pygame.Rect(i * 10, j * 10, 9,9)
                    surface.fill(colors[(i + j) % 2], irect)
        elif self.item in [9,10,11,12]:
            colors_list = ['darkolivegreen1','chocolate','darkgoldenrod','coral']
            fg = pygame.Color(colors_list[self.item % 4])
            bg = Vector(fg) * 0.5
            grad = gradient.horizontal((fg, bg), 30)
            letter = Scene.font.basic.render('ABCD'[self.item % 4], 1, (255,255,255))
            arect = letter.get_rect()
            arect.center = rect.center
            surface.blit(gradient.apply_surface(letter, grad), arect)
        elif self.item in [13,14,15,16,17]:
            colors_list = ['cornflowerblue','bisque3','limegreen','coral','honeydew']
            left = pygame.Color(colors_list[self.item % 5])
            right = (Vector(left) * 0.6).tup_cast()
            surface.fill(left, pygame.Rect(0,0,15,15))
            surface.fill(right, pygame.Rect(15,0,15,15))
            surface.fill(right, pygame.Rect(0,15,15,15))
            surface.fill(left, pygame.Rect(15,15,15,15))
        elif self.item in [18,19,20]:
            colors_list = ['deepskyblue1','firebrick1','limegreen']
            foreground = pygame.Color(colors_list[self.item % 3])
            background = (Vector(foreground) * 0.6).tup_cast()
            pygame.draw.circle(surface, foreground, (11, 12), 10)
            pygame.draw.circle(surface, background, (19, 18), 10)
        elif self.item in [21,22,23]:
            colors_list = ['deepskyblue1','firebrick1','limegreen']
            foreground = pygame.Color(colors_list[self.item % 3])
            pygame.draw.line(surface, foreground, (15,0), (15,30), 3)
            pygame.draw.line(surface, foreground, (0,15), (30,15), 3)
        elif self.item in [24,25,26]:
            colors_list = ['deepskyblue1','firebrick1','limegreen']
            foreground = pygame.Color(colors_list[self.item % 3])
            pygame.draw.line(surface, foreground, (0,0), (30,30), 3)
            pygame.draw.line(surface, foreground, (0,30), (30,0), 3)
        elif self.item in [27,28,29]:
            colors_list = ['deepskyblue1','firebrick1','limegreen']
            foreground = pygame.Color(colors_list[self.item % 3])
            pygame.draw.circle(surface, foreground, rect.center, 14)
            pygame.draw.circle(surface, (0,0,0), rect.center, 6)

        return surface

class Memory(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'Memory', mid, 20, Scene.font.basic, 'mediumorchid1').set_center()
        Button(self, 'Back', (10,10,100,30), self.push_back, None, 'mediumorchid1')
        Button(self, 'New Game', (10,50,100,30), self.push_newgame, None, 'mediumorchid1')
        self.move_text = Text(self, 'Moves: 0', mid, 100, Scene.font.basic, 'mediumorchid1').set_center()

        self.push_newgame(None, None)

    def push_newgame(self, button, pydata):
        self.cards = []
        self.move_text.set_text('Moves: 0')
        objects = list(range(30)) + list(range(30))
        for across in range(10):
            self.cards.append([])
            for down in range(6):
                pick = choice(objects)
                objects.remove(pick)
                x = across * 55 + 120
                y = down * 55 + 150
                self.cards[across].append(Card((x,y,50,50),pick))

        self.last_pick = []
        self.move_count = 0

    def entrance(self):
        QuitScene.last_scene = 'Memory'

    def push_back(self, button, pydata):
        Screen.set_scene = 'Intro'

    def blit(self, surface):
        surface.fill((40,0,40))
        for item in self.cards:
            for card in item:
                if card.show:
                    pos = card.rect.topleft
                    pos = pos[0] + 10, pos[1] + 10
                    surface.blit(card.image, pos)
                else:
                    surface.fill(pygame.Color('snow'), card.rect)

    def event(self, event):
        Quit.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                if 120 <= mx < 670 and 150 <= my < 480:
                    x = int((mx - 120) / 55)
                    y = int((my - 150) / 55)
                    #print(x, y)
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
                            self.move_text.set_text('Moves: ' + str(self.move_count))
                    else:
                        for cx,cy in self.last_pick:
                            self.cards[cx][cy].show = False
                        self.last_pick = [(x, y)]

class PuzzleBlock:
    def __init__(self, number):
        self.number = number
        self.image = pygame.Surface((65, 65))
        self.image.fill((pygame.Color('aquamarine')))
        surface = Scene.font.basic.render(str(number + 1), 1, (0,0,0))
        rect = surface.get_rect()
        rect.center = self.image.get_rect().center
        self.image.blit(surface, rect)

class Puzzle(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = self.get_centerx()
        Text(self, 'Puzzle', mid, 20, Scene.font.basic, 'aquamarine').set_center()
        Button(self, 'Back', (10,10,100,30), self.push_back, None, 'aquamarine')
        Button(self, 'New Game', (10,50,100,30), self.push_newgame, None, 'aquamarine')
        self.board = [PuzzleBlock(i) for i in range(15)] + [None]
        self.push_newgame(None, None)

    def entrance(self):
        QuitScene.last_scene = 'Puzzle'

    def push_newgame(self, button, pydata):
        shuffle(self.board)

    def push_back(self, button, pydata):
        Screen.set_scene = 'Intro'

    def blit(self, surface):
        surface.fill(pygame.Color('aquamarine4'))
        for enum, item in enumerate(self.board):
            if item:
                y = int(enum / 4) * 70 + 150
                x = int(enum - int(enum / 4) * 4) * 70 + 260
                surface.blit(item.image, (x, y))

    def event(self, event):
        Quit.event(self, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                if 260 <= mx <= 540 and 150 <= my < 430:
                    pos = int((mx - 260) / 70) + int((my - 150) / 70) * 4
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
                    if pos + 1 < 16:
                        setboard(pos + 1)
                    if pos - 1 >= 0:
                        setboard(pos - 1)

def main():
    Screen.center()
    Screen.open('Simple Games', (800, 600))
    Scene.font.basic = pygame.font.Font(None, 36)

    Screen.scenes['Intro'] = Intro()
    Screen.scenes['QuitScene'] = QuitScene()

    Screen.loop('Intro', 30)
    pygame.quit()

if __name__ == '__main__':
    main()
