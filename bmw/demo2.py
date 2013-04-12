from threading import Timer
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, action):
        self._timer     = None
        self.interval   = interval
        self.action = action
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.hello()
        self.start()

    def hello(self):
        print "Break My Work, Action = %s" % self.action
        
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



print "starting..."
action = "popup"
rt = RepeatedTimer(1, action) # it auto-starts, no need of rt.start()
try:
    sleep(5) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!