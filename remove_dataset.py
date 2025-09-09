from pymongo.mongo_client import MongoClient
from conf import conf
import argparse

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

parser = argparse.ArgumentParser(
                    prog='removeDatasetfromMongoDB',
                    description='This script removes all the records belonging to a dataset in MongoDB')

parser.add_argument('-d', '--datasetId', default=conf.datasetId)

args = parser.parse_args()

client.beacon.analyses.delete_many({"datasetId": args.datasetId})
print('analyses for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.biosamples.delete_many({"datasetId": args.datasetId})
print('biosamples for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.caseLevelData.delete_many({"datasetId": args.datasetId})
print('caseLevelData for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.cohorts.delete_many({"datasetId": args.datasetId})
print('cohorts for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.datasets.delete_many({"id": args.datasetId})
print('datasets for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.genomicVariations.delete_many({"datasetId": args.datasetId})
print('genomicVariations for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.individuals.delete_many({"datasetId": args.datasetId})
print('individuals for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.runs.delete_many({"datasetId": args.datasetId})
print('runs for dataset: {} removed successfully'.format(args.datasetId))
client.beacon.targets.delete_many({"datasetId": args.datasetId})
print('dataset: {} removed successfully'.format(args.datasetId))