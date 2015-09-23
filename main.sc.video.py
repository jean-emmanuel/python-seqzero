from pyOSCseq import *
from scenessc import v_scenes_list

v_seq = pyOSCseq(110, 12346, 'localhost:5556 192.168.0.112:56418 192.168.0.112:56417', v_scenes_list)


################# GENERIQUES ##########################

# CoffeeNoise

v_seq.addRandomSequence('CoffeeNoise', [
    [['/pyta/slide/visible', 80, 1], ['/pyta/slide/visible', 81, 0], ['/pyta/slide/visible', 82, 0], ['/pyta/slide/visible', 83, 0]],
    [['/pyta/slide/visible', 81, 1], ['/pyta/slide/visible', 80, 0], ['/pyta/slide/visible', 82, 0], ['/pyta/slide/visible', 83, 0]],
    [['/pyta/slide/visible', 82, 1], ['/pyta/slide/visible', 80, 0], ['/pyta/slide/visible', 81, 0], ['/pyta/slide/visible', 83, 0]],
    [['/pyta/slide/visible', 83, 1], ['/pyta/slide/visible', 80, 0], ['/pyta/slide/visible', 81, 0], ['/pyta/slide/visible', 82, 0]],
], 44)



################# Acte 0 ##############################

# Refrain
v_seq.addRandomSequence('A0 Refrain Alpha', [
    [['/pyta/slide/alpha', 79, 1]],
    [['/pyta/slide/alpha', 79, 0.99]],
    [['/pyta/slide/alpha', 79, 0.98]],
    [['/pyta/slide/alpha', 79, 0.97]],
    [['/pyta/slide/alpha', 79, 0.96]],
    [['/pyta/slide/alpha', 79, 0.95]],
    [['/pyta/slide/alpha', 79, 0.94]],
    [['/pyta/slide/alpha', 79, 0.93]],
    [['/pyta/slide/alpha', 79, 0.92]],
    [['/pyta/slide/alpha', 79, 0.91]],
    [['/pyta/slide/alpha', 79, 0.90]],
    [['/pyta/slide/alpha', 79, 0.89]],
    [['/pyta/slide/alpha', 79, 0.88]],
    [['/pyta/slide/alpha', 79, 0.87]],
    [['/pyta/slide/alpha', 79, 0.86]],
    [['/pyta/slide/alpha', 79, 0.85]],
    [['/pyta/slide/alpha', 79, 0.84]]
],45)


# Say Hello

v_seq.addSequence('A0 Say Hello', [
    ['/pyta/slide/visible', 79, 1],
    [],
])

v_seq.addSequence('A0 Say Hello Alpha', [
    ['/pyta/slide/alpha', 79, 1],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3], 
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3], # VP Jardin alpha a 1
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3], # VP Jardin alpha a 1
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 1],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 1],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3],
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3], # VP Cour alpha a 1
    ['/pyta/slide/alpha', 79, 0],
    ['/pyta/slide/alpha', 79, 0.3], # VP Jardin alpha a 1
    ['/pyta/slide/alpha', 79, 0],
])


################# Acte 1 ##############################
# Gals
v_seq.addRandomSequence('A1 Gals Grouille', [
    ['/pyta/slide/scale', 79, 805, 800, 0],
    ['/pyta/slide/scale', 79, 800, 800, 0],
    ['/pyta/slide/scale', 79, 800, 805, 0],
    ['/pyta/slide/scale', 79, 800, 800, 0],
], 128)

# Strange World sortie Reggae
v_seq.addSequence('A1 StrangeWorld Sortie Reggae', [
    ['/pyta/slide/rotate_z', 79, 0],
    ['/pyta/slide/rotate_z', 79, 90],
    ['/pyta/slide/rotate_z', 79, 180],
    ['/pyta/slide/rotate_z', 79, 270]
])

# Liba Libanese
v_seq.addSequence('A1 Liba Libanese', [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],

    ['/pyta/slide/visible', 80, 1],
    ['/pyta/slide/visible', 80, 0],
    ['/pyta/slide/visible', 81, 1],
    ['/pyta/slide/visible', 81, 0],

    [],
    [],
    [],
    [],

    [],
    ['/pyta/slide/visible', 82, 1],
    [['/pyta/slide/visible', 83, 1],['/pyta/slide/visible', 82, 0]],
    [['/pyta/slide/visible', 82, 0],['/pyta/slide/visible', 83, 0]],


    [],
    ['/pyta/slide/visible', 84, 1],
    [['/pyta/slide/visible', 85, 1],['/pyta/slide/visible', 84, 0]],
    [['/pyta/slide/visible', 84, 0],['/pyta/slide/visible', 85, 0]],

    [],
    [],

    ['/pyta/slide/visible', 85, 1],
    ['/pyta/slide/visible', 85, 0],

    ['/pyta/slide/visible', 86, 1],
    ['/pyta/slide/visible', 86, 0],

    [],
    [],

    [],
    ['/pyta/slide/visible', 87, 1],
    [['/pyta/slide/visible', 88, 1],['/pyta/slide/visible', 87, 0]],
    [['/pyta/slide/visible', 87, 0],['/pyta/slide/visible', 88, 0]],


    [],
    ['/pyta/slide/visible', 89, 1],
    [['/pyta/slide/visible', 80, 1],['/pyta/slide/visible', 89, 0]],
    [['/pyta/slide/visible', 89, 0],['/pyta/slide/visible', 80, 0]],

    [],
    [],
    ['/pyta/slide/visible', 85, 1],
    ['/pyta/slide/visible', 85, 0],

    [],
    [],
    [],
    [],

    [],
    ['/pyta/slide/visible', 82, 1],
    [['/pyta/slide/visible', 83, 1],['/pyta/slide/visible', 82, 0]],
    [['/pyta/slide/visible', 82, 0],['/pyta/slide/visible', 83, 0]],


    [],
    ['/pyta/slide/visible', 84, 1],
    [['/pyta/slide/visible', 85, 1],['/pyta/slide/visible', 84, 0]],
    [['/pyta/slide/visible', 84, 0],['/pyta/slide/visible', 85, 0]],

    [],
    [],
    ['/pyta/slide/visible', 86, 1],
    ['/pyta/slide/visible', 86, 0],

    ['/pyta/slide/visible', 87, 1],
    ['/pyta/slide/visible', 87, 0],
    [],
    [],

    [],
    ['/pyta/slide/visible', 88, 1],
    ['/pyta/slide/visible', 89, 1],
    [['/pyta/slide/visible', 88, 0],['/pyta/slide/visible', 89, 0]],

    ['/pyta/slide/visible', 80, 1],
    [['/pyta/slide/visible', 81, 1], ['/pyta/slide/visible', 80, 0]],
    [['/pyta/slide/visible', 82, 1], ['/pyta/slide/visible', 81, 0]],
    [['/pyta/slide/visible', 82, 0]],

    ['/pyta/slide/visible', 83, 1],
    [['/pyta/slide/visible', 84, 1], ['/pyta/slide/visible', 83, 0]],
    [['/pyta/slide/visible', 85, 1], ['/pyta/slide/visible', 84, 0]],
    [['/pyta/slide/visible', 85, 0], [':/Sequencer/DisableAll',1], [':/Sequencer/Sequence/Enable','AI Mathomag 1',1]], 
])

v_seq.play()
