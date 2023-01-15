import json
import csv

from tornado_server import *

with open("specific_ah_all_items_.txt", "r") as iFile:
    data = iFile.read()
    dump = json.loads(data)
    print(type(dump))
    for key in dump:
        #{'auctionHouseId': 4, 'itemId': 5042, 'petSpeciesId': None, 'minBuyout': 7400, 'quantity': 354, 'marketValue': 9330, 'historical': 19200, 'numAuctions': 16}
        if key['itemId'] != None:
            resp = create_realm_data(key)
            if not resp:
                print(key)
            
        
        #{'regionId': 1, 'itemId': 13367, 'petSpeciesId': None, 'quantity': 1, 'marketValue': 1761221570, 'avgSalePrice': 250100, 'salePct': 0, 'soldPerDay': 0, 'historical': 2764487700}