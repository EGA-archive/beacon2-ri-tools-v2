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

def commas(prova):
    length_iter=0
    array_of_newdicts=[]
    for key, value in prova.items():
        if isinstance(value, str):
            valuesplitted = value.split('|')
            length_iter=len(valuesplitted)
        elif isinstance(value, dict):
            for kval, vval in value.items():
                if isinstance(vval, str):
                    valsplitted = vval.split('|')
                    length_iter=len(valsplitted)
    if length_iter > 0:
        i=0
        while i < length_iter:
            newdict={}
            for key, value in prova.items():
                if isinstance(value, str):
                    valuesplitted = value.split('|')
                    if valuesplitted[i]!='' or valuesplitted[i]!={}:
                        newdict[key]=valuesplitted[i]
                elif isinstance(value, int):
                    valuesplitted = value.split('|')
                    if valuesplitted[i]!='' or valuesplitted[i]!={}:
                        newdict[key]=valuesplitted[i]
                elif isinstance(value, dict):
                    newdict[key]={}
                    for k, v in value.items():
                        if isinstance(v, str):
                            vsplitted = v.split('|')
                            try:
                                if vsplitted[i]!='' or vsplitted[i]!={}:
                                    newdict[key][k]=float(vsplitted[i])
                            except Exception:
                                #print(vsplitted)
                                #print(i)
                                if vsplitted[i]!='' or vsplitted[i]!={}:
                                    newdict[key][k]=vsplitted[i]
                        elif isinstance(v, int):
                            newdict[key][k]=v
                        elif isinstance(v, dict):
                            newdict[key][k]={}
                            for k1, v1 in v.items():
                                if isinstance(v1, str):
                                    v1splitted = v1.split('|')
                                    try:
                                        if v1splitted[i]!='' or v1splitted[i]!={} and len(v1splitted[i])!=0:
                                            newdict[key][k][k1]=v1splitted[i]
                                    except Exception:
                                        pass

                    if newdict[key][k]=={} or newdict[key][k]=="":
                        del newdict[key]
            array_of_newdicts.append(newdict)
            i+=1
    else:
        array_of_newdicts.append(prova)
    return(array_of_newdicts)

def check_new_item_and_append_it(current_dict, keys, value):
    key = keys[0]
    
    if len(keys) == 1:
        current_dict[key] = value
    else:
        if key not in current_dict:
            current_dict[key] = {}
        check_new_item_and_append_it(current_dict[key], keys[1:], value)

def process_dictionary(item, new_item, subitem_dict, dict_of_properties, num_process):
    for key, value in item.items():
        current_item = new_item + "|" + key
        if isinstance(value, dict):
            if current_item not in subitem_dict:
                subitem_dict, num_process = process_dictionary(value, current_item, subitem_dict, dict_of_properties, num_process)
        elif isinstance(value, list):
            processed_list, num_process = process_list(value, current_item, [], dict_of_properties, num_process)
            if processed_list:
                check_new_item_and_append_it(subitem_dict, current_item.split("|"), processed_list)
        else:
            propv = process_string(current_item, dict_of_properties)
            if propv is not None:
                if '|' in propv:
                    propv=propv.split('|')
                    if num_process == -1:
                        num_process=len(propv)-1
                    propv=propv[num_process]
                check_new_item_and_append_it(subitem_dict, current_item.split("|"), propv)

    return subitem_dict, num_process

def process_list(item, new_item, processed_list, dict_of_properties, num_process):
    for list_item in item:
        if isinstance(list_item, dict):
            sublist_dict, num_process = process_dictionary(list_item, new_item, {}, dict_of_properties, num_process)
            if sublist_dict !={}:
                splitted_list=new_item.split('|')
                if len(splitted_list)>1:
                    processed_list=sublist_dict[new_item.split('|')[0]][new_item.split('|')[1]]
                else:
                    processed_list.append(sublist_dict[new_item.split('|')[0]])
    return processed_list, num_process

def process_string(new_item, dict_of_properties):
    if new_item in dict_of_properties:
        return dict_of_properties[new_item]
    return None

def create_record(dict_properties, dict_of_properties):
    definitivedict = {}

    for key, value in dict_properties.items():
        if isinstance(value, list):
            value_list, num_of_processes = process_list(value, key, [], dict_of_properties, -1)
            if num_of_processes >=0:
                total_list=[]
                while num_of_processes>=0:
                    value_list, remainder = process_list(value, key, [], dict_of_properties, num_of_processes)
                    try:
                        total_list.append(value_list[0])
                    except Exception:
                        total_list = value_list
                    num_of_processes-=1
                if total_list:
                    definitivedict[key] = total_list   
            elif value_list:
                definitivedict[key] = value_list
        elif isinstance(value, dict):
            subitem_dict, num_of_processes = process_dictionary(value, key, {}, dict_of_properties, -1)
            if subitem_dict != {}:
                definitivedict[key] = subitem_dict[key]
        else:
            propv = process_string(key, dict_of_properties)
            if propv is not None:
                definitivedict[key] = propv

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
                        if '|' in valor:
                            dict_of_properties[property_value]=valor
                        else:
                            dict_of_properties[property_value]=valor
                        

                    elif valor == 0:
                        dict_of_properties[property_value]=valor

            #print(dict_properties)
            #print(dict_of_properties)

            definitivedict = create_record(dict_properties, dict_of_properties)
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

