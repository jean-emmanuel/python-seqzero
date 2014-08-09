from pyOSCseq import *
from scenessc import l_scenes_list

l_seq = pyOSCseq(150,12345,'localhost:7770 localhost:5555',l_scenes_list)


################# Acte I ##############################

# Intro

l_seq.addSequence('',[
    ['/BC/Red/Segment/1', 100],
    ['/BC/Red/Segment/1', 0]
])




l_seq.play()

