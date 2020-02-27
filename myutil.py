# -*- Coding: utf-8 -*-
from tornado.ioloop import IOLoop,PeriodicCallback
import signal, logging
class FastStop:
    def __init__(self):
        self.is_closing = False
    def enable(self):
        def signal_handler(signum, frame):
            self.is_closing = True
        def try_exit():
            if self.is_closing:
                # clean up here
                IOLoop.instance().stop()
        signal.signal(signal.SIGINT, signal_handler)
        PeriodicCallback(try_exit, 100).start()
