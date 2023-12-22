import json
import csv

collection = 'ref_schemas/genomicVariations'
file_to_open= collection + '.json'
# Opening JSON file 
new_file = open(file_to_open,) 
   
# returns JSON object as   
# a dictionary 
data = json.load(new_file) 

vrs_file = open('ref_schemas/vrs.json')
data_vrs = json.load(vrs_file)

   
commonDefinitions = open('ref_schemas/commondefinitions.json')
commonDefinitions = json.load(commonDefinitions)
commonComponents = open('ref_schemas/beaconcommoncomponents.json')
commonComponents = json.load(commonComponents)

dict_definitions={}
dict_vrs_definitions={}
dict_properties={}

def location():
    initial_dict={}
    second_dict={}
    item_dict={}
    initial_list=[]
    second_list=[]
    vrs = 'ref_schemas/vrs'
    file_vrs= vrs + '.json'
    new_vrs = open(file_vrs,) 
    datavrs = json.load(new_vrs)
    for key, value in datavrs.items():
        if key == 'definitions':
            initial_dict=value
    for key, value in initial_dict.items():
        if key == 'Location':
            second_dict=value
    for key, value in second_dict.items():
        if key == 'oneOf':
            initial_list=value
    for item in initial_list:
        for k,v in item.items():
            v_splitted = v.split('/')
            second_list.append(v_splitted[-1])
    for item in second_dict:
        for key, value in initial_dict.items():
            if key == item:
                item_dict=value
    new_dict={}
    for key, value in initial_dict.items():
        for item in second_list:
            if key == item:
                new_dict[key]=value
    new_dict2={}
    for key, value in new_dict.items():
        for k, v in value.items():
            if k == 'properties':
                new_dict2[key]=v
    new_dict3={}
    for key, value in new_dict2.items():
        new_dict3[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if k1 == '$ref':
                        v1_splitted = v1.split('/')
                        if 'CURIE' in v1_splitted[-1]:
                            new_dict3[key][k]=""
                        else:
                            for kd, vd in initial_dict.items():
                                if kd == v1_splitted[-1]:
                                    new_dict3[key][k]=vd
                    elif k1 == 'type':
                        if v1 == 'string':
                            new_dict3[key][k]=""  
                    elif k1 == 'oneOf':
                         new_dict3[key][k]=[]
                         for item in v1:
                             for kr, vr in item.items():
                                 vr_splitted = vr.split('/')
                                 for krd, vrd in initial_dict.items():
                                     if krd == vr_splitted[-1]:
                                        new_dict3[key][k].append(vrd)
    new_dict4={}
    for key, value in new_dict3.items():
        new_dict4[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if k1 == 'properties':
                        new_dict4[key][k]=v1
            else:
                new_dict4[key][k]=v
    new_dict5={}
    for key, value in new_dict4.items():
        new_dict5[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    for k2, v2 in v1.items():
                        if k2 == '$ref':
                            v2_splitted = v2.split('/')
                            if 'CURIE' in v2_splitted[-1]:
                                new_dict5[key][k]=""
                            else:
                                for kd, vd in initial_dict.items():
                                    if kd == v2_splitted[-1]:
                                        new_dict5[key][k]=vd
                        elif k2 == 'type':
                            if v2 == 'string':
                                new_dict5[key][k]=""  
            else:
                new_dict5[key][k]=v
    new_dict6={}
    for key, value in new_dict5.items():
        new_dict6[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if k1 == 'type':
                        if v1 == 'string':
                            new_dict6[key][k]=""   
            elif isinstance(v, list):
                new_dict6[key][k]=[]
                for item in v:
                    for ki, vi in item.items():
                        if ki == 'properties':
                            new_dict6[key][k].append(vi)
            else:
                new_dict6[key][k]=v
    new_dict7={}
    for key, value in new_dict6.items():
        new_dict7[key]={}
        for k, v in value.items():
            if isinstance(v, list):
                new_dict7[key][k]=[]
                for item in v:
                    if isinstance(item, dict):
                        itemdict={}
                        for k2, v2 in item.items():
                            for k1, v1 in v2.items():
                                if k1 == '$ref':
                                    v1_splitted = v1.split('/')
                                    if 'CURIE' in v1_splitted[-1]:
                                        itemdict[k2]=""
                                    else:
                                        for kd, vd in initial_dict.items():
                                            if kd == v1_splitted[-1]:
                                                itemdict[k2]=vd
                                elif k1 == 'type':
                                    if v1 == 'string':
                                        itemdict[k2]=''
                                    elif v1 == 'integer':
                                        itemdict[k2]=0
                                elif k1 == 'oneOf':
                                    itemdict[k2]=[]
                                    for item in v1:
                                        for kr, vr in item.items():
                                            vr_splitted = vr.split('/')
                                            for krd, vrd in initial_dict.items():
                                                if krd == vr_splitted[-1]:
                                                    itemdict[k2].append(vrd)
                        new_dict7[key][k].append(itemdict)
            else:
                new_dict7[key][k]=v

    new_dict8={}
    for key, value in new_dict7.items():
        new_dict8[key]={}
        for k, v in value.items():
            if isinstance(v, list):
                new_dict8[key][k]=[]
                for item in v:
                    if isinstance(item, dict):
                        itemdict={}
                        for k2, v2 in item.items():
                            if isinstance(v2, list):
                                itemdict[k2]=[]
                                for itemv2 in v2:
                                    for k1, v1 in itemv2.items():
                                        if k1 == 'properties':
                                            itemdict[k2].append(v1)

                            else:
                                itemdict[k2]=v2
                        new_dict8[key][k].append(itemdict)
            else:
                new_dict8[key][k]=v
    new_dict9={}
    
    for key, value in new_dict8.items():
        new_dict9[key]={}
        for k, v in value.items():
            if isinstance(v, list):
                new_dict9[key][k]=[]
                for item in v:
                    if isinstance(item, dict):
                        itemdict={}
                        for k2, v2 in item.items():
                            if isinstance(v2, list):
                                itemdict[k2]=[]
                                
                                for itemv2 in v2:
                                    v1dict={}
                                    for k1, v1 in itemv2.items():

                                        if isinstance(v1, dict):
                                            
                                            if k1 == 'type':
                                                for k3, v3 in v1.items():
                                                    if v3 == 'string':
                                                        v1dict[k1]=''
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                                    elif v3 == 'integer':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                                    elif v3 == 'number':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                            elif k1 == 'value':
                                                for k3, v3 in v1.items():
                                                    if v3 == 'integer':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                                    elif v3 == 'number':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                            else:
                                                for k3, v3 in v1.items():
                                                    if v3 == 'number':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                                    elif v3 == 'string':
                                                        v1dict[k1]=''
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)
                                                    elif v3 == 'integer':
                                                        v1dict[k1]=0
                                                        if v1dict not in itemdict[k2]:
                                                            itemdict[k2].append(v1dict)

                            else:
                                itemdict[k2]=v2
                    
                        new_dict9[key][k].append(itemdict)
            else:
                new_dict9[key][k]=v
    list_of_locations=[]
    for key,value in new_dict9.items():
        list_of_locations.append(value)
    return list_of_locations

def state(datavrs):
    initial_dict={}
    second_dict={}
    item_dict={}
    initial_list=[]
    second_list=[]

    for key, value in datavrs.items():
        if key == 'definitions':
            initial_dict=value
    for key, value in initial_dict.items():
        if key == 'Allele':
            second_dict=value
    for key, value in second_dict.items():
        if key == 'properties':
            third_dict=value
    
    for key, value in third_dict.items():
        if key == 'state':
            fourth_dict=value
    for key, value in fourth_dict.items():
        if key == 'oneOf':
            initial_list=value
    for item in initial_list:
        for k,v in item.items():
            v_splitted = v.split('/')
            second_list.append(v_splitted[-1])
    new_dict={}
    for key, value in initial_dict.items():
        for item in second_list:
            if key == item:
                new_dict[key]=value
    
    new_dict2={}
    for key, value in new_dict.items():
        for k, v in value.items():
            if k == 'properties':
                new_dict2[key]=v
    #print(new_dict2)
    new_dict3={}
    for key, value in new_dict2.items():
        new_dict3[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if k1 == '$ref':
                        v1_splitted = v1.split('/')
                        if 'CURIE' in v1_splitted[-1]:
                            new_dict3[key][k]=""
                        else:
                            for kd, vd in initial_dict.items():
                                if kd == v1_splitted[-1]:
                                    new_dict3[key][k]=vd
                    elif k1 == 'type':
                        if v1 == 'string':
                            new_dict3[key][k]=""  
                        elif v1 == 'boolean':
                            new_dict3[key][k]=True 
                    elif k1 == 'oneOf':
                         new_dict3[key][k]=[]
                         for item in v1:
                             for kr, vr in item.items():
                                 vr_splitted = vr.split('/')
                                 for krd, vrd in initial_dict.items():
                                     if krd == vr_splitted[-1]:
                                        new_dict3[key][k].append(vrd)
                    elif k1 == 'items':
                         new_dict3[key][k]=[]
                         for kit, vit in v1.items():
                             new_dict3[key][k]=vit
                             
    #print(new_dict3)
    new_dict4={}
    for key, value in new_dict3.items():
        new_dict4[key]={}
        for k, v in value.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if k1 == 'properties':
                        #print(v1)
                        new_dict4[key][k]=v1
                    elif k1 == 'type':
                        if v1 == 'string':
                            new_dict4[key][k]=''

            else:
                #print(k)
                new_dict4[key][k]=v
    #print(new_dict4)
    new_dict41={}
    for key, value in new_dict4.items():
        new_dict41[key]={}
        for k, v in value.items():
            if isinstance(v, list):
                new_dict41[key][k]=[]
                for item in v:
                    for ki, vi in item.items():
                        if ki == 'properties':
                            new_dict41[key][k].append(vi)
                        elif ki == '$ref':
                            vi_splitted = vi.split('/')
                            if 'CURIE' in vi_splitted[-1]:
                                new_dict41[key][k].append("")
                            else:
                                for kd, vd in initial_dict.items():
                                    if kd == vi_splitted[-1]:
                                        new_dict3[key][k].append(vd)

            elif k == 'location':
                new_dict41[key][k]='location'
            else:
                new_dict41[key][k]=v
    #print(new_dict41)
    new_dict42={}
    for key, value in new_dict41.items():
        new_dict42[key]={}
        for k, v in value.items():
            #print(k)
            if isinstance(v, list):
                new_dict42[key][k]=[]
                for item in v:
                    if isinstance(item, dict):
                        dictvi={}
                        for ki, vi in item.items():
                            if ki == 'location':
                                dictvi[ki]= 'location'
                            elif ki == 'sequence':
                                dictvi[ki]= ''
                            elif isinstance(vi, dict):
                                for ki1, vi1 in vi.items():
                                    
                                    if ki1 == 'type':
                                        #print(vi1)
                                        if vi1 == 'string':
                                            dictvi[ki]= ''
                                            
                                        elif vi1 == 'boolean':
                                            dictvi[ki]= ''
                                        elif vi1 == 'number':
                                            dictvi[ki]= 0
                                        elif vi1 == 'integer':
                                            dictvi[ki]= 0

                        new_dict42[key][k].append(dictvi) 
                              
            elif k == 'location':
                new_dict42[key][k]='location'
            else:
                #print(k)
                new_dict42[key][k]=v
    #print(new_dict42)
    new_dict43={}
    for key, value in new_dict42.items():
        new_dict43[key]={}
        for k, v in value.items():
            if isinstance(v, list):
                new_dict43[key][k]=[]
                for item in v:
                    if isinstance(item, dict):
                        dictvi={}
                        for ki, vi in item.items():
                            if ki == 'location':
                                dictvi[ki]= location()
                            else:
                                dictvi[ki]= vi


                        new_dict43[key][k].append(dictvi) 
                              
            elif k == 'location':
                new_dict43[key][k]=location()
            else:
                new_dict43[key][k]=v
        
    list_of_states=[]
    for key,value in new_dict43.items():
        list_of_states.append(value)
    #print(list_of_states)
    return list_of_states

def count_list(countlist, data_vrs):
    for key, value in data_vrs.items():
        if key == 'definitions':
            initial_dict=value

    listnew=[]
    for item in countlist:
        for k, v in item.items():
            vsplitted = v.split('/')
            listnew.append(vsplitted[-1])
    list2=[]
    for item in  listnew:
        for kd, vd in initial_dict.items():
            if kd == item:
                list2.append(vd)
    #print(list2)
    list3=[]
    for item in list2:
        for k, v in item.items():
            if k == 'properties':
                list3.append(v)
    #print(list3)
    list4=[]
    
    for item in list3:
        dict4={}
        for k, v in item.items():
            for k1, v1 in v.items():
                if k1 == 'type':
                    if v1 == 'string':
                        dict4[k]=''
                    elif v1 == 'integer':
                        dict4[k]=0
                    elif v1 == 'number':
                        dict4[k]=0

        list4.append(dict4)
    return list4


def subject(list_subject):
    initial_dict={}
    new_list_subject=[]
    vrs = 'ref_schemas/vrs'
    file_vrs= vrs + '.json'
    new_vrs = open(file_vrs,) 
    datavrs = json.load(new_vrs)
    for key, value in datavrs.items():
        if key == 'definitions':
            initial_dict=value
    for subject in list_subject:
        for k, v in subject.items():
            vsplitted = v.split('/')
            new_list_subject.append(vsplitted[-1])
    v1dict={}
    newlist2=[]
    for subject in new_list_subject:
        print(subject)
        for kd, vd in initial_dict.items():
            if kd == subject:
                print(kd)
                newlist2.append(vd)
    newlist3=[]
    for item in newlist2:
        for k, v in item.items():
            if k == 'properties':
                newlist3.append(v)

    newlist4=[]

    #print(newlist3)

    for item in newlist3:
        v1dict={}
        for k, v in item.items():
            for k1, v1 in v.items():
                if k1 == '$ref':
                    v1_splitted = v1.split('/')
                    if 'CURIE' in v1_splitted[-1]:
                        v1dict[k]=""
                    else:
                        for kd, vd in initial_dict.items():
                            if kd == v1_splitted[-1]:
                                v1dict[k]=vd
                elif k1 == 'type':
                    if v1 == 'string':
                        v1dict[k]=''
                elif isinstance(v1, list):
                    v1dict[k]=v1
        newlist4.append(v1dict)

    newlist5=[]

    for item in newlist4:
        v1dict={}
        for k, v in item.items():
            if isinstance(v, dict):
                v1dict[k]=''
            elif isinstance(v, list):
                v1dict[k]=''
                    
            else:
                v1dict[k]=v
        newlist5.append(v1dict)



    return newlist5

def vrs(data_vrs):
    dict_vrs_definitions={}
    for key, value in data_vrs.items():
        if key == 'definitions':
            initial_dict=value
    second_dict={}
    for k, v in initial_dict.items():
        if k == 'SystemicVariation':
            second_dict[k]=v
        elif k == 'MolecularVariation':
            second_dict[k]=v

    third_dict={}
    for key, value in second_dict.items():
        for k, v in value.items():
            if k == 'oneOf':
                third_dict[key]=v
    fourth_dict={}
    for key, value in third_dict.items():
        list_of_ref=[]
        for item in value:
            for k, v in item.items():
                if k == '$ref':
                    vsplitted = v.split('/')
                    for ki, vi in initial_dict.items():
                        if ki == vsplitted[-1]:
                            list_of_ref.append(vi)
            fourth_dict[key]=list_of_ref
    #print(fourth_dict)
    new_dict3={}
    for key, value in fourth_dict.items():
        new_dict3[key]=[]
        for item in value:
            for k, v in item.items():
                if isinstance(v, dict):
                    v1dict={}
                    if k == 'properties':
                        v1dict=v
                    new_dict3[key].append(v1dict)
    #print(new_dict3)
    new_dict4={}
    for key, value in new_dict3.items():
        v1dict={}
        new_dict4[key]=[]
        for item in value:
            for k, v in item.items():
                if k == 'location':
                    v1dict[k]=location()
                elif k == 'state':
                    v1dict[k]=state(data_vrs)
                elif isinstance(v, dict):
                    for k1, v1 in v.items():
                        if k1 == '$ref':
                            v1_splitted = v1.split('/')
                            if 'CURIE' in v1_splitted[-1]:
                                v1dict[k]=""
                            else:
                                for kd, vd in initial_dict.items():
                                    if kd == v1_splitted[-1]:
                                        v1dict[k]=vd
                        elif k1 == 'type':
                            if v1 == 'string':
                                v1dict[k]="" 
                        elif k1 == 'items':
                            #print(v1)
                            
                            for k2, v2 in v1.items():
                                if k2 == '$ref':
                                    v2_splitted = v2.split('/')
                                    for kd, vd in initial_dict.items():
                                        if kd == v2_splitted[-1]:
                                            
                                            for kd1, vd1 in vd.items():
                                                if kd1 == 'properties':
                                                    vd3dict={}
                                                    
                                                    for kd2, vd2 in vd1.items():
                                                        for kd3, vd3 in vd2.items():
                                                            if vd3 == 'string':
                                                                vd3dict[kd2]=''
                                                            elif kd3 == 'oneOf':
                                                                count=count_list(vd3,data_vrs)
                                                                #print(count)
                                                                vd3dict[kd2]=count
                                                    v1dict[k]=vd3dict
                        elif k1 == 'oneOf':
                            v1dict[k]=[{'_id': '', 'type': '', 'species_id': '', 'chr': '', 'interval': ''}, {'type': '', 'gene_id': ''}, {'_id': '', 'type': '', 'sequence_id': '', 'interval': ''}]

                            
                                            







                if v1dict not in new_dict4[key]:
                    new_dict4[key].append(v1dict)
    #print(new_dict4)


    list_of_variations=[]
    for key,value in new_dict4.items():
        list_of_variations.append(value)
    #print(list_of_variations)
    return list_of_variations
    
def oneof_function(oneof_array):
    list_oneof=[]
    for value in oneof_array:
        value1=subtypes(value)
        list_oneof.append(value1)
    for val in list_oneof:
        for k, v in val.items():
            if k == 'oneOf':
                list_oneof2=[]
                for lor in v:
                    lor1=subtypes(lor)
                    list_oneof2.append(lor1)

                nova_llista=[]
                for item in list_oneof2:
                    for clau, valor in item.items():
                        if 'ontologyTerm' in valor:
                            nou_dict={}
                            nou_dict[clau]={}
                            nou_dict[clau]['id']=""
                            nou_dict[clau]['label']=""
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif '.json' in valor:
                            nou_dict={}
                            nou_dict[clau]=subtypes(valor)
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif 'number' in valor:
                            nou_dict[clau]=0
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif 'string' in valor:
                            nou_dict[clau]=""
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
            else:
                if isinstance(v, dict):
                    new_dict={}
                    new_dict[k]={}
                    for ki, vi in v.items():
                        new_dict[k][ki]={}
                        if 'ontologyTerm' in vi:
                            new_dict[k][ki]["id"]=""
                            new_dict[k][ki]["label"]=""
                            if new_dict not in nova_llista:
                                nova_llista.append(new_dict)
                        elif '.json' in vi:
                            elementvi=subtypes(vi)
                            new_dict[k][ki]=elementvi
                            if new_dict not in nova_llista:
                                nova_llista.append(new_dict)
    listing=[]
    for item in nova_llista:
        new_dict={}
        for k, v in item.items():
            new_dict[k]={}
            if isinstance(v,dict):
                for key, value in v.items():
                    if 'ontologyTerm' in value:
                        new_dict[k][key]={}
                        new_dict[k][key]["id"]=""
                        new_dict[k][key]["label"]=""
                    elif '.json' in value:
                        valornou=subtypes(value)
                        new_dict[k][key]=valornou
                    elif 'number' in value:
                        new_dict[k][key]=0
                    elif 'string' in value:
                        new_dict[k][key]=""
                    elif key == 'type':
                        pass
                    else:
                        new_dict[k][key]=value
            elif k == 'value':
                new_dict[k]=0

        listing.append(new_dict)
    new_listing=[]
    for item in listing:
        typed_dict={}
        for k, v in item.items():
            if k == 'typedQuantities':
                typed_dict[k]={}
                for key, value in v.items():
                    if key == 'quantity':
                        typed_dict[k][key]={}
                        for clau, valor in value.items():
                            if 'ontologyTerm' in valor:
                                typed_dict[k][key][clau]={}
                                typed_dict[k][key][clau]["id"]=""
                                typed_dict[k][key][clau]["label"]=""
                            elif '.json' in valor:
                                valor_nou=subtypes(valor)
                                typed_dict[k][key][clau]=valor_nou
                            elif 'number' in valor:
                                typed_dict[k][key][clau]=0
                            elif 'string' in valor:
                                typed_dict[k][key][clau]=""
                            elif clau == 'type':
                                pass
                            else:
                                typed_dict[k][key][clau]=valor
        
            else:
                new_listing.append(item)
        new_listing.append(typed_dict)
    nuevalista=[]
    for item in new_listing:
        if item != {}:
            nuevalista.append(item)
    llisteta=[]
    for item in nuevalista:
        typed_dict2={}
        for k, v in item.items():
            if k == 'typedQuantities':
                typed_dict2[k]={}
                for key, value in v.items():
                    if key == 'quantity':
                        typed_dict2[k][key]={}
                        if isinstance(value, dict):
                            for clau, valor in value.items():
                                typed_dict2[k][key][clau]={}
                                if isinstance(valor, dict):
                                    for ki, vi in valor.items():
                                        if 'ontologyTerm' in vi:
                                            typed_dict2[k][key][clau][ki]={}
                                            typed_dict2[k][key][clau][ki]["id"]=""
                                            typed_dict2[k][key][clau][ki]["label"]=""
                                        elif '.json' in vi:
                                            valor_nou=subtypes(vi)
                                            typed_dict2[k][key][clau][ki]=valor_nou
                                        elif 'number' in vi:
                                            typed_dict2[k][key][clau][ki]=0
                                        elif 'string' in vi:
                                            typed_dict2[k][key][clau][ki]=""
                                        elif ki == 'type':
                                            pass
                                        else:
                                            typed_dict2[k][key][clau][ki]=vi
                                elif clau == 'value':
                                        typed_dict2[k][key][clau]=0
            else:
                if item not in llisteta:
                    llisteta.append(item)
        llisteta.append(typed_dict2)
    llista_final=[]
    for item in llisteta:
        if item != {}:
            llista_final.append(item)
    return llista_final

def oneofunc(array):
    new_array=[]
    for item in array:
        if 'ontologyTerm' in item:
            new_item={}
            new_item['id']=""
            new_item['label']=""
        elif 'Timestamp' in item:
            new_item=""
        else:
            new_item = subtypes(item)
        new_array.append(new_item)
    new_array2=[]
    for item in new_array:
        dict_2={}
        if isinstance(item, dict):
            for k,v in item.items():
                if 'string' in v:
                    dict_2[k]=""
                elif 'ontologyTerm' in v:
                    dict_2[k]={}
                    dict_2[k]["id"]=""
                    dict_2[k]["label"]=""
                elif '.json' in v:
                    element=subtypes(v)
                    dict_2[k]=element
                elif 'integer' in v:
                    dict_2[k]=0
                elif 'type' in k:
                    pass
                else:
                    dict_2[k]=v
        new_array2.append(dict_2)
    new_array3=[]
    for item in new_array2:
        dict_3={}
        if isinstance(item, dict):
            for k,v in item.items():
                dict_3[k]={}
                if isinstance(v, dict):
                    for key, value in v.items():
                        if 'string' in value:
                            dict_3[k][key]=""
                else:
                    dict_3[k]=v
        new_array3.append(dict_3)
    new_array4=[]
    for item in new_array3:
        if item == {}:
            new_array4.append("")
        else:
            new_array4.append(item)   

    return new_array4    

def overtypes(element):
    overtypes={}
    if isinstance(element, dict):
        for key, value in element.items():
            if isinstance(value, bool):
                overtypes[key]=value
            elif '.json' in value:
                new_value=subtypes(value)
                overtypes[key]=new_value
            elif 'string' in value:
                new_value=""
                overtypes[key]=new_value
            elif 'CURIE' in value:
                new_value=""
                overtypes[key]=new_value
            elif 'boolean' in value:
                new_value=''
                overtypes[key]=new_value
            elif isinstance(value, dict):
                new_value=""
                for k, v in value.items():
                    if k == 'oneOf':
                        if 'complexValue.json' in v:
                            new_value=oneof_function(v)
                        else:
                            new_value=oneofunc(v)
                if new_value != "":
                    overtypes[key]=new_value
                else:
                    overtypes[key]=value
            elif isinstance(value, list):
                overtypes[key]=value   
            elif value=='':
                overtypes[key]=value                
    return overtypes

def ontologyTerm():
    element=subtypes('ontologyTerm.json')
    element=overtypes(element)
    return element

def subtypes(file):
    openfile='ref_schemas/'+file
    age = open(openfile) 
    subdict = {}
    data = json.load(age)
    for key, value in data.items():
        if key == 'properties':
            for k,v in value.items():
                if k == 'required':
                    subdict[k]=v
                else:
                    subdict[k]=""
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        if k1 == 'type':
                            if v1 == 'array':
                                subdict[k]['type']='array'
                            else:
                                subdict[k]=v1
                        elif k1 == '$ref':
                            if 'ontologyTerm' in v1:
                                subdict[k]= 'ontologyTerm.json'
                            elif 'commonDefinitions' in v1:
                                v1_splitted = v1.split('/')
                                for kcd, vcd in commonDefinitions.items():
                                    if kcd == v1_splitted[-1]:
                                        for kcd1, vcd1 in vcd.items():
                                            if 'ontologyTerm' in vcd1:
                                                subdict[k]='ontologyTerm.json'
                                            elif kcd1 == 'type':
                                                subdict[k]={}
                                                subdict[k]=vcd1

                            else:
                                v1_splitted = v1.split('/')
                                subdict[k]=v1_splitted[-1]
                        elif k1 == 'oneOf':
                            subdict[k]={}
                            subdict[k]['oneOf']=[]
                            for valor in v1:
                                for kval, vval in valor.items():
                                    if kval == '$ref':
                                        vval_splitted = vval.split('/')
                                        subdict[k]['oneOf'].append(vval_splitted[-1])
                        elif k1 == 'items':
                            for k2, v2 in v1.items():
                                if k2 == '$ref':
                                    if '.json' in v2:
                                        v2_splitted = v2.split('/')
                                        subdict[k]={}
                                        subdict[k]['items']=v2_splitted[-1]
                                    else:
                                        v2_splitted = v2.split('/')
                                        subdict[k]={}
                                        for keyx, valuex in data.items():
                                            if keyx == 'definitions':
                                                for kx, vx in valuex.items():
                                                    if kx == v2_splitted[-1]:
                                                        for k1x, v1x in vx.items():
                                                            if k1x == 'properties':
                                                                for k2x, v2x in v1x.items():
                                                                    for k3x, v3x in v2x.items():
                                                                        if k3x == '$ref':
                                                                            if 'ontologyTerm' in v3x:
                                                                                subdict[k][k2x]='ontologyTerm.json'
                                                                            else:
                                                                                splitted_v = v3x.split('/')
                                                                                double_split = splitted_v[-1].split('/')
                                                                                subdict[k][k2x]=double_split[-1]
                                                                        elif k3x == 'type':
                                                                            subdict[k][k2x]=v3x
                                                            elif k1x == 'required':
                                                                subdict[k][k1x]=v1x
        elif key == 'type':
            subdict['type']=value
        elif key == 'oneOf':
            subdict['oneOf']=[]
            for valor in value:
                for kval, vval in valor.items():
                    if kval == '$ref':
                        vval_splitted = vval.split('/')
                        subdict['oneOf'].append(vval_splitted[-1])
    return subdict

for key, value in data.items():
    if key == 'definitions':
        definitions_array=value
for key, value in definitions_array.items():
    for k, v in value.items():
        if k == 'properties':
            dict_definitions[key]=v
for key, value in dict_definitions.items():
    for k, v in value.items():
        for k1, v1 in v.items():
            if k1 == '$ref':
                if 'ontologyTerm' in v1:
                    dict_definitions[key][k]=ontologyTerm()
                elif 'definitions' in v1:
                    v1_splitted = v1.split('/')
                    dict_definitions[key][k]=v1_splitted[-1]
            elif k1 == 'type':
                if 'string' in v1:
                    dict_definitions[key][k]=''
                elif 'number' in v1:
                    dict_definitions[key][k]=0
                elif 'object' in v1:
                    dict_definitions[key][k]={}
            elif k1 == 'items':
                for k2, v2 in v1.items():
                    if k2 == '$ref':
                        v2_splitted = v2.split('/')
                        dict_definitions[key][k]=[]
                        dict_definitions[key][k].append(v2_splitted[-1])
                    elif k2 == 'type':
                        if 'string' in v2:
                            dict_definitions[key][k]=[]
                            dict_definitions[key][k].append('')


for key, value in dict_definitions.items():
    for k, v in value.items():
        if isinstance(v, str):
            if v != '':
                for kd, vd in dict_definitions.items():
                    if kd == v:
                        dict_definitions[key][k]=vd
        elif isinstance(v, list):
            if v != ['']:
                if 'ontologyTerm' in v[0]:
                    new_list=[]
                    new_list.append(ontologyTerm())
                    dict_definitions[key][k]=new_list
                else:
                    for kl, vl in dict_definitions.items():
                        if kl == v[0]:
                            new_list=[]
                            new_list.append(vl)
                            dict_definitions[key][k]=new_list


for key, value in data.items():
    if key == 'properties':
        properties_array=value


for key, value in properties_array.items():
    for k, v in value.items():
        if k == '$ref':
            if 'ontologyTerm' in v:
                dict_properties[key]=ontologyTerm()
            elif 'definitions' in v:
                v_splitted = v.split('/')
                dict_properties[key]=v_splitted[-1]
        elif k == 'type':
            if 'string' in v:
                dict_properties[key]=''
            elif 'number' in v:
                dict_properties[key]=0
            elif 'object' in v:
                dict_properties[key]={}
        elif k == 'items':
            for k2, v2 in v.items():
                if k2 == '$ref':
                    v2_splitted = v2.split('/')
                    dict_properties[key]=[]
                    dict_properties[key].append(v2_splitted[-1])
                elif k2 == 'type':
                    if 'string' in v2:
                        dict_properties[key]=[]
                        dict_properties[key].append('')
        elif k == 'oneOf':
            list_elements=[]
            for element in v:
                for ke, ve in element.items():
                    ve_splitted = ve.split('/')
                    list_elements.append(ve_splitted[-1])
            dict_properties[key]={}
            dict_properties[key]['oneOf']=list_elements



for k, v in dict_properties.items():
    if isinstance(v, str):
        if v != '':
            for kd, vd in dict_definitions.items():
                if kd == v:
                    dict_properties[k]=vd
    elif isinstance(v, list):
        if v != ['']:
            if 'ontologyTerm' in v[0]:
                new_list=[]
                new_list.append(ontologyTerm())
                dict_properties[k]=new_list
            elif '.json' in v[0]:
                new_list=[]
                new_list.append(subtypes(v[0]))
                dict_properties[k]=new_list
            else:
                for kl, vl in dict_definitions.items():
                    if kl == v[0]:
                        new_list=[]
                        new_list.append(vl)
                        dict_properties[k]=new_list
    elif isinstance(v, dict):
        new_list=[]
        for k1, v1 in v.items():
            for item in v1:
                if item == 'LegacyVariation':
                    for kl, vl in dict_definitions.items():
                        if kl == item:
                            new_list.append(vl)
                else:
                    vrs_file = open('ref_schemas/vrs.json')
                    data_vrs = json.load(vrs_file)
                    state_=vrs(data_vrs)
                    for items in state_:
                        for itemstate in items:
                            new_list.append(itemstate)
                    
            dict_properties[k]=new_list

#print(dict_properties)

for key, value in dict_properties.items():
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, str):
                if v != '':
                    if v == 'Location':
                        dict_properties[key][k]=location()
                    else:
                        for kd, vd in dict_definitions.items():
                            if kd == v:
                                dict_properties[key][k]=vd
            elif isinstance(v, list):
                if v != ['']:
                    if '.json' in v[0]:
                        new_list=[]
                        new_list.append(subtypes(v[0]))
                        dict_properties[key][k]=new_list
                    else:
                        for kl, vl in dict_definitions.items():
                            if kl == v[0]:
                                new_list=[]
                                new_list.append(vl)
                                dict_properties[key][k]=new_list
    elif isinstance(value, list):
        dict_properties[key]=[]
        for item in value:
            dictitem={}
            for k, v in item.items():
                if isinstance(v, str):
                    if v != '':
                        if v == 'Location':
                            dictitem[k]=location()
                    else:
                        dictitem[k]=v
                else:
                    dictitem[k]=v
            dict_properties[key].append(dictitem)
                


#print(dict_properties)

list_of_definitions_required=[]
first_list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]


for key, value in definitions_array.items():
    for k, v in value.items():
        if k == 'required':
            for item in v:
                all_name = key + '|' + item
                list_of_headers_definitions_required.append(key)
                first_list_of_definitions_required.append(all_name)

for key, value in data.items():
        if key == 'required':
            for item in value:
                list_of_properties_required.append(item)



def generate(dict_properties):
    list_of_excel_items=[]
    for key, value in dict_properties.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for ki, vi in item.items():
                        if isinstance(vi, list):
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
                                                                new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2 + "|" + k3
                                                                if new_item not in list_of_excel_items:
                                                                    list_of_excel_items.append(new_item)            
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                            if new_item not in list_of_excel_items:
                                                                list_of_excel_items.append(new_item)                                        
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k + "|" + k1
                                                    if new_item not in list_of_excel_items:
                                                        list_of_excel_items.append(new_item)
                                        elif isinstance(v, list):
                                            for itemv in v:
                                                if isinstance(itemv, dict):
                                                    for kiv, viv in itemv.items():
                                                        if isinstance(viv,list):
                                                            for vivitem in viv:
                                                                for kivi, vivi in vivitem.items():
                                                                    if isinstance(vivi, list):
                                                                        for vivitem1 in vivi:
                                                                            for kivivi, vivivi in vivitem1.items():
                                                                                if isinstance(vivivi, list):
                                                                                    for vivivitem in vivivi:
                                                                                        for kivitem, vivitem in vivivitem.items():
                                                                                            new_item = ""
                                                                                            new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi + "|" + kivitem
                                                                                            if new_item not in list_of_excel_items:
                                                                                                #print(new_item)
                                                                                                list_of_excel_items.append(new_item)                                                                               
                                                                                else:
                                                                                    new_item = ""
                                                                                    new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi
                                                                                    if new_item not in list_of_excel_items:
                                                                                        list_of_excel_items.append(new_item)
                                                                    else:
                                                                        new_item = ""
                                                                        new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi
                                                                        if new_item not in list_of_excel_items:
                                                                            list_of_excel_items.append(new_item)
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + kiv
                                                            #print(new_item)
                                                            if new_item not in list_of_excel_items:
                                                                list_of_excel_items.append(new_item)
                                        elif ki == 'copies':
                                            new_item = ""
                                            new_item = key + "|" + ki
                                            if new_item not in list_of_excel_items:
                                                list_of_excel_items.append(new_item)
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + k
                                            
                                            if new_item not in list_of_excel_items:
                                                #print(new_item)
                                                list_of_excel_items.append(new_item)
                        elif isinstance(vi, dict):
                            for ki1, vi1 in vi.items():
                                if isinstance(vi1, dict):
                                    for ki2, vi2 in vi1.items():
                                        new_item = ""
                                        new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                        if new_item not in list_of_excel_items:
                                            list_of_excel_items.append(new_item)
                                elif ki1 == 'variation':
                                    new_item = ""
                                    new_item = key + "|" + ki + "|" + ki1
                                    #print(new_item)
                                    if new_item not in list_of_excel_items:
                                        list_of_excel_items.append(new_item)  
                                elif isinstance(vi1, list):
                                    for itemvi1 in vi1:
                                        for kvi, vvi in itemvi1.items():
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1 + "|" + kvi
                                            #print(new_item)
                                            if new_item not in list_of_excel_items:
                                                list_of_excel_items.append(new_item) 
                                else:
                                    new_item = ""
                                    new_item = key + "|" + ki + "|" + ki1
                                    if new_item not in list_of_excel_items:
                                        list_of_excel_items.append(new_item)      
                        else:
                            new_item = ""
                            new_item = key + "|" + ki
                            if new_item not in list_of_excel_items:
                                list_of_excel_items.append(new_item)
                        if ki == 'members':
                            new_item = ""
                            new_item = key + "|" + ki
                            if new_item not in list_of_excel_items:
                                list_of_excel_items.append(new_item)

        elif isinstance(value, dict):
            for kd, vd in value.items():
                if isinstance(vd, list):
                    for itemvd in vd:
                        if isinstance(itemvd, dict):
                            for kd1, vd1 in itemvd.items():
                                if isinstance(vd1, dict):
                                    for kd2, vd2 in vd1.items():
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                        if new_item not in list_of_excel_items:
                                            list_of_excel_items.append(new_item)
                                elif isinstance(vd1, list):
                                    for item in vd1:
                                        for kd2, vd2 in item.items():
                                            if isinstance(vd2, list):
                                                for itemvd2 in vd2:
                                                    for kd3, vd3 in itemvd2.items():
                                                        new_item = ""
                                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                                        if new_item not in list_of_excel_items:
                                                            list_of_excel_items.append(new_item)
                                            else:
                                                new_item = ""
                                                new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                                if new_item not in list_of_excel_items:
                                                    list_of_excel_items.append(new_item)
                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd + "|" + kd1
                                    if new_item not in list_of_excel_items:
                                        list_of_excel_items.append(new_item)
                        else:
                            new_item = ""
                            new_item = key + "|" + kd
                            if new_item not in list_of_excel_items:
                                list_of_excel_items.append(new_item)  
                elif isinstance(vd, dict):
                    for kd1, vd1 in vd.items():
                        if isinstance(vd1, dict):
                            for kd2, vd2 in vd1.items():
                                if isinstance(vd2, dict):
                                    for kd3, vd3 in vd2.items():
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                        if new_item not in list_of_excel_items:
                                            list_of_excel_items.append(new_item)
                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                    if new_item not in list_of_excel_items:
                                        list_of_excel_items.append(new_item)
                        else:

                            new_item = ""
                            new_item = key + "|" + kd + "|" + kd1
                            if new_item not in list_of_excel_items:
                                list_of_excel_items.append(new_item)
                
                else:
                    new_item = ""
                    new_item = key + "|" + kd
                    if new_item not in list_of_excel_items:
                        list_of_excel_items.append(new_item)

        else:
            new_item = ""
            new_item = key
            if new_item not in list_of_excel_items:
                list_of_excel_items.append(new_item)


    for excel_item in list_of_excel_items:
        if '|start|iso8601duration' in excel_item:
            excel_splitted = excel_item.split('|start|iso8601duration')
            if excel_splitted[0] not in list_of_excel_items:
                list_of_excel_items.append(excel_splitted[0])
    
    list_of_excel_items=sorted(list_of_excel_items)

    for defreq in first_list_of_definitions_required:
        defreq_splitted = defreq.split('|')
        #print(defreq)
        #print(defreq_splitted[-1])
        for propreq in list_of_excel_items:
            #print(propreq)
            if propreq.endswith(defreq_splitted[-1]):
                if propreq not in list_of_definitions_required:
                    list_of_definitions_required.append(propreq)
            elif propreq.endswith('|id'):
                if propreq not in list_of_definitions_required:
                    list_of_definitions_required.append(propreq)
    #print(list_of_definitions_required)


    with open('csv/templates/genomicVariations.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_of_excel_items)
        csvfile.close()

    with open("files/headers/genomicVariations.txt", "w") as txt_file:
        for line in list_of_excel_items:
            txt_file.write("".join(line) + "\n")

    with open("files/required/definitions/genomicVariations.txt", "w") as txt_file:
        for line in list_of_definitions_required:
            txt_file.write("".join(line) + "\n")

    with open("files/required/header_definitions/genomicVariations.txt", "w") as txt_file:
        for line in list_of_headers_definitions_required:
            txt_file.write("".join(line) + "\n")

    with open("files/required/properties/genomicVariations.txt", "w") as txt_file:
        for line in list_of_properties_required:
            txt_file.write("".join(line) + "\n")

    with open('files/deref_schemas/genomicVariations.json', 'w') as f:
        json.dump(dict_properties, f)




dict_generado = generate(dict_properties)