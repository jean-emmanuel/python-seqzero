from pyOSCseq import *
from scenessc import l_scenes_list, v_scenes_list, a_scenes_list, m_scenes_list

v_seq = pyOSCseq(110, 12346, 'localhost:5556', v_scenes_list)
l_seq = pyOSCseq(110, 12345, 'localhost:7770 localhost:5555', l_scenes_list)
a_seq = pyOSCseq(110, 12344, 'scson:56418 scson:5554 localhost:5554', a_scenes_list)
m_seq = pyOSCseq(110, 12343, 'localhost:12344 localhost:12345 localhost:12346 localhost:5553', m_scenes_list)

################# Acte I ##############################

# Intro

l_seq.addSequence('FSF Bourrin',[
    ['/BC/White/Segment/1', 255],
    ['/BC/White/Segment/1', 0]
])



while True:
    pass
print "Launching the main sequencer"
m_seq.play()


