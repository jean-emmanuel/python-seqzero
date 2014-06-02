from pyOSCseq import *
from scenessc import scenes_list

# sequencer creation
seq = pyOSCseq(640,123451,'192.168.0.112:56418 192.168.0.112:7770 localhost:5555',scenes_list)


# sequences creation


# Run
seq.play()
