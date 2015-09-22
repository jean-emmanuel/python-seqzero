"""
OSC Scenes for pyOSCseq
"""

from time import sleep, time
from liblo import send
from threading import Thread

slide = '/pyta/slide/'
visible = slide+'visible'
alpha = slide+'alpha'
position_x = slide+'position_x'
position_y = slide+'position_y'
translate_x = slide+'translate_x'
load =  slide+'load_state'
pv_animate = slide+'animate'

"""
Animate function for pyOSCseq's osc sending method :
Execute the given function for different values of its last argument,
computed between 'start' and 'end'.
- duration (s) : time to complete the animation
- step (s) : delay between each step
- function : function to animate, most likely 'send' (which is an alias for pyOSCseq.parseOscArgs()
- args : tuple containing the first arguments passed to the function (these won't be animated)
"""
def animate(start,end,duration,step,function,args, mode='float'):
    def threaded(start,end,duration,step,function,args, mode):
        nb_step = int(round(duration/step))
        a = float(end-start)/nb_step
        args.append(0)
        for i in range(nb_step+1):
            args[-1] = a*i+start
            if mode == 'integer':
                args[-1] = int(args[-1])
            function([args])
            if i!=nb_step:
                sleep(step)
    t = Thread(target=threaded, args=([start,end,duration,step,function,args, mode]))
    t.start()

"""
Repeat function for pyOSCseq's osc sending method :
Execute the given function nb_repeat times, and waits interval seconds between each call
"""
def repeat(nb_repeat,interval,function,args):
    def threaded(nb_repeat,interval,function,args):
        for i in range(nb_repeat):
            function([args])
            sleep(interval)
    t = Thread(target=threaded, args=([nb_repeat,interval,function,args]))
    t.start()

"""
Scenes list
The 'send' argument retrieves pyOSCseq osc sending function to dispatch the messages.
    usage : send([path,arg1,arg2])
"""

# Videos
def v_scenes_list(send, name):
    if name == 'Intro_init':
        #Loading slides
        suffix = '.generique.state'
        send([[load,'s0.featuring'+suffix],[load,'s1.jaquie.body'+suffix],[load,'s2.michel.body'+suffix],[load,'s3.michel.head'+suffix],[load,'s5.jaquie.head'+suffix],[load,'s7.the.nots.awful.geminos'+suffix]])
         

    if name == "LoadWhite":
        send([load, 's99.white.state'])

    if name == 'LoadCoffeeNoise':
        for i in [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
            send([load, 's'+str(i)+'.coffeenoise.state'])


    # Acte 0 ##############################
    # Say Hello
    if name == "A0 Say Hello":
            send([pv_animate,79,-700,0,120,.02,'position_y'])
            send([pv_animate,99,0.9,0,120,.02,'alpha'])


# Lights
def l_scenes_list(send, name):
    # Acte I ##############################
    # Intro
    if name == 'Intro':
        # Flash
        send(['/BJ/White/Segment/All', 255])
        send(['/BC/White/Segment/All', 255])
        sleep(0.04)
        send(['/BJ/White/Segment/All', 0])
        send(['/BC/White/Segment/All', 0])


        sleep(22.905)
        # Allumage Violet
        animate(0, 100, 4, 0.04, send,['/CJ/Red/Segment/1'], 'integer')
        animate(0, 100, 4, 0.04, send,['/CC/Red/Segment/1'], 'integer')
        animate(0, 100, 4, 0.04, send,['/CJ/Blue/Segment/1'], 'integer')
        animate(0, 100, 4, 0.04, send,['/CC/Blue/Segment/1'], 'integer')

        sleep(10)
        # Allumage decoupes
        animate(0, 150, 4, 0.04, send, ['/Decoupes/Cour/Dimmer'], 'integer')
        animate(0, 150, 4, 0.04, send, ['/Decoupes/Jardin/Dimmer'], 'integer')

    # Entree des Geminos
    if name == 'Entree Geminos':
        send(['/CJ/Red/Segment/1', 100])
        send(['/CC/Red/Segment/1', 100])        
        send(['/CJ/Blue/Segment/1', 100])
        send(['/CC/Blue/Segment/1', 100])        
        send(['/CJ/Red/Segment/8', 100])
        send(['/CC/Red/Segment/8', 100])        
        send(['/CJ/Blue/Segment/8', 100])
        send(['/CC/Blue/Segment/8', 100])

        send(['/Decoupes/Jardin/Dimmer', 0])
        send(['/Decoupes/Cour/Dimmer', 0])

    # Couplet
    if name == 'Couplet CC':
        sleep(0.15)
        animate(0, 180, 1.6, 0.02, send, ['/CC/Red/Segment/All'], 'integer')
        animate(0, 180, 0.9, 0.02, send, ['/CC/Blue/Segment/All'], 'integer')
        sleep(1)
        animate(180, 0, 0.5, 0.02, send, ['/CC/Blue/Segment/All'], 'integer')
        animate(180, 0, 0.15, 0.02, send, ['/CC/Red/Segment/All'], 'integer')
    if name == 'Couplet CJ':
        sleep(0.15)
        animate(180, 0, 1.6, 0.02, send, ['/CJ/Red/Segment/All'], 'integer')
        animate(180, 0, 0.9, 0.02, send, ['/CJ/Blue/Segment/All'], 'integer')
        sleep(1)
        animate(0, 180, 0.5, 0.02, send, ['/CJ/Blue/Segment/All'], 'integer')
        animate(0, 180, 0.15, 0.02, send, ['/CJ/Red/Segment/All'], 'integer')


    if name == 'AI MathoMag II':
        sleep(0.875)
        send(['/CC/White/Segment/All', 255])
        send(['/CJ/White/Segment/All', 255])
        sleep(0.125)
        send(['/CC/White/Segment/All', 0])
        send(['/CJ/White/Segment/All', 0])
        sleep(1)
        for i in range(4):
            send(['/BC/White/Segment/All', 255])
            send(['/BJ/White/Segment/All', 255])
            sleep(0.125)
            send(['/BC/White/Segment/All', 0])
            send(['/BJ/White/Segment/All', 0])
            sleep(4)

    if name == 'AII HG2':
        for s in ['CC','CJ','BC','BJ']:
            send(['/'+s+'/White/Segment/All',255])
        sleep(.2)
        for s in ['CC','CJ','BC','BJ']:
            animate(255, 0, 1, 0.02, send, ['/'+s+'/White/Segment/All'], 'integer')
        for s in ['CC','CJ','BC','BJ']:
            animate(255, 0, 12.4, 0.4, send, ['/'+s+'/Blue/Segment/All'], 'integer')
        sleep(12.4)
        for s in ['CC','CJ','BC','BJ']:
            send(['/'+s+'/Blue/Segment/All',0])
        sleep(1.2)
        for s in ['CC','CJ','BC','BJ']:
            send(['/'+s+'/Blue/Segment/All',255])
            send(['/'+s+'/White/Segment/All',255])
    	sleep(0.2)
        for s in ['CC','CJ','BC','BJ']:
            send(['/'+s+'/White/Segment/All',0])
        sleep(0.2)
        for s in ['CC','CJ','BC','BJ']:
            send(['/'+s+'/White/Segment/All',255])
    	sleep(0.2)

        send([':/Sequencer/Trigger', 1])
        send([':/Sequencer/Set_bpm', 600])
        send([':/Sequencer/Sequence/Enable', 'AII HGII', 1])

	if name == 'AII MEP':
		send(['/CJ/Blue/Segment/All', 180])
		send(['/CJ/Blue/Segment/8', 240])
		sleep(0.4)
		send(['/CC/Blue/Segment/All', 180])
		send(['/CC/Blue/Segment/8', 240])
		sleep(0.4)
		send(['/BJ/Blue/Segment/All', 180])
		send(['/BJ/Blue/Segment/8', 240])
		sleep(0.4)
		send(['/BC/Blue/Segment/All', 180])
		send(['/BC/Blue/Segment/8', 240])
		sleep(0.2)
		send(['/Decoupes/Jeannot/Dimmer', 255])

# Audio
def a_scenes_list(send, name):
    if name == 'Intro':
        send(['/Sequencer/Intro', 127])
        #send(['/pedalBoard/button', 4])

        sleep(22.909)
        send(['/pedalBoard/button', 2])        

# Main
def m_scenes_list(send, name):
    if name == "Debut":
        send(['/Sequencer/Play'])
        send(['/Sequencer/Scene/Play', 'Intro'])
