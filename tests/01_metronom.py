# encoding: utf-8

import sys
sys.path.append("..")

from seqzero import Sequencer
from liblo import ServerThread
from time import time

bpm = 20000

# Sequencer
seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')
seq.addSequence('metronom',[
    ['/tic'],
    ['/tic'],
])

shift = 0
def print_diff():
    global t, shift
    if bpm != seq.bpm:
        shift=0
    nt = time()
    shift += 60. / seq.bpm - (nt - t)
    t = time()

    print('shift: ' + str(shift) + 's')

sequencer_monitor = ServerThread(port=9900)
sequencer_monitor.add_method('/tic', None, print_diff)
sequencer_monitor.start()




seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

t = time()
seq.start()
