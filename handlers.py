
import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options

define('gmaps-key', default='NOKEY', help='GMaps Api key')
define('wiki-key', default='NOKEY', help='MediaWiki Api key')


async def fetch_json(url):
    response = await AsyncHTTPClient().fetch(url)
    print(response.body)
    return json.loads(response.body)


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = None

    def prepare(self):
        method = self.request.method
        path = self.request.path
        args = tuple((x, tuple(y)) for x, y in self.request.arguments.items())
        self.cache = self.application.cache.get((method, path, args))
        self.application.req_log.append(f'{method} {path} -> {args}')

    def on_finish(self):
        pass


class GeoHandler(BaseHandler):

    async def get(self):
        self.request
        addr = self.get_argument('address')
        cached_res = self.application.cache.get(('geoc', addr))
        if cached_res:
            print('cached')
            self.write(cached_res)
        gmaps_qry = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                    f'address={addr}&key={options.gmaps_key}'
        gmaps_res = await fetch_json(gmaps_qry)
        res = gmaps_res.get('results')[0]['geometry']['location']
        self.application.cache[('geoc', addr)] = res
        # TODO: change 'lng' key to 'lon'
        self.write(res)


class WikiHandler(BaseHandler):

    async def get(self):
        lat = self.get_argument('lat')
        lng = self.get_argument('lng')
        cached_res = self.application.cache.get(('wiki', (lat, lng)))
        if cached_res:
            print('cached')
            self.write(cached_res)
            return

        wiki_qry = f'https://en.wikipedia.org/w/api.php?action=query&list=' \
                   f'geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=10&format=json'
        res = await self.fetch_wiki_art(wiki_qry)

        self.application.cache[('wiki', (lat, lng))] = res
        self.write(res)

    async def fetch_wiki_art(self, wiki_qry):
        wiki_res = await fetch_json(wiki_qry)
        locations = wiki_res.get('query').get('geosearch')
        res = list()
        # TODO: add thumbnailURL
        for art in locations:
            res.append(
                {'title': art.get('title'),
                 'thumbnailURL': None,
                 'coordinates':
                     {'lat': art['lat'],
                      'lon': art['lon']}})
        res = json.dumps(res)
        return res


class PurgeHandler(BaseHandler):

    def get(self):
        self.application.cache = dict()

    def post(self):
        self.application.cache = dict()


class UsageHandler(BaseHandler):

    def get(self):
        self.write(json.dumps(self.application.req_log))