# encoding: utf-8

import sys
sys.path.append("../..")

from seqzero import Sequencer
from liblo import time
from time import sleep

# Sequencer



class Scenes():

    def test(self, seq, timer):

        print('Network + Code latency = %f ms' % ((time() - timer.clock)*1000))
        timer.wait(1, 'beat')
        seq.send(':/Sequencer/Scene/Play', 'test', ('t', time()))

seq = Sequencer(bpm=240, port=12345, target='localhost:9900', scenes=Scenes())
seq.scene_play('test')
seq.play()
seq.start()
