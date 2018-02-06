import pygame

class TypeWriter():
    def __init__(self, parent, interval, callback=None, pydata=None):
        self.parent = parent
        height = self.parent._rect.height
        self.clip_rect = pygame.Rect(0,0,0,height)
        self.letter = 0
        self.finish = False
        self.interval = interval
        self.callback = callback
        self.pydata = pydata

        self.parent._parent.timer.add(self.parent._key + 'writer_timer__', self.interval,
        self.elaspe_time)

    def reset(self):
        self.letter = 0
        self.finish = False
        self.clip_rect.width = 0
        self.parent._parent.timer.add(self.parent._key + 'writer_timer__', self.interval,
        self.elaspe_time)

    def elaspe_time(self, timer):
        if not self.finish:
            text = self.parent._text
            self.letter += 1
            if self.letter < len(text):
                font = self.parent._font
                self.clip_rect.width = font.size(text[:self.letter])[0]
            else:
                self.finish = True
                if self.callback:
                    self.callback(self, self.pydata)
                #self.parent._parent.timer.pop(self.parent._key + 'writer_timer__')
