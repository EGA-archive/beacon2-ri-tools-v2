

import csv
import os
import json
from conf.conf import output_docs_folder, csv_folder, datasetId, entry_type
import argparse
from tqdm import tqdm
import hashlib
from importlib import import_module
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def csv_to_bff(args):
    if args.input.endswith('.csv'):
        filename = args.input
    else:
        filename = os.path.join(args.input, args.entry_type+'.csv')

    name = Path(filename).stem

    module = import_module(f"validators.{name}")

    class_name = name.capitalize()
    ValidatorClass = getattr(module, class_name)
    total_dict=[]
    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        num_rows = sum(1 for row in reader)

    pbar = tqdm(total = num_rows)

    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        k=1
        for line in reader:
            dict_of_properties={}
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                if property_value == None:
                    continue
                property_value=property_value.replace('\ufeff', '')


                
                valor = vline


                if k > 0:
                    
                    if valor != '':


                        list_of_filled_items.append(property_value)

                    if valor:
                        if '|' in valor:
                            dict_of_properties[property_value]=valor
                        else:
                            dict_of_properties[property_value]=valor
                        

                    elif valor == 0:
                        dict_of_properties[property_value]=valor
            ValidatorClass.CONFIG=dict_of_properties
            ValidatorClass.ENTRY_TYPE=args.entry_type
            obtained_class = ValidatorClass()
            definitivedict = obtained_class.model_dump(mode="json",exclude_none=True)
            if args.entry_type != 'datasets':
                definitivedict["datasetId"]=args.datasetId
            if args.entry_type == 'genomicVariations':
                definitivedict["_id"]=get_hash(args.datasetId+definitivedict["variantInternalId"])
            elif args.entry_type == 'patients':
                definitivedict["_id"]=get_hash(args.datasetId+definitivedict["patientId"])
            else:
                definitivedict["_id"]=get_hash(args.datasetId+definitivedict["id"])
            total_dict.append(definitivedict)
            pbar.update(1)
            if k > num_rows:
                break
            k+=1
            #print(dict_properties)
            #print(dict_of_properties)

    return total_dict, k


parser = argparse.ArgumentParser(
                    prog='convert_csv_to_bff',
                    description='This script translates a csv to BFF')
parser.add_argument('-o', '--output', default=output_docs_folder)
parser.add_argument('-d', '--datasetId', default=datasetId)
parser.add_argument('-i', '--input', default=csv_folder)
parser.add_argument('-e', '--entry_type', default=entry_type, choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all', 'collections', 'imageStudies', 'patients'])

args = parser.parse_args()

if __name__ == '__main__':
    choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs']
    if args.entry_type == 'all':
        for entrytype in choices:
            args.entry_type = entrytype

            try:
                dict_generado, total_i=csv_to_bff(args)
            except FileNotFoundError:
                continue

            output = os.path.join(args.output, args.entry_type+'.json')

            if total_i-1 > 0:

                print('Successfully converted {} registries into {}'.format(total_i-1, output))

            else:
                print('No registries found.')

            with open(output, 'w') as f:
                json.dump(dict_generado, f)
    else:
        path = args.entry_type
        if args.entry_type not in choices:
            path = 'EUCAIM/' + args.entry_type


        dict_generado, total_i=csv_to_bff(args)

        output = os.path.join(args.output, args.entry_type+'.json')

        if total_i-1 > 0:

            print('Successfully converted {} registries into {}'.format(total_i-1, output))

        else:
            print('No registries found.')

        with open(output, 'w') as f:
            json.dump(dict_generado, f)