"""
OSC Scenes for pyOSCseq
"""

from time import sleep, time
from liblo import send
from threading import Thread

slide = '/pyta/slide/'
visible = slide+'visible'
position_x = slide+'position_x'
load =  slide+'load_state'

"""
Animate function for pyOSCseq's osc sending method :
Execute the given function for different values of its last argument,
computed between 'start' and 'end'.
- duration (s) : time to complete the animation
- step (s) : delay between each step
- function : function to animate, most likely 'send' (which is an alias for pyOSCseq.parseOscArgs()
- args : tuple containing the first arguments passed to the function
"""
def animate(start,end,duration,step,function,args):
    def threaded(start,end,duration,step,function,args):
        nb_step = int(round(duration/step))
        a = float(end-start)/nb_step
        args.append(0)
        print nb_step
        for i in range(nb_step+1):
            args[-1] = a*i+start
            print a*i+start
            function([args])
            if i!=nb_step:
                sleep(step)
    t = Thread(target=threaded, args=([start,end,duration,step,function,args]))
    t.start()
            
"""
Scenes list
The 'send' argument retrieves pyOSCseq osc sending function to dispatch the messages.
    usage : send([path,arg1,arg2])
"""
def scenes_list(send, name):
    if name == 'Intro_init':
        #Loading slides
        suffix = '.generique.state'
        send([[load,'s0.featuring'+suffix],[load,'s1.jaquie.body'+suffix],[load,'s2.michel.body'+suffix],[load,'s3.michel.head'+suffix],[load,'s5.jaquie.head'+suffix],[load,'s7.the.nots.awful.geminos'+suffix],[load,'s0.featuring'+suffix]])
         
    if name == 'Intro_generique':
        #Generique
        """
        for i in [0,1,2,3,5,7]:
            send([visible,i,1])
        """

        animate(-1000,0,.2,.02,send,[position_x,0])
        

