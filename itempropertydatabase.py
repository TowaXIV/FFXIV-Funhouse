import json
version = 'v2'
"""
Type of database: JSON
Purpose:
    - Structured storage of items, their IDs (required for some interfaces), pricing (user-defined value)
    - Provides information on item dependencies (crafting)
    - Called on by scripts to provide meta-information and can be updated by scripts
3rd party permissions: read/write
Structure:
{
    "version": version, #string, version
    "data": [ #list, item entry
        {
            "id": 0, #int, ID of the item
            "name": "", #item name
            "price": 0, # average price history on FFXIV marketboard
            "lastUpdate": "", # last date an interface updated info of the entry
            "acquisition": "", # whether item is crafted, gathered, or bought from vendor
            "ingredients": [ # required items to craft 1 of entry
                {
                    "id": 0, # itemID of item N
                    "quantity": 0 # required number of item N for 1 craft
                } # ingredient N
            ]
        }
    ]
}
"""
#%% Item JSON Database Class
class ItemDatabase:
    def __init__(self,itemName):
        self.name = itemName

    def newEntry(self): #provide directory and name for database 
        entry = {
            "id": 0, #int, ID of the item
            "name": self.name, #str, item name
            "price": 0, #int, average price history on FFXIV marketboard
            "lastUpdate": "", #str, last date an interface updated info of the entry
        }
        return entry

    def newIDListing(self):
        entry = ItemDatabase(self.name).newEntry()
        print(entry)
#        url = rf"https://xivapi.com/search?indexes=item&string={item}"
#        response, newItemID = api.itemIDSearch(url,item)
#        if response.status_code != 200:
#            print(f"Something went wrong fetching ID from XIVAPI, status code: {response.status_code}")
#        entry[item]["ID"] = newItemID["ID"]
#        with open(f"{gRootDir}\\_newItemID\\{item}.json",'w') as f: # save data for logging
#            json.dump(response.json(), f, indent=4)
#        return entry

ItemDatabase('fire shard').newIDListing()

#%% Changelog
"""
    v2 (2023/*)
        revise data structure (include version, list data in array, sortable)

    v1 (2023/09/23)
        Set-up database with ID, name, price, last update.
"""