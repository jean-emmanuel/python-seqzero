from time import sleep 
import liblo as _liblo
from kthread import KThread

       
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
         
        self.server = _liblo.ServerThread(self.port)
        self.server.register_methods(self)
        self.server.start()
        
    @_liblo.make_method('/Sequencer/Play', 'f')
    def play(self):
        self.is_playing = 1
        self.cursor = 0
        while self.is_playing:
            for name in self.sequences:
                self.parseOscArgs(self.sequences[name].getArgs(self.cursor))
            self.cursor += 1
            sleep(60./self.bpm)
            
    @_liblo.make_method('/Sequencer/Stop', 'f')
    def stop(self):
        self.is_playing = 0
        
    @_liblo.make_method('/Sequencer/Sequence/Enable', 'si')
    def enable_sequence(self,path,args):
        self.sequences[args[0]].enable(args[1])
    
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
