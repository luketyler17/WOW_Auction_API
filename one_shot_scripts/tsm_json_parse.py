import json



with open("specific_region_all_items.txt", "r") as iFile:
    data = iFile.read()
    dump = json.loads(data)
    print(type(dump))
    for key in dump:
        #{'auctionHouseId': 4, 'itemId': 5042, 'petSpeciesId': None, 'minBuyout': 7400, 'quantity': 354, 'marketValue': 9330, 'historical': 19200, 'numAuctions': 16}
        print(key)
        #{'auctionHouseId': 4, 'itemId': 7099, 'petSpeciesId': None, 'minBuyout': 150000, 'quantity': 42, 'marketValue': 14468570, 'historical': 250000, 'numAuctions': 5}