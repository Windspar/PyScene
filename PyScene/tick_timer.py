
class TickTimerInfo:
    def __init__(self, interval, callback, pydata):
        self.next_tick = TickTimer.ticks + interval
        self.interval = interval
        self.callback = callback
        self.pydata = pydata

class TickTimer:
    ticks = 0

    def __init__(self, ticks):
        self.callbacks = {}
        self.tick_stop = 0
        TickTimer.ticks = ticks

    def add(self, key, interval, callback, pydata=None):
        self.callbacks[key] = TickTimerInfo(interval, callback, pydata)

    def reset(self, key, offset=None):
        if offset:
            self.callbacks[key].next_tick = TickTimer.ticks + offset
        else:
            self.callbacks[key].next_tick = TickTimer.ticks + self.callbacks[key].interval

    def stop(self):
        self.tick_stop = TickTimer.ticks

    def time_elaspe(self):
        if self.tick_stop > 0:
            elaspe = TickTimer.ticks - self.tick_stop
            for info in self.callbacks.values():
                info.next_tick += elaspe

    def update(self, ticks):
        TickTimer.ticks = ticks
        for key, item in self.callbacks.items():
            if ticks > item.next_tick:
                item.next_tick += item.interval
                item.callback(item)

    def pop(self, key):
        self.callbacks.pop(key)
