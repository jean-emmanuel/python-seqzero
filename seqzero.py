# encoding: utf-8

from liblo import ServerThread, make_method
from time import sleep , time
from random import random
from multiprocessing import Manager, Process, current_process
from os import kill
from signal import signal, SIGINT, SIGTERM, SIGKILL

class Server(ServerThread):
    """
    OCS Server with namespace prefixed to osc methods
    """
    def __init__(self, namespace, **kwargs):

        self.namespace = namespace if namespace[0] == '/' else '/' + namespace

        ServerThread.__init__(self, **kwargs)

    def add_method(self, path, typespec, func, user_data=None):

        ServerThread.add_method(self, self.namespace + path, typespec, func, user_data=None)


class Sequencer(object):
    """
    OSC Sequencer
    """

    def __init__(self, name='Sequencer', bpm=120, port=12345, target=None, scenes=None):

        self.bpm = bpm
        self.port = port
        self.target = target.split(' ') if target is not None else []
        self.timer = Timer(self)
        self.cursor = 0
        self.is_playing = 0
        self.sequences = {}
        self.scenes = {}
        self.scenes_list = scenes
        self.scenes_subprocesses = Manager().dict() # this will be shared accross processes
        self.trigger = 0

        self.server = Server(port=self.port, namespace=name)
        self.server.register_methods(self)
        self.server.start()

        self.exiting = False
        signal(SIGINT, self.exit)
        signal(SIGTERM, self.exit)

    def start(self):
        """
        Start the sequencer main loop
        """

        print 'OSC Sequencer: started'

        while not self.exiting:

            if self.is_playing:

                for name in self.sequences:
                    self.playStep(self.sequences[name].getStep(self.cursor))

                self.cursor += 1

                self.timer.wait(1, 'beat')

                if self.trigger == 1:
                    self.cursor = 0
                    self.trigger = 0
                    self.timer.reset()

            else:

                sleep(0.001)



        self.disable_all('', '')
        self.server.stop()
        print 'OSC Sequencer: terminated'



    def exit(self, *args):
        """
        Handle process termination gracefully (stop the main loop)
        """
        self.exiting = True

    @make_method('/Play', None)
    def play(self):
        """
        Make the sequencer play and read enabled sequnces
        """

        if self.is_playing:
             return self.trig()

        self.is_playing = 1
        self.cursor = 0
        self.trigger = 0
        self.timer.reset()

    @make_method('/Resume', None)
    def resume(self):
        """
        Make the sequencer play from where is stopped
        """

        if not self.is_playing:
             return self.play()

        self.is_playing = 1
        self.timer.reset()

    @make_method('/Stop', None)
    def stop(self):
        """
        Stop the sequencer
        """
        self.is_playing = 0

    @make_method('/Trigger', None)
    def trig(self):
        """
        Reset the sequencer's cursor on next beat : sequences restart from beginning
        """
        if not self.is_playing:
             return self.play()

        self.trigger = 1


    @make_method('/Bpm', 'i')
    def set_bpm(self, path, args):
        """
        Set the sequencer's bpm
        """
        self.bpm = args[0]

    @make_method('/Sequence/Toggle', 'si')
    def toggle_sequence(self, path, args):
        """
        Toggle a sequence's state
        """
        self.sequences[args[0]].toggle(args[1])

    @make_method('/Sequence/Enable', 's')
    def enable_sequence(self, path, args):
        """
        Enable a sequence
        """
        self.sequences[args[0]].toggle(1)

    @make_method('/Sequence/Disable', 's')
    def disable_sequence(self, path, args):
        """
        Disable a sequence
        """
        self.sequences[args[0]].toggle(0)

    @make_method('/DisableAll', None)
    def disable_all(self, path, args):
        """
        Stop all sequences and scenes
        """
        for s in self.sequences:
            self.sequences[s].toggle(0)
        for s in self.scenes:
            self.stop_scene(False, [s])

    @make_method('/Scene/Play', 's')
    def play_scene(self, path, args):
        """
        Start a scene (restart it if its already playing)
        """

        if args[0] in self.scenes:
            self.stop_scene(False, [args[0]])
            del self.scenes[args[0]]

        if hasattr(self.scenes_list, args[0]):
            self.scenes[args[0]] = Process(target=self.scenes_list.__dict__[args[0]], args=[self, Timer(self)])
            self.scenes[args[0]].start()


    @make_method('/Scene/Stop', 's')
    def stop_scene(self, path, args):
        """
        Stop a scene
        """

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

    @make_method('/Debug', None)
    def log(self, path, args):
        """
        Log something in the console
        """

        print '[debug] Sequencer says: ' + str(args)

    def addSequence(self, name, steps):
        """
        Add a sequence
        """

        self.sequences[name] = Sequence(self, name, steps)

    def addRandomSequence(self, name, steps, n_steps):
        """
        Add a randomized sequence with NON-REPEATING steps
        """

        stepsR = []
        oldir = -1
        for i in range(0, n_steps - 1):
            ir = random() * len(steps)
            if i == 0:
                origin = int(ir) # detection du premier pas pour le bouclage de la boucle
            if i < n_steps - 1:
                while int(ir) == oldir:
                    ir = random() * len(steps)
            else:
                while int(ir) == oldir or int(ir) == origin:
                    ir = random() * len(steps)
            stepsR.append(steps[int(ir)])
            oldir = int(ir)

        self.sequences[name] = self.sequence(self, name, stepsR)

    def playStep(self, args):
        """
        Parse a Sequence's step
        """
        if not args:
            return

        if type(args[0]) is list:
            for i in range(len(args)):
                self.send(*args[i])
        else:
            self.send(*args)

    def send(self, path, *args):
        """
        Send osc messages
        """

        if path[0] == ':':
            self.server.send('osc.udp://localhost:' + str(self.port), path[1:], *args)

        else:
            for i in range(len(self.target)):
                self.server.send('osc.udp://' + self.target[i], path, *args)

    def registerSceneSubprocess(self, target, args):
        """
        Register threaded functions (animate, repeat) to stop them when stopping the scene
        """

        process = Process(target=target, args=args)
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


    def animate(self, args, start, end, duration, framerate=10, mode='float'):
        """
        Animate function for pyOSCseq's osc sending method :
        Execute the given function for different values of its last argument,
        computed between 'start' and 'end'.
        - args : osc path string or tuple containing the first arguments passed to the function (these won't be animated)
        - duration (s) : time to complete the animation
        - framerate (hz) : frames per seconds
        - mode ('float'|'integer'): send floats or integers
        """
        def threaded(args, start, end, duration, framerate=10, mode='float'):

            timer = Timer(self)

            message = [args] if type(args) != list else args
            framelength = 1.0 / (duration * framerate)
            n_steps = int(round(duration / framelength))
            coefficient = float(end - start) / n_steps

            message.append(0)

            for x in range(n_steps + 1):

                message[-1] = coefficient * x + start

                if mode == 'integer':
                    message[-1] = int(message[-1])

                self.send(*message)

                if x != n_steps:
                    timer.wait(framelength, 'seconds')

        self.registerSceneSubprocess(threaded, [args, start, end, duration, framerate, mode])

    def repeat(self, args, nb_repeat, interval):
        """
        Repeat function for pyOSCseq's osc sending method :
        Execute the given function nb_repeat times, and waits interval seconds between each call
        """
        def threaded(args, nb_repeat, interval):

            timer = Timer(self)

            for i in range(nb_repeat):
                begin = time()
                self.send(*args)
                timer.wait(interval, 'seconds')

        self.registerSceneSubprocess(threaded, [args, nb_repeat, interval, function])

    def beatsToSeconds(self, beats):
        """Convert beats to seconds)"""
        return 60. / self.bpm * beats


class Timer(object):
    """
    Timer with latency compensation
    """

    def __init__(self, sequencer):

        self.sequencer = sequencer
        self.clock = time()

    def reset(self):

        self.clock = time()

    def wait(self, n, mode='beats'):

        if mode[0] == 'b':
            delay = self.sequencer.beatsToSeconds(n)
        elif mode[0] == 's':
            delay = n

        while time() - self.clock < delay:
            sleep(0.001)

        self.clock += delay

class Sequence(object):
    """
    Sequence: event loop synchronized by the sequencer's tempo
    """
    def __init__(self, parent=None, name=None, steps=None):

        self.name = name
        self.steps = steps
        self.beats = len(self.steps)
        self.is_playing = False

    def getStep(self, cursor):

        if not self.is_playing:
            return None

        return self.steps[cursor%self.beats]

    def toggle(self, x):

        self.is_playing = bool(x)
