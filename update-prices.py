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
gItemIgnore = 'ItemIgnore.txt'

# Boot database subdir
global gRootDir
gRootDir = fr'{dataDir}\\pricing-update-{gTimestamp}'
os.mkdir(gRootDir)

#%%     Functions
def getPrices(url):
    #retrieve data from universalis
    request_object = api.marketBoardCurrentData(url)
    #check status code

    #log data
    with open(fr"{gRootDir}\\_universalis-prices.json", 'w') as f:
        json.dump(request_object.json(), f, indent=4)
    return request_object

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
#%%     Load in pricing & itemID list
# ItemProperties
itemProps = JSONClass(os.path.join(dataDir,gItemProperties)).readjson()
saveItemProps(itemProps)
itemProps = itemProps["data"]

# Pricing
pricingData = CSVClass(os.path.join(dataDir,gPricingData)).readcsv()
savePricing(pricingData)
pricingData = pricingData["data"]

# Set-up list of unique Pricing items
lItems = pricingData["Item Name"].values.tolist()
lItems = list(dict.fromkeys(lItems))
lItems.sort()

# Remove items on the ignore list
itemIgnore = CSVClass(os.path.join(dataDir,gItemIgnore)).readcsv()
itemIgnore = list(itemIgnore["data"])
print(lItems)

# Identify items with no ID


# Update all prices with api
getUrl = 'https://universalis.app/api/v2/Europe/2,3?listings=2&entries=2&noGst=1&hq=false&statsWithin=86000000&entriesWithin=86000000'
getPrices(getUrl)

#%%     Update spreadsheet pricing
