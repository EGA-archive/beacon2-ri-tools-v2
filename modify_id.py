import json
import hashlib

with open('files/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)

caseLevelData=[]

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

for record in dict_properties:
    caseObject={}
    try:
        caseObject = record
        _id=get_hash(record["datasetId"]+record["identifiers"]["genomicHGVSId"])
        caseObject["_id"]= _id
        caseObject["variantInternalId"]= _id
        caseLevelData.append(caseObject)
    except Exception:
        continue

with open("files/genomicVariations_.json", 'w') as f:
    json.dump(caseLevelData, f)