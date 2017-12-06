#                          Welcome to PyScene
#                       This is my boiler plate

import pygame
from PyScene import scene
from PyScene.widgets import Text, Button, Textbox
from PyScene.tool.gradient import vertical, horizontal

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
        # text is auto center
        Text(self, 'Welcome To PyScene', mid, 20, scene.Font.basic, 'blue')
        Button(self, "Push Me", (10,70,100,30), self.push)

        colorful_surface = vertical(('blue', 'red', 'wheat4', 'green', 'burlywood'))
        Text(self, 'Colorful Text', mid, 400, scene.Font.basic, colorful_surface)
        colorful_surface = horizontal(('blue', 'red', 'wheat4', 'green', 'burlywood'))
        Text(self, 'Colorful Text', mid, 440, scene.Font.basic, colorful_surface)


        self.groups = [
            ("Group Example",
            Text(self, "Text Group Example", mid, 100, scene.Font.basic, 'wheat4')),
            ("Colors",
            Text(self, "Built In Colors", mid, 150, scene.Font.basic, 'wheat4'))
            ]
        for data, text in self.groups:
            text.set_hilight('burlywood')
            text.set_callback(self.text_callback, data)

        Textbox(self, (mid - 100, 300, 200, 40), scene.Font.basic)

    def push(self, button, pydata):
        # let switch scene
        scene.Screen.set_scene = "Push Me"

    def text_callback(self, text, pydata):
        scene.Screen.set_scene = pydata

    # main draw loop
    def blit(self, surface):
        surface.fill((0,0,30))

class GroupExample(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        # text is auto center
        self.intro = Text(self, 'Text Group Example', mid, 20, scene.Font.basic, 'orange')
        self.back = Button(self, 'Back', (10, 70, 100, 30), self.back_push, None, 'orange')
        self.texts = [
            Text(self, 'Me First', mid, 200, scene.Font.small, 'wheat4', 'me_group'),
            Text(self, 'Pick Me', mid, 250, scene.Font.small, 'wheat4', 'me_group'),
            Text(self, 'Click Me', mid, 300, scene.Font.small, 'wheat4', 'me_group')
        ]

        for t in self.texts:
            t.set_hilight('burlywood')
            t.set_toggle('wheat')

    def blit(self, surface):
        surface.fill((30,30,30))

    def back_push(self, button, pydata):
        scene.Screen.set_scene = "Intro"

    # when you enter the scene
    def entrance(self):
        self.texts[0].set_focus()

class PushMe(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        self.intro = Text(self, 'Whoa! You Push Me.', mid, 20, scene.Font.basic, 'red')
        self.push_me = Button(self, "Push Me", (10,70,100,30), self.push, None, 'red')

    def push(self, button, pydata):
        scene.Screen.set_scene = "Intro"

    def blit(self, surface):
        surface.fill((30,0,0))

class Colors(Quit, scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        mid = scene.Screen.size[0] / 2
        self.page = 1
        self.intro = Text(self, 'Built In Colors ' + str(self.page), mid, 20, scene.Font.basic, 'snow')
        self.back = Button(self, 'Back', (10, 20, 100, 30), self.push_back, None, 'snow')
        self.back.text.set_color('dodgerblue')
        self.keys = list(pygame.color.THECOLORS.keys())
        self.keys.sort()
        self.keys_group = []
        for i in range(100):
            y = i % 20 * 25 + 70
            x = int(i / 20) * 150 + 100
            self.keys_group.append( Text(self, "None", x, y, scene.Font.small, (0,0,0)) )
        self.update_colors()

        prev = Button(self, 'Prev', (mid - 150, 560, 100, 30), self.prev_page, None, 'snow')
        prev.text.set_color('dodgerblue')
        nextp = Button(self, 'Next', (mid + 50, 560, 100, 30), self.next_page, None, 'snow')
        nextp.text.set_color('dodgerblue')

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
        if self.page < 7:
            self.page += 1
            self.update_colors()
            self.intro.set_text('Built In Colors ' + str(self.page))

    def push_back(self, button, pydata):
        scene.Screen.set_scene = "Intro"

    def blit(self, surface):
        surface.fill((0,0,0))
        for rect in self.rects:
            surface.fill(pygame.Color('grey15'), rect)

def main():
    scene.Screen.center()
    scene.Screen.init('Welcome To PyScene', (800, 600))
    # Setting fonts global through scene
    scene.Font.basic = pygame.font.Font(None, 36)
    scene.Font.small = pygame.font.Font(None, 24)
    # store my scenes
    scene.Screen.scenes['Intro'] = Intro()
    scene.Screen.scenes['Colors'] = Colors()
    scene.Screen.scenes['Push Me'] = PushMe()
    scene.Screen.scenes['Group Example'] = GroupExample()

    # mainloop, First scene, fps
    scene.Screen.loop('Intro', 30)
    pygame.quit()

if __name__ == '__main__':
    main()
