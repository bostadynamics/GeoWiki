
from tornado.web import Application
from tornado.ioloop import IOLoop

import handlers

urls = [
    (r'/geocode*',  handlers.GeoHandler),
    (r'/wikiNearby', handlers.WikiHandler),
    (r'/purgeCache', handlers.PurgeHandler),
    (r'/usage', handlers.UsageHandler)
]


if __name__ == '__main__':
    app = Application(urls)
    app.listen(8888)
    IOLoop.current().start()