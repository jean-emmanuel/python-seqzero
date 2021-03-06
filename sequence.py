# encoding: utf-8

from .utils import KillableThread as Thread
from .timer import Timer

from random import randint

class Sequence(object):
    """
    Sequence: event loop synchronized by the sequencer's tempo
    """
    def __init__(self, sequencer=None, name=None, steps=None):

        self.sequencer = sequencer
        self.name = name
        self.steps = steps
        self.beats = len(self.steps)
        self.playing = False
        self.random = False
        self.last_random = -1

    def toggle(self, state):

        self.playing = bool(state)

    def play(self, step=None, divider=1, clock=None):
        """
        Play a step

        Args:
            step:
                  (int): sequencer's transport position
                 (list): list of messages / message (list of args for sequencer.send())
                (tuple): array of substeps

            divider     (int): number of substeps in current context
            clock   (timetag): starting clock for substeps' timer
        """

        if not self.playing:
            return None

        if type(step) is int:

            if self.random and divider == 1:
                cursor = -1
                while cursor == -1 or cursor == self.last_random:
                    cursor = randint(0, self.beats - 1)
                self.last_random = cursor
            else:
                cursor = step % self.beats

            step = self.steps[cursor]

        if step is None:
            return

        if type(step) is tuple:
            clock = clock if clock is not None else self.sequencer.timer.clock
            self.play(step[0], divider * len(step), clock)
            t = Thread(target=self.play_substeps, args=[step, divider, clock])
            t.start()

        elif type(step) is list and type(step[0]) is list:

            for i in range(len(step)):
                self.sequencer.send(*step[i])

        elif type(step) is list:
            self.sequencer.send(*step)

    def play_substeps(self, step, divider, clock):
        timer = Timer(self.sequencer, clock)
        n = len(step)
        for i in range(1, n):
            if not self.playing:
                return
            timer.wait(1. / n / divider, 'beat')
            self.play(step[i], n * divider, timer.clock)
