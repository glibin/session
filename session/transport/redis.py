# -*- coding: utf-8 -*-

from session import Transport

import redis
import re
import tornado.escape

class Redis(Transport):
    def __init__(self, options):
        self.redis = options['redis']
        self.namespace = ('namespace' in options) and options['namespace'] or 'sess_'

        if not options['token']:
            options['token'] = self.genid()

        key = "{0}{1}".format(self.namespace, re.sub('[^a-z0-9]+', '', options['token'][:32]))
        Transport.__init__(self, key)

        self.options = options

    def key_exists(self, key):
        response = self.redis.exists("{0}{1}".format(self.namespace, key))

        if response: return True

        return False

    def read(self):

        response = self.redis.get(self.key)

        if not response: return None

        response = tornado.escape.json_decode(response)

        return response

    def write(self, value):
        if isinstance(value, dict):
            value = tornado.escape.json_encode(value)

        self.redis.setex(self.key, value, self.options['expire'])