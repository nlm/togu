from __future__ import print_function, unicode_literals
import sys
import os
import pycurl
import datetime
from supervisor.childutils import listener, getRPCInterface
from abc import abstractmethod
from StringIO import StringIO

class IncompleteEnvironmentException(Exception):
    pass

class SupervisorEventHandler(object):

    def __init__(self, port, service, rpc=None,
                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        self.port = port
        self.service = service
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        if rpc is None:
            try:
                rpc = getRPCInterface(os.environ)
            except KeyError as error:
                raise IncompleteEnvironmentException(error)
        self.rpc = rpc

    def log(self, string):
        self.stderr.write('[{0}] {1}\n'.format(datetime.datetime.now(),
                                               string))
        self.stderr.flush()

    def start_process(self, name):
        if self.rpc is None:
            return None
        return self.rpc.supervisor.startProcess(name)

    def stop_process(self, name):
        if self.rpc is None:
            return None
        return self.rpc.supervisor.stopProcess(name)

    @abstractmethod
    def run(self):
        pass

    def wait(self, stdin=None, stdout=None):
        stdin = self.stdin if stdin is None else stdin
        stdout = self.stdout if stdout is None else stdout
        return listener.wait(stdin, stdout)

    def ok(self, stdout=None):
        stdout = self.stdout if stdout is None else stdout
        return listener.ok(stdout)

    def fail(self, stdout=None):
        stdout = self.stdout if stdout is None else stdout
        return listener.fail(stdout)


class Togu(SupervisorEventHandler):

    def __init__(self, port, service, timeout, max_errors):
        super(self.__class__, self).__init__(port, service)
        self.timeout = int(timeout)
        self.max_errors = int(max_errors)

    def check_ping(self):
        buf = StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'http://127.0.0.1:{0}/ping'.format(self.port))
        c.setopt(pycurl.TIMEOUT, self.timeout)
        c.setopt(pycurl.WRITEDATA, buf)

        try:
            c.perform()
            response = buf.getvalue()
            if response != '"pong"':
                self.log('bad response: {}'.format(response))
                return False
        except pycurl.error as error:
            self.log('curl error: {}'.format(error))
            return False

        c.close()
        return True

    def run(self):
        errors = 0
        while True:
            headers, data = self.wait()
            result = self.check_ping()
            if result is False:
                errors += 1
                if errors >= self.max_errors:
                    self.log('restarting service "{0}" after {1} errors'
                             .format(self.service, errors))
                    self.stop_process(self.service)
                    self.start_process(self.service)
                    errors = 0
            else:
                if errors > 0:
                    self.log('service "{0}" recovered'.format(self.service))
                errors = 0
            self.ok(stdout=self.stdout)
