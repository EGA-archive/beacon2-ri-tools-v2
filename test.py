from cyvcf2 import VCF
import json
from tqdm import tqdm
import glob
import re
import conf.conf as conf
import json
import gc
import gzip
from pymongo.mongo_client import MongoClient
from validators.genomicVariations import GenomicVariations, LegacyVariation, SequenceLocation, SequenceInterval, Number
from pymongo.errors import BulkWriteError
import hashlib
import argparse
import os
from typing import Any, Dict

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
class Item(GenomicVariations):
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop('exclude_none')
        return super().dict(*args, exclude_none=True, **kwargs)

start = Number(type="Number", value=16050074)
end = Number(type="Number", value=16050075)
interval = SequenceInterval(type="SequenceInterval", start=start, end=end)
location = SequenceLocation(type="SequenceLocation", interval=interval, sequence_id="HGVSid:22:g.16050074A>G")
variation = LegacyVariation(alternateBases="G", referenceBases="A", variantType="SNP", location=location)
g_variant = Item(variantInternalId='a', variation=variation)
print(g_variant)
print(g_variant.model_dump(exclude_none=True))