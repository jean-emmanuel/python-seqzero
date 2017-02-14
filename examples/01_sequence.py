# encoding: utf-8

import sys
sys.path.append("../..")

from seqzero import Sequencer

# Instanciate a sequencer listening on port 12345
# sending osc messages to localhost on port 5555
# with a bpm set to 120
seq = Sequencer(bpm=120, port=12345, target='localhost:5555 localhost:10001')


# Add a sequence
seq.sequence_add('test',[
    (['/step', 1],['/step', 1.2],['/step', 1.3],['/step', 1.4],['/step', 1.5],['/step', 1.6],['/step', 1.7],['/step', 1.8]),
    ['/step',2],
    ['/step', 3],
    [['/step',4], ['/step', 4, 'extra bonus !']]
])

# Enale the sequence
seq.send(':/Sequencer/Sequence/Enable', 'test')

# Start the sequencer
seq.send(':/Sequencer/Play')

seq.start()

# now listen on port 5555 with your favorite tool...
