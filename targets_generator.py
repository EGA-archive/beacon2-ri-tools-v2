import json
import hashlib

with open('files/biosamples.json') as json_file:
    dict_properties = json.load(json_file)

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

caseLevelData=[]
caseObject={}
caseObject["biosampleIds"]=[]

for record in dict_properties:
    try:
        if record["id"] not in caseObject["biosampleIds"]:
            caseObject["biosampleIds"].append(record["id"])
        
    except Exception:
        continue

caseObject["id"]= get_hash("coadread_tcga_pan_can_atlas_2018")
caseObject["datasetId"]= "coadread_tcga_pan_can_atlas_2018"
caseLevelData.append(caseObject)

with open("files/targets.json", 'w') as f:
    json.dump(caseLevelData, f)