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

def check(name, list_of_filled_items):
    measures_list_1 = ['measures|measurementValue|referenceRange|high', 'measures|measurementValue|referenceRange|low', 'measures|measurementValue|referenceRange|unit|id', 'measures|measurementValue|referenceRange|unit|label']
    measures_list_2 = ['measures|measurementValue|unit|id', 'measures|measurementValue|unit|label', 'measures|measurementValue|value']
    measures_list_3 = ['measures|measurementValue|typedQuantities|quantity|referenceRange|high', 'measures|measurementValue|typedQuantities|quantity|referenceRange|low', 'measures|measurementValue|typedQuantities|quantity|referenceRange|unit', 'measures|measurementValue|typedQuantities|quantity|unit|id', 'measures|measurementValue|typedQuantities|quantity|unit|label', 'measures|measurementValue|typedQuantities|quantity|value']
    observation_list_1 = ['measures|observationMoment']
    observation_list_2 = ['measures|observationMoment|days', 'measures|observationMoment|weeks']
    observation_list_3 = ['measures|observationMoment|end', 'measures|observationMoment|start']
    observation_list_4 = ['measures|observationMoment|end|iso8601duration', 'measures|observationMoment|start|iso8601duration']
    observation_list_5 = ['measures|observationMoment|iso8601duration']
    observation_list_6 = ['measures|observationMoment|id', 'measures|observationMoment|label']
    ageOfOnset_list_1 = ['diseases|ageOfOnset']
    ageOfOnset_list_2 = ['diseases|ageOfOnset|days', 'diseases|ageOfOnset|weeks']
    ageOfOnset_list_3 = ['diseases|ageOfOnset|end', 'diseases|ageOfOnset|start']
    ageOfOnset_list_4 = ['diseases|ageOfOnset|end|iso8601duration', 'diseases|ageOfOnset|start|iso8601duration']
    ageOfOnset_list_5 = ['diseases|ageOfOnset|iso8601duration']
    ageOfOnset_list_6 = ['diseases|ageOfOnset|id', 'diseases|ageOfOnset|label']
    onset_list_1 = ['phenotypicFeatures|onset']
    onset_list_2 = ['phenotypicFeatures|onset|days', 'phenotypicFeatures|onset|weeks']
    onset_list_3 = ['phenotypicFeatures|onset|end', 'phenotypicFeatures|onset|start']
    onset_list_4 = ['phenotypicFeatures|onset|end|iso8601duration', 'phenotypicFeatures|onset|start|iso8601duration']
    onset_list_5 = ['phenotypicFeatures|onset|iso8601duration']
    onset_list_6 = ['phenotypicFeatures|onset|id', 'phenotypicFeatures|onset|label']
    measure_check=0

    list_of_checks=[]
    i=0
    if name == 'measures':
        for measure in list_of_filled_items:
            if 'measurementValue' in measure:
                if measure in measures_list_1:
                    measure_check+=1
                    measures_list_1=[]
                elif measure in measures_list_2:
                    measure_check+=1
                    measures_list_2=[]
                elif measure in measures_list_3:
                    measure_check+=1
                    measures_list_3=[]
        if measure_check > 1:
            raise Exception(('please, choose only one {} format').format('measurementValue'))
    elif name == 'observations':
        for measure in list_of_filled_items:
            if 'observationMoment' in measure:
                if measure in observation_list_1:
                    measure_check+=1
                    observation_list_1=[]
                elif measure in observation_list_2:
                    measure_check+=1
                    observation_list_2=[]
                elif measure in observation_list_3:
                    measure_check+=1
                    observation_list_3=[]
                elif measure in observation_list_4:
                    measure_check+=1
                    observation_list_4=[]
                elif measure in observation_list_5:
                    measure_check+=1
                    observation_list_5=[]
                elif measure in observation_list_6:
                    measure_check+=1
                    observation_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('observationMoment'))
    elif name == 'procedures':
        for measure in list_of_filled_items:
            if 'ageAtProcedure' in measure:
                if measure in ageAtProcedure_list_1:
                    measure_check+=1
                    ageAtProcedure_list_1=[]
                elif measure in ageAtProcedure_list_2:
                    measure_check+=1
                    ageAtProcedure_list_2=[]
                elif measure in ageAtProcedure_list_3:
                    measure_check+=1
                    ageAtProcedure_list_3=[]
                elif measure in ageAtProcedure_list_4:
                    measure_check+=1
                    ageAtProcedure_list_4=[]
                elif measure in ageAtProcedure_list_5:
                    measure_check+=1
                    ageAtProcedure_list_5=[]
                elif measure in ageAtProcedure_list_6:
                    measure_check+=1
                    ageAtProcedure_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('ageAtProcedure'))
    elif name == 'diseases':
        for measure in list_of_filled_items:
            if 'ageOfOnset' in measure:
                if measure in ageOfOnset_list_1:
                    measure_check+=1
                    ageOfOnset_list_1=[]
                elif measure in ageOfOnset_list_2:
                    measure_check+=1
                    ageOfOnset_list_2=[]
                elif measure in ageOfOnset_list_3:
                    measure_check+=1
                    ageOfOnset_list_3=[]
                elif measure in ageOfOnset_list_4:
                    measure_check+=1
                    ageOfOnset_list_4=[]
                elif measure in ageOfOnset_list_5:
                    measure_check+=1
                    ageOfOnset_list_5=[]
                elif measure in ageOfOnset_list_6:
                    measure_check+=1
                    ageOfOnset_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('ageOfOnset'))
    elif name == 'phenotypic':
        for measure in list_of_filled_items:
            if 'onset' in measure:
                if measure in onset_list_1:
                    measure_check+=1
                    onset_list_1=[]
                elif measure in onset_list_2:
                    measure_check+=1
                    onset_list_2=[]
                elif measure in onset_list_3:
                    measure_check+=1
                    onset_list_3=[]
                elif measure in onset_list_4:
                    measure_check+=1
                    onset_list_4=[]
                elif measure in onset_list_5:
                    measure_check+=1
                    onset_list_5=[]
                elif measure in onset_list_6:
                    measure_check+=1
                    onset_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('onset'))

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
            for key, value in dict_properties.items():
                if isinstance(value, list):
                    definitivedict[key]=[]
                    value_list=[]
                    for item in value:
                        if isinstance(item, dict):
                            item_dict={}
                            for ki, vi in item.items():
                                
                                if isinstance(vi, list):
                                    vi_list=[]
                                    for subitem in vi:
                                        if isinstance(subitem, dict):

                                            subitem_dict={}
                                            for k, v in subitem.items():
                                                if isinstance(v, dict):
                                                    subitem_dict[k]={}
                                                    for k1, v1 in v.items():
                                                        if isinstance(v1, dict):
                                                            subitem_dict[k][k1]={}
                                                            for k2, v2 in v1.items():
                                                                if isinstance(v2, dict): 
                                                                    subitem_dict[k][k1][k2]={}
                                                                    for k3, v3 in v2.items():
                                                                        new_item = ""
                                                                        new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2 + "|" + k3
                                                                        for propk, propv in dict_of_properties.items():
                                                                            if propk == new_item:
                                                                                subitem_dict[k][k1][k2][k3]=propv
                                                                    if subitem_dict[k][k1][k2]=={}:
                                                                        del subitem_dict[k][k1][k2]
                                                                else:
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            #print(propk)
                                                                            #print(propv)
                                                                            subitem_dict[k][k1][k2]=propv   
                                                            if subitem_dict[k][k1]=={}:
                                                                del subitem_dict[k][k1]
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + k1
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:

                                                                    #print(propk)
                                                                    subitem_dict[k][k1]=propv 
                                                    if subitem_dict[k]=={}:
                                                        del subitem_dict[k]
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            #print(propk)
                                                            subitem_dict[k]=propv

                                                if subitem_dict != {}:
                                                    if subitem_dict not in vi_list:
                                                        vi_list.append(subitem_dict)
                                                        if ki == 'modifiers':
                                                            item_dict[ki]=vi_list
                                                        elif ki == 'measurementValue' and len(vi_list)>2:
                                                            #print(vi_list)
                                                            dict_1=vi_list[0]
                                                            dict_2=vi_list[1]
                                                            dict_1['unit']=dict_2['unit']
                                                            dict_1['value']=dict_2['value']

                                                            item_dict[ki]=[dict_1]
                                                            #print(item_dict)
                                                        elif ki == 'measurementValue':
                                                            #print(vi_list)
                                                            item_dict[ki]=vi_list[0]
                                                        else:
                                                            item_dict[ki]=vi_list[0]
                    
                                elif isinstance(vi, dict):
                                    
                                    vi_dict={}
                                    for ki1, vi1 in vi.items():
                                        if isinstance(vi1, dict):
                                            
                                            members={}
                                            for ki2, vi2 in vi1.items():
                                                if isinstance(vi2, dict):
                                                    for ki3, vi3 in vi2.items():
                                                        new_item = ""
                                                        new_item = key + "|" + ki + "|" + ki1 + "|" + ki2 + "|" + ki3
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                #print(propk)
                                                                try:
                                                                    vi_dict[ki1][ki2][ki3]=propv
                                                                except Exception:
                                                                    try:
                                                                        vi_dict[ki1][ki2]={}
                                                                        vi_dict[ki1][ki2][ki3]=propv
                                                                    except Exception:
                                                                        vi_dict[ki1]={}
                                                                        vi_dict[ki1][ki2]={}
                                                                        vi_dict[ki1][ki2][ki3]=propv
                                                    if vi_dict != {}:
                                                        #procedure: print(ki)
                                                        item_dict[ki]=vi_dict
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            #print(propk)
                                                            try:
                                                                vi_dict[ki1][ki2]=propv
                                                            except Exception:
                                                                vi_dict[ki1]={}
                                                                vi_dict[ki1][ki2]=propv

                                                    #if vi_dict != {} and vi_dict[ki1] != {}:
                                                    if vi_dict != {}:
                                                        #procedure: print(ki)
                                                        item_dict[ki]=vi_dict
                                        elif isinstance(vi1, list):
                                            for vi1item in vi1:
                                                if isinstance(vi1item, dict):
                                                    vi1item_dict={}
                                                    for key1item, value1item in vi1item.items():
                                                        if isinstance(value1item, dict):
                                                            for key2item, value2item in value1item.items():
                                                                new_item = ""
                                                                new_item = key + "|" + ki + "|" + ki1 + "|" + key1item + "|" + key2item
                                                                for propk, propv in dict_of_properties.items():
                                                                    if propk == new_item:
                                                                        vi1item_dict[key1item]={}
                                                                        vi1item_dict[key1item][key2item]=propv
                                                                        vi_dict[ki1]=vi1item_dict
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + ki1 + "|" + key1item
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:
                                                                    vi1item_dict[key1item]=propv
                                                                    vi_dict[ki1]=vi1item_dict
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    #print(propk)
                                                    # dateOfprocedure print(propk)
                                                    if propv == 'true' or propv.lower() == 'true':
                                                        propv = bool(propv)
                                                    elif propv == 'false' or propv.lower()== 'false':
                                                        propv = bool("")
                                                    try:
                                                        vi_dict[ki1]=propv 
                                                    except Exception:
                                                        vi_dict[ki1]={}
                                                        vi_dict[ki1]=propv
                                                    item_dict[ki]=vi_dict
            
                                else:
                                    new_item = ""
                                    new_item = key + "|" + ki
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            if propv == 'TRUE' or propv == 'true' or propv == 'FALSE' or propv == 'false':
                                                propv = bool(propv)
                                            item_dict[ki]=propv
                                #print(item_dict)
                                if item_dict != {} and item_dict != [{}]:
                                    if item_dict not in value_list:
                                        value_list.append(item_dict)
                                        #print(value_list)

                            if value_list != []:
                                list_to_def=[]
                                #print(value_list)
                                
                                if key == 'pedigrees':
                                    for itemvl in value_list:
                                        list_to_def.append(itemvl)
                                        
                                        for itemldf in list_to_def:
                                            if itemldf not in definitivedict[key]:
                                                if key == 'pedigrees':
                                                    memberlist=[]
                                                    
                                                    for k, v in itemldf.items():
                                                        if k == 'members':
                                                            
                                                            for kmem, vmem in v.items():
                                                                if kmem == 'role':
                                                                    for kmem1,vmem1 in vmem.items():
                                                                        if kmem1 == 'id':
                                                                            roleid=vmem1.split('|')
                                                                        else:
                                                                            rolelabel=vmem1.split('|')
                                                                elif kmem == 'affected':
                                                                    #print(propk)
                                                                    #print(propv)
                                                                    try:
                                                                        affected=vmem.split('|')
                                                                    except Exception:
                                                                        affected=['True']
                                                                elif kmem == 'memberId':
                                                                    memberId = vmem.split('|')
                                                            
                                                            pnum=0
                                                            while pnum < len(memberId):
                                                                memberitems={}
                                                                memberitems['affected']=bool(affected[pnum])
                                                                memberitems['memberId']=memberId[pnum]
                                                                memberitems['role']={}
                                                                memberitems['role']['id']=roleid[pnum]
                                                                memberitems['role']['label']=rolelabel[pnum]
                                                                memberlist.append(memberitems)
                                                                pnum+=1



                                                            itemvl['members']=memberlist
                                        definitivedict[key].append(itemvl)
                                elif key == 'measures':
                                    #print(value_list)
                                    commetize=False
                                    for key0, value0 in value_list[0].items():
                                        if '|' in value0:
                                            commetize=True
                                    if commetize==True:
                                        defig=commas(value_list[0])
                                        definitivedict[key]=defig
                                    else:
                                        definitivedict[key]=value_list
                                else:
                                    definitivedict[key]=value_list

                            else:
                                for itemvl in value_list:
                                    definitivedict[key].append(itemvl)     
                    if definitivedict[key]==[]:
                        del definitivedict[key]
                elif isinstance(value, dict):
                    value_dict={}
                    for kd, vd in value.items():
                        if isinstance(vd, list):
                            vd_list=[]
                            if isinstance(vd[0], dict):
                                for kd1, vd1 in vd[0].items():
                                    if isinstance(vd1, dict):
                                        for kd2, vd2 in vd1.items():
                                            new_item = ""
                                            new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    value_dict[kd]={}
                                                    value_dict[kd][kd1]={}
                                                    value_dict[kd][kd1][kd2]=propv
                                    else:
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                #print(propv)
                                                if '|' in propv:
                                                    propv_splitted = propv.split('|')
                                                    for itemsplitted in propv:
                                                        value_dict[kd]={}
                                                        value_dict[kd][kd1]=propv_splitted
                                                        if value_dict not in vd_list:
                                                            vd_list.append(value_dict)
                                                else:
                                                    value_dict[kd]={}
                                                    value_dict[kd][kd1]=propv
                                    
                                    if value_dict != {}:
                                        if value_dict not in vd_list:
                                            vd_list.append(value_dict)
                                if vd_list != []:
                                    definitivedict[key]=vd_list
                            else:
                                new_item = ""
                                new_item = key + "|" + kd
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        value_dict[kd]=propv
                                        definitivedict[key]=value_dict
                        else:
                            new_item = ""
                            new_item = key + "|" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    #print(propk)
                                    value_dict[kd]=propv
                                    definitivedict[key]=value_dict
                    if value == {}:
                        new_item = ""
                        new_item = key
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                try:
                                    propvalue={}
                                    propvalue_splitted = propv.split(':')
                                    propvalue[propvalue_splitted[0]]=propvalue_splitted[1]
                                    definitivedict[key]=propvalue
                                except Exception:
                                    pass
                else:
                    new_item = ""
                    new_item = key
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            definitivedict[key]=propv
            #print(definitivedict)
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

