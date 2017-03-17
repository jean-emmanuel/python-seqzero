# encoding: utf-8

from liblo import ServerThread
from inspect import getmembers
from timer import Timer

class Server(ServerThread):
    """
    OSC Server derivated from liblo's with
    - namespace prefixed to osc methods
    - case-insensitive osc address matching
    - sending protocol set to udp
    - optional timestamp argument for methods
    - permissive number of argument (extra arguments are ignored, timestamp is always the last one)
    """

    def __init__(self, namespace, **kwargs):
        """
        Server contructor

        Args:
            namespace (str): osc method addresses will be prefixed with /namespace
                             disabled with an empty string

        """

        ServerThread.__init__(self, reg_methods=False, **kwargs)

        self.namespace = namespace if namespace[0] == '/' or namespace == '' else '/' + namespace
        self.osc_methods = {}
        self.add_method(None, None, self.route_osc)

    def register_api(self, obj):
        """
        Resister all @API decorated methods found in obj
        """

        for name, method in getmembers(obj):

            if hasattr(method, '_osc_address'):
                addresses = method._osc_address

                for address in addresses:
                    self.osc_methods[(self.namespace + address).lower()] = method

    def send(self, target, *message):
        """
        Send osc message over udp
        """

        if target.isdigit():
            target = '127.0.0.1:' + target

        if 'osc.udp://' not in target:
            target = 'osc.udp://' + target

        ServerThread.send(self, target, *message)

    def route_osc(self, address, *args):
        """
        OSC address vs method lookup
        Parse or generate the timestamp if the method takes one
        """

        address = address.lower()

        if address in self.osc_methods:
            method = self.osc_methods[address]
            arguments = args[0]
            types = args[1]

            if method._takes_timestamp:

                if types[-1] == 't':
                    timestamp = arguments[-1]
                else:
                    timestamp = Timer.time()

                method(*arguments[:method._argcount-2], timestamp=timestamp)

            else:

                method(*arguments[:method._argcount-1])


class API():
    """
    Decorator to bind methods to OSC addresses and tell if they handle timestamps
    """

    def __init__(self, address, timestamp=False):

        self.address = address
        self.timestamp = timestamp

    def __call__(self, method):

        if hasattr(method, '_osc_address'):
            method._osc_address.append(self.address)
        else:
            method._osc_address = []
            method._osc_address.append(self.address)

        method._argcount = method.func_code.co_argcount

        method._takes_timestamp = self.timestamp

        return method
