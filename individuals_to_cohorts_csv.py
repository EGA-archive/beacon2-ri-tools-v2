import json
from tqdm import tqdm
import conf.conf as conf
import csv
from validators.cohorts import Cohorts
import hashlib
import argparse
import os

with open("files/headers/individuals.txt", "r") as txt_file:
    list_of_headers=txt_file.read().splitlines() 

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def generate(list_of_headers, args):

    if args.input.endswith('.csv'):
        filename = args.input
    else:
        filename = os.path.join(args.input, 'individuals.csv')
    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        num_rows = sum(1 for row in reader)
    
    total_dict =[]

    k=0
    pbar = tqdm(total = num_rows)
    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        i=1
        definitivedict={}
        definitivedict["id"]=args.cohortId
        definitivedict["name"]=args.cohortName
        definitivedict["cohortType"]=args.cohortType
        definitivedict["collectionEvents"]=[]
        event={}
        event["eventSize"]=num_rows
        for line in reader:
            
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                property_value=property_value.replace('\ufeff', '')
                if property_value not in list_of_headers:
                    raise Exception(('the header {} is not allowed. Please, take a look at csv templates to check the headers allowed.').format(property_value))


                if '|' in vline:
                    valors = vline.split('|')
                else:
                    valors = [vline]

                if i > 0:
                    
                    if vline != '':


                        list_of_filled_items.append(property_value)

                    if valors and vline != '':
                        if 'age' in kline.lower():
                            print(valors)
                            try:
                                event["eventAgeRange"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventAgeRange"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventAgeRange"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventAgeRange"]={}
                                event["eventAgeRange"]["availability"]=True
                                event["eventAgeRange"]["availabilityCount"]=1
                                event["eventAgeRange"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventAgeRange"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventAgeRange"]["distribution"][str(valor)]=1
                        elif kline == 'diseases|diseaseCode|id':
                            try:
                                event["eventDiseases"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventDiseases"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventDiseases"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventDiseases"]={}
                                event["eventDiseases"]["availability"]=True
                                event["eventDiseases"]["availabilityCount"]=1
                                event["eventDiseases"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventDiseases"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventDiseases"]["distribution"][str(valor)]=1
                        elif kline == 'ethnicity|id':
                            try:
                                event["eventEthnicities"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventEthnicities"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventEthnicities"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventEthnicities"]={}
                                event["eventEthnicities"]["availability"]=True
                                event["eventEthnicities"]["availabilityCount"]=1
                                event["eventEthnicities"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventEthnicities"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventEthnicities"]["distribution"][str(valor)]=1
                        elif kline == 'sex|id':
                            try:
                                event["eventGenders"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventGenders"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventGenders"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventGenders"]={}
                                event["eventGenders"]["availability"]=True
                                event["eventGenders"]["availabilityCount"]=1
                                event["eventGenders"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventGenders"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventGenders"]["distribution"][str(valor)]=1
                        elif kline == 'geographicOrigin|id':
                            try:
                                event["eventLocations"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventLocations"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventLocations"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventLocations"]={}
                                event["eventLocations"]["availability"]=True
                                event["eventLocations"]["availabilityCount"]=1
                                event["eventLocations"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventLocations"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventLocations"]["distribution"][str(valor)]=1
                        elif kline == 'phenotypicFeatures|featureType|id':
                            try:
                                event["eventPhenotypes"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventPhenotypes"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventPhenotypes"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventPhenotypes"]={}
                                event["eventPhenotypes"]["availability"]=True
                                event["eventPhenotypes"]["availabilityCount"]=1
                                event["eventPhenotypes"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventPhenotypes"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventPhenotypes"]["distribution"][str(valor)]=1
            
            pbar.update(1)
            if i > num_rows:
                break
            i+=1
    definitivedict["collectionEvents"].append(event)
    Cohorts(**definitivedict)
    definitivedict["datasetId"]=args.datasetId
    definitivedict["_id"]=get_hash(args.datasetId+definitivedict["id"])
    total_dict.append(definitivedict)
    pbar.close()
    return total_dict, i


parser = argparse.ArgumentParser(
                    prog='IndividualsToCohorts',
                    description='This script translates a csv of individuals to a beaconized json of cohorts')

parser.add_argument('-i', '--input', default=conf.csv_folder)
parser.add_argument('-o', '--output', default=conf.output_docs_folder)
parser.add_argument('-d', '--datasetId', default=conf.datasetId)
parser.add_argument('-c', '--cohortId', default='cohortId')
parser.add_argument('-n', '--cohortName', default='cohortName')
parser.add_argument('-t', '--cohortType', default='user-defined')
args = parser.parse_args()

dict_generado, total_i=generate(list_of_headers, args)

output = os.path.join(args.output, 'cohorts.json')

if total_i-1 > 0:

    print('Successfully transformed {} individual registries into a cohort file in {}'.format(total_i-1, output))

else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)

