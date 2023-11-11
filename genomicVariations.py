import json
import openpyxl
from tqdm import tqdm

list_of_excel_items=[]
list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]

with open("files/items/genomicVariations.txt", "r") as txt_file:
    list_of_excel_items=txt_file.read().splitlines() 
with open("files/properties/genomicVariations.txt", "r") as txt_file:
    list_of_properties_required=txt_file.read().splitlines() 
with open("files/headers/genomicVariations.txt", "r") as txt_file:
    list_of_headers_definitions_required=txt_file.read().splitlines()
with open('files/dictionaries/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)





def generate(list_of_excel_items, list_of_properties_required, list_of_headers_definitions_required,dict_properties):
    num_registries=1006
    xls_Book = 'datasheets/genomicVariations.xlsx'

    wb = openpyxl.load_workbook(xls_Book)

    sheet = wb['Sheet1']

    list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CC', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DD', 'DD', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EE', 'EE', 'EE', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
    ]

    dict_of_properties={}
    list_of_filled_items=[]
    total_dict =[]

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

                    
                    for header in list_of_headers_definitions_required:
                        header2 = header[0].lower() + header[1:]
                        if header2 in header:
                            if header2 not in list_of_properties_required:
                                list_of_properties_required.append(header2)
                            for h2 in list_of_definitions_required:
                                if header in h2:
                                    h2 = h2[0].lower() + h2[1:]
                                    if h2 not in list_of_properties_required:
                                        list_of_properties_required.append(h2)
            for filled_item in list_of_filled_items:
                if isinstance(filled_item, str): 
                    if 'variation' in filled_item:
                        try:
                            list_of_properties_required.remove('variation')
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
                                        for k, v in subitem.items():
                                            if isinstance(v, dict):
                                                for k1, v1 in v.items():
                                                    if isinstance(v1, dict):
                                                        for k2, v2 in v1.items():
                                                            if isinstance(v2, dict): 
                                                                for k3, v3 in v2.items():
                                                                    new_item = ""
                                                                    new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2 + "_" + k3
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            subitem_dict={}
                                                                            subitem_dict[k]={}
                                                                            subitem_dict[k][k1]={}
                                                                            subitem_dict[k][k1][k2]={}
                                                                            subitem_dict[k][k1][k2][k3]=propv
                                                            else:
                                                                new_item = ""
                                                                new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2
                                                                for propk, propv in dict_of_properties.items():
                                                                    if propk == new_item:
                                                                        subitem_dict={}
                                                                        subitem_dict[k]={}
                                                                        subitem_dict[k][k1]={}
                                                                        subitem_dict[k][k1][k2]=propv                                      
                                                    else:
                                                        new_item = ""
                                                        new_item = key + "_" + ki + "_" + k + "_" + k1
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                subitem_dict={}
                                                                subitem_dict[k]={}
                                                                subitem_dict[k][k1]=propv    
                                            else:
                                                new_item = ""
                                                new_item = key + "_" + ki + "_" + k
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        subitem_dict={}
                                                        subitem_dict[k]=propv
                                                        if subitem_dict != {}:
                                                            if subitem_dict not in vi_list:
                                                                vi_list.append(subitem_dict)
                                                            item_dict[ki]=vi_list[0]
                            elif isinstance(vi, dict):
                                vi_dict={}
                                for ki1, vi1 in vi.items():
                                    if isinstance(vi1, dict):
                                        for ki2, vi2 in vi1.items():
                                            new_item = ""
                                            new_item = key + "_" + ki + "_" + ki1 + "_" + ki2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict={}
                                                    vi_dict[ki1]={}
                                                    vi_dict[ki1][ki2]=propv
                                            if vi_dict != {}:
                                                item_dict[ki]=vi_dict    
                                    else:
                                        new_item = ""
                                        new_item = key + "_" + ki + "_" + ki1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                vi_dict[ki1]=propv 
                                                item_dict[ki]=vi_dict
                            else:
                                new_item = ""
                                new_item = key + "_" + ki
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
                            for itemvl in value_list:
                                
                                for kvl, vvl in itemvl.items():
                                    if isinstance(vvl, str):
                                        if ',' in vvl:
                                            itemv={}
                                            v_array = vvl.split(',')
                                            itemv[kvl]=v_array
                                            v_key = kvl
                                    elif isinstance(vvl, dict):
                                        v1_array=[]
                                        itemdict[kvl]={}
                                        v1_keys = []
                                        for kvl1, vvl1 in vvl.items():
                                            itemdict[kvl][kvl1]={}
                                            if isinstance(vvl1, str) and ',' in vvl1:
                                                vvl1_array = vvl1.split(',')
                                                for vvlitem in vvl1_array:
                                                    v1_array.append(vvlitem)
                                                v1_bigkeys = kvl
                                                if kvl1 not in v1_keys:
                                                    v1_keys.append(kvl1)

                            if v1_keys != []:
                                n=0
                                list_to_def=[]
                                half_array_number = len(v1_array)/2
                                itemdict[v1_bigkeys]={}
                                while n < int(half_array_number):
                                    newdict={}
                                    newdict[v1_bigkeys]={}
                                    num=int(half_array_number+n)
                                    newdict[v_key]=v_array[n]
                                    newdict[v1_bigkeys][v1_keys[0]]=v1_array[n]
                                    newdict[v1_bigkeys][v1_keys[1]]=v1_array[num]
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
                        value_dict[kd]={}
                        

                        if isinstance(vd[0], dict):
                            for kd1, vd1 in vd[0].items():
                                
                                if isinstance(vd1, dict):
                                    
                                    for kd2, vd2 in vd1.items():
                                        new_item = ""
                                        new_item = key + "_" + kd + "_" + kd1 + "_" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                
                                                value_dict[kd][kd1]={}
                                                value_dict[kd][kd1][kd2]=propv
                                else:
                                    new_item = ""
                                    new_item = key + "_" + kd + "_" + kd1
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            if ',' in propv:
                                                propv_splitted = propv.split(',')
                                                for itemsplitted in propv:
                                                    value_dict[kd][kd1]=propv_splitted
                                                    if value_dict not in vd_list:
                                                        vd_list.append(value_dict)
                                            else:
                                                value_dict[kd][kd1]=propv


                                value_dict = {ka:va for ka,va in value_dict.items() if va != {}}
                                if value_dict != {}:
                                    if value_dict not in vd_list:
                                        vd_list.append(value_dict)
                            if vd_list != []:
                                definitivedict[key]=vd_list
                        else:
                            new_item = ""
                            new_item = key + "_" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    value_dict[kd]=[]
                                    value_dict[kd].append(propv)
                    elif isinstance(vd, dict):
                        value_dict[kd]={}
                        for kd1, vd1 in vd.items():
                            if isinstance(vd1, dict):
                                value_dict[kd][kd1]={}
                                for kd2, vd2 in vd1.items():
                                    if isinstance(vd2, dict):
                                        value_dict[kd][kd1][kd2]={}
                                        for kd3, vd3 in vd2.items():
                                            new_item = ""
                                            new_item = key + "_" + kd + "_" + kd1 + "_" + kd2 + "_" + kd3
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    
                                                    
                                                    
                                                    value_dict[kd][kd1][kd2][kd3]=propv
                                                    definitivedict[key]=value_dict
                                    else:
                                        new_item = ""
                                        new_item = key + "_" + kd + "_" + kd1 + "_" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                value_dict[kd][kd1][kd2]=propv
                                                definitivedict[key]=value_dict
                            else:
                                new_item = ""
                                new_item = key + "_" + kd + "_" + kd1
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        value_dict[kd][kd1]=propv
                                        definitivedict[key]=value_dict
                        else:
                            new_item = ""
                            new_item = key + "_" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    value_dict[kd]=propv
                                    definitivedict[key]=value_dict
                else:
                    new_item = ""
                    new_item = key + "_" + kd
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            value_dict[kd]=propv
                            definitivedict[key]=value_dict
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


with open('output_schemas/genomicVariations.json', 'w') as f:
    json.dump(dict_generado, f)

