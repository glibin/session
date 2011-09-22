import tornado.web
import session

class Handler(tornado.web.RequestHandler):
    @property
    def redis(self):
        return self.application.redis

    def finish(self, chunk=None):
        super(Handler, self).finish(chunk)
        if hasattr(self, 'session') and self.session:
            self.session.write()

    def prepare(self):
        token = self.get_argument('token', None)

        try:
            self.session = session.SessionManager({'token' : token, 'redis' : self.redis})
        except session.TransportError:
            raise tornado.web.HTTPError(500)
        except session.SessionSecurityError:
            raise tornado.web.HTTPError(403)