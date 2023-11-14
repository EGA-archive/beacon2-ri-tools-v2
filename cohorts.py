import json
import openpyxl
import re
from tqdm import tqdm

list_of_excel_items=[]
list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]

with open("files/items/cohorts.txt", "r") as txt_file:
    list_of_excel_items=txt_file.read().splitlines() 
with open("files/properties/cohorts.txt", "r") as txt_file:
    list_of_properties_required=txt_file.read().splitlines() 
with open("files/headers/cohorts.txt", "r") as txt_file:
    list_of_headers_definitions_required=txt_file.read().splitlines()
with open('files/dictionaries/cohorts.json') as json_file:
    dict_properties = json.load(json_file)




def generate(list_of_excel_items, list_of_properties_required, list_of_headers_definitions_required,dict_properties):
    

    wb = openpyxl.load_workbook('datasheets/cohorts.xlsx')

    sheet = wb['Sheet1']

    list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
    ]


    dict_of_properties={}
    list_of_filled_items=[]
    total_dict =[]
    num_registries = 3
    k=0
    j=2
    pbar = tqdm(total = num_registries-2)
    while j < num_registries:
        i=0
        while i <(len(list_of_excel_items)+2):
            property = list_columns[i]+str(1)
            property_value = sheet[property].value

            number_sheet = list_columns[i]+str(j)
            

            
            valor = sheet[number_sheet].value
            if i > 1:
                if valor != '':
                    list_of_filled_items.append(property_value)



            for filled_item in list_of_filled_items:
                if isinstance(filled_item, str): 
                    if 'sex' in filled_item:
                        try:
                            list_of_properties_required.remove('sex')
                        except Exception:
                            pass
            if valor:
                dict_of_properties[property_value]=valor
            i +=1

        

        for lispro in list_of_properties_required:
            if lispro not in list_of_filled_items:
                raise Exception(('error: you are not filling all the required fields. missing field is: {}').format(lispro))

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
                                        if ',' in vvl:
                                            v_array = vvl.split(',')
                                            for vitem in v_array:
                                                v1_array.append(vitem)
                                            if kvl not in v1_bigkeys:
                                                v1_bigkeys.append(kvl)
                                    elif isinstance(vvl, dict):
                                        itemdict[kvl]={}
                                        for kvl1, vvl1 in vvl.items():
                                            itemdict[kvl][kvl1]={}
                                            if isinstance(vvl1, str) and ',' in vvl1:
                                                vvl1_array = vvl1.split(',')
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
                                            if ',' in propv:
                                                if propv_splitted_id != []:
                                                    propv_splitted_label = propv.split(',')
                                                else:
                                                    
                                                    propv_splitted_id = propv.split(',')
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
                            propvalue={}
                            propvalue_splitted = propv.split(':')
                            propvalue[propvalue_splitted[0]]=propvalue_splitted[1]
                            definitivedict[key]=propvalue
            else:
                new_item = ""
                new_item = key
                for propk, propv in dict_of_properties.items():
                    if propk == new_item:
                        definitivedict[key]=propv
        total_dict.append(definitivedict)
        j+=1
        pbar.update(1)
    pbar.close()
    return total_dict




dict_generado=generate(list_of_excel_items, list_of_properties_required, list_of_headers_definitions_required,dict_properties)


with open('output_schemas/cohorts.json', 'w') as f:
    json.dump(dict_generado, f)

