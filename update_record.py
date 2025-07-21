from pymongo.mongo_client import MongoClient
from conf import conf
import json
from validators.update.genomicVariations import GenomicVariations
from validators.update.analyses import Analyses
from validators.update.biosamples import Biosamples
from validators.update.cohorts import Cohorts
from validators.update.datasets import Datasets
from validators.update.individuals import Individuals
from validators.update.runs import Runs

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

def validate_record(json_record):
    if conf.record_type == 'genomicVariation':
        GenomicVariations(**json_record)
    elif conf.record_type == 'analysis':
        Analyses(**json_record)
    elif conf.record_type == 'biosample':
        Biosamples(**json_record)
    elif conf.record_type == 'cohort':
        Cohorts(**json_record)
    elif conf.record_type == 'dataset':
        Datasets(**json_record)
    elif conf.record_type == 'individual':
        Individuals(**json_record)
    elif conf.record_type == 'run':
        Runs(**json_record)


def convert_record(json_record):
    update_dict={}
    validate_record(json_record)
    if conf.record_type == 'genomicVariation':
        search_dict={}
        try:
            search_dict["datasetId"]=json_record["datasetId"]
        except Exception:
            print('record to update needs to include a datasetId')
        try:
            search_dict["identifiers.genomicHGVSId"]=json_record["identifiers"]["genomicHGVSId"]
        except Exception:
            print('record to update needs to include a genomicHGVSId')
        update_dict["$set"]=json_record
        initial_record=client.beacon[conf.collection_name].find(search_dict)
        client.beacon[conf.collection_name].update_many(search_dict, update_dict)
        updated_record=client.beacon[conf.collection_name].find(search_dict)
        try:
            validate_record(updated_record[0])
            print('record {} for dataset: {} updated successfully'.format(json_record["identifiers"]["genomicHGVSId"],json_record["datasetId"]))
        except Exception:
            client.beacon[conf.collection_name].delete_one(search_dict)
            client.beacon[conf.collection_name].insert_one(initial_record[0])
            print('record {} for dataset: {} update failed. The document could not be validated against Beacon v2 standards. Please, compare the documents you are updating to resolve the confllicts.'.format(json_record["identifiers"]["genomicHGVSId"],json_record["datasetId"]))
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
        initial_record=client.beacon[conf.collection_name].find(search_dict)
        client.beacon[conf.collection_name].update_many(search_dict, update_dict)
        updated_record=client.beacon[conf.collection_name].find(search_dict)
        try:
            validate_record(updated_record[0])
            print('record {} for dataset: {} updated successfully'.format(json_record["variantInternalId"],json_record["datasetId"]))
        except Exception:
            client.beacon[conf.collection_name].delete_one(search_dict)
            client.beacon[conf.collection_name].insert_one(initial_record[0])
            print('record {} for dataset: {} update failed. The document could not be validated against Beacon v2 standards. Please, compare the documents you are updating to resolve the confllicts.'.format(json_record["variantInternalId"],json_record["datasetId"]))

def update_record():
    with open('files/updated_json/update.json') as json_file:
        json_record = json.load(json_file)
    if isinstance(json_record,list):
        for record in json_record:
            convert_record(record)
    else:
        convert_record(json_record)

update_record()