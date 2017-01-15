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
    ['/tic',1],
    ['/tic',0]
])

diff = 0
n = 1
def print_diff():
    global t, diff, n, bpm
    if bpm != seq.bpm:
        bpm=seq.bpm
        diff = 0
        n = 1
        t= time()
        return
    diff += time() - t
    print("Average error = %s%.3f ms"  % (' ' if str((60./bpm - 1.0 * diff / n))[0] != '-' else '',round((60./bpm - 1.0 * diff / n) * 1000000) / 1000))
    n += 1
    t = time()


sequencer_monitor = ServerThread(port=9900)
sequencer_monitor.add_method('/tic', None, print_diff)
sequencer_monitor.start()


seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

t = time()
seq.start()
