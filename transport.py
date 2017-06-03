# encoding: utf-8

from .utils import KillableThread as Thread

from time import sleep


WRONG_VERSION = False
NOT_INSTALLED = False

try:
    import jack
    if not 'get_beat_infos' in dir(jack):
        WRONG_VERSION = True
except:
    NOT_INSTALLED = True


if NOT_INSTALLED or WRONG_VERSION:

    def Transport(*args, **kwargs):

        if NOT_INSTALLED:
            print('Warning: python-jack not found')

        if WRONG_VERSION:
            print('Warning: the installed version of python-jack doesn\'t match seqzero\'s requirements')

        print('jack transport support disabled')

        return None


else:

    class Transport(object):
        """
        Jack Transport client
        """

        def __init__(self, name, timer):

            self.name = name
            self.timer = timer
            self.client = None

            self.connected = False
            self.hand_shaked = False

            self.exiting = False

            self.status = {
                'playing': False,
                'position': 0,
                'repositionned': False,
                'sample_rate': 44100.
            }

            self.connection_thread = Thread(target=self.live)
            self.connection_thread.start()

        def live(self):

            while not self.exiting:

                self.connect()

                if not self.hand_shaked and self.connected:

                    try:
                        self.status['sample_rate'] = self.client.get_sample_rate() * 1.
                        self.hand_shaked = True
                    except:
                        pass

                self.timer.wait(1, 's')


        def connect(self):

            try:

                if self.client is None:
                    self.client = jack.Client(self.name)

                else:
                    self.client.attach(self.name)

                self.connected = True


            except jack.UsageError:

                self.connected = True
                # print('Jack: Already connected')


            except:

                self.connected = False
                self.hand_shaked = False
                # print('Jack: connection failed')


        def exit(self):

            self.exiting = True

            if self.connected:

                try:

                    self.client.detach()
                    self.hand_shaked = False
                    self.connected = False

                except:

                    pass
                    # print('Jack: already detached')


        def set_playing(self, state):

            self.connect()
            if self.connected:

                if state:
                    self.client.transport_start()
                else:
                    self.client.transport_stop()

        def set_position(self, position):

            self.connect()
            if self.connected:
                self.client.transport_locate(position)


        def update_status(self):

            self.connect()
            if self.connected:
                self.status['repositionned'] = self.client.get_transport_state() == 3
                self.status['playing'] = self.client.get_transport_state() == 1
                self.status['position'] = self.client.get_current_transport_frame()

                bbt = self.client.get_beat_infos()
                self.status['bpm'] = bbt['beats_per_minute']
                self.status['bar'] = bbt['bar']
                self.status['beats_per_bar'] = bbt['beats_per_bar']
                self.status['beat_type'] = bbt['beat_type']
                self.status['beat'] = bbt['beat']
