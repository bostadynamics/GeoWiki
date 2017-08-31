
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    cache = dict()
    usage = list()


class GeoHandler(BaseHandler):

    def get(self, *args, **kwargs):
        pass


class WikiHandler(BaseHandler):

    def get(self, *args, **kwargs):
        pass


class PurgeHandler(BaseHandler):

    def post(self):
        pass


class UsageHandler(BaseHandler):

    def get(self):
        pass