
import pymongo
import logging
from bson.json_util import dumps, loads 

__all__ = ['create_region_data', 'create_realm_data', 'create_blizz_data',
           'update_region_data', 'update_realm_data', 'update_blizz_data',
           'read_region_data'  , 'read_realm_data'  , 'read_blizz_data'  ,
           'delete_region_data', 'delete_realm_data', 'delete_blizz_data',
          ]
'''
    RegionData dict format:::
        {
            *UNIQUE regionId = int
            *UNIQUE itemId = int
            petSpeciesId = str
            quantity = int
            marketValue = int
            avgSalePrice = int
            salePct = int
            soldPerDay = int
            historical = int
        }
    
    RealmData dict format:::
        {
            *UNIQUE auctionHouseId = int
            *UNIQUE itemId = int
            petSpeciesId = str
            minBuyout = int
            quantity = int
            marketValue = int
            historical = int
            numAuctions = int
        }
    
    BlizzData dict format:::
        {
            *UNIQUE itemId = int
            itemName = str
            vendorBuy = int
            vendorSell = int
            source //// maybe
        }   


'''

__myclient = pymongo.MongoClient("mongodb://localhost:27017/")
__database = __myclient["wow_item_info"]
__region_collection = __database["region_data"]
__blizz_collection = __database["blizz_data"]
__realm_collection = __database["realm_data"]
__tsm_region_collection = __database["tsm_region_data"]
__tsm_realm_collection = __database["tsm_realm_data"]
__region_collection.create_index([('regionId', 1), ('itemId', 1)], unique=True)
__blizz_collection.create_index('itemId', unique=True)
__realm_collection.create_index([('auctionHouseId', 1), ('itemId', 1)], unique=True)
#__tsm_region_collection.create_index([(''])
logging.basicConfig(filename="../logging/database_logs.txt",
                    filemode="a",
                    format='%(asctime)s %(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def blizz_create_region_data(input_obj):
    __doc__ = '''Creates entry into region_data collection. Takes single dictionary as argument returns bool.
                 If True, entry was successfully created.
                 Calling convention -> create_region_data({'regionId': 1, ....ect})
                 '''
    try:
        response = __region_collection.insert_one(input_obj)
        return response.acknowledged

    except pymongo.errors.DuplicateKeyError:
        logging.info(f"Object:: {input_obj}\n found in region_data table -- insert attempt FAILED")

def blizz_create_blizz_data(input_obj):
    __doc__ = '''Creates entry into blizz_data collection. Takes single dictionary as argument returns bool.
                 If True, entry was successfully created.
                 Calling convention -> create_blizz_data({'itemId': 123456, ....ect})
                 '''
    try:
        response = __blizz_collection.insert_one(input_obj)
        return response.acknowledged

    except pymongo.errors.DuplicateKeyError:
        logging.info(f"Key {input_obj.itemId} found in blizz_data table -- insert attempt FAILED")

def blizz_create_realm_data(input_obj):
    __doc__ = '''Creates entry into realm_data collection. Takes single dictionary as argument returns bool.
                 If True, entry was successfully created.
                 Calling convention -> create_realm_data({'auctionHouseId': 1, ....ect})
                 '''
    try:
        response = __realm_collection.insert_one(input_obj)
        return response.acknowledged

    except pymongo.errors.DuplicateKeyError:
        logging.info(f"Key {input_obj.itemId} found in realm_data table -- insert attempt FAILED")

def blizz_read_region_data(regionId, list_of_ids, id_type):
    __doc__ = '''Reads region_data database from type of IDs sent into function, Present the regionId, a list of IDs and what type of field those ids are.
                 E.G read_region_data(1, ['12345'], 'itemId') <- will search for itemId 12345 from Region 1 in region_data collection.
                 If presented with more than one ID function will return list of dicts containing information, 
                 if presented one ID will return a list with a single item'''
    try:
        return_list = []
        for id in list_of_ids:
            if type(id) != int or type(regionId) != int:
                id = int(id)
                regionId = int(regionId)
            cursor = __region_collection.find_one({'regionId': regionId, id_type: id}, {"_id":0})
            
            return_list.append(cursor)
        return return_list
    except Exception as e:
        logging.warning(f"READ REGION DATA::: {Exception}")
        print(e)

def blizz_read_realm_data(ahId, list_of_ids, id_type):
    __doc__ = '''Reads realm database from type of IDs sent into function, Present the auctionHouseId, list of IDs and what type of field those ids are.
                 E.G read_realm_data(1, ['12345'], 'itemId') <- will search for itemId 12345 from Realm #1 in realm_data collection.
                 If presented with more than one ID function will return list of dicts containing information, 
                 if presented one ID will return a list with a single item'''
    try:
        return_list = []
        for id in list_of_ids:
            if type(id) != int or type(ahId) != int:
                id = int(id)
                ahId = int(ahId)
            returnObj = __realm_collection.find_one({'auctionHouseId': ahId, id_type: id}, {"_id":0})
            return_list.append(returnObj)
        return return_list
    except Exception as e:
        logging.warning(f"READ REALM DATA::: {Exception}")
        print(e)

def blizz_read_blizz_data(list_of_ids, id_type):
    __doc__ = '''Reads blizz database from type of IDs sent into function, Present the list of IDs and what type of field those ids are.
                 E.G read_blizz_data([12345], 'itemId') <- will search for itemId 12345 in blizz_data collection.
                 If presented with more than one ID function will return list of dicts containing information, 
                 if presented one ID will return a list with a single item'''
    try:
        return_list = []
        for id in list_of_ids:
            if type(id) != int or type(regionId) != int:
                id = int(id)
                regionId = int(regionId)
            return_dict = __region_collection.find_one({id_type: id})
            return_list.append(return_dict)
        return return_list
    except Exception as e:
        logging.warning(f"READ BLIZZ DATA::: {Exception}")
        print(e)

def blizz_update_region_data(realm, id_to_update, id_type, update_info):
    __doc__ = '''Finds matching object in region_data table, and passes updated dictonary into the table
                 calling convention -> update_region_data(1, 12345, 'itemId', {marketValue = 123456789})
                 Returns none if none found
              '''
    try:
        response = __region_collection.find_one_and_update({'realmId':realm, id_type: id_to_update}, update_info)
        return response
    except Exception as e:
        logging.warning(f"UPDATE REGION DATA::: {Exception}")
        print(e)

def blizz_update_realm_data(auctionHouseId, id_to_update, id_type, update_info):
    __doc__ = '''Finds matching object in realm_data table, and passes updated dictonary into the table
                 calling convention -> update_realm_data(1, 12345, 'itemId', {marketValue = 123456789})
                 Returns none if none found
              '''
    try:
        response = __realm_collection.find_one_and_update({'auctionHouseId':auctionHouseId, id_type: id_to_update}, update_info)
        return response
    except Exception as e:
        logging.warning(f"UPDATE REALM DATA::: {Exception}")
        print(e)

def blizz_update_blizz_data(id_to_update, id_type, update_info):
    __doc__ = '''Finds matching object in region_data table, and passes updated dictonary into the table
                 calling convention -> update_blizz_data(12345, 'itemId', {vendorBuy = 10000})
                 Returns none if none found
              '''
    try:
        response = __blizz_collection.find_one_and_update({id_type: id_to_update}, update_info)
        return response
    except Exception as e:
        logging.warning(f"UPDATE BLIZZ DATA::: {Exception}")
        print(e)


def blizz_delete_region_data(regionId, itemId):
    __doc__ = '''Finds item by matching regionId and ItemId in Database, if found, deletes the item 
                 and returns the number of entries deleted, if not found returns 0
                 calling convention -> delete_region_data(1, 12345)'''
    try:
        response = __region_collection.delete_one({'regionId': regionId, 'itemId': itemId})
        return response.deleted_count
    except Exception as e:
        logging.warning(f"DELETE REGION DATA::: {Exception}")
        print(e)

def blizz_delete_realm_data(auctionHouseId, itemId):
    __doc__ = '''Finds item by matching RealmId and ItemId in Database, if found, deletes the item 
                 and returns the number of entries deleted, if not found returns 0
                 calling convention -> delete_realm_data(1, 12345)'''
    try:
        response = __region_collection.delete_one({'auctionHouseId': auctionHouseId, 'itemId': itemId})
        return response.deleted_count
    except Exception as e:
        logging.warning(f"DELETE BLIZZ DATA::: {Exception}")
        print(e)

def blizz_delete_blizz_data(itemId):
    __doc__ = '''Finds item by matching ItemId in Database, if found, deletes the item 
                 and returns the number of entries deleted, if not found returns 0
                 calling convention -> delete_blizz_data(12345)'''
    try:
        response = __blizz_collection.delete_one({'itemId': itemId})
        return response.deleted_count
    except Exception as e:
        logging.warning(f"DELETE BLIZZ DATA::: {Exception}")
        print(e)

#######
#CREATE TSM CRUD CALLS
######

def tsm_create_region_data(inputObj):
    pass


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    #have to impliment try/except block -> if entering in values that exist into databse will throw err and crash python script that object already exists within database
    print(myclient.list_database_names())
    print(mydb.list_collection_names())

    # config = {
    #     'host' : 'localhost',
    #     'port' : 27018,
    #     'user' : 'root',
    #     'password': 'password',
        
    # }


