import tornado.web
import session

class Handler(tornado.web.RequestHandler):
    @property
    def redis(self):
        return self.application.redis

    def finish(self, chunk=None):
        if hasattr(self, 'session') and self.session:
            self.session.write()

            if 'use_cookies' in self.application.settings and self.application.settings['use_cookies'] and self.session.is_fresh():
                self.set_cookie(
                    'token',
                    self.session.token(),
                    domain = self.application.settings['cookie_domain'] if 'cookie_domain' in self.application.settings else None,
                    expires_days = int(self.session.options['expire'] / 86400)
                )

        super(Handler, self).finish(chunk)


    def prepare(self):
        token = self.get_argument('token', None)

        if 'use_cookies' in self.application.settings and self.application.settings['use_cookies']:
            token = self.get_cookie('token')

        try:
            self.session = session.SessionManager({
                'token' : token,
                'redis' : self.redis,
                'namespace' : self.application.settings['namespace'] if 'namespace' in self.application.settings else '',
                'expire' : self.application.settings['expire'] if 'expire' in self.application.settings else 86400

            })
        except session.TransportError:
            raise tornado.web.HTTPError(500)
        except session.SessionSecurityError:
            raise tornado.web.HTTPError(403)