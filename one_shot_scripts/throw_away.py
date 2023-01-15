
import requests
import secrets_wow
import json



with open("active_auctions.txt", "w+") as oFile:
    token = secrets_wow.b_get_access_token 
    url = ""
    resp = requests.get(f"https://us.api.blizzard.com/data/wow/auctions/commodities?namespace=dynamic-us&locale=en_US&access_token=US8SN3w5KJ2MGye2LqZPwOoLT9DQTzSYq5")
    oFile.write(resp.text)
    print("finished")
    oFile.close