from pyOSCseq import *
from scenes import scenes_list

seq = pyOSCseq(640,123451,'192.168.1.82:56418 192.168.1.82:7770 localhost:5555',scenes_list)



seq.addSequence('test',[
    [':/Sequencer/Scene/Play', 'Intro_generique'],
    [':/Sequencer/Sequence/Stop', 'test']
])

seq.play()
