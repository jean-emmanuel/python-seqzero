"""
OSC Scenes for pyOSCseq
"""

from time import sleep, time

slide = '/pyta/slide/'
visible = slide+'visible'
alpha = slide+'alpha'
position_x = slide+'position_x'
position_y = slide+'position_y'
translate_x = slide+'translate_x'
load =  slide+'load_state'


"""
Scenes list
The 'send' argument retrieves pyOSCseq osc sending function to dispatch the messages.
    usage : send([path,arg1,arg2])
"""
def scenes_list(sequencer, name):
    send = sequencer.parseOscArgs
    animate = sequencer.animate
    repeat = sequencer.repeat

    if name == 'Intro_init':
        #Loading slides
        suffix = '.generique.state'
        send([[load,'s0.featuring'+suffix],[load,'s1.jaquie.body'+suffix],[load,'s2.michel.body'+suffix],[load,'s3.michel.head'+suffix],[load,'s5.jaquie.head'+suffix],[load,'s7.the.nots.awful.geminos'+suffix]])

    if name == 'Intro_generique':
        #Generique

        for i in [0,1,2,3,5,7]:
            send([visible,i,1])

        animate(-1000,0,.2,.02,send,[position_x,0])

        sleep(0.3)

        for i in [1,2,3,5]:
            repeat(10,.2,send,[translate_x,i,-84])

        sleep(0.15)

        animate(100,200,.1,.02,send,[position_y,0])

        sleep(1)

        for i in [2,3]:
            repeat(12,.2,send,[translate_x,i,-10])

        sleep(1.8)

        animate(0,1,.3,.01,send,[alpha,7])
