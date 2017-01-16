# encoding: utf-8

from liblo import ServerThread, make_method, Address

class Server(ServerThread):
    """
    OSC Server with namespace prefixed to osc methods
    """
    def __init__(self, namespace, **kwargs):

        self.namespace = namespace if namespace[0] == '/' else '/' + namespace

        ServerThread.__init__(self, **kwargs)

    def add_method(self, path, typespec, func, user_data=None):

        ServerThread.add_method(self, self.namespace + path, typespec, func, user_data=None)


class API(make_method):
    """
    Wrapper around liblo's make_method decorator:
    - make types argument optionnal
    - only pass self and arguments to the method (strip out osc address and extra infos)
    """

    def __init__(self, path, types=None, user_data=None):
        make_method.__init__(self, path, types, user_data)

    def __call__(self, method):

        def f(self, *args):
            if len(args) >= 3 and type(args[3]) == Address:
                method(self, *args[1])
            else:
                method(self, *args)

        if not hasattr(f, '_method_spec'):
            f._method_spec = []
        f._method_spec.append(self.spec)

        return f
