# encoding: utf-8

import sys
sys.path.append("..")

from seqzero import Sequencer
from liblo import send

# Instanciate a sequencer listening on port 12345
# sending osc messages to localhost on port 5555
# with a bpm set to 120
seq = Sequencer(bpm=120, port=12345, target='localhost:5555 localhost:10001')


# Add a sequence
seq.addSequence('test',[
    [['/step', 1]],
    [['/step',0]],
    [['/step', 1]],
    [['/step',0]]
])

# Enale the sequence
send('osc.udp://localhost:12345', '/Sequencer/Sequence/Enable', 'test')

# Start the sequencer
send('osc.udp://localhost:12345', '/Sequencer/Play')

seq.start()

# now listen on port 5555 with your favorite tool...
