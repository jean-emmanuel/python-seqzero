from time import sleep , time
import liblo as _liblo
from random import random
from multiprocessing import *
from os import urandom, kill
from signal import SIGTERM


class pyOSCseq(object):
    def __init__(self,bpm,port,target,scenes_list):
        self.bpm = bpm
        self.port = port
        self.target = target.split(' ')
        self.cursor = 0
        self.is_playing = 0
        self.sequences = {}
        self.scenes = {}
        self.scenes_list = scenes_list
        self.scenes_subprocesses = Manager().dict() # this will be shared accross processes
        self.trigger = 0

        self.server = _liblo.ServerThread(self.port)
        self.server.register_methods(self)
        self.server.start()

    @_liblo.make_method('/Sequencer/Play', 'f')
    def play(self):
        self.is_playing = 1
        self.cursor = 0
        while self.is_playing:
            debut = time()
            #print "c: " + str(self.cursor) + " / " + str(time())
            for name in self.sequences:
                self.parseOscArgs(self.sequences[name].getArgs(self.cursor))
            self.cursor += 1
            while time() - debut < 60./self.bpm and self.trigger == 0:
                pass
            if self.trigger == 1:
                self.cursor = 0
                self.trigger = 0
            #sleep(60./self.bpm - debut + time())

    @_liblo.make_method('/Sequencer/Stop', 'f')
    def stop(self):
        self.is_playing = 0

    @_liblo.make_method('/Sequencer/Trigger', 'i')
    def trig(self):
        self.trigger = 1


    @_liblo.make_method('/Sequencer/Set_bpm', 'i')
    def set_bpm(self, path, args):
        #print "bpm: " + str(args[0]) + " / " + str(time())
        self.bpm = args[0]

    @_liblo.make_method('/Sequencer/Sequence/Enable', 'si')
    def enable_sequence(self,path,args):
        self.sequences[args[0]].enable(args[1])

    @_liblo.make_method('/Sequencer/DisableAll', 'i')
    def disable_all(self, path, args):
        for s in self.sequences:
            self.sequences[s].enable(0)
        for s in self.scenes:
            self.stop_scene(False,[s])

    @_liblo.make_method('/Sequencer/Scene/Play', 's')
    def play_scene(self,path,args):
        if args[0] in self.scenes:
            self.stop_scene(False,[args[0]])
            self.scenes[args[0]]

        self.scenes[args[0]] = Process(target=self.scenes_list,args=[self,args[0]])
        self.scenes[args[0]].start()


    @_liblo.make_method('/Sequencer/Scene/Stop', 's')
    def stop_scene(self,path,args):
        if self.scenes[args[0]].pid in self.scenes_subprocesses:
            pids = self.scenes_subprocesses[self.scenes[args[0]].pid]
            for pid in pids:
                kill(pid, SIGTERM)
            del self.scenes_subprocesses[self.scenes[args[0]].pid]

        self.scenes[args[0]].terminate()
        self.scenes[args[0]].join()
        # del self.scenes[args[0]]

    @_liblo.make_method('/test', None)
    def test(self,path,args):
        print 'Test : ' + str(args)

    def addSequence(self,name,events):
        self.sequences[name] = self.sequence(self,name,events)

    def addRandomSequence(self,name,events,steps):
        ''' This method adds a randomized sequence with NON-REPEATING steps'''
        eventsr=[]
        oldir=-1
        for i in range(0, steps-1):
            ir = random()*len(events)
            if i == 0:
                origin = int(ir) # detection du premier pas pour le bouclage de la boucle
            if i < steps-1:
                while int(ir) == oldir:
                    ir = random()*len(events)
            else:
                while int(ir) == oldir or int(ir) == origin:
                    ir = random()*len(events)
            eventsr.append(events[int(ir)])
            oldir = int(ir)
        self.sequences[name] = self.sequence(self,name,eventsr)

    def addClip(self,name,events):
        self.clips[name] = self.clip(self,name,events)

    def parseOscArgs(self,args):

        if not args:
            return

        if type(args[0]) is list:
            for i in range(len(args)):
                self.sendOsc(args[i])
        else:
            self.sendOsc(args)

    def sendOsc(self,args):
        path = str(args[0])
        if path[0]== ':':
            _liblo.send('osc.udp://localhost:'+str(self.port), path[1:], *args[1:])

        else:
            for i in range(len(self.target)):
                _liblo.send('osc.udp://'+self.target[i], path, *args[1:])


    """
    Sequence subclass : event loop synchronized by the sequencer's tempo
    """
    class sequence(object):
        def __init__(self,parent=None,name=None,events=None):
            self.name = name
            self.events = events
            self.beats = len(self.events)
            self.is_playing = False

        def getArgs(self,cursor):
            if not self.is_playing:
                return False
            return self.events[cursor%self.beats]

        def enable(self,x):
            self.is_playing = bool(x)





    def registerSceneSubprocess(self,target,args):

        process = Process(target=target,args=args)
        process.start()

        parentPid = current_process().pid

        # we need need to do this trick
        # using a proxy variable before modifying self.scenes_subprocesses
        # ensures the Manager see the change and sync the object accross processe

        proxy = []
        if parentPid in self.scenes_subprocesses:
            proxy= self.scenes_subprocesses[parentPid]
        proxy.append(process.pid)

        self.scenes_subprocesses[parentPid] = proxy




    """
    Animate function for pyOSCseq's osc sending method :
    Execute the given function for different values of its last argument,
    computed between 'start' and 'end'.
    - duration (s) : time to complete the animation
    - step (s) : delay between each step
    - function : function to animate, most likely 'send' (which is an alias for pyOSCseq.parseOscArgs()
    - args : tuple containing the first arguments passed to the function (these won't be animated)
    """
    def animate(self,start,end,duration,step,function,args, mode='float'):
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

        self.registerSceneSubprocess(threaded,[start,end,duration,step,function,args, mode])



    """
    Repeat function for pyOSCseq's osc sending method :
    Execute the given function nb_repeat times, and waits interval seconds between each call
    """
    def repeat(self,nb_repeat,interval,function,args):
        def threaded(nb_repeat,interval,function,args):
            for i in range(nb_repeat):
                function([args])
                sleep(interval)
        self.registerSceneSubprocess(threaded,[nb_repeat,interval,function,args])
