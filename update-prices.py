#%% Modules
# official modules
import json
import logging
import os
import pandas as pd
from datetime import datetime
import logging
import logging.config
# for custom modules, see below logging boot
#%%     Global Constants

# Database identifier
global dataDir
dataDir = r'C:\Python\FFXIV-Funhouse\database'
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

# Logging boot
LOG_CONFIG = json.load(open('config/logging/logging.conf', 'r'))
LOG_CONFIG['handlers']['file']['filename'] = f'{gRootDir}/logfile.log'

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger(__name__)

logger.info(f'Running {__file__}.')
logger.info(f'Logger configured using logging.conf in .../config/logging.')

# custom modules
from accessFile import CSVClass, JSONClass
import apiUniversalis as api
from itempropertydatabase import ItemDatabase

#%%     Functions
def getPrices(item,id):
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

def listRemoveDuplicates(source,filter): # check list source & list filter, del matches in source + return
    source = [x.lower() for x in source]
    filter = [x.lower() for x in filter]
    source.sort()
    filter.sort()
    filtered_list = source.copy()
    for i in source:
        if i in filter:
            filtered_list.remove(i)
    return filtered_list

def updatePrices(entries, database): # fetch prices for objects using Universalis API
    for item in database["data"]: 
        if item["name"] in entries:
            price = getPrices(item["name"],item["id"])
            price = price["averagePrice"]
            rPrice = eval('price / 10')
            rPrice = round(rPrice,0)
            rPrice = int(eval('rPrice * 10'))
            print(f"Current price for {item['name']} (average): {price}, rounded: {rPrice}")
            item["price"] = rPrice
            item["lastUpdate"] = gTimestamp
    with open(f"{dataDir}\\{gItemProperties}",'w') as f:
        json.dump(database, f, indent=4)
    return database

#%%     Load in pricing & itemID list
def main():
    logger.info('Start function "main".')
    logger.info(f'data directory set as {dataDir}.')
    # ItemProperties
    itemProps = JSONClass(os.path.join(dataDir,gItemProperties)).readjson()
    logger.info(f'Successfully read data in from Item Properties: "{gItemProperties}".')
    logger.info('Saving backup to local database.')
    saveItemProps(itemProps) #save backup in local database
    itemProps = itemProps["data"] #strip to only data
    logger.debug('Stripping dirpath metadata from data. Should not do this.')

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

    # Identify items with no entry in database
    lItemsWithID = [i.get('name') for i in itemProps["data"]] # retrieve list of items in ItemDB
    lItemsWithoutID = lItems.copy() # copy list for local processing
    lItemsToProcess = listRemoveDuplicates(lItemsWithoutID,lItemsWithID)

    logger.info(f"New items to include in databse: {lItemsToProcess}")
    if len(lItemsToProcess) > 0: # check if all items have ID, skip if True
        os.mkdir(f"{gRootDir}\\_newItemID")
        for x in lItemsToProcess:
            newItem, response = ItemDatabase(x).newIDListing() # fetch ID with api
            with open(f"{gRootDir}\\_newItemID\\{x}.json",'w') as f: # save data for logging
                json.dump(response.json(), f, indent=4)
            itemProps["data"].append(newItem)
        # somehow sort

    # Update all prices in spreadsheet with api
    """
    updatePrices has a high load due to the API requests.
    Can be commented for testing/debugging with current prices in JSON.
        - probably make a check if script has run in the past 24 hours,
            unlikely(?) to need a price update more than once per day.
    """
    itemProps = updatePrices(lItems, itemProps)
    
    #%%     Update spreadsheet pricing
    lItemIgnore = [x.lower() for x in lItemIgnore]
    for row_index, row in pricingData.iterrows():
        item = pricingData.at[row_index, 'Item Name'].lower()
        if item not in lItemIgnore:
            dbEntry = next(i for i in itemProps["data"] if i["name"] == item)
            itemPrice = dbEntry.get('price')
            itemUpdate = dbEntry.get('lastUpdate')
            pricingData.at[row_index, 'Price to buy'] = itemPrice
            pricingData.at[row_index, 'Last Updated'] = itemUpdate

    #   save to database file
    pricingData.to_csv(rf"{dataDir}\\{gPricingData}", sep=';',index=False)
    print(pricingData)

#%%     Main
if __name__ == "__main__":
    logger.debug('Module ran as __main__.')
    main()