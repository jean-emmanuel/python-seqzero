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

#duration & step en secondes
def line(start,end,duration,step,function,args):

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

        line(-1000,0,.2,.02,send,[position_x,0])
        

