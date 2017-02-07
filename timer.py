# encoding: utf-8

from time import sleep, time

class Timer(object):
    """
    Timer with latency compensation
    """

    def __init__(self, sequencer, timestamp=None):

        self.sequencer = sequencer
        self.rate = 1 / 1000.0
        self.trigger = 0
        self.reset(timestamp)

    def reset(self, timestamp=None):

        self.clock = time() if timestamp == None else timestamp

    def trig(self, timestamp=None):

        self.trigger = 1
        self.reset(timestamp)

    def wait(self, n, mode='beats'):

        if mode[0] == 'b':
            delay = n * 60. / self.sequencer.bpm
        elif mode[0] == 's':
            delay = n

        while time() - self.clock < delay - 2 * self.rate and not self.trigger and not self.sequencer.exiting:
            sleep(self.rate)

        if self.trigger:
            self.trigger = 0
        else:
            self.clock += delay
