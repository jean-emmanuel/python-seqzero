# encoding: utf-8

import sys
sys.path.append("..")

from seqzero import Sequencer
from pyo import Server, Metro, Trig, Timer, Change, OscDataReceive, TrigFunc


bpm = 120

s = Server(audio="jack")
s.boot()
s.start()


# Metronom
metronom = Metro(60. / bpm)

# Sequencer
seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')
seq.addSequence('metronom',[
    ['/tic'],
    ['/tic'],
])

# Sequencer's monitor
t = False
sequencer_trig = Trig()
def tic(a):
    sequencer_trig.play()
    # launch the metronom at first msg
    global t
    if not t:
        metronom.play()

sequencer_monitor = OscDataReceive(9900, "/tic", tic)


# Compute & print difference between the two
timer = Timer(metronom, sequencer_trig)

def print_diff():
    print abs(timer.get() - 0.25) - 0.25

change = Change(timer)
printer = TrigFunc(change, print_diff)


seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

seq.start()
