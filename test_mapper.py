import json
from tqdm import tqdm
import conf.conf as conf
import csv
import sys
from validators.individuals import Individuals
import hashlib
import argparse
import os

with open("files/headers/individuals.txt", "r") as txt_file:
    list_of_headers=txt_file.read().splitlines() 
with open('files/deref_schemas/individuals.json') as json_file:
    dict_properties = json.load(json_file)

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def create_dict(dict_properties):
    definitivedict={}
    print(dict_properties)
    for key, value in dict_properties.items():
        
        if '|' in value:
            pass
        else:
            props_splitted = key.split('|')
        populate_dict=definitivedict
        for index, item in enumerate(props_splitted):
            print(props_splitted)
            if item not in populate_dict:
                if index == 6:
                    definitivedict[props_splitted[index-6]][props_splitted[index-5]][props_splitted[index-4]][props_splitted[index-3]][props_splitted[index-2]][props_splitted[index-1]][props_splitted[index]]=value
                elif index == 5:
                    definitivedict[props_splitted[index-5]][props_splitted[index-4]][props_splitted[index-3]][props_splitted[index-2]][props_splitted[index-1]][props_splitted[index]]=value
                elif index == 4:
                    definitivedict[props_splitted[index-4]][props_splitted[index-2]][props_splitted[index-1]][props_splitted[index]]=value
                elif index == 3:
                    definitivedict[props_splitted[index-3]][props_splitted[index-2]][props_splitted[index-1]][props_splitted[index]]=value
                elif index == 2:
                    definitivedict[props_splitted[index-2]][props_splitted[index-1]][props_splitted[index]]=value
                elif index == 1:
                    definitivedict[props_splitted[index-1]][props_splitted[index]]=value
                else:
                    new_dict=current = {}
                    for element in props_splitted[:-1]:
                        current[element] = {}
                        current = current[element]

                    current[props_splitted[-1]] = value
                    definitivedict[item]=new_dict[item]
                break
            else:
                populate_dict=populate_dict[item]


        print(definitivedict)

    print(definitivedict)
    return definitivedict

def generate(dict_properties, list_of_headers, args):
    #filename = conf.filename
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
        for line in reader:
            dict_of_properties={}
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                property_value=property_value.replace('\ufeff', '')
                if property_value not in list_of_headers:
                    raise Exception(('the header {} is not allowed. Please, take a look at csv templates to check the headers allowed.').format(property_value))


                
                valor = vline

                if i > 0:
                    
                    if valor != '':


                        list_of_filled_items.append(property_value)

                    if valor:
                        dict_of_properties[property_value]=valor
                        

                    elif valor == 0:
                        dict_of_properties[property_value]=valor

            #print(dict_properties)
            #print(dict_of_properties)


            definitivedict={}


            definitivedict=create_dict(dict_of_properties)

            

            print(definitivedict)
            Individuals(**definitivedict)
            definitivedict["datasetId"]=args.datasetId
            definitivedict["_id"]=get_hash(args.datasetId+definitivedict["id"])
            total_dict.append(definitivedict)

            
            pbar.update(1)
            if i > num_rows:
                break
            i+=1

            

    pbar.close()
    return total_dict, i


parser = argparse.ArgumentParser(
                    prog='individualsCSVtOBFF',
                    description='This script translates a individuals csv to BFF')
parser.add_argument('-o', '--output', default=conf.output_docs_folder)
parser.add_argument('-d', '--datasetId', default=conf.datasetId)
parser.add_argument('-i', '--input', default=conf.csv_folder)

args = parser.parse_args()


    
dict_generado, total_i=generate(dict_properties, list_of_headers, args)


output = os.path.join(args.output, 'individuals.json')

if total_i-1 > 0:

    print('Successfully converted {} registries into {}'.format(total_i-1, output))

else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)