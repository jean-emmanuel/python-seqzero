from pyOSCseq import *
from scenessc import m_scenes_list

m_seq = pyOSCseq(110, 12343, 'localhost:12344 localhost:12345 localhost:12346 localhost:5553', m_scenes_list)

################# Acte I ##############################

# Intro


print "Launching the main sequencer"
m_seq.play()


