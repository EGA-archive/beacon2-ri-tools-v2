import json
import re
from tqdm import tqdm
import conf.conf as conf
import csv
import sys
from validators.biosamples import Biosamples

with open("files/headers/biosamples.txt", "r") as txt_file:
    list_of_headers=txt_file.read().splitlines() 
with open('files/deref_schemas/biosamples.json') as json_file:
    dict_properties = json.load(json_file)

csv_filename = sys.argv[1]
output_path = sys.argv[2]

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

def generate(dict_properties, list_of_headers):
    #csv_filename = conf.csv_filename
    with open(csv_filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        num_rows = sum(1 for row in reader)
    total_dict =[]

    k=0
    pbar = tqdm(total = num_rows)
    with open(csv_filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        i=1
        for line in reader:
            dict_of_properties={}
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                property_value=property_value.replace('\ufeff', '')
                valor = vline
                if property_value not in list_of_headers:
                    raise Exception(('the header {} is not allowed. Please, take a look at files/headers/biosamples.txt to check the headers allowed.').format(property_value))

                if i > 0:
                    if valor is not None and valor != '':
                        list_of_filled_items.append(property_value)

                if valor:
                    dict_of_properties[property_value]=valor

            #print(dict_properties)
            #print(dict_of_properties)
            definitivedict={}
            for key, value in dict_properties.items():
                if isinstance(value, list):
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
                                                    for k1, v1 in v.items():
                                                        if isinstance(v1, dict):
                                                            for k2, v2 in v1.items():
                                                                if isinstance(v2, dict): 
                                                                    for k3, v3 in v2.items():
                                                                        new_item = ""
                                                                        new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2 + "|" + k3
                                                                        for propk, propv in dict_of_properties.items():
                                                                            if propk == new_item:
                                                                                subitem_dict[k][k1]={}
                                                                                subitem_dict[k][k1][k2]={}
                                                                                subitem_dict[k][k1][k2][k3]=propv
                                                                else:
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            subitem_dict[k][k1]={}
                                                                            subitem_dict[k][k1][k2]=propv   
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + k1
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:
                                                                    if subitem_dict == {}:
                                                                        subitem_dict[k]={}
                                                                    subitem_dict[k][k1]=propv  
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            subitem_dict[k]=propv
                                                            if subitem_dict != {} and subitem_dict[k] != {}:
                                                                if subitem_dict not in vi_list:
                                                                    vi_list.append(subitem_dict)
                                                                    item_dict[ki]=vi_list[0]
                                                                    
                                                    
                                elif isinstance(vi, dict):
                                    vi_dict={}
                                    for ki1, vi1 in vi.items():
                                        if isinstance(vi1, dict):
                                            vi_dict={}
                                            vi_dict[ki1]={}
                                            if vi1 == {}:
                                                new_item = ""
                                                new_item = key + "|" + ki + "|" + ki1
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        propv = re.sub(r'\s', '', propv)
                                                        respropv = json.loads(propv)                                                    
                                                        item_dict[ki][ki1]=respropv 
                                            else:  
                                                for ki2, vi2 in vi1.items():
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            vi_dict[ki1][ki2]=propv
                                                    if vi_dict != {}:
                                                        vivilist=[]
                                                        for kivi, vivi in vi_dict.items():
                                                            if vivi != {}:
                                                                vivilist.append(vivi)
                                                        for vivitem in vivilist:
                                                            if vivitem != {}:
                                                                item_dict[ki]=vi_dict    
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict[ki1]=propv 
                                                    item_dict[ki]=vi_dict
                                else:
                                    new_item = ""
                                    new_item = key + "|" + ki
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            item_dict[ki]=propv
                                if item_dict != {} and item_dict != [{}]:
                                    if item_dict not in value_list:
                                        value_list.append(item_dict)
                            if value_list != []:
                                for itemvl in value_list:
                                    list_to_def=commas(itemvl)
                                    for itemldf in list_to_def:
                                        try:
                                            if itemldf not in definitivedict[key]:
                                                if key == 'pedigrees':
                                                    for k, v in itemldf.items():
                                                        if k == 'members':
                                                            list_members=[]
                                                            list_members.append(v)
                                                    try:
                                                        itemldf['members']=list_members
                                                    except Exception:
                                                        pass
                                                definitivedict[key].append(itemldf)
                                        except Exception:
                                            definitivedict[key]=[]
                                            definitivedict[key].append(itemldf)
                            else:
                                for itemvl in value_list:
                                    definitivedict[key].append(itemvl)     
                                else:
                                    for itemvl in value_list:
                                        definitivedict[key].append(itemvl)       
                elif isinstance(value, dict):
                    value_dict={}
                    for kd, vd in value.items():
                        if isinstance(vd, list):
                            vd_list=[]
                            
                            
                            if isinstance(vd[0], dict):
                                dicty={}
                                propv_splitted_id=[]
                                propv_splitted_label=[]
                                arrayofkdvs=[]
                                
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
                                                if '|' in propv:
                                                    if propv_splitted_id != []:
                                                        propv_splitted_label = propv.split('|')
                                                    else:
                                                        
                                                        propv_splitted_id = propv.split('|')
                                                    if propv_splitted_label != []:
                                                        n=0
                                                        while n < len(propv_splitted_id):
                                                            dicty={}
                                                            dicty['id']=propv_splitted_id[n]
                                                            dicty['label']=propv_splitted_label[n]
                                                            for kdv, vdv in value_dict.items():
                                                                arrayofkdvs.append(kdv)
                                                            if kd not in arrayofkdvs:
                                                                value_dict[kd]=[]
                                                            value_dict[kd].append(dicty)
                                                            n+=1


                                                else:
                                                    dicty[kd1]=propv
                                                    arrayofkdvs=[]
                                                    for kdv, vdv in value_dict.items():
                                                        arrayofkdvs.append(kdv)
                                                    if kd not in arrayofkdvs:
                                                        value_dict[kd]=[]
                                                    if dicty not in value_dict[kd]:
                                                        value_dict[kd].append(dicty)

                                    
                                    if value_dict != {}:
                                        if value_dict not in vd_list:
                                            vd_list.append(value_dict)
                                if vd_list != []:
                                    definitivedict[key]=vd_list


                        elif isinstance(vd, dict):
                            for kd1, vd1 in vd.items():
                                if isinstance(vd1, dict):
                                    for kd2, vd2 in vd1.items():
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                if value_dict == {}:
                                                    value_dict[kd]={}
                                                value_dict[kd][kd1]={}
                                                value_dict[kd][kd1][kd2]=propv
                                                definitivedict[key]=value_dict
                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd + "|" + kd1
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            value_dict[kd][kd1]=propv
                                            definitivedict[key]=value_dict
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
                                    value_dict[kd]=propv
                                    definitivedict[key]=value_dict
                    if value == {}:
                        new_item = ""
                        new_item = key
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                propv = re.sub(r'\s', '', propv)
                                respropv = json.loads(propv)  
                                definitivedict[key]=respropv
                else:
                    new_item = ""
                    new_item = key
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            definitivedict[key]=propv
            Biosamples(**definitivedict)
            total_dict.append(definitivedict)

            
            pbar.update(1)
            if i > num_rows:
                break
            i+=1
    pbar.close()
    return total_dict, i




dict_generado, total_i=generate(dict_properties, list_of_headers)


output = conf.output_docs_folder + 'biosamples.json'

if total_i-1 > 0:

    print('Successfully converted {} registries into {}'.format(total_i-1, output))

else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)
