from pyOSCseq import *
from scenessc import l_scenes_list

l_seq = pyOSCseq(440,12345,'localhost:7770',l_scenes_list)


################# Acte I ##############################

# Intro

l_seq.addSequence('FSF Bourrin',[
    ['/BC/White/Segment/1', 255],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 255],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 255],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/BC/White/Segment/1', 20],
    ['/BC/White/Segment/1', 0],
    ['/CJ/White/Segment/All', 255],
    [['/CC/White/Segment/All', 255], ['/CJ/White/Segment/All', 0]],
    [['/CC/White/Segment/All', 0],['/BC/White/Segment/1', 255]],
    ['/BC/White/Segment/1', 0],
    ['/CJ/White/Segment/All', 255],
    [['/CC/White/Segment/All', 255], ['/CJ/White/Segment/All', 0]],
])




l_seq.play()
