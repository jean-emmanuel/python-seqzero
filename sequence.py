# encoding: utf-8

class Sequence(object):
    """
    Sequence: event loop synchronized by the sequencer's tempo
    """
    def __init__(self, parent=None, name=None, steps=None):

        self.name = name
        self.steps = steps
        self.beats = len(self.steps)
        self.is_playing = False

    def getStep(self, cursor):

        if not self.is_playing:
            return None

        return self.steps[cursor%self.beats]

    def toggle(self, state):

        self.is_playing = bool(state)
