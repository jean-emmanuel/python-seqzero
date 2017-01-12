# encoding: utf-8



import sys
sys.path.append("..")

from pyOSCseq import Sequencer
from liblo import send

import scenes

# Define the scenes
# must be a function taking 2 arguments
# - the sequencer object,
# - the name
def scenes(sequencer, name):
    if scenes.hasattr(name):
        scenes[name](sequencer, name)



# Instanciate a sequencer listening on port 12345
# sending osc messages to localhost on port 5555
# with a bpm set to 120
seq = Sequencer(bpm=120, port=12345, target='localhost:5555')


# Add a sequence
seq.addSequence('test',[
    ['/step', 1],
    ['/step', 2],
    ['/step', 3, 'extra argument !']
])

# Enale the sequence
send('osc.udp://localhost:12345', '/Sequencer/Sequence/Enable', 'test')

# Start the sequencer
send('osc.udp://localhost:12345', '/Sequencer/Play')

# keep the script running
raw_input('OSC Sequencer: press enter to quit...')

# now listen on port 5555 with your favorite tool...
