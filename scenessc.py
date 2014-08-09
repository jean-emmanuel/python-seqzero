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

"""
Animate function for pyOSCseq's osc sending method :
Execute the given function for different values of its last argument,
computed between 'start' and 'end'.
- duration (s) : time to complete the animation
- step (s) : delay between each step
- function : function to animate, most likely 'send' (which is an alias for pyOSCseq.parseOscArgs()
- args : tuple containing the first arguments passed to the function (these won't be animated)
"""
def animate(start,end,duration,step,function,args):
    def threaded(start,end,duration,step,function,args):
        nb_step = int(round(duration/step))
        a = float(end-start)/nb_step
        args.append(0)
        for i in range(nb_step+1):
            args[-1] = a*i+start
            function([args])
            if i!=nb_step:
                sleep(step)
    t = Thread(target=threaded, args=([start,end,duration,step,function,args]))
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

# Vidéos
def v_scenes_list(send, name):
    if name == 'Intro_init':
        #Loading slides
        suffix = '.generique.state'
        send([[load,'s0.featuring'+suffix],[load,'s1.jaquie.body'+suffix],[load,'s2.michel.body'+suffix],[load,'s3.michel.head'+suffix],[load,'s5.jaquie.head'+suffix],[load,'s7.the.nots.awful.geminos'+suffix]])
         
    if name == 'Intro_generique':
        #Generique

        for i in [0,1,2,3,5,7]:
            send([visible,i,1])

        animate(-1000,0,.2,.02,send,[position_x,0])
        
        sleep(1)
        
        for i in [1,2,3,5]:
            repeat(100,.015,send,[translate_x,i,-8.4])
        
        sleep(0.15)

        
        animate(100,200,.1,.02,send,[position_y,0])

        sleep(1)
        

        
        for i in [2,3]:
            repeat(120,.015,send,[translate_x,i,-1])
        
        sleep(1.8)
        
        animate(0,1,.3,.01,send,[alpha,7])
        

# Lights
def l_scenes_list(send, name):
    pass
