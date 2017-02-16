from os import kill as _kill
from os import system
from psutil import Process
from signal import SIGKILL

def kill(pid, process=None):
    try:
        _kill(pid, SIGKILL)
    except:
        try:
            p = Process(pid) if process == None else process
            p.terminate()
        except:
            pass
