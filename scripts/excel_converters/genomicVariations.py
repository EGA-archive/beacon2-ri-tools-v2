import json
import openpyxl
from tqdm import tqdm
import re
from . import conf

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
    num_rows=1004
    xls_Book = conf.excel_filename

    wb = openpyxl.load_workbook(xls_Book)

    sheet = wb['genomicVariations']
    list_columns = ['AAA', 'AAB', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
                    'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FU', 'FV', 'FW', 'FX', 'FY', 'FZ',
                    'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GV', 'GW', 'GX', 'GY', 'GZ',
                    'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HU', 'HV', 'HW', 'HX', 'HY', 'HZ',
                    'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL', 'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IV', 'IW', 'IX', 'IY', 'IZ',

    ]
    
    list_of_filled_items=[]
    total_dict =[]

    k=0
    j=2
    pbar = tqdm(total = num_rows)
    while j < num_rows+2:
        i=0
        dict_of_properties={}
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
                

            elif valor == 0:
                dict_of_properties[property_value]=valor

            i +=1

        

        for lispro in list_of_properties_required:
            if lispro not in list_of_filled_items:
                raise Exception(('error: you are not filling all the required fields. missing field is: {}').format(lispro))
                

        #print(dict_properties)
        #print(dict_of_properties)
        definitivedict={}
        for key, value in dict_properties.items():
            if isinstance(value, list):
                value_list=[]
                item_dict={}
                for item in value:
                    outcome = 0
                    if isinstance(item, dict):
                        
                        for ki, vi in item.items():
                            if isinstance(vi, list):
                                vi_list=[]
                                subitem_dict={}
                                for subitem in vi:
                                    if isinstance(subitem, dict):
                                        
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
                                                                        subitem_dict[k][k1][k2]=propv
                                                        if subitem_dict[k][k1]=={}:
                                                            del subitem_dict[k][k1]                                      
                                                    else:
                                                        new_item = ""
                                                        new_item = key + "|" + ki + "|" + k + "|" + k1
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                subitem_dict[k][k1]=propv 
                                                if subitem_dict[k]=={}:
                                                    del subitem_dict[k]  
                                            elif isinstance(v, list):
                                                listitemv=[]
                                                vivdict={}
                                                for itemv in v:
                                                
                                                    if isinstance(itemv, dict):
                                                        #print('ki is {}'.format(ki))
                                                        #print('k is {}'.format(k))
                                                        #print(itemv)
                                                        
                                                        for kiv, viv in itemv.items():
                                                            

                                                            if isinstance(viv, list):

                                                                for itemviv in viv:
                                                                    if isinstance(itemviv, dict):
                                                                        
                                                                        for kivi, vivi in itemviv.items():
                                                                            
                                                                            if isinstance(vivi, list):
                                                                                
                                                                                for vivitem1 in vivi:
                                                                                    
                                                                                    for kivivi, vivivi in vivitem1.items():
                                                                                        if isinstance(vivivi, dict):
                                                                                            
                                                                                            for kivivi1, vivivi1 in vivivi.items():
                                                                                                new_item = ""
                                                                                                new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi + "|" + kivivi1
                                                                                                for propk, propv in dict_of_properties.items():
                                                                                                    if propk == new_item:
                                                                                                        print(propk)
                                                                                                        try:
                                                                                                            vivdict[kiv][kivi][kivivi][kivivi1]=propv  
                                                                                                        except Exception:
                                                                                                            vivdict[kiv]={}
                                                                                                            vivdict[kiv][kivi]={}
                                                                                                            vivdict[kiv][kivi][kivivi]={}
                                                                                                            vivdict[kiv][kivi][kivivi][kivivi1]=propv
                                                                                        elif isinstance(vivivi, list):
                                                                                            for vivivitem in vivivi:
                                                                                                for kivitem, vivitem in vivivitem.items():
                                                                                                    new_item = ""
                                                                                                    new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi + "|" + kivitem
                                                                                                    for propk, propv in dict_of_properties.items():
                                                                                                        if propk == new_item:
                                                                                                            try:
                                                                                                                vivdict[kiv][kivi][kivivi][kivitem]=propv
                                                                                                            except Exception:
                                                                                                                try:
                                                                                                                    vivdict[kiv][kivi][kivivi]={}
                                                                                                                    vivdict[kiv][kivi][kivivi][kivitem]=propv
                                                                                                                except Exception:

                                                                                                                    vivdict[kiv][kivi]={}
                                                                                                                    vivdict[kiv][kivi][kivivi]={}
                                                                                                                    vivdict[kiv][kivi][kivivi][kivitem]=propv
                                                                                                                

                                                                                        else:
                                                                                            
                                                                                            new_item = ""
                                                                                            new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi
                                                                                            #print(new_item)
                                                                                            for propk, propv in dict_of_properties.items():
                                                                                                if propk == new_item:
                                                                                                    try:
                                                                                                        vivdict[kiv][kivi][kivivi]=propv
                                                                                                    except Exception:
                                                                                                        vivdict[kiv]={}
                                                                                                        vivdict[kiv][kivi]={}
                                                                                                        vivdict[kiv][kivi][kivivi]=propv

                                                                            else:
                                                                                new_item = ""
                                                                                new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi
                                                                                for propk, propv in dict_of_properties.items():
                                                                                    if propk == new_item:
                                                                                        try:
                                                                                            vivdict[kiv][kivi]=propv
                                                                                        except Exception:
                                                                                            vivdict[kiv]={}
                                                                                            vivdict[kiv][kivi]=propv
                                                                                    elif propk == key + "|" + ki + "|" + k + "|" + kiv:
                                                                                        vivdict[kiv]=propv
                                                                            



                                                                                
                                                        


                                                            else:
                                                                new_item = ""
                                                                new_item = key + "|" + ki + "|" + k + "|" + kiv
                                                                for propk, propv in dict_of_properties.items():
                                                                    if propk == new_item:
                                                                        vivdict[kiv]=propv





                                                        

                                                    if vivdict != {}:
                                                        #print(vivdict)
                                                        subitem_dict[k]=vivdict
                                            elif ki == 'copies':
                                                new_item = ""
                                                new_item = key + "|" + ki
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        propv = re.sub(r'\s', '', propv)
                                                        respropv = json.loads(propv) 
                                                        subitem_dict=respropv

                                            else:
                                                new_item = ""
                                                new_item = key + "|" + ki + "|" + k
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        try:
                                                            propv = re.sub(r'\s', '', propv)
                                                            respropv = json.loads(propv) 
                                                            subitem_dict[k]=respropv
                                                        except Exception:
                                                            subitem_dict[k]=propv


                                    if subitem_dict != {}:
                                        if subitem_dict not in vi_list and subitem_dict != {}:
                                            vi_list.append(subitem_dict)
                                        
                                        item_dict[ki]=vi_list[0]
                            elif isinstance(vi, dict):

                                vi_dict={}
                                for ki1, vi1 in vi.items():
                                    if isinstance(vi1, dict):
                                        vi_dict[ki1]={}
                                        for ki2, vi2 in vi1.items():
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict[ki1][ki2]=propv
                                            if vi_dict != {}:
                                                item_dict[ki]=vi_dict
                                        if vi_dict[ki1]=={}:
                                            del vi_dict[ki1]
                                    elif ki1 == 'variation':
                                        vi_dict[ki1]={}
                                        new_item = ""
                                        new_item = key + "|" + ki + "|" + ki1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                vi_dict[ki1]=propv
                                    elif isinstance(vi1, list):
                                        vi_dict[ki1]=[]
                                        dictkvi={}
                                        for itemvi1 in vi1:
                                            for kvi, vvi in itemvi1.items():
                                                new_item = ""
                                                new_item = key + "|" + ki + "|" + ki1 + "|" + kvi
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        dictkvi[kvi]=vvi
                                        vi_dict[ki1]=dictkvi
                                    else:
                                        new_item = ""
                                        new_item = key + "|" + ki + "|" + ki1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                vi_dict[ki1]=propv 
                                                item_dict[ki]=vi_dict
                                if vi_dict=={}:
                                    del vi_dict
                            else:
                                
                                new_item = ""
                                new_item = key + "|" + ki
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        if '|' in propv:
                                            outcome +=1
                                            v1_keys=[]
                                        item_dict[ki]=propv

                            if ki == 'members':
                                new_item = ""
                                new_item = key + "|" + ki
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        #print(propk)
                                        propv = re.sub(r'\s', '', propv)
                                        respropv = json.loads(propv)  
                                        item_dict[ki]=respropv
    
                        if item_dict != {} and item_dict != [{}]:
                            

                            if outcome > 0:
                                if item_dict not in value_list:
                                    value_list.append(item_dict)
                                if value_list != []:
                                    itemdict={}
                                    definitivedict[key]=[]
                                    v_array=[]
                                    for itemvl in value_list:

                                        for kvl, vvl in itemvl.items():
                                            if isinstance(vvl, str):
                                                if '|' in vvl:
                                                    itemv={}
                                                    v_array = vvl.split('|')
                                                    itemv[kvl]=v_array
                                                    v_key = kvl
                                            elif isinstance(vvl, dict):
                                                
                                                v1_array=[]
                                                itemdict[kvl]={}
                                                v1_keys = []
                                                for kvl1, vvl1 in vvl.items():
                                                    itemdict[kvl][kvl1]={}
                                                    if isinstance(vvl1, str) and '|' in vvl1:
                                                        vvl1_array = vvl1.split('|')
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
                                    elif len(v_array) > 1:
                                        list_to_def=[]
                                        
                                        for itva in v_array:
                                            newdict={}
                                            newdict[v_key]=itva
                                            list_to_def.append(newdict)
                                        for itemldf in list_to_def:
                                            definitivedict[key].append(itemldf)
                                    else:
                                        for itemvl in value_list:
                                            definitivedict[key].append(itemvl) 
                            else:
                                if key == 'caseLevelData':
                                    definitivedict[key]=[]
                                    definitivedict[key].append(item_dict)
                                else:
                                    definitivedict[key]=item_dict
                                
            elif isinstance(value, dict):
                value_dict={}
                for kd, vd in value.items():
                    if isinstance(vd, list):
                        vd_list=[]
                        value_dict[kd]={}
                        for itemvd in vd:
                            if isinstance(itemvd, dict):
                                dict_mol={}
                                for kd1, vd1 in itemvd.items():
                                    if isinstance(vd1, dict):
                                        value_dict[kd][kd1]={}
                                        for kd2, vd2 in vd1.items():
                                            new_item = ""
                                            new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    value_dict[kd][kd1][kd2]=propv
                                        if value_dict[kd][kd1]=={}:
                                            del value_dict[kd][kd1]
                                    elif isinstance(vd1, list):
                                        value_dict[kd][kd1]={}
                                        for item in vd1:
                                            for kd2, vd2 in item.items():
                                                if isinstance(vd2, list):
                                                    value_dict[kd][kd1][kd2]={}
                                                    for itemvd2 in vd2:
                                                        for kd3, vd3 in itemvd2.items():
                                                            new_item = ""
                                                            new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:
                                                                    value_dict[kd][kd1][kd2][kd3]=propv
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            value_dict[kd][kd1][kd2]=propv
                                        if value_dict[kd][kd1]=={}:
                                            del value_dict[kd][kd1]
                                    else:
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                if '|' in propv:
                                                    propv_splitted = propv.split('|')
                                                    for itemsplitted in propv:
                                                        value_dict[kd][kd1]=propv_splitted
                                                        if value_dict not in vd_list:
                                                            vd_list.append(value_dict)
                                                else:
                                                    if value_dict == {}:
                                                        value_dict[kd]={}
                                                    if 'molecularEffects' in kd:
                                                        try:
                                                            dict_mol[kd1]=propv
                                                            value_dict[kd].append(dict_mol)
                                                        except Exception:
                                                            dict_mol[kd1]=propv
                                                            value_dict[kd]=[]
                                                    else:                                                          
                                                        value_dict[kd][kd1]=propv



                            else:
                                new_item = ""
                                new_item = key + "|" + kd
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        value_dict[kd]=[]
                                        value_dict[kd].append(propv)


                            value_dict = {ka:va for ka,va in value_dict.items() if va != {}}
                            if value_dict != {}:
                                definitivedict[key]=value_dict
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
                                            new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    value_dict[kd][kd1][kd2][kd3]=propv
                                                    definitivedict[key]=value_dict
                                    else:
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
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


output = conf.output_docs_folder + 'genomicVariations.json'

with open(output, 'w') as f:
    json.dump(dict_generado, f)

