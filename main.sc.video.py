from pyOSCseq import *
from scenessc import v_scenes_list

v_seq = pyOSCseq(110, 12346, 'localhost:5556', v_scenes_list)


################# Acte I ##############################

# Intro

v_seq.play()
