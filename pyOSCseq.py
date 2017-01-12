# encoding: utf-8

import liblo
from time import sleep , time
from random import random
from multiprocessing import *
from os import kill
from signal import SIGKILL


class Sequencer(object):

    def __init__(self, bpm=120, port=12345, target=None, scenes_list=None):

        self.bpm = bpm
        self.port = port
        self.target = target.split(' ') if target is not None else []
        self.cursor = 0
        self.is_playing = 0
        self.sequences = {}
        self.scenes = {}
        self.scenes_list = scenes_list
        self.scenes_subprocesses = Manager().dict() # this will be shared accross processes
        self.trigger = 0

        self.server = liblo.ServerThread(self.port)
        self.server.register_methods(self)
        self.server.start()

    @liblo.make_method('/Sequencer/Play', None)
    def play(self):

        if (self.is_playing) return
        self.is_playing = 1
        self.cursor = 0
        while self.is_playing:
            debut = time()
            for name in self.sequences:
                self.parseOscArgs(self.sequences[name].getArgs(self.cursor))
            self.cursor += 1
            while time() - debut < 60./self.bpm and self.trigger == 0:
                sleep(0.0001)
            if self.trigger == 1:
                self.cursor = 0
                self.trigger = 0

    @liblo.make_method('/Sequencer/Stop', None)
    def stop(self):

        self.is_playing = 0

    @liblo.make_method('/Sequencer/Trigger', None)
    def trig(self):

        self.trigger = 1


    @liblo.make_method('/Sequencer/Bpm', 'i')
    def set_bpm(self, path, args):

        self.bpm = args[0]

    @liblo.make_method('/Sequencer/Sequence/Toggle', 'si')
    def toggle_sequence(self,path,args):

        self.sequences[args[0]].toggle(args[1])

    @liblo.make_method('/Sequencer/Sequence/Enable', 's')
    def enable_sequence(self,path,args):

        self.sequences[args[0]].toggle(1)

    @liblo.make_method('/Sequencer/Sequence/Disable', 's')
    def disable_sequence(self,path,args):

        self.sequences[args[0]].toggle(0)

    @liblo.make_method('/Sequencer/DisableAll', None)
    def disable_all(self, path, args):

        for s in self.sequences:
            self.sequences[s].enable(0)
        for s in self.scenes:
            self.stop_scene(False,[s])

    @liblo.make_method('/Sequencer/Scene/Play', 's')
    def play_scene(self,path,args):

        if args[0] in self.scenes:
            self.stop_scene(False,[args[0]])
            del self.scenes[args[0]]

        self.scenes[args[0]] = Process(target=self.scenes_list,args=[self,args[0]])
        self.scenes[args[0]].start()


    @liblo.make_method('/Sequencer/Scene/Stop', 's')
    def stop_scene(self,path,args):

        if self.scenes[args[0]].pid in self.scenes_subprocesses:
            pids = self.scenes_subprocesses[self.scenes[args[0]].pid]
            for pid in pids:
                try:
                    kill(pid, SIGKILL)
                except:
                    pass
            del self.scenes_subprocesses[self.scenes[args[0]].pid]

        self.scenes[args[0]].terminate()
        self.scenes[args[0]].join()

    @liblo.make_method('/Sequencer/Debug', None)
    def log(self,path,args):

        print '[debug] Sequencer says: ' + str(args)

    def addSequence(self,name,events):

        self.sequences[name] = self.Sequence(self,name,events)

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
            self.server.send('osc.udp://localhost:'+str(self.port), path[1:], *args[1:])

        else:
            for i in range(len(self.target)):
                self.server.send('osc.udp://'+self.target[i], path, *args[1:])

    def registerSceneSubprocess(self,target,args):

        process = Process(target=target,args=args)
        process.start()

        parentPid = current_process().pid

        # we need (need) to do this trick
        # using a proxy variable before modifying self.scenes_subprocesses
        # ensures that the Manager sees the change and sync the object accross processes

        proxy = []
        if parentPid in self.scenes_subprocesses:
            proxy= self.scenes_subprocesses[parentPid]
        proxy.append(process.pid)

        self.scenes_subprocesses[parentPid] = proxy



    def animate(self,start,end,duration,step,function,args, mode='float'):
        """
        Animate function for pyOSCseq's osc sending method :
        Execute the given function for different values of its last argument,
        computed between 'start' and 'end'.
        - duration (s) : time to complete the animation
        - step (s) : delay between each step
        - function : function to animate, most likely 'send' (which is an alias for pyOSCseq.parseOscArgs()
        - args : tuple containing the first arguments passed to the function (these won't be animated)
        """
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



    def repeat(self,nb_repeat,interval,function,args):
        """
        Repeat function for pyOSCseq's osc sending method :
        Execute the given function nb_repeat times, and waits interval seconds between each call
        """
        def threaded(nb_repeat,interval,function,args):

            for i in range(nb_repeat):
                function([args])
                sleep(interval)

        self.registerSceneSubprocess(threaded,[nb_repeat,interval,function,args])

    class Sequence(object):
        """
        Sequence subclass : event loop synchronized by the sequencer's tempo
        """
        def __init__(self,parent=None,name=None,events=None):

            self.name = name
            self.events = events
            self.beats = len(self.events)
            self.is_playing = False

        def getArgs(self,cursor):

            if not self.is_playing:
                return False
            return self.events[cursor%self.beats]

        def toggle(self,x):

            self.is_playing = bool(x)
