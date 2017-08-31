
import json
from tornado import gen
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient

gmaps_key = ''
wiki_key = ''

async def fetch_json(url):
    response = await AsyncHTTPClient().fetch(url)
    return json.loads(response.body)


class BaseHandler(RequestHandler):
    cache = dict()
    usage = list()


class GeoHandler(BaseHandler):

    async def get(self):
        addr = self.get_argument('address')
        gmaps_qry = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                    f'address={addr}&key={gmaps_key}'
        res = await fetch_json(gmaps_qry)
        self.write(res.get('results')[0]['geometry']['location'])


class WikiHandler(BaseHandler):

    def get(self, *args, **kwargs):
        pass


class PurgeHandler(BaseHandler):

    def post(self):
        pass


class UsageHandler(BaseHandler):

    def get(self):
        pass