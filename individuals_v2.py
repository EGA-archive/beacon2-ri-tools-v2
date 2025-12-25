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

def check_new_item_and_append_it(current_dict, keys, value):
    # If the dictionary is a nested dictionary, continue creating the subdictionaries until we reach the end, then we store the value.
    key = keys[0]
    if len(keys) == 1:
        if isinstance(value, str):
            if value.lower() == 'true' or value.lower() == 'false':
                value = bool(value)
        current_dict[key] = value
    else:
        if key not in current_dict:
            current_dict[key] = {}
        check_new_item_and_append_it(current_dict[key], keys[1:], value)

def process_dictionary(item, new_item, subitem_dict, dict_of_properties, num_process, list_of_provs):
    for key, value in item.items():
        current_item = new_item + "|" + key
        # If we find that the item is a dictionary inside a dictionary, call the method again.
        if isinstance(value, dict):
            if current_item not in subitem_dict:
                subitem_dict, num_process = process_dictionary(value, current_item, subitem_dict, dict_of_properties, num_process, list_of_provs)
        # If we find it is an inner list, process it as a list.
        elif isinstance(value, list):
            # If the list has values with pipes |, process it iterating each value of the value with pipes.
            if num_process >=0:
                # Let's store the num_process for later iterations of the inner list, so we process all the possible pipe splitted values.
                list_of_processes=[]
                list_of_processes.append(str(num_process))
                # Start the array to check that the num_process didn't kick in for an inner key of an inner parent key so we keep the num_process alive.
                processed_list=[]
                # If there is the need of still process a splitted pipe value, execute the list processing.
                while num_process >=0:
                    sublist, num_process, list_of_provs = process_list(value, current_item, [], dict_of_properties, num_process, list_of_provs)
                    # If the returned value is an empty list, it means that there are no splitted values, so no need to continue processing this inner key.
                    if sublist == []:
                        num_process = -1
                    # If the returned value is a dictionary, process the value as a simple list and break the iteration, as it means this inner key is not meant to have the processing.
                    elif isinstance(sublist, dict):
                        processed_list, num_process, list_of_provs = process_list(value, current_item, [], dict_of_properties, num_process, list_of_provs)
                        list_of_provs.append('continue')
                        break
                    # Else, continue iterating the value with pipes until they are all processed. Then, we store the parent key in list_of_provs so the parent function knows this has already been processed.
                    else:
                        processed_list.append(sublist[0])
                        num_process-=1
                        if num_process == -1:
                            list_of_provs.append(item)
                # Keep the num process alive for later inner keys that do need to process pipe splitted values..
                if processed_list == []:
                    num_process = int(list_of_processes[0])
            else:
                processed_list, num_process, list_of_provs = process_list(value, current_item, [], dict_of_properties, num_process, list_of_provs)
            if processed_list:
                check_new_item_and_append_it(subitem_dict, current_item.split("|"), processed_list)
        else:
            # If the value is a string, process it and append it, unless it is a piped | value, where we start the wheel of multiple processing of the values that belong to a list, letting the parent function now by stargint the num_process variable as the number of times (values) needing to be processed.
            propv = process_string(current_item, dict_of_properties)
            if propv is not None:
                if '|' in propv:
                    propv=propv.split('|')
                    if num_process == -1:
                        num_process=len(propv)-1
                    propv=propv[num_process]
                check_new_item_and_append_it(subitem_dict, current_item.split("|"), propv)

    return subitem_dict, num_process

def process_list(item, new_item, processed_list, dict_of_properties, num_process, list_of_provs):
    # As we can only have dictionaries inside lists in Beacon v2, we process each item with the function to process dictionaries.
    for list_item in item:
        if isinstance(list_item, dict):
            sublist_dict, num_process = process_dictionary(list_item, new_item, {}, dict_of_properties, num_process, list_of_provs)
            if sublist_dict !={}:
                splitted_list=new_item.split('|')
                # In case the returning object is a list that is not meant to be a list (e.g. measurementValue and not modifiers or members), we process it as a dictionary.
                # TODO: Try a non hardcoded alternative.
                if len(splitted_list)>1 and 'modifiers' not in new_item and 'members' not in new_item:
                    processed_list=sublist_dict[new_item.split('|')[0]][new_item.split('|')[1]]
                elif 'modifiers' in new_item or 'members' in new_item:
                    processed_list.append(sublist_dict[new_item.split('|')[0]][new_item.split('|')[1]])
                else:
                    processed_list.append(sublist_dict[new_item.split('|')[0]])
    return processed_list, num_process, list_of_provs

def process_string(new_item, dict_of_properties):
    if new_item in dict_of_properties:
        return dict_of_properties[new_item]
    return None

def create_record(dict_properties, dict_of_properties):
    # Create dictionary for each record
    definitivedict = {}
    for key, value in dict_properties.items():
        # Start a list where we will assign which parent keys have already processed the value that contains a pipe |
        list_of_provs=[]
        if isinstance(value, list):
            # Get the list for the key, the number of times this list has to be processed in case there is a pipe | and if the pipe has been processed in an inner list with list_of_provs.
            value_list, num_of_processes, list_of_provs = process_list(value, key, [], dict_of_properties, -1, list_of_provs)
            # If the instance is a list, where the pipe values can happen, let's check if it's the case for the parent key
            if num_of_processes >=0:
                total_list=[]
                # If the num_of_proceesses is equal or greater than 0 and the parent key has not already been processed (appears inside list_of_provs), continue processing the items of the list.
                while num_of_processes>=0 and key not in list_of_provs:
                    # As the generic num_of_processes is different for each iteration of the list item, we call the subprocesses that come from inner lists as remainder, to not conflict with the greater num processes.
                    value_list, remainder, list_of_provs = process_list(value, key, [], dict_of_properties, num_of_processes, list_of_provs)
                    try:
                        total_list.append(value_list[0])
                    except Exception:
                        total_list = value_list
                    if 'continue' not in list_of_provs:
                        list_of_provs.append(key)
                    num_of_processes-=1
                # Assign the processed the list to the parent key
                if total_list:
                    definitivedict[key] = total_list
            # Assign the simple list to the parent key
            elif value_list:
                definitivedict[key] = value_list
        elif isinstance(value, dict):
            # If the value is a dictionary, process it
            subitem_dict, num_of_processes = process_dictionary(value, key, {}, dict_of_properties, -1, list_of_provs)
            if subitem_dict != {}:
                definitivedict[key] = subitem_dict[key]
        else:
            # If the value is just a string, process it and append it
            # TODO: Some values like for measurementValue are still strings, need to convert them to integers or float and check why validator is not kicking in.
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
                if property_value == None:
                    continue
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

