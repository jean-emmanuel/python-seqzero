# encoding: utf-8

from time import sleep
from liblo import time

class Timer(object):
    """
    Timer with latency compensation
    """

    def __init__(self, sequencer, timestamp=None):

        self.sequencer = sequencer
        self.rate = 1 / 1000.0
        self.trigger = 0
        self.reset(timestamp)

    def time(self):
        return Timer.time()

    def reset(self, timestamp=None):

        self.clock = Timer.time() if timestamp == None else timestamp

    def trig(self, timestamp=None):

        self.trigger = 1
        self.reset(timestamp)

    def wait(self, n, mode='beats'):

        if mode[0] == 'b':
            delay = n * 60. / self.sequencer.bpm
        elif mode[0] == 's':
            delay = n

        while Timer.time() - self.clock < delay - 2 * self.rate and not self.trigger and not self.sequencer.exiting:
            Timer.sleep(self.rate)

        if self.trigger:
            self.trigger = 0
        else:
            self.clock += delay

    @staticmethod
    def time():
        return time()

    @staticmethod
    def sleep(s):
        return sleep(s)
