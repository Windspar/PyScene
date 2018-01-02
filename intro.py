#                          Welcome to PyScene
#                       This is my boiler plate

import pygame
from pyscene import Scene, Screen, Scenery, Text, Button, Textbox

class Quit(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.add_scenery(QuitScenery(self), 'Quit')

    def event(self, event):
        if event.type == pygame.QUIT:
            self.show_scenery('Quit')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_scenery('Quit')

class QuitScenery(Scenery):
    def __init__(self, parent):
        center = parent.get_center()
        position = center[0] - 150, center[1] - 60
        Scenery.__init__(self, position, (300,120), False, False)
        mid = self.get_center() # PySceneObject need screen position
        Text(self, 'Confirm Quit', (mid[0], 40), self.font.basic, 'mediumorchid').anchor('center', 'center')
        Button(self, 'Yes', (mid[0] - 100, mid[1] + 20, 80, 34), (self.push_confirm, True), 'red')
        Button(self, 'No', (mid[0] + 20, mid[1] + 20, 80, 34), (self.push_confirm, False), 'green')

    def push_confirm(self, button, pydata):
        if pydata:
            self.close_screen()
        else:
            self.show = False

    def blit(self, surface):
        surface.fill(pygame.Color('mediumorchid4'))

class Intro(Quit):
    def __init__(self):
        #Scene.__init__(self)
        Quit.__init__(self)
        mid = self.get_centerx()
        Text(self, 'Welcome To PyScene', (mid, 20), self.font.basic, 'dodgerblue').anchor('center', 'center')
        Button(self, "Push Me", (10,70,100,30), self.push)

        Text(self, "Button Styles", (60, 150), self.font.small, 'dodgerblue').anchor('center', 'center')
        Button(self, "Simple", (10,170,100,30), None, 'mistyrose') # simple is default
        Button(self, "Normal", (10,210,100,30), None, 'darkseagreen', None, 'normal')
        Button(self, "Box", (10,250,100,30), None, 'forestgreen', None, 'box')

        colors = ('blue', 'red', 'wheat4', 'green', 'burlywood')
        Text(self, 'Colorful Text', (mid, 400), self.font.basic, colors).anchor('center', 'center')
        colors = ('h-hsl', 'blue', 'red', 'wheat4', 'green', 'burlywood')
        Text(self, 'Colorful Text', (mid, 440), self.font.basic, colors).anchor('center', 'center')
        colors = ('v-rgb', 'blue', 'red', 'wheat4', 'green', 'burlywood')
        Text(self, 'Colorful Text', (mid, 480), self.font.basic, colors).anchor('center', 'center')
        colors = ('h-rgb', 'blue', 'red', 'wheat4', 'green', 'burlywood')
        Text(self, 'Colorful Text', (mid, 520), self.font.basic, colors).anchor('center', 'center')
        colors = ('h-hsl','white', 'snow', 'blue', 'snow', 'white')
        Text(self, 'Angle Text', (120, 500), self.font.basic, 'dodgerblue',
            angle = (45),
            blink = (colors, 1200, 600))

        self.groups = [
            ("Group Example",
            Text(self, "Text Group Example", (mid, 100), self.font.basic, 'wheat4')),
            ("Colors",
            Text(self, "Built In Colors", (mid, 150), self.font.basic, 'wheat4')),
            ("GrayColors",
            Text(self, "Built In Colors GrayScale", (mid, 200), self.font.basic, 'wheat4'))
            ]
        for data, text in self.groups:
            text.anchor('center', 'center')
            text.set_hilight('burlywood')
            text.set_callback(self.text_callback, data)

        tb = Textbox(self, (mid - 125, 300, 250, 40), Scene.font.basic)
        tb.set_ghost('Enter Name Here', 'lightskyblue', 60)

    def push(self, button, pydata):
        # let switch scene
        self.set_scene("PushMe")

    def text_callback(self, text, pydata):
        self.set_scene(pydata)

    # main draw loop
    def blit(self, surface):
        surface.fill((0,0,30))

class GroupExample(Quit):
    def __init__(self):
        #Scene.__init__(self)
        Quit.__init__(self)
        mid = self.get_centerx()
                # text is auto center
        self.intro = Text(self, 'Text Group Example', (mid, 20), self.font.basic, 'orange').anchor('center', 'center')
        self.back = Button(self, 'Back', (10, 70, 100, 30), self.back_push, 'orange')
        self.texts = [
            Text(self, 'Me First', (mid, 200), self.font.small, 'wheat4', None, 'me_group'),
            Text(self, 'Pick Me', (mid, 250), self.font.small, 'wheat4', None, 'me_group'),
            Text(self, 'Click Me', (mid, 300), self.font.small, 'wheat4', None, 'me_group')
        ]

        for t in self.texts:
            t.anchor('center', 'center')
            t.set_hilight('burlywood')
            t.set_toggle('wheat')

    def blit(self, surface):
        surface.fill((30,30,30))

    def back_push(self, button, pydata):
        self.set_scene("Intro")

    # when you enter the scene
    def entrance(self):
        self.texts[0].set_focus()

class PushMe(Quit):
    def __init__(self):
        #Scene.__init__(self)
        Quit.__init__(self)
        mid = self.get_centerx()
        self.intro = Text(self, 'Whoa! You Push Me.', (mid, 20), self.font.basic, 'red').anchor('center', 'center')
        self.push_me = Button(self, "Push Me", (10,70,100,30), self.push, 'red')

    def push(self, button, pydata):
        self.set_scene("Intro")

    def blit(self, surface):
        surface.fill((30,0,0))

class Colors(Quit):
    def __init__(self, grayscale=False):
        #Scene.__init__(self)
        Quit.__init__(self)
        mid = self.get_centerx()
        self.page = 1
        self.intro = Text(self, 'Built In Colors ' + str(self.page), (mid, 10), self.font.basic, 'snow', anchorx='center')
        self.back = Button(self, 'Back', (10, 20, 100, 30), self.push_back, 'snow')
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
            self.keys_group.append( Text(self, "None", (x, y), self.font.small, (0,0,0)).anchor('center', 'center') )
        self.update_colors()

        prev = Button(self, 'Prev', (mid - 150, 560, 100, 30), self.prev_page, 'snow')
        prev.text.set_color('dodgerblue')
        nextp = Button(self, 'Next', (mid + 50, 560, 100, 30), self.next_page, 'snow')
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
        self.set_scene("Intro")

    def blit(self, surface):
        surface.fill((0,0,0))
        for rect in self.rects:
            surface.fill(pygame.Color('grey15'), rect)

def main():
    Screen.center()
    Screen.open('Welcome To PyScene', (800, 600))
    # Setting fonts global through scene
    Scene.font.basic = pygame.font.Font(None, 36)
    Scene.font.small = pygame.font.Font(None, 24)
    # store my scenes
    # scene string name will be the same as class name
    Screen.add_scene(Intro()) # 'Intro'
    Screen.add_scene(Colors())
    Screen.add_scene(PushMe())
    # if you want scene to have a different name
    Screen.add_scene(Colors(True), 'GrayColors')
    Screen.add_scene(GroupExample(), 'Group Example')

    # mainloop, First scene, fps
    Screen.loop('Intro', 30)

if __name__ == '__main__':
    main()
