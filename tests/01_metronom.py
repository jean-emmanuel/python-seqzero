# encoding: utf-8

import sys
sys.path.append("..")

from seqzero import Sequencer
from liblo import ServerThread
from time import time

bpm = 2000

# Sequencer
seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')
seq.addSequence('metronom',[
    ['/tic',1],
    ['/tic',0]
])

error = 0
def print_diff():
    global t, error, bpm
    if bpm != seq.bpm:
        bpm=seq.bpm
        error = 0
        t = time()
        return
    nt = time()
    error += 60. / bpm - (nt - t)
    t = nt
    print("Cumulated error: %s%.3f ms (%5.2f" % (' ' if str(error)[0]!='-' else '',round(1000000 * error)/1000, abs(100 * error / (60. / bpm))) + "%) at " + str(bpm) + " bpm")


sequencer_monitor = ServerThread(port=9900)
sequencer_monitor.add_method('/tic', None, print_diff)
sequencer_monitor.start()


seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

t = time()
seq.start()
