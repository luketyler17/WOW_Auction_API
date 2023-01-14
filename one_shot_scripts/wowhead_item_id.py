'''
    Taking list of items that you are able to buy from a vendor and turning into complete data...
    Manipulates return JSON string from BlizzAPI to access individual cell values
        E.G Finding Sell/Buy from vendor price and putting into CSV file for future use
        
    OBJECT.purchase_price === Price when buying from vendor
    OBJECT.sell_price === Price when selling to vender
    OBJECT.preview_item.sell_price.value === Current selling price from the Tooltip / Can be based on Ilvl of item & different from OBJECT.sell_price
''' 
import requests
import json
import csv
import struct
import codecs
import sys
import secrets_wow
import ratelimit


def wow_item_request(item_id):
        pass
    
 

access_token = secrets_wow.keys.b_get_access_token()

if __name__ == '__main__':
    with open("/home/luke/Documents/wowhead_items_id.csv", "r") as iFile:
        dataCSV = csv.reader(iFile)
        for row in dataCSV:
            url = f"https://us.api.blizzard.com/data/wow/item/201323?namespace=static-us&locale=en_US&access_token={access_token}"
            print(row[0])
            resp = requests.get(url)
            print(resp.text)
            resp_dict = json.loads(resp.text)
            resp_dict
            break
