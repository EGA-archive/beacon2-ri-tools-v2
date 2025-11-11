import json

with open('files/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)

with open('files/targets.json') as json_file:
    dict_targets = json.load(json_file)

caseLevelData=[]

for record in dict_properties:
    caseObject={}
    try:
        for biosample in record["caseLevelData"]:
            if biosample["biosampleId"] in dict_targets[0]["biosampleIds"]:
                ind = int(dict_targets[0]["biosampleIds"].index(biosample["biosampleId"]))
                str_ind = str(ind)
                if biosample["zygosity"]["label"] == "0/1":
                    caseObject[str_ind] = "01"
                elif biosample["zygosity"]["label"] == "1/1":
                    caseObject[str_ind] = "11"
                elif biosample["zygosity"]["label"] == "1/0":
                    caseObject[str_ind] = "10"
        caseObject["id"]= record["identifiers"]["genomicHGVSId"]
        caseObject["datasetId"]= "coadread_tcga_pan_can_atlas_2018"
        caseObject["_id"]= record["_id"]
        caseLevelData.append(caseObject)
    except Exception as e:
        print(e)
        continue

with open("files/caseLevelData.json", 'w') as f:
    json.dump(caseLevelData, f)