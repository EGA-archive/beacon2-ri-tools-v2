from pymongo.mongo_client import MongoClient
from conf import conf
import json

client = MongoClient(
        #"mongodb://127.0.0.1:27017/"
        "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
            conf.database_user,
            conf.database_password,
            conf.database_host,
            conf.database_port,
            conf.database_name,
            conf.database_auth_source,
        )
    )

def convert_record(json_record):
    update_dict={}
    if conf.genomicVariation == True:
        search_dict={}
        try:
            search_dict["datasetId"]=json_record["datasetId"]
        except Exception:
            print('record to update needs to include a datasetId')
        try:
            search_dict["variantInternalId"]=json_record["variantInternalId"]
        except Exception:
            print('record to update needs to include a variantInternalId')
        update_dict["$set"]=json_record
        client.beacon[conf.collection].update_many(search_dict, update_dict)
        print('record {} for dataset: {} updated successfully'.format(json_record["variantInternalId"],json_record["datasetId"]))
    else:
        search_dict={}
        try:
            search_dict["datasetId"]=json_record["datasetId"]
        except Exception:
            print('record to update needs to include a datasetId')
        try:
            search_dict["id"]=json_record["id"]
        except Exception:
            print('record to update needs to include an id')
        update_dict["$set"]=json_record
        client.beacon[conf.collection].update_many(search_dict, update_dict)
        print('record {} for dataset: {} updated successfully'.format(json_record["id"],json_record["datasetId"]))

def update_record():
    with open('files/updated_json/update.json') as json_file:
        json_record = json.load(json_file)
    if isinstance(json_record,list):
        for record in json_record:
            convert_record(record)
    else:
        convert_record(json_record)

update_record()