#%% Modules
# official modules
import json
import os
import pandas as pd
from datetime import datetime

# custom scripts
from accessFile import CSVClass, JSONClass
import apiUniversalis as api
from itempropertydatabase import ItemDatabase

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

def listRemoveDuplicates(source,filter):
    source = [x.lower() for x in source]
    filter = [x.lower() for x in filter]
    for i in source[:]:
        if i in filter:
            source.remove(i)
    return source

def updatePrices(database):
    for entry in database["data"]: # fetch price for object
        """
        price = getPrices(key,value["ID"])
        price = price["averagePrice"]
        rPrice = eval('price / 10')
        rPrice = round(rPrice,0)
        rPrice = int(eval('rPrice * 10'))
        print(f"Current price for {key} (average): {price}, rounded: {rPrice}")
        database[key]["Price"] = rPrice
        database[key]["LastUpdate"] = gTimestamp
        """
    #   save to root database
    with open(f"{dataDir}\\{gItemProperties}",'w') as f:
        json.dump(database, f, indent=4)


#%%     Load in pricing & itemID list
def main():
    # ItemProperties
    itemProps = JSONClass(os.path.join(dataDir,gItemProperties)).readjson()
    saveItemProps(itemProps) #save backup in local database
    itemProps = itemProps["data"] #strip to only data
    print(itemProps["version"])

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
    lItemsWithoutID = lItems.copy()
    for item in lItemsWithoutID:
        if itemProps["data"]["name"] == item:
            lItemsWithoutID.remove(item)
    print(f"New items to include in databse: {lItemsWithoutID}")
    if len(lItemsWithoutID) > 0: # check if all items have ID, skip if True
        os.mkdir(f"{gRootDir}\\_newItemID")
        for x in lItemsWithoutID:
            newItem, response = ItemDatabase(x).newIDListing() # fetch ID with api
            with open(f"{gRootDir}\\_newItemID\\{x}.json",'w') as f: # save data for logging
                json.dump(response.json(), f, indent=4)
            itemProps["data"].append(newItem)
        # somehow sort

    # Update all prices in itemProps with api
    """
    updatePrices has a high load due to the API requests.
    Can be commented for testing/debugging with current prices in JSON.
        - probably make a check if script has run in the past 24 hours,
            unlikely(?) to need a price update more than once per day.
    """
    updatePrices(itemProps)
    
    #%%     Update spreadsheet pricing
    #print(pricingData)
    lItemIgnore = [x.lower() for x in lItemIgnore]
    for row_index, row in pricingData.iterrows():
        item = pricingData.at[row_index, 'Item Name'].lower()
        if item in lItemIgnore:
            pass
        else:
            itemPrice = itemProps.get(item, {}).get('Price')
            itemUpdate = itemProps.get(item, {}).get('LastUpdate')
            pricingData.at[row_index, 'Price to buy'] = itemPrice
            pricingData.at[row_index, 'Last Updated'] = itemUpdate
            #pricingData["Price to buy"] = pricingData["Price to buy"].astype('int')
    #   save to database file
    pricingData.to_csv(rf"{dataDir}\\{gPricingData}", sep=';',index=False)
    print(pricingData)

#%%     Main
if __name__ == "__main__":
    main()