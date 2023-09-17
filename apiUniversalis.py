import requests

r"""
API Server

GET, request data

Status codes (GET)
200 - Everything went OK.
301 - Server is redirecting you to a different endpoint.
400 - Bad request. Check data input.
401 - Bad authentication.
403 - Insufficient permissions, access forbidden.
404 - Data not found.
503 - The server was not ready to handle the request.

Default url chain:
    https://universalis.app

Path arguments:
    .../<argument>/

Query arguments:
    .../<path>?<argument>=<value>&<argument>=<value>
"""

def marketBoardCurrentData(url):
    r"""
    GET - /api/v2/{worldDcRegion}/{itemIds}
    Retrieves the data currently shown on the market board for the requested item(s) and world(s).
    Up to 100 itemIDs can be comma-separated in order to retrieve data for multiple items at once.

    Responses
    200 | Data retrieved successfully
    400 | Invalid parameters
    404 | The world/DC or item requested is invalid. Not caused by multiple items with some/all invalid, the returned list of unresolved itemIDs will contain the invalid itemIDs or IDs.
    
    ItemIds         | string, path. The item ID or comma-separated item IDs to retrieve data for.
    worldDcRegion   | string, path. The world, data center, or region to retrieve data for. May be ID or name. Regions should be specified as Japan, Europe, North-America, Oceania, China
    listings        | string, query. Number of listings to return per item (default: all).
    entries         | string, query. The number of recent history entries to return per item (default: 5).
    noGst           | string, query. If gil sales tax (GST) should not be factored in (default: false).
    hq              | string, query. Filter for HQ listings and entires, false = NQ, true = HQ (default: blank).
    statsWithin     | string, query. The amount of time before now to calculate stats over, in milliseconds (default: 7 days).
    entriesWithin   | string, query. The amount of time before now to take entries within, in seconds. Negative values will be ignored.
    fields          | string, query. Comma separated list of fields that should be included in the response (default, all fields | example: listings.pricePerUnit).
    """
    response = requests.get(url)
    return response

if __name__ == '__main__':
    response = requests.get("https://universalis.app/api/v2/Europe/2,3?listings=2&entries=2&noGst=1&statsWithin=86000000&entriesWithin=86000000&fields=listings.pricePerUnit%2CaveragePrice")
    print(response.status_code)
    print(type(response))