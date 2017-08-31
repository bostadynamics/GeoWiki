
import json
from tornado import gen
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
        gmaps_qry = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                    f'address={addr}&key={options.gmaps_key}'
        res = await fetch_json(gmaps_qry)
        print(res)
        # TODO: change 'lng' key to 'ion'
        self.write(res.get('results')[0]['geometry']['location'])


class WikiHandler(BaseHandler):

    async def get(self):
        lat = self.get_argument('lat')
        lng = self.get_argument('lng')
        wiki_qry = f'https://en.wikipedia.org/w/api.php?action=query&list=' \
                   f'geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=10&format=json'
        wiki_res = await fetch_json(wiki_qry)
        locations = wiki_res.get('query').get('geosearch')
        res = list()
        for item in locations:
            res.append(
                {'title': item.get('title'),
                 'coordinates':
                     {'lat': item['lat'],
                      'lon': item['lon']}})
        self.write(json.dumps(res))


class PurgeHandler(BaseHandler):

    def post(self):
        pass


class UsageHandler(BaseHandler):

    def get(self):
        pass