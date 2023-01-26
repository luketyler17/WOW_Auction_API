import tornado.ioloop
from tornado_server import *
from bson.json_util import dumps, loads 
#map requests to request handlers -> HTTP requesthandlers
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        print("hello")
        self.write("Hello, Tornado")

class PostHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>This is Post 1 </h1>")

class RealmHandler(tornado.web.RequestHandler):
    #{"auctionHouseId":4,"itemId":44709,"petSpeciesId":null,"minBuyout":60000000,"quantity":2,"marketValue":162538315,"historical":175006200,"numAuctions":2},{"auctionHouseId":4,"itemId":44716,"petSpeciesId":null,"minBuyout":1117600,"quantity":9,"marketValue":1034883,"historical":230000,"numAuctions":1}
    def get(self):
        adId = (self.get_argument("ahId"))
        itemId = [(self.get_argument("itemId"))]
        returnObj = db_calls.blizz_read_realm_data(adId, itemId, "itemId")
        print(returnObj)
        self.write(dumps(returnObj))

class RegionHandler(tornado.web.RequestHandler):
    def get(self):
        regionId = self.get_argument("regionId")
        itemId = [self.get_argument("itemId")]
        returnObj = db_calls.blizz_read_region_data(regionId, itemId, "itemId")
        self.write(dumps(returnObj))

class BlizzHandler(tornado.web.RequestHandler):
    def get(self):
        itemId = [self.get_argument("itemId")]
        returnObj = db_calls.blizz_read_blizz_data(itemId, "itemId")
        self.write(dumps(returnObj))
    
def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
        (r"/post", PostHandler),
        (r"/realm", RealmHandler),
        (r"/region", RegionHandler),
        (r"/blizz", BlizzHandler)
    ],
    debug = True,
    autoreload = True
    )

if __name__ == '__main__':
    app = make_app()
    port = 8888
    app.listen(port)
    print(f"Server is listening on localhost on port {port}")
    tornado.ioloop.IOLoop.current().start()