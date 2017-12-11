#                          Welcome to PyScene
#                       This is my boiler plate

import pygame
from PyScene import Scene, Screen, Font, Text, Button, Textbox, gradient

class Quit:
    def event(self, event):
        if event.type == pygame.QUIT:
            Screen.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Screen.running = False

class Intro(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = Screen.size[0] / 2
        # text is auto center
        Text(self, 'Welcome To PyScene', mid, 20, Font.basic, 'dodgerblue')
        Button(self, "Push Me", (10,70,100,30), self.push)

        Text(self, "Button Styles", 60, 150, Font.small, 'dodgerblue')
        Button(self, "Simple", (10,170,100,30), None, None, 'mistyrose') # simple is default
        Button(self, "Normal", (10,210,100,30), None, None, 'darkseagreen', None, 'normal')
        Button(self, "Box", (10,250,100,30), None, None, 'forestgreen', None, 'box')

        colorful_surface = gradient.vertical(('blue', 'red', 'wheat4', 'green', 'burlywood'))
        Text(self, 'Colorful Text', mid, 400, Font.basic, colorful_surface)
        colorful_surface = gradient.horizontal(('blue', 'red', 'wheat4', 'green', 'burlywood'))
        Text(self, 'Colorful Text', mid, 440, Font.basic, colorful_surface)
        t = Text(self, 'Angle Text', 100, 500, Font.basic, 'dodgerblue')
        t.set_angle(45)
        colorful_surface = gradient.horizontal(('white', 'snow', 'blue', 'snow', 'white'))
        t.set_blink(colorful_surface, 1000, 400)

        self.groups = [
            ("Group Example",
            Text(self, "Text Group Example", mid, 100, Font.basic, 'wheat4')),
            ("Colors",
            Text(self, "Built In Colors", mid, 150, Font.basic, 'wheat4')),
            ("GrayColors",
            Text(self, "Built In Colors GrayScale", mid, 200, Font.basic, 'wheat4'))
            ]
        for data, text in self.groups:
            text.set_hilight('burlywood')
            text.set_callback(self.text_callback, data)

        tb = Textbox(self, (mid - 125, 300, 250, 40), Font.basic)
        tb.set_ghost('Enter Name Here', 60)

    def push(self, button, pydata):
        # let switch scene
        Screen.set_scene = "Push Me"

    def text_callback(self, text, pydata):
        Screen.set_scene = pydata

    # main draw loop
    def blit(self, surface):
        surface.fill((0,0,30))

class GroupExample(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = Screen.size[0] / 2
                # text is auto center
        self.intro = Text(self, 'Text Group Example', mid, 20, Font.basic, 'orange')
        self.back = Button(self, 'Back', (10, 70, 100, 30), self.back_push, None, 'orange')
        self.texts = [
            Text(self, 'Me First', mid, 200, Font.small, 'wheat4', 'me_group'),
            Text(self, 'Pick Me', mid, 250, Font.small, 'wheat4', 'me_group'),
            Text(self, 'Click Me', mid, 300, Font.small, 'wheat4', 'me_group')
        ]

        for t in self.texts:
            t.set_hilight('burlywood')
            t.set_toggle('wheat')

    def blit(self, surface):
        surface.fill((30,30,30))

    def back_push(self, button, pydata):
        Screen.set_scene = "Intro"

    # when you enter the scene
    def entrance(self):
        self.texts[0].set_focus()

class PushMe(Quit, Scene):
    def __init__(self):
        Scene.__init__(self)
        mid = Screen.size[0] / 2
        self.intro = Text(self, 'Whoa! You Push Me.', mid, 20, Font.basic, 'red')
        self.push_me = Button(self, "Push Me", (10,70,100,30), self.push, None, 'red')

    def push(self, button, pydata):
        Screen.set_scene = "Intro"

    def blit(self, surface):
        surface.fill((30,0,0))

class Colors(Quit, Scene):
    def __init__(self, grayscale=False):
        Scene.__init__(self)
        mid = Screen.size[0] / 2
        self.page = 1
        self.intro = Text(self, 'Built In Colors ' + str(self.page), mid, 20, Font.basic, 'snow')
        self.back = Button(self, 'Back', (10, 20, 100, 30), self.push_back, None, 'snow')
        self.back.text.set_color('dodgerblue')
        if grayscale:
            self.keys = [key for key in list(pygame.color.THECOLORS.keys())
                if key[:4] in ['gray', 'grey']]
        else:
            self.keys = [key for key in list(pygame.color.THECOLORS.keys())
                if key[:4] not in ['gray', 'grey']]
        self.keys.sort()
        self.keys_group = []
        for i in range(100):
            y = i % 20 * 25 + 70
            x = int(i / 20) * 150 + 100
            self.keys_group.append( Text(self, "None", x, y, Font.small, (0,0,0)) )
        self.update_colors()

        prev = Button(self, 'Prev', (mid - 150, 560, 100, 30), self.prev_page, None, 'snow')
        prev.text.set_color('dodgerblue')
        nextp = Button(self, 'Next', (mid + 50, 560, 100, 30), self.next_page, None, 'snow')
        nextp.text.set_color('dodgerblue')

        self.max_page = int(len(self.keys) / 100) + 1

    def update_colors(self):
        self.rects = []
        keys = self.keys[100 * (self.page - 1): 100 * self.page]
        for enum, key in enumerate(keys):
            self.keys_group[enum].set_text(key)
            self.keys_group[enum].set_color(key)
            color =  pygame.Color(key)
            if color.r < 30 and color.g < 30 and color.b < 30:
                self.rects.append(self.keys_group[enum]._rect)

        if len(keys) < 100:
            for n in range(enum + 1, 100):
                self.keys_group[n].set_text(" ")

    def prev_page(self, button, pydata):
        if self.page > 1:
            self.page -= 1
            self.update_colors()
            self.intro.set_text('Built In Colors ' + str(self.page))

    def next_page(self, button, pydata):
        if self.page < self.max_page:
            self.page += 1
            self.update_colors()
            self.intro.set_text('Built In Colors ' + str(self.page))

    def push_back(self, button, pydata):
        Screen.set_scene = "Intro"

    def blit(self, surface):
        surface.fill((0,0,0))
        for rect in self.rects:
            surface.fill(pygame.Color('grey15'), rect)

def main():
    Screen.center()
    Screen.init('Welcome To PyScene', (800, 600))
    # Setting fonts global through scene
    Font.basic = Font.load(36)
    Font.small = Font.load(24)
    # store my scenes
    Screen.scenes['Intro'] = Intro()
    Screen.scenes['Colors'] = Colors()
    Screen.scenes['GrayColors'] = Colors(True)
    Screen.scenes['Push Me'] = PushMe()
    Screen.scenes['Group Example'] = GroupExample()

    # mainloop, First scene, fps
    Screen.loop('Intro', 30)

if __name__ == '__main__':
    main()
