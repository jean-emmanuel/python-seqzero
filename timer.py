# encoding: utf-8

from time import sleep, time

class Timer(object):
    """
    Timer with latency compensation
    """

    def __init__(self, sequencer):

        self.sequencer = sequencer
        self.trigger = 0
        self.clock = time()
        self.time = time()
        self.shift = 0

    def reset(self):

        self.clock = time()
        self.time = time()
        self.shift = 0

    def trig(self):

        self.trigger = 1
        self.reset()

    def wait(self, n, mode='beats'):

        if mode[0] == 'b':
            delay = n * 60. / self.sequencer.bpm
        elif mode[0] == 's':
            delay = n

        while time() - self.clock < delay and not self.trigger and not self.sequencer.exiting:
            sleep(0.001)

        if self.trigger:
            self.trigger = 0
        else:
            t = time()
            self.shift += delay - (t - self.time)
            self.clock += self.shift + delay
            self.time = t
