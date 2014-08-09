from pyOSCseq import *
from scenes_sc_lights import l_scenes_list

# sequencer creation
l_seq = pyOSCseq(640,123451,'192.168.0.112:56418 192.168.0.112:7770 localhost:5555',l_scenes_list)


# sequences creation
l_seq.addSequence('test',[
    [':/Sequencer/Scene/Play', 'Intro_generique'],
    [':/Sequencer/Sequence/Stop', 'test']
])

# Run
l_seq.play()
