
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import parse_command_line

import handlers

urls = [
    (r'/geocode',  handlers.GeoHandler),
    (r'/wikiNearby', handlers.WikiHandler),
    (r'/purgeCache', handlers.PurgeHandler),
    (r'/usage', handlers.UsageHandler)
]

class App(Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = dict()
        self.req_log = list()

if __name__ == '__main__':
    parse_command_line()
    app = App(urls, debug=True)
    app.listen(8888)
    IOLoop.current().start()