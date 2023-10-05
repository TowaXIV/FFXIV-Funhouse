import json

with open(r"database\\ItemProperties.json", 'r') as f:
    data = json.load(f)
    test = [ i.get('name') for i in data["data"]]
    print(test)