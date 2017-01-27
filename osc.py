# encoding: utf-8

from liblo import ServerThread
from inspect import getmembers

class Server(ServerThread):
    """
    OSC Server derivated from liblo's with
    - namespace prefixed to osc methods
    - case-insensitive osc address matching
    - sending protocol set to udp
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

        ServerThread.send(self, 'osc.udp://' + target, *message)

    def route_osc(self, address, *args):
        """
        OSC address vs method lookup
        """
        address = address.lower()
        if address in self.osc_methods:
            self.osc_methods[address](*args[0])


class API():
    """
    Decorator to bind methods to OSC addresses
    """

    def __init__(self, address, types=None):

        self.address = address

    def __call__(self, method):

        if hasattr(method, '_osc_address'):
            method._osc_address.append(self.address)
        else:
            method._osc_address = []
            method._osc_address.append(self.address)

        return method
