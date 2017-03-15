from threading import Thread, current_thread
from sys import settrace

class KillableThread(Thread):
    """
    A subclass of Thread, with a kill() method.
    https://github.com/WKPlus/blog/blob/cc3e723cbed3424fa704003109f63b05139ea4bf/content/python/python%E4%B8%AD%E5%A6%82%E4%BD%95%E7%BB%88%E6%AD%A2%E4%B8%80%E4%B8%AA%E7%BA%BF%E7%A8%8B.md
    """

    def __init__(self, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run # Force the Thread to install our trace.
        Thread.start(self)

    def __run(self):
        """ Hacked run function, which installs the trace."""
        settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

    def get_current(self):
        return current_thread()
