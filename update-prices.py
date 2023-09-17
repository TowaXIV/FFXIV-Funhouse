from accessFile import CSVClass, JSONClass
import apiUniversalis as api
import json
import os
import pandas as pd
from datetime import datetime

#%%     Global Constants

# Database identifier
global dataDir
dataDir = r'C:\Users\Martijn\Documents\Python\Funhouse\database'
# Runtime identifier
global gTimestamp
now = datetime.now()
gTimestamp = now.strftime("%Y%m%d-%H%M%S")
# Item Properties identifier
global gItemProperties
gItemProperties = 'ItemProperties.json'
# Pricing identifier
global gPricingData
gPricingData = 'PricingData.csv'
# Ignore list identifier
global gItemIgnore
gItemIgnore = 'ItemIgnore.csv'

# Boot database subdir
global gRootDir
gRootDir = fr'{dataDir}\\pricing-update-{gTimestamp}'
os.mkdir(gRootDir)
# Boot database universalis prices subdir
global gPricesDir
gPricesDir = f"{gRootDir}\\_universalis-prices"
os.mkdir(gPricesDir)

#%%     Functions
def getPrices(item,id):
#   https://universalis.app/api/v2/Europe/2?listings=0&entries=0
    region = 'Europe'
    listings = 0
    entries = 0
    response = api.marketBoardCurrentData(
        rf"https://universalis.app/api/v2/{region}/{id}?listings={listings}&entries={entries}")

    #log data
    with open(fr"{gPricesDir}\\{item}.json", 'w') as f:
        json.dump(response.json(), f, indent=4)
    return response.json()

def saveItemProps(data):
    data["dirpath"] = gRootDir
    ssRootname = data["rootname"]
    data["rootname"] = f"{ssRootname}-before-{gTimestamp}"
    JSONClass(data).savejson() 

def savePricing(data):
    data["dirpath"] = gRootDir
    ssRootname = data["rootname"]
    data["rootname"] = f"{ssRootname}-before-{gTimestamp}"
    CSVClass(data).savetocsv()

def listRemoveDuplicates(source,filter):
    source = [x.lower() for x in source]
    filter = [x.lower() for x in filter]
    for i in source[:]:
        if i in filter:
            source.remove(i)
    return source

def newIDListing(item):
    entry = {item:{"ID":"","Price":"","LastUpdate":""}}
    url = rf"https://xivapi.com/search?indexes=item&string={item}"
    response, newItemID = api.itemIDSearch(url,item)
    if response.status_code != 200:
        print(f"Something went wrong fetching ID from XIVAPI, status code: {response.status_code}")
    entry[item]["ID"] = newItemID["ID"]
    with open(f"{gRootDir}\\_newItemID\\{item}.json",'w') as f: # save data for logging
        json.dump(response.json(), f, indent=4)
    return entry

#%%     Load in pricing & itemID list
def main():
    # ItemProperties
    itemProps = JSONClass(os.path.join(dataDir,gItemProperties)).readjson()
    saveItemProps(itemProps) #save backup in local database
    itemProps = itemProps["data"] #strip to only data

    # Pricing spreadsheet
    pricingData = CSVClass(os.path.join(dataDir,gPricingData)).readcsv()
    savePricing(pricingData) #save backup in local database
    pricingData = pricingData["data"] #strip to only data

    # Set-up list of unique Pricing items
    lItems = pricingData["Item Name"].values.tolist()
    lItems = list(dict.fromkeys(lItems))
    lItems.sort()

    # Remove items on the ignore list
    lItemIgnore = CSVClass(os.path.join(dataDir,gItemIgnore)).readcsv()
    lItemIgnore = lItemIgnore["data"]["Item Name"].values.tolist()
    lItems = listRemoveDuplicates(lItems,lItemIgnore)

    # Identify items with no ID
    lItemPropsWithID = list(dict.fromkeys(itemProps))
    lItemsWithoutID = listRemoveDuplicates(lItems,lItemPropsWithID)
    print(f"New items to include in databse: {lItemsWithoutID}")
    if len(lItemsWithoutID) > 0: # check if all items have ID, skip if True
        os.mkdir(f"{gRootDir}\\_newItemID")
        for x in lItemsWithoutID:
            newItem = newIDListing(x) # fetch ID with api
            itemProps.update(newItem)

    # Update all prices in itemProps with api
    """
    This has a high load due to the API requests.
    Can be commented for testing/debugging with current prices in JSON.
    
    for key, value in itemProps.items(): # fetch price for object
        price = getPrices(key,value["ID"])
        price = price["averagePrice"]
        rPrice = eval('price / 10')
        rPrice = round(rPrice,0)
        rPrice = int(eval('rPrice * 10'))
        print(f"Current price for {key} (average): {price}, rounded: {rPrice}")
        itemProps[key]["Price"] = rPrice
        itemProps[key]["LastUpdate"] = gTimestamp
    #   save to root database
    with open(f"{dataDir}\\{gItemProperties}",'w') as f:
        json.dump(itemProps, f, indent=4)
    """
    #%%     Update spreadsheet pricing
    # pricingData <-- Data to paste pricing to
    # itemProps <-- Data with pricing to copy
    

#%%     Main
if __name__ == "__main__":
    main()