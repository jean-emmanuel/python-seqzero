# encoding: utf-8

from osc import Server, API
from timer import Timer
from sequence import Sequence

from time import sleep
from random import random
from multiprocessing import Manager, Process, current_process
from os import kill
from signal import signal, SIGINT, SIGTERM, SIGKILL

from threading import Thread

class Sequencer(object):
    """
    OSC Sequencer
    """

    def __init__(self, name='Sequencer', bpm=120, port=12345, target=[], scenes=None):
        """
        Sequencer contructor

        Args:
            name      (str): will be prepended to all OSC API addresses
            bpm     (float): tempo in beats per minute
            target   (list): 'ip:port' pairs to send the osc messages to
            scenes (module): imported python module containing the scenes
        """

        # Engine
        self.bpm = bpm
        self.timer = Timer(self)
        self.cursor = 0
        self.is_playing = False

        # Sequences & Scenes
        self.sequences = {}
        self.scenes = {}
        self.scenes_list = scenes
        self.scenes_subprocesses = Manager().dict() # this will be shared accross processes

        # OSC
        self.port = port
        self.target = target.split(' ') if target is not None else []
        self.server = Server(port=self.port, namespace=name)
        self.server.register_methods(self)
        self.server.start()

        # Process
        self.thread = None
        self.exiting = False
        signal(SIGINT, self.exit)
        signal(SIGTERM, self.exit)


    """
    Engine
    """

    def start(self):
        """
        Start the sequencer main loop
        """

        print('OSC Sequencer: started')

        while not self.exiting:

            if self.is_playing:

                for name in self.sequences:
                    self.sequence_play_step(name, self.cursor)

                self.cursor += 1

                self.timer.wait(1, 'beat')

            else:

                sleep(0.001)


        print('OSC Sequencer: terminated')

    def start_threaded(self):
        """
        Start the sequencer's main loop without blocking the thread
        /!\ exit() must be called to stop it (ctrl+c alone won't work)
        """
        self.thread = Thread(target=self.start)
        self.thread.start()

    def exit(self, *args):
        """
        Handle process termination gracefully (stop the main loop)
        """
        self.exiting = True
        self.disable_all()
        self.server.stop()

        if self.thread is not None:
            self.thread.join(0.0)


    """
    Transport
    """

    @API('/Play')
    def play(self):
        """
        Make the sequencer play and read enabled sequnces
        """

        if self.is_playing:
             return self.trig()

        self.cursor = 0
        self.timer.reset()
        self.is_playing = True

    @API('/Resume')
    def resume(self):
        """
        Make the sequencer play from where it stopped
        """

        if not self.is_playing:
             return self.play()

        self.is_playing = True
        self.timer.reset()

    @API('/Stop')
    def stop(self):
        """
        Stop the sequencer
        """
        self.is_playing = False

    @API('/Trigger')
    def trig(self):
        """
        Reset the sequencer's cursor on next beat : sequences restart from beginning
        """
        if not self.is_playing:
             return self.play()

        self.timer.trig()
        self.cursor = 0

    @API('/Bpm')
    def set_bpm(self, bpm):
        """
        Set the sequencer's bpm
        - bpm: integer
        """
        self.bpm = float(bpm)

    """
    Sequences
    """

    @API('/Sequence/Toggle', 'si')
    def sequence_toggle(self, name, state):
        """
        Toggle a sequence's state

        Args:
            name  (str): sequence's name
            state (int): 0 or 1
        """
        self.sequences[name].toggle(state)

    @API('/Sequence/Enable', 's')
    def sequence_enable(self, name):
        """
        Enable a sequence

        Args:
            name  (str): sequence's name
        """
        self.sequences[name].toggle(1)

    @API('/Sequence/Disable', 's')
    def sequence_disable(self, name):
        """
        Disable a sequence

        Args:
            name  (str): sequence's name
        """
        if name == '*':

            self.sequence_disable_all()

        elif self.sequences.has_key(name):

            self.sequences[name].toggle(0)

    def sequence_disable_all(self):
        """
        Stop all sequences
        """

        for name in self.sequences:
            self.sequences[name].toggle(0)

    def sequence_add(self, name, steps):
        """
        Add a sequence

        Args:
            name   (str): sequence's name
            steps (list): steps cas be
                - messages (list): ['/path', arg1, arg2]
                - list of messages to be sent at the same time
                - False or None for empty steps
        """

        self.sequences[name] = Sequence(self, name, steps)


    def sequence_add_random(self, name, steps, n_steps):
        """
        Add a randomized sequence with NON-REPEATING steps

        Args:
            name    (str): sequence's name
            steps  (list): steps to shuffle
            n_steps (int): total number of steps
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

    def sequence_play_step(self, name, cursor):
        """
        Parse a Sequence's step

        Args:
            name   (str): sequence's name
            cursor (int): sequencer's transport position
        """

        step = self.sequences[name].getStep(cursor)

        if not step:
            return

        if type(step[0]) is list:
            for i in range(len(step)):
                self.send(*step[i])
        else:
            self.send(*step)


    """
    Scenes
    """

    @API('/Scene/Play', 's')
    def scene_play(self, name):
        """
        Start a scene (restart it if its already playing)

        Args:
            name (str): scenes's name
        """

        if name in self.scenes:
            self.scene_stop(name)
            del self.scenes[name]

        if hasattr(self.scenes_list, name):
            self.scenes[name] = Process(target=self.scenes_list.__dict__[name], args=[self, Timer(self)])
            self.scenes[name].start()


    @API('/Scene/Stop', 's')
    def scene_stop(self, name):
        """
        Stop a scene

        Args:
            name (str): scenes's name
        """

        if name == '*':
            return self.scene_stop_all()

        if self.scenes[name].pid in self.scenes_subprocesses:
            pids = self.scenes_subprocesses[self.scenes[name].pid]
            for pid in pids:
                try:
                    kill(pid, SIGKILL)
                except:
                    pass
            del self.scenes_subprocesses[self.scenes[name].pid]


        try:
            kill(self.scenes[name].pid, SIGKILL)
        except:
            pass

        self.scenes[name].terminate()
        self.scenes[name].join(0.0)

    def scene_stop_all(self):
        """
        Stop all scenes
        """
        for name in self.scenes:
            self.scene_stop(name)

    def scene_run_subprocess(self, target, args):
        """
        Register threaded functions (animate, repeat) to stop them when stopping the scene

        Args:
            target (function): function to run in a new process
            args       (list): arguments passed to the function
        """

        process = Process(target=target, args=args)
        process.start()

        parentPid = current_process().pid

        # we need (need) to do this trick
        # using a proxy variable before modifying self.scenes_subprocesses
        # ensures that the Manager sees the change and sync the object accross processes

        proxy = []
        if parentPid in self.scenes_subprocesses:
            proxy = self.scenes_subprocesses[parentPid]
        proxy.append(process.pid)

        self.scenes_subprocesses[parentPid] = proxy

    """
    Misc
    """

    @API('/Log')
    def log(self, *message):
        """
        Log something in the console

        Args:
            message: anything
        """

        print('[debug] Sequencer says: ' + str(message))

    @API('/DisableAll')
    def disable_all(self):
        """
        Disable all sequences and stop all scenes
        """
        self.sequence_disable_all()
        self.scene_stop_all()

    """
    OSC
    """

    def send(self, address, *args):
        """
        Send osc messages

        Args:
            address (str): osc address
            args         : anything
        """

        if address[0] == ':':
            self.server.send('osc.udp://localhost:' + str(self.port), address[1:], *args)

        else:
            for i in range(len(self.target)):
                self.server.send('osc.udp://' + self.target[i], address, *args)



    """
    Utils
    """

    def animate(self, args, start, end, duration, framerate=10, mode='float'):
        """
        Animate function for pyOSCseq's osc sending method :
        Execute the given function for different values of its last argument,
        computed between 'start' and 'end'.

        Args:
            args   (str|list): osc address string or tuple containing the first arguments passed to the function (these won't be animated)
            duration  (float): time to complete the animation in seconds
            framerate (float): frames per seconds
            mode        (str): output number format, 'float' or 'integer'
            easing (function): custom easing function taking (start, end, frame, n_frames) for arguments
                default is linear: it returns (end - start) / n_frames * frame + start
                frame: current frame number
                n_frames: total number of frames
        """
        def threaded(args, start, end, duration, framerate=10, mode='float', easing=None):

            timer = Timer(self)

            message = [args] if type(args) != list else args
            framelength = 1.0 / (duration * framerate)
            n_frames = int(round(duration / framelength))
            coefficient = float(end - start) / n_frames

            message.append(0)

            for frame in range(n_frames + 1):

                if callable(easing):
                    message[-1] = easing(start, end, frame, n_frames)
                else:
                    message[-1] = coefficient * frame + start

                if mode == 'integer':
                    message[-1] = int(message[-1])

                self.send(*message)

                if frame != n_frames:
                    timer.wait(framelength, 'seconds')

        self.scene_run_subprocess(threaded, [args, start, end, duration, framerate, mode])

    def repeat(self, args, nb_repeat, interval):
        """
        Repeat function for pyOSCseq's osc sending method :
        Execute the given function nb_repeat times, and waits interval seconds between each call

        Args:
            args      (list): osc message's address and arguments
            nb_repeat  (int): numbers of repetition
            interval (float): delay between iteration in seconds
        """
        def threaded(args, nb_repeat, interval):

            timer = Timer(self)

            for i in range(nb_repeat):
                self.send(*args)
                timer.wait(interval, 'seconds')

        self.scene_run_subprocess(threaded, [args, nb_repeat, interval, function])
