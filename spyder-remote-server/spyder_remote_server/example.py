import subprocess
import threading
import queue
import time

import tornado

class Test:

    def output_reader(self, proc, outq):
        for line in iter(proc.stdout.readline, b''):
            self.outq.put(line.decode('utf-8'))

    def run(self):
        self._proc = subprocess.Popen(
            # ["conda", "create", "-n", "test", "anaconda", "--dry-run", "--json"],
            ["conda", "search", "anaconda", "--json"],
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def get_status(self):
        if self._proc.poll() is not None:
            stdout = self._proc.stdout
            print([stdout])
            print("BOOM!")


class MyHandler(tornado.web.RequestHandler):

    def on_done(self, status, stdout, stderr):
        self.write( stdout )
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        t = tornado_subprocess.Subprocess( self.on_done, timeout=30, args=[ "cat", "/etc/passwd" ] )
        t.start()


MyHandler()
MyHandler.get()
