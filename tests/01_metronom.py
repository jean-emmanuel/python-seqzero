# encoding: utf-8

bpm = 200


from pyo import *

import sys
sys.path.append("..")


s = Server(audio="jack")
s.boot()
s.start()

attack1 = Adsr(dur=0.2, mul=.5)
attack2 = Adsr(dur=0.2, mul=.5)
sine1 = Sine(freq=2000, mul=attack1).mix(2).out()
sine2 = Sine(freq=2000, mul=attack2).mix(2).out()





from seqzero import Sequencer

seq = Sequencer(bpm=bpm, port=12345, target='localhost:9900')

seq.addSequence('metronom',[
    ['/tic'],
])


trigged = False

def tic(*args):
    attack1.play()

def tac(*args):
    global trigged
    attack2.play()
    if trigged is False:
        trigged = True
        seq.send(':/Sequencer/Trigger')


sequencer_monitor = OscDataReceive(9900, "/tic", tic)
metronom = Pattern(tac, 60. / bpm)



seq.send(':/Sequencer/Sequence/Enable', 'metronom')
seq.send(':/Sequencer/Play')

metronom.play()
seq.start()
