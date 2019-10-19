# encoding: utf-8

import sys
sys.path.append("../..")

from seqzero import Sequencer
from liblo import time
from time import sleep

# Sequencer



class Scenes():

    def test(self, seq, timer, *args):

        print('Extra args: ', args)
        # print('Extra args: ', 'no')
        # -> ('Extra args: ', (1, 'hello'))


seq = Sequencer(bpm=240, port=12345, target='localhost:9900', scenes=Scenes())

seq.send(':/Sequencer/Scene/Play', 'test', 1, 'hello')

seq.start()
