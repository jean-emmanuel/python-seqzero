from pyOSCseq import *
from scenessc import v_scenes_list

v_seq = pyOSCseq(110, 12346, 'localhost:5556 192.168.0.112:56418 192.168.0.112:56417', v_scenes_list)


################# GENERIQUES ##########################

# CoffeeNoise
v_seq.addSequence('CoffeeNoise', [
    [['/pyta/slide/visible', 80, 1], ['/pyta/slide/visible', 83, 0]],
    [['/pyta/slide/visible', 81, 1], ['/pyta/slide/visible', 80, 0]],
    [['/pyta/slide/visible', 82, 1], ['/pyta/slide/visible', 81, 0]],
    [['/pyta/slide/visible', 83, 1], ['/pyta/slide/visible', 82, 0]],
])


################# Acte I ##############################

# Intro


v_seq.play()
