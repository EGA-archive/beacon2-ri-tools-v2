from pymongo.mongo_client import MongoClient
from conf import conf

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

client.beacon.analyses.delete_many({"datasetId": conf.datasetId})
print('analyses for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.biosamples.delete_many({"datasetId": conf.datasetId})
print('biosamples for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.caseLevelData.delete_many({"datasetId": conf.datasetId})
print('caseLevelData for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.cohorts.delete_many({"datasetId": conf.datasetId})
print('cohorts for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.datasets.delete_many({"datasetId": conf.datasetId})
print('datasets for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.genomicVariations.delete_many({"datasetId": conf.datasetId})
print('genomicVariations for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.individuals.delete_many({"datasetId": conf.datasetId})
print('individuals for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.runs.delete_many({"datasetId": conf.datasetId})
print('runs for dataset: {} removed successfully'.format(conf.datasetId))
client.beacon.targets.delete_many({"datasetId": conf.datasetId})
print('dataset: {} removed successfully'.format(conf.datasetId))