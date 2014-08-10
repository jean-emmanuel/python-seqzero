from pyOSCseq import *
from scenessc import l_scenes_list

l_seq = pyOSCseq(150,12345,'localhost:7770 localhost:5555',l_scenes_list)


################# Acte I ##############################

# Intro

l_seq.addSequence('FSF Bourrin',[
    ['/BC/White/Segment/1', 255],
    ['/BC/White/Segment/1', 0]
])




l_seq.play()
