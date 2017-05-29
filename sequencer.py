
# encoding: utf-8

from .osc import Server, API
from .timer import Timer
from .sequence import Sequence
from . import feeds as Feeds
from .utils import KillableThread as Thread
from .transport import Transport

from random import random
from math import floor

from signal import signal, SIGINT, SIGTERM

from inspect import getmembers

from json import loads as JSON_decode
from json import dumps as JSON_encode

class Sequencer(object):
    """
    OSC Sequencer
    """

    def __init__(self, name='Sequencer', bpm=120, port=12345, target=None, scenes=None, frequency=1000, jack_transport=False):
        """
        Sequencer contructor

        Args:
            name            (str): will be prepended to all OSC API addresses
            bpm           (float): tempo in beats per minute
            target          (str): ip:port hosts separated by spaces
                                   (osc messages will be send to these)
            scenes       (module): imported python module containing the scenes
            frequency (int|float): timer's update frequency in Hz
                                   higher value can increase precision (and cpu load)
        """

        self.name = name

        # Engine
        self.bpm = bpm
        self.rate = 1. / frequency
        self.timer = Timer(self)
        self.subtimer = Timer(self)
        self.cursor = 0
        self.playing = False

        # Sequences & Scenes
        self.sequences = {}
        self.scenes = {}
        self.scenes_list = {}
        for sname, scene in getmembers(scenes):
            if callable(scene) and sname[0] != '_':
                self.scenes_list[sname] = scene
        self.scenes_subthreads = {}

        # OSC
        self.port = port
        self.target = target.split(' ') if target is not None else []
        self.server = Server(port=self.port, namespace=name)
        self.server.register_api(self)
        self.server.start()

        # Feedback
        self.feeds = {}
        self.feeding = False
        self.feed_history = {}
        for name, feed in getmembers(Feeds):
            if callable(feed) and name[0] != '_':
                self.feeds[name] = {
                    'fetch': feed,
                    'subscribers': []
                }
            self.feed_history[name] = ''

        # Thread
        self.thread = None
        self.exiting = False
        signal(SIGINT, self.exit)
        signal(SIGTERM, self.exit)

        # Jack Transport
        self.jack_transport = Transport(self.name, Timer(self)) if jack_transport else None
        self.jack_repositionned = False

    """
    Engine
    """

    def start(self):
        """
        Start the sequencer main loop
        """

        print('OSC Sequencer: started')

        while not self.exiting:

            if self.jack_transport and self.jack_transport.connected:

                self.jack_transport.update_status()

                self.playing = self.jack_transport.status['playing']

                if self.jack_transport.status['bpm'] > 0.1:
                    self.bpm = self.jack_transport.status['bpm']

                jack_position = self.jack_transport.status['position']\
                                / self.jack_transport.status['sample_rate']\
                                * self.bpm / 60.

                if self.jack_transport.status['bar'] > 0:
                    jack_cursor = (self.jack_transport.status['bar'] -1)\
                                  * self.jack_transport.status['beats_per_bar']\
                                  + self.jack_transport.status['beat'] - 1
                else:
                    jack_cursor = floor(jack_position)

                if self.jack_transport.status['repositionned']:
                    self.jack_repositionned = jack_position == floor(jack_position)
                    Timer.sleep(self.rate)
                    continue

                if self.playing and (jack_cursor != self.cursor or self.jack_repositionned):
                    self.jack_repositionned = False
                    self.timer.reset()
                    self.cursor = int(jack_cursor)

                    for name in self.sequences:
                        self.sequences[name].play(self.cursor)

            elif self.playing:

                for name in self.sequences:
                    self.sequences[name].play(self.cursor)

                self.cursor += 1

                self.timer.wait(1, 'beat')

                continue

            Timer.sleep(self.rate)


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
        Handle thread termination gracefully (stop the main loop)
        Don't call self.server.stop(): it dies fine on its own (calling the method can deadlock in stress situation)
        """
        self.exiting = True
        self.disable_all()

        if self.jack_transport:
            self.jack_transport.exit()

    """
    Transport
    """

    @API('/Play', True)
    def play(self, timestamp=None):
        """
        Make the sequencer play and read enabled sequnces

        Args:
            timestamp   (float): time reference as returned by liblo.time()

        OSC:
            timestamp (timetag): time reference as returned by liblo.time()
                                 passing this ensures the time reference is set to the sending time
                                 this will only work if the time function is consistent accross sender and receiver

        """

        if self.playing:
             return self.trig()

        if self.jack_transport and self.jack_transport.connected:
            self.jack_transport.set_position(0)
            self.jack_transport.set_playing(True)

        else:
            self.cursor = 0
            self.timer.reset(timestamp)
            self.playing = True


    @API('/Resume', True)
    def resume(self, timestamp=None):
        """
        Make the sequencer play from where it stopped

        Args:
            timestamp   (float): time reference as returned by liblo.time()

        OSC:
            timestamp (timetag): time reference as returned by liblo.time()
                                 passing this ensures the time reference is set to the sending time
                                 this will only work if the time function is consistent accross sender and receiver

        """

        if self.jack_transport and self.jack_transport.connected:
            self.jack_transport.set_playing(True)

        else:
            self.playing = True
            self.timer.reset(timestamp)

    @API('/Stop')
    def stop(self):
        """
        Stop the sequencer
        """

        if self.jack_transport and self.jack_transport.connected:
            self.jack_transport.set_playing(False)

        else:
            self.playing = False

    @API('/Trig', True)
    @API('/Trigger', True)
    def trig(self, timestamp=None):
        """
        Reset the sequencer's cursor on next beat : sequences restart from beginning

        Args:
            timestamp   (float): time reference as returned by liblo.time()

        OSC:
            timestamp (timetag): time reference as returned by liblo.time()
                                 passing this ensures the time reference is set to the sending time
                                 this will only work if the time function is consistent accross sender and receiver
        """
        if not self.playing:
             return self.play(timestamp)

        if self.jack_transport and self.jack_transport.connected:
            self.jack_transport.set_position(0)

        else:
            self.timer.trig(timestamp)
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

    @API('/Sequence/Toggle')
    def sequence_toggle(self, name, state):
        """
        Toggle a sequence's state

        Args:
            name  (str): sequence's name
            state (int): 0 or 1
        """
        self.sequences[name].toggle(state)

    @API('/Sequence/Enable')
    def sequence_enable(self, name):
        """
        Enable a sequence

        Args:
            name  (str): sequence's name
        """
        self.sequences[name].toggle(1)

    @API('/Sequence/Disable')
    def sequence_disable(self, name):
        """
        Disable a sequence

        Args:
            name (str): sequence's name
                        set to '*' to stop all

        """
        if name == '*':

            self.sequence_disable_all()

        elif name in self.sequences:

            self.sequences[name].toggle(0)

    def sequence_disable_all(self):
        """
        Stop all sequences
        """

        for name in self.sequences:
            self.sequences[name].toggle(0)

    @API('/Sequence/Add')
    def sequence_add(self, name, steps):
        """
        Add a sequence

        Args:
            name   (str): sequence's name
            steps (list): a step cas be
                - a message (list): ['/path', arg1, arg2]
                - a list of messages to be sent at the same time
                - False or None for empty steps

        OSC:
            steps  (str): list written as a JSON string
        """
        if type(steps) is str and steps[0] == '[' and steps[-1] == ']':
            steps = JSON_decode(steps)

        self.sequences[name] = Sequence(self, name, steps)

    @API('/Sequence/Add/Random')
    def sequence_add_random(self, name, steps, n_steps):
        """
        Add a randomized sequence with NON-REPEATING steps

        Args:
            name    (str): sequence's name
            steps  (list): steps to shuffle
            n_steps (int): total number of steps

        OSC:
            steps   (str): list written as a JSON string
        """

        if type(steps) is str and steps[0] == '[' and steps[-1] == ']':
            steps = JSON_decode(steps)

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

    def sequence_play_step(self, name, step, divider=1, clock=None):
        """
        Parse a Sequence's step

        Args:
            name   (str): sequence's name
            cursor (int): sequencer's transport position
        """

        if not step:
            return

        if type(step) is tuple:

            self.sequence_play_step(name, step[0])
            t = Thread(target=self.sequence_play_substeps, args=[name, step, clock if clock is not None else self.timer.clock, divider])
            t.start()


        elif type(step[0]) is list:

            for i in range(len(step)):
                self.send(*step[i])

        else:
            self.send(*step)

    def sequence_play_substeps(self, name, step, clock, divider):
        timer = Timer(self, clock)
        n = len(step)
        for i in range(1, n):
            if not self.sequences[name].playing:
                return
            timer.wait(1. / n / divider, 'beat')
            self.sequence_play_step(name, step[i], n, timer.clock)

    """
    Scenes
    """

    @API('/Scene/Play', True)
    def scene_play(self, name, timestamp=None):
        """
        Start a scene (restart it if its already playing)

        Args:
            name          (str): scenes's name
            timestamp   (float): time reference as returned by liblo.time()

        OSC:
            timestamp (timetag): time reference as returned by liblo.time()
                                 passing this ensures the time reference is set to the sending time
                                 this will only work if the time function is consistent accross sender and receiver

        """

        if name in self.scenes and self.scenes[name] is not None:
            self.scene_stop(name)

        if name in self.scenes_list:
            self.scenes[name] = Thread(target=self.scenes_list[name], args=[self, Timer(self, timestamp)])
            self.scenes[name].start()


    @API('/Scene/Stop')
    def scene_stop(self, name):
        """
        Stop a scene

        Args:
            name (str): scenes's name
                        set to '*' to stop all
        """

        if name == '*':
            return self.scene_stop_all()


        if not name in self.scenes or self.scenes[name] is None:
            return

        id = self.scenes[name].ident
        self.scenes[name].kill()

        if id in self.scenes_subthreads:

            for subthread in self.scenes_subthreads[id]:
                subthread.kill()

            del self.scenes_subthreads[id]


        self.scenes[name] = None

    def scene_stop_all(self):
        """
        Stop all scenes
        """
        for name in self.scenes:
            self.scene_stop(name)

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

    def scene_run_subscene(self, function, args=None, blocking=False):
        """
        Run a function in its own thread

        Args:
            function (function): function to run in a new thread
            args         (list): arguments passed to the function
            blocking     (bool): False = threaded, non-blocking
                                 True  = blocking
        """
        if not blocking:
            thread = Thread(target=function, args=args)
            thread.start()
            id = Thread.get_current().ident
            if id not in self.scenes_subthreads:
                self.scenes_subthreads[id] = []
            self.scenes_subthreads[id].append(thread)
        else:
            function(*args)


    """
    OSC
    """

    def send(self, address, *args):
        """
        Send osc messages

        Args:
            target  (str): (optional) ip:port pair *
            address (str): osc address
            args         : anything

        * if no target is set (ie the first arg is the osc address), self.target will be used

        """

        if type(address) == int:
            address = str(address)

        if address[0] == ':':

            if len(args) and (type(args[-1]) != tuple or args[-1][0] != 't'):
                args = list(args)
                args.append(('t', Timer.time()))

            self.server.send('localhost:' + str(self.port), address[1:], *args)

        elif address.isdigit() or (':' in address and address.split(':')[-1].isdigit()):
            self.server.send(address, *args)

        else:
            for i in range(len(self.target)):
                self.server.send(self.target[i], address, *args)



    """
    Utils
    """

    def animate(self, args, start, end, duration, dmode='seconds', framerate=10, mode='float', easing=None, timestamp=None, blocking=False):
        """
        Animate function for pyOSCseq's osc sending method :
        Execute the given function for different values of its last argument,
        computed between 'start' and 'end'.

        Args:
            args   (str|list): osc address string or tuple containing the first arguments passed to the function (these won't be animated)
            duration  (float): time to complete the animation in seconds
            dmode       (str): duration mode, 'seconds' or 'beats'
            framerate (float): frames per seconds
            mode        (str): output number format, 'float' or 'integer'
            easing (function): custom easing function taking (start, end, frame, n_frames) for arguments
                default is linear: it returns (end - start) / n_frames * frame + start
                frame: current frame number
                n_frames: total number of frames

            blocking   (bool): False = threaded, non-blocking
                               True  = blocking
            timestamp (float): time reference as returned by liblo.time()
                               (useful for giving the same timestamp to multiple animates
                                to ensure they finish at the same time)
        """
        def subscene(args, start, end, duration, dmode, framerate, mode, easing, timestamp):

            timer = Timer(self, timestamp)

            message = [args] if type(args) != list else args
            framelength = 1.0 / (duration * framerate)
            n_frames = int(round(duration / framelength))
            coefficient = float(end - start) / n_frames

            if '$' not in message:
                message.append('$')

            for frame in range(n_frames + 1):

                if callable(easing):
                    v = easing(start, end, frame, n_frames)
                else:
                    v = coefficient * frame + start

                if mode == 'integer':
                    v = int(v)

                msg = []

                for i in range(len(message)):
                    if message[i] == '$':
                        msg.append(v)
                    else:
                        msg.append(message[i])

                self.send(*msg)

                if frame != n_frames:
                    timer.wait(framelength, dmode)

        self.scene_run_subscene(subscene, [args, start, end, duration, dmode, framerate, mode, easing, timestamp], blocking)

    def repeat(self, args, nb_repeat, interval, timestamp=None, blocking=False):
        """
        Repeat function for osc sending method :
        Execute the given function nb_repeat times, and waits interval seconds between each call

        Args:
            args      (list): osc message's address and arguments
            nb_repeat  (int): numbers of repetition
            interval (float): delay between iteration in seconds

            blocking  (bool): False = threaded, non-blocking
                              True  = blocking
            timestamp (float): time reference as returned by liblo.time()

           """
        def subscene(args, nb_repeat, interval, timestamp):

            timer = Timer(self, timestamp)

            for i in range(nb_repeat):
                self.send(*args)
                timer.wait(interval, 'seconds')

        self.scene_run_subscene(subscene, [args, nb_repeat, interval, timestamp], blocking=False)



    """
    Feedback API
    """

    @API('/Feed/Subscribe')
    def feed_subscribe(self, host, name):
        """
        Subscribe to a feed. Requested feed's updates will be sent to the host

        Args:
            host (str): ip:address
            name (str): feed's name
        """

        if name in self.feeds and host not in self.feeds[name]['subscribers']:
            self.feeds[name]['subscribers'].append(host)

            data = self.feed_fetch(name)
            self.feed_history[name] = data
            self.server.send(host, '/' + name, data)

            if not self.feeding:
                self.feeding = Thread(target=self.feed_start)
                self.feeding.start()


    @API('/Feed/Unsubscribe')
    def feed_unsubscribe(self, host, name):
        """
        Unsubscribe from a feed. Requested feed updates will no longer be sent to the host

        Args:
            host (str): ip:address
            name (str): feed's name
        """

        if name in self.feeds and host in self.feeds[name]['subscribers']:
            self.feeds[name]['subscribers'].remove(host)


    def feed_send_subscribers(self):

        for name in self.feeds:

            if len(self.feeds[name]['subscribers']):
                data = self.feed_fetch(name)
                if (self.feed_history[name] != data):
                    self.feed_history[name] = data

                    for host in self.feeds[name]['subscribers']:
                        self.server.send(host, '/' + name, data)

    def feed_fetch(self, name):

        return JSON_encode(self.feeds[name]['fetch'](self))

    def feed_start(self):

        while True:

            self.feed_send_subscribers()
            Timer.sleep(self.rate)
