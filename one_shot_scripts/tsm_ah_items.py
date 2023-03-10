import requests
import json
import csv
import struct
import codecs
import sys
import secrets_wow
import ratelimit

# Pricing API LIMITS:
# /region/{regionId}/item/{itemId} - 500 per 24 hours
# /ah/{auctionHouseId}/item/{itemId} - 500 per 24 hours
# /region/{regionId} - 10 per 24 hours
# /ah/{auctionHouseId} - 100 per 24 hours

#TSM API URLs
#https://realm-api.tradeskillmaster.com/public
#https://pricing-api.tradeskillmaster.com/public
#
#getreqHEADER = {'Authorization': 'Bearer <ACCESS KEY>'}
#
#Fetch all item stats for a given auction house
#https://pricing-api.tradeskillmaster.com/ah/{auctionHouseId}
#
#Fetch item stats for a given item in a given auction house
#https://pricing-api.tradeskillmaster.com/ah/{auctionHouseId}/item/{itemId}
#
#Fetch all item stats for a given region
#https://pricing-api.tradeskillmaster.com/region/{regionID}
#
#Fetch item stats for an item in a given region
#https://pricing-api.tradeskillmaster.com/region/{regionId}/item/{itemId}
#
#***Region, Realm, Server, Auction IDs***
#"regionId":1
#"realmId":5
#"name":"Tichondrius"
#"auctionHouseId":4



__all__ = ['specific_ah_all_items', 'specific_ah_specific_item', 'specific_region_all_items', 'specific_region_specific_item']


#Access token used to run get() requests
__access_token = secrets_wow.keys.t_get_access_token()

#Grabs all item auction data for a specific auction house
def specific_ah_all_items(auctionHouseId):
    url = f"https://pricing-api.tradeskillmaster.com/ah/{auctionHouseId}"
    resp = __fetch_component(url, __access_token)
    with open("specific_ah_all_items.txt", "w+") as oFile:
        oFile.write(resp.text)
        oFile.close()

#Grabs specific item auction data for a specific auction house
def specific_ah_specific_item(itemId, auctionHouseId):
    url = f"https://pricing-api.tradeskillmaster.com/ah/{auctionHouseId}/item/{itemId}"
    resp = __fetch_component(url, __access_token)
    with open("specific_ah_specific_item.txt", "w+") as oFile:
        oFile.write(resp.text)
        oFile.close()

#Grabs all item auction data for a specific region
def specific_region_all_items(regionId):
    url = f"https://pricing-api.tradeskillmaster.com/region/{regionId}"
    resp = __fetch_component(url, __access_token)
    with open("specific_region_all_items.txt", "w+") as oFile:
        oFile.write(resp.text)
        oFile.close()

#Grabs specific item auction data for a specific region
def specific_region_specific_item(regionId, itemId):
    url = f"https://pricing-api.tradeskillmaster.com/region/{regionId}/item/{itemId}"
    resp = __fetch_component(url, __access_token)
    with open("specific_region_specific_item.txt", "w+") as oFile:
        oFile.write(resp.text)
        oFile.close()

#Requests passed in URL with Bearer token into TSM to return JSON dump of requested information
def __fetch_component(url, token):
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    return resp
    

if __name__ == '__main__':
    #Hardcoded variables for our specific server/region
    regionId = 1
    realmId = 5
    name = "Tichondrius"
    auctionHouseIdTest = 4
    #specific_ah_all_items(auctionHouseIdTest)
    specific_region_all_items(regionId)