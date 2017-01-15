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

error = 0
def print_diff():
    global t, error, bpm
    if bpm != seq.bpm:
        bpm=seq.bpm
        diff = 0
        t = time()
        return
    nt = time()
    error += (nt - t) - 60. / bpm
    t = nt
    print("Cumulated error: %s%.3f ms" % (' ' if str(error)[0]!='-' else '',round(1000000 * error)/1000))


sequencer_monitor = ServerThread(port=9900)
sequencer_monitor.add_method('/tic', None, print_diff)
sequencer_monitor.start()


seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

t = time()
seq.start()
