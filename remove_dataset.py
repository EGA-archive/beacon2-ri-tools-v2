from conf import conf
import argparse
from mongo_connection import build_mongo_database

db = build_mongo_database()

def remove_dataset(args):
    db.analyses.delete_many({"datasetId": args.datasetId})
    print('analyses for dataset: {} removed successfully'.format(args.datasetId))
    db.biosamples.delete_many({"datasetId": args.datasetId})
    print('biosamples for dataset: {} removed successfully'.format(args.datasetId))
    db.caseLevelData.delete_many({"datasetId": args.datasetId})
    print('caseLevelData for dataset: {} removed successfully'.format(args.datasetId))
    db.cohorts.delete_many({"datasetId": args.datasetId})
    print('cohorts for dataset: {} removed successfully'.format(args.datasetId))
    db.datasets.delete_many({"id": args.datasetId})
    print('datasets for dataset: {} removed successfully'.format(args.datasetId))
    db.genomicVariations.delete_many({"datasetId": args.datasetId})
    print('genomicVariations for dataset: {} removed successfully'.format(args.datasetId))
    db.individuals.delete_many({"datasetId": args.datasetId})
    print('individuals for dataset: {} removed successfully'.format(args.datasetId))
    db.runs.delete_many({"datasetId": args.datasetId})
    print('runs for dataset: {} removed successfully'.format(args.datasetId))
    db.targets.delete_many({"datasetId": args.datasetId})
    print('dataset: {} removed successfully'.format(args.datasetId))

parser = argparse.ArgumentParser(
                    prog='removeDatasetfromMongoDB',
                    description='This script removes all the records belonging to a dataset in MongoDB')

parser.add_argument('-d', '--datasetId', default=conf.datasetId)

args = parser.parse_args()

if __name__ == '__main__':
    remove_dataset(args)
