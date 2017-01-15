# encoding: utf-8

import sys
sys.path.append("..")

from pyo import *
from seqzero import Sequencer

bpm = 120

s = Server(audio="jack").boot()

# Sequencer
seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')
seq.addSequence('metronom',[
    ['/tic'],
])

def tic(*a):
    env.play()
osc = OscDataReceive(9900, '/tic', tic)
env = Adsr(attack=0.01, decay=0.1, sustain=0.1, release=0.1, dur=0.2, mul=0.5)
sin = Sine(1500, mul=env).mix(2).out()

seq.send(':/Sequencer/Sequence/Enable', 'metronom')

seq.play()

s.start()
seq.start()
