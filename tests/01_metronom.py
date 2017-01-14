# encoding: utf-8

import sys
sys.path.append("..")

from seqzero import Sequencer
from liblo import ServerThread
from time import time

bpm = 120

# Sequencer
seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')
seq.addSequence('metronom',[
    ['/tic'],
    ['/tic'],
])

t = time()
def print_diff():
    global t
    l = str(round(10000 * (60. / seq.bpm - (time() - t))) / 10) + 'ms'
    l = ' ' + l if l[0] != '-' else l
    print('latency: ' + l)

    t = time()

sequencer_monitor = ServerThread(port=9900)
sequencer_monitor.add_method('/tic', None, print_diff)
sequencer_monitor.start()




seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

seq.start()
