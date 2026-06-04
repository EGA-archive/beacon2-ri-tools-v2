from conf import conf
import json
from validators.update.genomicVariations import GenomicVariations
from validators.update.analyses import Analyses
from validators.update.biosamples import Biosamples
from validators.update.cohorts import Cohorts
from validators.update.datasets import Datasets
from validators.update.individuals import Individuals
from validators.update.runs import Runs
import argparse
import os
from mongo_connection import build_mongo_database

db = build_mongo_database()

def validate_record(json_record, args):
    if args.recordType == 'genomicVariation':
        GenomicVariations(**json_record)
    elif args.recordType == 'analysis':
        Analyses(**json_record)
    elif args.recordType == 'biosample':
        Biosamples(**json_record)
    elif args.recordType == 'cohort':
        Cohorts(**json_record)
    elif args.recordType == 'dataset':
        Datasets(**json_record)
    elif args.recordType == 'individual':
        Individuals(**json_record)
    elif args.recordType == 'run':
        Runs(**json_record)


def convert_record(json_record, args):
    update_dict={}
    validate_record(json_record, args)
    if args.recordType == 'genomicVariation':
        search_dict={}
        search_dict["datasetId"]=json_record["datasetId"]
        search_dict["_id"]=json_record["_id"]
        update_dict["$set"]=json_record
        initial_record=db[args.collection].find(search_dict)
        db[args.collection].update_many(search_dict, update_dict)
        updated_record=db[args.collection].find(search_dict)
        try:
            validate_record(updated_record[0], args)
        except Exception:
            db[args.collection].delete_one(search_dict)
            db[args.collection].insert_one(initial_record[0])
            print('record {} for dataset: {} update failed. The document could not be validated against Beacon v2 standards. Please, compare the documents you are updating to resolve the confllicts.'.format(json_record["_id"],json_record["datasetId"]))
        print('record {} for dataset: {} updated successfully'.format(json_record["_id"],json_record["datasetId"]))
    else:
        search_dict={}
        if args.recordType != 'dataset':
            search_dict["datasetId"]=json_record["datasetId"]
        search_dict["id"]=json_record["id"]
        update_dict["$set"]=json_record
        initial_record=db[args.collection].find(search_dict)
        db[args.collection].update_many(search_dict, update_dict)
        updated_record=db[args.collection].find(search_dict)
        try:
            validate_record(updated_record[0], args)
            if args.recordType != 'dataset':
                print('record {} for dataset: {} updated successfully'.format(json_record["id"],json_record["datasetId"]))
            else:
                print('record {} for dataset: {} updated successfully'.format(json_record["id"],json_record["id"]))
        except Exception:
            db[args.collection].delete_one(search_dict)
            db[args.collection].insert_one(initial_record[0])
            print('record {} for dataset: {} update failed. The document could not be validated against Beacon v2 standards. Please, compare the documents you are updating to resolve the confllicts.'.format(json_record["variantInternalId"],json_record["datasetId"]))
        
def update_record(args):
    with open(args.file) as json_file:
        json_record = json.load(json_file)
    
    if isinstance(json_record,list):
        for record in json_record:
            convert_record(record, args)
    else:
        convert_record(json_record,args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='UpdateRecordInMongoDB',
                        description='This script updates a record in MongoDB')

    parser.add_argument('-f', '--file', default=os.path.join(conf.output_docs_folder, 'test.json'))
    parser.add_argument('-r', '--recordType', default=conf.record_type)
    parser.add_argument('-c', '--collection', default=conf.collection_name)
    args = parser.parse_args()


    update_record(args)
