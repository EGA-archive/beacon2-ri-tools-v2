import json
import re
from tqdm import tqdm
import conf.conf as conf
import csv
import sys
from validators.cohorts import Cohorts
import hashlib

csv_filename = sys.argv[1]
output_path = sys.argv[2]

with open("files/headers/cohorts.txt", "r") as txt_file:
    list_of_headers=txt_file.read().splitlines() 
with open('files/deref_schemas/cohorts.json') as json_file:
    dict_properties = json.load(json_file)

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def generate(dict_properties, list_of_headers):
    #csv_filename = conf.csv_filename
    total_dict =[]
    with open(csv_filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        num_rows = sum(1 for row in reader)

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
                valor = vline
                property_value=property_value.replace('\ufeff', '')
                if property_value not in list_of_headers:
                    raise Exception(('the header {} is not allowed. Please, take a look at files/headers/cohorts.txt to check the headers allowed.').format(property_value))

                if i > 0:
                    if valor != '':
                        list_of_filled_items.append(property_value)


                if valor:
                    dict_of_properties[property_value]=valor



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
                                                                                #print(propk)
                                                                                subitem_dict[k][k1]={}
                                                                                subitem_dict[k][k1][k2]={}
                                                                                subitem_dict[k][k1][k2][k3]=propv
                                                                else:
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            #print(propk)
                                                                            subitem_dict[k][k1]={}
                                                                            subitem_dict[k][k1][k2]=propv   
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + k1
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:
                                                                    #print(propk)
                                                                    if subitem_dict == {}:
                                                                        subitem_dict[k]={}
                                                                    subitem_dict[k][k1]=propv  
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            #print(propk)
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
                                                        #print(propk)
                                                        propv = re.sub(r'\s', '', propv)
                                                        respropv = json.loads(propv)
                                                        item_dict[ki][ki1]=respropv 
                                            else:
                                                for ki2, vi2 in vi1.items():
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            #print(propk)
                                                            vi_dict[ki1][ki2]=propv
                                                    if vi_dict != {}:
                                                        item_dict[ki]=vi_dict    
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    #print(propk)
                                                    if propk.endswith('availability'):
                                                        vi_dict[ki1]=bool(propv)
                                                        item_dict[ki]=vi_dict
                                                    elif propk.endswith('availabilityCount'):
                                                        vi_dict[ki1]=int(propv)
                                                        item_dict[ki]=vi_dict
                                                    else:
                                                        vi_dict[ki1]=propv
                                                        item_dict[ki]=vi_dict
                                else:
                                    new_item = ""
                                    new_item = key + "|" + ki
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            #print(propk)
                                            item_dict[ki]=propv
                                if item_dict != {} and item_dict != [{}]:
                                    if item_dict not in value_list:
                                        value_list.append(item_dict)
                            if value_list != []:
                                itemdict={}
                                definitivedict[key]=[]
                                v_array=[]
                                v1_array=[]
                                v2_array=[]
                                v1_keys = []
                                v2_keys=[]
                                kv2dict={}
                                kvl2dict={}
                                v1_bigkeys=[]
                                v2_bigkeys=[]
                                v3_bigkeys=[]
                                for itemvl in value_list:
                                    for kvl, vvl in itemvl.items():
                                        if isinstance(vvl, str):
                                            if '|' in vvl:
                                                v_array = vvl.split('|')
                                                for vitem in v_array:
                                                    v1_array.append(vitem)
                                                if kvl not in v1_bigkeys:
                                                    v1_bigkeys.append(kvl)
                                        elif isinstance(vvl, dict):
                                            itemdict[kvl]={}
                                            for kvl1, vvl1 in vvl.items():
                                                itemdict[kvl][kvl1]={}
                                                if isinstance(vvl1, str) and '|' in vvl1:
                                                    vvl1_array = vvl1.split('|')
                                                    for vvlitem in vvl1_array:
                                                        v1_array.append(vvlitem)
                                                    if kvl not in v1_bigkeys:
                                                        v1_bigkeys.append(kvl)
                                                    if kvl1 not in v1_keys:
                                                        v1_keys.append(kvl1)
                                                elif isinstance(vvl1, dict):
                                                    if kvl1 not in v2_bigkeys:
                                                        v2_bigkeys.append(kvl1)
                                                        
                                    if v1_keys != []:
                                        n=0
                                        list_to_def=[]
                                        newdict={}
                                        for v1bigkey in v1_bigkeys:
                                            newdict[v1bigkey]={}
                                            if v1bigkey == 'measurementValue':
                                                newdict[v1bigkey][v2_bigkeys[0]]={}
                                                newdict[v1bigkey][v2_bigkeys[0]][v3_bigkeys[0]]=''
                                                newdict[v1bigkey][v2_bigkeys[0]][v3_bigkeys[1]]=''
                                            elif v1bigkey == 'assayCode':
                                                newdict[v1bigkey][v1_keys[0]]=""




                                        while n < len(v_array):
                                            num=int(n+len(v_array)-1)
                                            num2=int(n+len(v_array))
                                            num4=int(n+(len(v_array)*2))
                                            num6=int(n+(len(v_array)*3))
                                            for v1bigkey in v1_bigkeys:                                            
                                                if v1bigkey == 'measurementValue':
                                                    newdict[v1bigkey][v2_bigkeys[0]][v3_bigkeys[0]]=v2_array[n]
                                                    newdict[v1bigkey][v2_bigkeys[0]][v3_bigkeys[1]]=v2_array[num2]
                                                    newdict[v1bigkey][v1_keys[3]]=v1_array[num6]
                                                elif v1bigkey == 'assayCode':
                                                    newdict[v1bigkey][v1_keys[0]]=v1_array[n]
                                                    newdict[v1bigkey][v1_keys[1]]=v1_array[num2]
                                                elif v1bigkey == 'date':
                                                    newdict[v1bigkey]=v1_array[num4]
                                            list_to_def.append(newdict)
                                            
                                            n +=1
                                        for itemldf in list_to_def:
                                            definitivedict[key].append(itemldf)
                                else:
                                    for itemvl in value_list:
                                        definitivedict[key].append(itemvl)       
                elif isinstance(value, dict):
                    value_dict={}
                    for kd, vd in value.items():
                        if isinstance(vd, list):
                            vd_list=[]
                            
                            
                            if isinstance(vd[0], dict):
                                value_dict[kd]={}
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
                                                    #print(propk)
                                                    try:
                                                        value_dict[kd][0][kd1][kd2]=propv
                                                    except Exception:
                                                        try:
                                                            value_dict[kd][0][kd1]={}
                                                            value_dict[kd][0][kd1][kd2]=propv
                                                        except Exception:
                                                            value_dict[kd][kd1]={}
                                                            value_dict[kd][kd1][kd2]=propv
                                                    try:
                                                        vdictitem=value_dict[kd][0]
                                                        value_dict[kd]=[vdictitem]
                                                    except Exception:
                                                        pass
                                    elif isinstance(vd1, list):
                                        arrayofkdvs=[]
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                #print(propk)
                                                if '|' in propv:
                                                    if propv_splitted_id != [] and propv_splitted_label != []:
                                                        propv_splitted_version = propv.split(',')
                                                    elif propv_splitted_id != []:
                                                        propv_splitted_label = propv.split(',')
                                                    else:
                                                        propv_splitted_id = propv.split(',')
                                                    if propv_splitted_version != []:
                                                        n=0
                                                        while n < len(propv_splitted_id):
                                                            dicty={}
                                                            dicty['id']=propv_splitted_id[n]
                                                            dicty['label']=propv_splitted_label[n]
                                                            dicty['version']=propv_splitted_version[n]
                                                            for kdv, vdv in value_dict.items():
                                                                arrayofkdvs.append(kdv)
                                                            if kd not in arrayofkdvs:
                                                                value_dict[kd]=[]
                                                            value_dict[kd].append(dicty)
                                                            n+=1
                                                else:
                                                    try:
                                                        jsonedpropv=json.loads(propv)
                                                        if kd1 == 'ageOfOnset':
                                                            dicty[kd1]=jsonedpropv
                                                        elif kd1 == 'onset':
                                                            dicty[kd1]=jsonedpropv
                                                        elif kd1 == 'resolution':
                                                            dicty[kd1]=jsonedpropv
                                                        else:
                                                            dicty[kd1]=[jsonedpropv]
                                                        if dicty not in arrayofkdvs:
                                                            arrayofkdvs.append(dicty)
                                                        value_dict[kd]=arrayofkdvs
                                                    except Exception:
                                                        jsonedpropv=propv
                                                        dicty[kd1]=jsonedpropv
                                                        if dicty not in arrayofkdvs:
                                                            arrayofkdvs.append(dicty)
                                                        value_dict[kd]=arrayofkdvs

                                    else:
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                #print(propk)
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
                                                            if value_dict[kd]=={}:
                                                                value_dict[kd]=[]
                                                            value_dict[kd].append(dicty)
                                                            n+=1


                                                else:
                                                    if propv == 'TRUE' or propv == 'true' or propv == 'FALSE' or propv == 'false':
                                                        propv = bool(propv)
                                                    dicty[kd1]=propv
                                                    arrayofkdvs=[]
                                                    for kdv, vdv in value_dict.items():
                                                        arrayofkdvs.append(kdv)
                                                    if kd not in arrayofkdvs:
                                                        value_dict[kd]=[]
                                                    try:
                                                        if dicty not in value_dict[kd]:
                                                            if dicty != {}:
                                                                value_dict[kd].append(dicty)
                                                    except Exception:
                                                        if key == 'inclusionCriteria' or key == 'exclusionCriteria':
                                                            try:
                                                                if dicty != {}:
                                                                    value_dict[kd].append(dicty)
                                                            except Exception:
                                                                if dicty != {}:
                                                                    value_dict[kd]=[]
                                                                    value_dict[kd].append(dicty)
                                                        else:
                                                            value_dict[kd]=dicty

                                    
                                    if value_dict != {}:
                                        if value_dict not in vd_list:
                                            vd_list.append(value_dict)
                                if vd_list != []:
                                    definitive_vd_dict={}
                                    for kdv,vdv in vd_list[0].items():
                                        if vdv == {}:
                                            pass
                                        else:
                                            definitive_vd_dict[kdv]=vdv
                                    if definitive_vd_dict!={}:
                                        definitivedict[key]=definitive_vd_dict


                        elif isinstance(vd, dict):
                            value_dict[kd]={}
                            for kd1, vd1 in vd.items():
                                if isinstance(vd1, dict):
                                    for kd2, vd2 in vd1.items():
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                #print(propk)
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
                                            #print(propk)
                                            value_dict[kd][kd1]=propv
                                            definitivedict[key]=value_dict
                            else:
                                new_item = ""
                                new_item = key + "|" + kd
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        #print(propk)
                                        value_dict[kd]=propv
                                        definitivedict[key]=value_dict
                        else:
                            new_item = ""
                            new_item = key + "|" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    #print(propk)
                                    value_dict[kd]=propv
                                    if key == 'cohortDataTypes':
                                        definitivedict[key]=[value_dict]
                                    else:
                                        definitivedict[key]=value_dict
                    if value == {}:
                        new_item = ""
                        new_item = key
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                #print(propk)
                                propvalue={}
                                propvalue_splitted = propv.split(':')
                                propvalue[propvalue_splitted[0]]=propvalue_splitted[1]
                                print(key)
                                print(value)
                                definitivedict[key]=propvalue
                else:
                    new_item = ""
                    new_item = key
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            try:
                                propv = int(propv)
                            except Exception:
                                propv = propv
                            #print(key)
                            #print(propv)
                            definitivedict[key]=propv
            #print(definitivedict)
            Cohorts(**definitivedict)
            definitivedict["datasetId"]=conf.datasetId
            definitivedict["_id"]=get_hash(conf.datasetId+definitivedict["id"])
            total_dict.append(definitivedict)

            
            pbar.update(1)
            if i > num_rows:
                break
            i+=1
    pbar.close()
    return total_dict, i




dict_generado, total_i=generate(dict_properties, list_of_headers)


output = conf.output_docs_folder + 'cohorts.json'

if total_i-1 > 0:

    print('Successfully converted {} registries into {}'.format(total_i-1, output))

else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)

