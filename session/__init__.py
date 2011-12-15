import sys
from UserDict import UserDict
import uuid, M2Crypto

class TransportError(Exception):
    def __init__(self, *args):
        self.args = args

class SessionSecurityError(Exception):
    def __init__(self, *args):
        self.args = args

class Transport():
    def __init__(self, key):
        self.key = key
        self.tries = 10

    def read(self):
        pass

    def write(self, value):
        pass

    def key_exists(self, id):
        return False

    def genid(self):
        id = str(uuid.UUID(bytes = M2Crypto.m2.rand_bytes(16))).replace('-', '')

        if self.key_exists(id):
            self.tries -= 1
            if self.tries < 0: raise TransportError()

            return self.genid()

        return id

class SessionManager(UserDict):
    def __init__(self, options, transport='redis'):
        UserDict.__init__(self)

        self.options = {
            'expire' : 86400,
            'namespace' : ''
        }

        for (k, v) in options.items():
            self.options[k] = v

        self.modified = False
        self.exists = False

        subclass = transport.lower().capitalize()
        module = "%s.transport.%s" % (Transport.__module__, transport)
        __import__(module)

        self.transport = getattr(sys.modules[module], subclass)(self.options)
        self.read()

    def __setitem__(self, key, item):
        self.modified = True
        UserDict.__setitem__(self, key, item)

    def token(self):
        return self.transport.key

    def read(self):
        data = self.transport.read()

        if data and isinstance(data, dict):
            #check security
            if ('ua' in self.options) and ('ua' in data):
                if self.options['ua'] != data['ua']:
                    raise SessionSecurityError()

            if ('ip' in self.options) and ('ip' in data):
                if self.options['ip'] != data['ip']:
                    raise SessionSecurityError()

            self.exists = True
            for (k, v) in data.items():
                self[k] = v

    def is_fresh(self):
        return self.modified and not self.exists

    def write(self):
        if self.modified:
            self.transport.write(self.data)
