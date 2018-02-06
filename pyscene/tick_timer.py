
class TickTimerInfo:
    def __init__(self, interval, callback, pydata):
        self.next_tick = TickTimer.ticks + interval
        self.interval = interval
        self.callback = callback
        self.pydata = pydata
        self.stop = False

class TickTimer:
    ticks = 0

    def __init__(self, ticks):
        self.callbacks = {}
        self.tick_stop = 0
        TickTimer.ticks = ticks

    def __getitem__(self, key):
        return self.callbacks[key]

    def __setitem__(self, key, value):
        if isinstance(value, TickTimerInfo):
            self.callbacks[key] = value

    def add(self, key, interval, callback, pydata=None):
        self.callbacks[key] = TickTimerInfo(interval, callback, pydata)

    def reset(self, key, offset=None):
        if offset:
            self.callbacks[key].next_tick = TickTimer.ticks + offset
        else:
            self.callbacks[key].next_tick = TickTimer.ticks + self.callbacks[key].interval

    def stop(self, key):
        self.callbacks[key].stop = True

    def start(self, key):
        self.callbacks[key].stop = False
        self.callbacks[key].next_tick = TickTimer.ticks + self.callbacks[key].interval

    # PyScene.Scene use only
    def _stop(self):
        if self.tick_stop == 0:
            self.tick_stop = TickTimer.ticks

    # PyScene.Scene use only
    def _start(self):
        if self.tick_stop > 0:
            elaspe = TickTimer.ticks - self.tick_stop
            self.tick_stop = 0
            for info in self.callbacks.values():
                info.next_tick += elaspe

    # PyScene.Scene use only
    def _update(self, ticks):
        TickTimer.ticks = ticks
        for key, item in self.callbacks.items():
            if item.stop is False:
                if ticks > item.next_tick:
                    item.callback(item)
                    item.next_tick += item.interval
                    if ticks > item.next_tick:
                        item.next_tick = ticks

    def pop(self, key):
        self.callbacks.pop(key)
