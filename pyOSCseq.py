from time import sleep , time
import liblo as _liblo
from kthread import KThread
from random import random

       
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
            print s
            self.scenes[s].kill()
        self.scenes = {}
    
    @_liblo.make_method('/Sequencer/Scene/Play', 's')
    def play_scene(self,path,args):
        if not args[0] in self.scenes:   
            self.scenes[args[0]] = KThread(target=self.scenes_list, args=([self.parseOscArgs,args[0]]))
            self.scenes[args[0]].start()
        if not self.scenes[args[0]].is_alive():
            self.scenes[args[0]] = KThread(target=self.scenes_list, args=([self.parseOscArgs,args[0]]))
            self.scenes[args[0]].start()

    @_liblo.make_method('/Sequencer/Scene/Stop', 's')
    def stop_scene(self,path,args):
        self.scenes[args[0]].kill()
        del self.scenes[args[0]]
        
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
        print eventsr
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
