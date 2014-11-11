from pyOSCseq import *
from scenessc import a_scenes_list

a_seq = pyOSCseq(110, 12344, 'localhost:56418 localhost:5554', a_scenes_list)


################# Acte I ##############################

# Intro

a_seq.play()
