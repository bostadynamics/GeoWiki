
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
    cache = dict()
    usage = list()


class GeoHandler(BaseHandler):

    async def get(self):
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
        # TODO: change 'lng' key to 'ion'
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
        wiki_res = await fetch_json(wiki_qry)
        locations = wiki_res.get('query').get('geosearch')
        res = list()
        # TODO: add thumbnailURL
        for item in locations:
            res.append(
                {'title': item.get('title'),
                 'thumbnailURL': None,
                 'coordinates':
                     {'lat': item['lat'],
                      'lon': item['lon']}})
        res = json.dumps(res)
        self.application.cache[('wiki', (lat, lng))] = res
        self.write(res)


class PurgeHandler(BaseHandler):

    def get(self):
        self.application.cache = dict()


class UsageHandler(BaseHandler):

    def get(self):
        pass