from pyOSCseq import *
from scenessc import l_scenes_list

#l_seq = pyOSCseq(440,12345,'127.0.0.1:7777',l_scenes_list)

l_seq = pyOSCseq(440,12345,'192.168.0.13:7770',l_scenes_list)

################# Acte 0 ##############################

# Intro

l_seq.addSequence('FSF Bourrin',[
    [['/CC/Red/Segment/1', 180],    ['/CC/Red/Segment/8', 180],    ['/CJ/Red/Segment/1', 180],    ['/CJ/Red/Segment/8', 180],    ['/CC/Red/Segment/4', 0],    ['/CC/Red/Segment/5', 0],    ['/CJ/Red/Segment/4', 0],    ['/CJ/Red/Segment/5', 0], ['/CC/Blue/Segment/1', 180],    ['/CC/Blue/Segment/8', 180],    ['/CJ/Blue/Segment/1', 180],    ['/CJ/Blue/Segment/8', 180],    ['/CC/Blue/Segment/4', 0],    ['/CC/Blue/Segment/5', 0],    ['/CJ/Blue/Segment/4', 0],    ['/CJ/Blue/Segment/5', 0]],
    [],
    [],
    [],
    [],
    [],
    [['/CC/Red/Segment/1', 0],    ['/CC/Red/Segment/8', 0],    ['/CJ/Red/Segment/1', 0],    ['/CJ/Red/Segment/8', 0],    ['/CC/Red/Segment/4', 180],    ['/CC/Red/Segment/5', 180],    ['/CJ/Red/Segment/4', 180],    ['/CJ/Red/Segment/5', 180], ['/CC/Blue/Segment/1', 0],    ['/CC/Blue/Segment/8', 0],    ['/CJ/Blue/Segment/1', 0],    ['/CJ/Blue/Segment/8', 0],    ['/CC/Blue/Segment/4', 180],    ['/CC/Blue/Segment/5', 180],    ['/CJ/Blue/Segment/4', 180],    ['/CJ/Blue/Segment/5', 180]],
    [],
    [],
    [],
    [],
    [],
    [['/CC/Red/Segment/1', 180],    ['/CC/Red/Segment/8', 180],    ['/CJ/Red/Segment/1', 180],    ['/CJ/Red/Segment/8', 180],    ['/CC/Red/Segment/4', 0],    ['/CC/Red/Segment/5', 0],    ['/CJ/Red/Segment/4', 0],    ['/CJ/Red/Segment/5', 0], ['/CC/Blue/Segment/1', 180],    ['/CC/Blue/Segment/8', 180],    ['/CJ/Blue/Segment/1', 180],    ['/CJ/Blue/Segment/8', 180],    ['/CC/Blue/Segment/4', 0],    ['/CC/Blue/Segment/5', 0],    ['/CJ/Blue/Segment/4', 0],    ['/CJ/Blue/Segment/5', 0]],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [['/BJ/White/Segment/All', 255],     ['/CC/Red/Segment/1', 0],    ['/CC/Red/Segment/8', 0],    ['/CJ/Red/Segment/1', 0],    ['/CJ/Red/Segment/8', 0],    ['/CC/Red/Segment/4', 180],    ['/CC/Red/Segment/5', 180],    ['/CJ/Red/Segment/4', 180],    ['/CJ/Red/Segment/5', 180], ['/CC/Blue/Segment/1', 0],    ['/CC/Blue/Segment/8', 0],    ['/CJ/Blue/Segment/1', 0],    ['/CJ/Blue/Segment/8', 0],    ['/CC/Blue/Segment/4', 180],    ['/CC/Blue/Segment/5', 180],    ['/CJ/Blue/Segment/4', 180],    ['/CJ/Blue/Segment/5', 180]],
    [['/BC/White/Segment/All', 255], ['/BJ/White/Segment/All', 0]],
    ['/BC/White/Segment/All', 0],
    [],
    ['/BJ/White/Segment/All', 0],
    [['/BC/White/Segment/All', 0], ['/BJ/White/Segment/All', 0]],
])


# Theme

l_seq.addSequence('Theme',[
    [['/BC/White/Segment/All', 255], ['/BJ/White/Segment/All', 255]],
    [['/BC/White/Segment/All', 0], ['/BJ/White/Segment/All', 0]],
    [['/BC/White/Segment/All', 255], ['/BJ/White/Segment/All', 255]],
    [['/BC/White/Segment/All', 0], ['/BJ/White/Segment/All', 0]],
    [],
    [['/CC/Blue/Segment/7', 100], ['/CJ/Blue/Segment/7', 100], ['/CC/Blue/Segment/2', 100], ['/CJ/Blue/Segment/2', 100]],
    [['/CC/Blue/Segment/7', 0], ['/CJ/Blue/Segment/7', 0],     ['/CC/Blue/Segment/2', 0], ['/CJ/Blue/Segment/2', 0]],
    [['/CC/Blue/Segment/6', 100], ['/CJ/Blue/Segment/3', 100], ['/CC/Blue/Segment/3', 100], ['/CJ/Blue/Segment/6', 100]],
    [['/CC/Blue/Segment/6', 0], ['/CJ/Blue/Segment/3', 0],     ['/CC/Blue/Segment/3', 0], ['/CJ/Blue/Segment/6', 0]],
    [],
    [['/CC/Blue/Segment/5', 100], ['/CJ/Blue/Segment/5', 100], ['/CC/Blue/Segment/4', 100], ['/CJ/Blue/Segment/2', 100]],
    [['/CC/Blue/Segment/5', 0], ['/CJ/Blue/Segment/5', 0],     ['/CC/Blue/Segment/4', 0], ['/CJ/Blue/Segment/2', 0]],
    [['/CC/Blue/Segment/2', 100], ['/CJ/Blue/Segment/4', 100], ['/CC/Blue/Segment/5', 100], ['/CJ/Blue/Segment/4', 100]],
    [['/CC/Blue/Segment/2', 0], ['/CJ/Blue/Segment/4', 0],     ['/CC/Blue/Segment/5', 0], ['/CJ/Blue/Segment/4', 0]],

])

# Couplet
l_seq.addSequence('Couplet',[
        [[':/Sequencer/Scene/Play', 'Couplet CJ'],        [':/Sequencer/Scene/Play', 'Couplet CC']],
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
        []
])


################# Acte I ##############################

# Couplet
l_seq.addSequence('AI Couplet',[
    [['/CC/White/Segment/1', 255], ['/CJ/White/Segment/1', 255]],
    [['/CC/White/Segment/1', 0], ['/CJ/White/Segment/1', 0]],        
])

# Pont Guitare

l_seq.addSequence('AI Pont Guitare',[
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

    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],

    [],
    [],
    [],
    [],

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],

    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],
    [],
    [],

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],

    [],
    [],
    [],
    [],

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],    

    [],
    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],

    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 0]],
    [],
    [],

    [],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],    

    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    [['/CC/Green/Segment/All', 0], ['/CJ/Green/Segment/All', 255]],
    [['/CC/Green/Segment/All', 255], ['/CJ/Green/Segment/All', 0]],
    
    [['/CC/Green/Segment/All', 0],['/CC/White/Segment/All', 255], ['/CJ/White/Segment/All', 255]],
    [['/CC/White/Segment/All', 0], ['/CJ/White/Segment/All', 0]],
    [['/CC/White/Segment/All', 255], ['/CJ/White/Segment/All', 255]],
    [['/CC/White/Segment/All', 0], ['/CJ/White/Segment/All', 0], [':/Sequencer/DisableAll',1], [':/Sequencer/Sequence/Enable','AI Mathomag 2',1]],  
])


l_seq.addSequence('AI Mathomag 2',[
    [],

    [],
    [['/CC/Red/Segment/All', 255], ['/CJ/Red/Segment/All', 255]], ##
    [['/CC/Red/Segment/All', 0], ['/CJ/Red/Segment/All', 0]],
    [],
    
    [], #
    [],
    [],
    [],
    
    [],
    [],
    [], ##
    [],
    
    [], #
    [], ##
    []
])

l_seq.addSequence('AI Metal',[
        [['/BC/White/Segment/All',230],['/BJ/White/Segment/All',230]],
        [['/BC/White/Segment/All',30],['/BJ/White/Segment/All',30]]
])

l_seq.addSequence('AI Forain',[
        [['/CC/Red/Segment/All',255],['/CC/Green/Segment/All',255],['/CJ/Red/Segment/All',255],['/CJ/Green/Segment/All',255]],
        [],
        [['/CC/Red/Segment/All',0],['/CC/Green/Segment/All',0],['/CJ/Red/Segment/All',0],['/CJ/Green/Segment/All',0]],
        [['/CC/Red/Segment/All',255],['/CC/Green/Segment/All',255],['/CJ/Red/Segment/All',255],['/CJ/Green/Segment/All',255]],
        [],
        [['/CC/Red/Segment/All',0],['/CC/Green/Segment/All',0],['/CJ/Red/Segment/All',0],['/CJ/Green/Segment/All',0]],
        [['/CC/Red/Segment/All',255],['/CC/Green/Segment/All',255],['/CJ/Red/Segment/All',255],['/CJ/Green/Segment/All',255]],
        [],
        [['/CC/Red/Segment/All',0],['/CC/Green/Segment/All',0],['/CJ/Red/Segment/All',0],['/CJ/Green/Segment/All',0]],
        [['/CC/Red/Segment/All',255],['/CC/Green/Segment/All',255],['/CJ/Red/Segment/All',255],['/CJ/Green/Segment/All',255]],
        [],[],[],[],[],
        [['/CC/Red/Segment/All',0],['/CC/Green/Segment/All',0],['/CJ/Red/Segment/All',0],['/CJ/Green/Segment/All',0]],

])

l_seq.addSequence('AII HGII',[
        [],
        [],
        [['/CJ/White/Segment/All',255],['/CC/White/Segment/All',255],['/BJ/White/Segment/All',255],['/BC/White/Segment/All',255]],
        [['/CJ/White/Segment/All',0],['/CC/White/Segment/All',0],['/BJ/White/Segment/All',0],['/BC/White/Segment/All',0]],
        [],
        [],
        [['/CJ/White/Segment/All',255],['/CC/White/Segment/All',255],['/BJ/White/Segment/All',255],['/BC/White/Segment/All',255]],
        [['/CJ/White/Segment/All',0],['/CC/White/Segment/All',0],['/BJ/White/Segment/All',0],['/BC/White/Segment/All',0]],
        [],
        [],
        [['/CJ/White/Segment/All',255],['/CC/White/Segment/All',255],['/BJ/White/Segment/All',255],['/BC/White/Segment/All',255]],
        [['/CJ/White/Segment/All',0],['/CC/White/Segment/All',0],['/BJ/White/Segment/All',0],['/BC/White/Segment/All',0]],
        [],
        [],
        [],
        [],

])

l_seq.addSequence('AII Chase1',[
        [       ['/CJ/Blue/Segment/1',255],['/CJ/Blue/Segment/3',255],['/CJ/Blue/Segment/5',255],['/CJ/Blue/Segment/7',255],
                ['/CJ/Green/Segment/2',0],['/CJ/Green/Segment/4',0],['/CJ/Green/Segment/6',0],['/CJ/Green/Segment/8',0],
                ['/CC/Blue/Segment/1',255],['/CC/Blue/Segment/3',255],['/CC/Blue/Segment/5',255],['/CC/Blue/Segment/7',255],
                ['/CC/Green/Segment/2',0],['/CC/Green/Segment/4',0],['/CC/Green/Segment/6',0],['/CC/Green/Segment/8',0]
        ],
        [       ['/CJ/Blue/Segment/1',0],['/CJ/Blue/Segment/3',0],['/CJ/Blue/Segment/5',0],['/CJ/Blue/Segment/7',0],
                ['/CJ/Green/Segment/2',255],['/CJ/Green/Segment/4',255],['/CJ/Green/Segment/6',255],['/CJ/Green/Segment/8',255],
                ['/CC/Blue/Segment/1',0],['/CC/Blue/Segment/3',0],['/CC/Blue/Segment/5',0],['/CC/Blue/Segment/7',0],
                ['/CC/Green/Segment/2',255],['/CC/Green/Segment/4',255],['/CC/Green/Segment/6',255],['/CC/Green/Segment/8',255]
        ]

])

l_seq.addSequence('AII Chase2',[
        [
                ['/BJ/Blue/Segment/1',255],['/BJ/Green/Segment/1',255],['/BC/Blue/Segment/1',255],['/BC/Green/Segment/1',255],
                ['/BJ/Blue/Segment/8',0],['/BJ/Green/Segment/8',0],['/BC/Blue/Segment/8',0],['/BC/Green/Segment/8',0]
        ],
        [
                ['/BJ/Blue/Segment/2',255],['/BJ/Green/Segment/2',255],['/BC/Blue/Segment/2',255],['/BC/Green/Segment/2',255],
                ['/BJ/Blue/Segment/1',0],['/BJ/Green/Segment/1',0],['/BC/Blue/Segment/1',0],['/BC/Green/Segment/1',0]
        ],
        [
                ['/BJ/Blue/Segment/3',255],['/BJ/Green/Segment/3',255],['/BC/Blue/Segment/3',255],['/BC/Green/Segment/3',255],
                ['/BJ/Blue/Segment/2',0],['/BJ/Green/Segment/2',0],['/BC/Blue/Segment/2',0],['/BC/Green/Segment/2',0]
        ],
        [
                ['/BJ/Blue/Segment/4',255],['/BJ/Green/Segment/4',255],['/BC/Blue/Segment/4',255],['/BC/Green/Segment/4',255],
                ['/BJ/Blue/Segment/3',0],['/BJ/Green/Segment/3',0],['/BC/Blue/Segment/3',0],['/BC/Green/Segment/3',0]
        ],
        [
                ['/BJ/Blue/Segment/5',255],['/BJ/Green/Segment/5',255],['/BC/Blue/Segment/5',255],['/BC/Green/Segment/5',255],
                ['/BJ/Blue/Segment/4',0],['/BJ/Green/Segment/4',0],['/BC/Blue/Segment/4',0],['/BC/Green/Segment/4',0]
        ],
        [
                ['/BJ/Blue/Segment/6',255],['/BJ/Green/Segment/6',255],['/BC/Blue/Segment/6',255],['/BC/Green/Segment/6',255],
                ['/BJ/Blue/Segment/5',0],['/BJ/Green/Segment/5',0],['/BC/Blue/Segment/5',0],['/BC/Green/Segment/5',0]
        ],
        [
                ['/BJ/Blue/Segment/7',255],['/BJ/Green/Segment/7',255],['/BC/Blue/Segment/7',255],['/BC/Green/Segment/7',255],
                ['/BJ/Blue/Segment/6',0],['/BJ/Green/Segment/6',0],['/BC/Blue/Segment/6',0],['/BC/Green/Segment/6',0]
        ],
        [
                ['/BJ/Blue/Segment/8',255],['/BJ/Green/Segment/8',255],['/BC/Blue/Segment/8',255],['/BC/Green/Segment/8',255],
                ['/BJ/Blue/Segment/7',0],['/BJ/Green/Segment/7',0],['/BC/Blue/Segment/7',0],['/BC/Green/Segment/7',0]
        ],

])

l_seq.addSequence('AII Chase3',[
        [
                ['/Decoupes/Jardin/Dimmer',255],['/Decoupes/Cour/Dimmer',0]
        ],
        [
                ['/Decoupes/Jardin/Dimmer',0],['/Decoupes/Cour/Dimmer',255]
        ]
])

l_seq.addSequence('AII Chase4',[
        [
                ['/CJ/Green/Segment/1',255],['/CC/Green/Segment/1',255],
                ['/CJ/Green/Segment/8',0],['/CC/Green/Segment/8',0]
        ],
        [
                ['/CJ/Green/Segment/2',255],['/CC/Green/Segment/2',255],
                ['/CJ/Green/Segment/1',0],['/CC/Green/Segment/1',0]
        ],
        [
                ['/CJ/Green/Segment/3',255],['/CC/Green/Segment/3',255],
                ['/CJ/Green/Segment/2',0],['/CC/Green/Segment/2',0]
        ],
        [
                ['/CJ/Green/Segment/4',255],['/CC/Green/Segment/4',255],
                ['/CJ/Green/Segment/3',0],['/CC/Green/Segment/3',0]
        ],
        [
                ['/CJ/Green/Segment/5',255],['/CC/Green/Segment/5',255],
                ['/CJ/Green/Segment/4',0],['/CC/Green/Segment/4',0]
        ],
        [
                ['/CJ/Green/Segment/6',255],['/CC/Green/Segment/6',255],
                ['/CJ/Green/Segment/5',0],['/CC/Green/Segment/5',0]
        ],
        [
                ['/CJ/Green/Segment/7',255],['/CC/Green/Segment/7',255],
                ['/CJ/Green/Segment/6',0],['/CC/Green/Segment/6',0]
        ],
        [
                ['/CJ/Green/Segment/8',255],['/CC/Green/Segment/8',255],
                ['/CJ/Green/Segment/7',0],['/CC/Green/Segment/7',0]
        ],

])

l_seq.addSequence('AII Chase5',[
        [
                ['/BC/White/Segment/All',255],['/BJ/White/Segment/All',255]
        ],
        [
                ['/BC/White/Segment/All',0],['/BJ/White/Segment/All',0]
        ],
        []
])

l_seq.addSequence('AII Chase6',[
        [
                ['/CJ/White/Segment/1',255],['/CC/White/Segment/1',255],
                ['/CJ/White/Segment/8',0],['/CC/White/Segment/8',0]
        ],
        [
                ['/CJ/White/Segment/2',255],['/CC/White/Segment/2',255],
                ['/CJ/White/Segment/1',0],['/CC/White/Segment/1',0]
        ],
        [
                ['/CJ/White/Segment/3',255],['/CC/White/Segment/3',255],
                ['/CJ/White/Segment/2',0],['/CC/White/Segment/2',0]
        ],
        [
                ['/CJ/White/Segment/4',255],['/CC/White/Segment/4',255],
                ['/CJ/White/Segment/3',0],['/CC/White/Segment/3',0]
        ],
        [
                ['/CJ/White/Segment/5',255],['/CC/White/Segment/5',255],
                ['/CJ/White/Segment/4',0],['/CC/White/Segment/4',0]
        ],
        [
                ['/CJ/White/Segment/6',255],['/CC/White/Segment/6',255],
                ['/CJ/White/Segment/5',0],['/CC/White/Segment/5',0]
        ],
        [
                ['/CJ/White/Segment/7',255],['/CC/White/Segment/7',255],
                ['/CJ/White/Segment/6',0],['/CC/White/Segment/6',0]
        ],
        [
                ['/CJ/White/Segment/8',255],['/CC/White/Segment/8',255],
                ['/CJ/White/Segment/7',0],['/CC/White/Segment/7',0]
        ],

])

l_seq.play()
