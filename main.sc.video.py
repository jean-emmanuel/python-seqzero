from pyOSCseq import *
from scenessc import v_scenes_list

v_seq = pyOSCseq(110, 12346, 'localhost:5556 192.168.0.112:56418 192.168.0.112:56417', v_scenes_list)


################# GENERIQUES ##########################

# CoffeeNoise
v_seq.addSequence('CoffeeNoise', [
    [['/pyta/slide/visible', 0, 1], ['/pyta/slide/visible', 3, 0]],
    [['/pyta/slide/visible', 1, 1], ['/pyta/slide/visible', 0, 0]],
    [['/pyta/slide/visible', 2, 1], ['/pyta/slide/visible', 1, 0]],
    [['/pyta/slide/visible', 3, 1], ['/pyta/slide/visible', 2, 0]]
])


################# Acte I ##############################

# Intro


v_seq.play()
