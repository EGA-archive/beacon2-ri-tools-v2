import json
import xlwings as xw
   
# Opening JSON file 
f = open('individuals.json',) 
   
# returns JSON object as  
# a dictionary 
data = json.load(f) 
   
commonDefinitions = open('commondefinitions.json')
commonDefinitions = json.load(commonDefinitions)

commonComponents = open('beaconcommoncomponents.json')
commonComponents = json.load(commonComponents)

dict_types={}


for kprinc, vprinc in data.items():
    if kprinc == 'properties':
        for key, value in vprinc.items():
            dict_types[key]={}
            for k, v in value.items():
                if k == "type":
                    dict_types[key]['type']=v
                elif k == '$ref':
                    dict_types[key]['type']={}
                    if 'commonDefinitions' in v:
                        v_splitted = v.split('/')
                        for kcd, vcd in commonDefinitions.items():
                            if kcd == v_splitted[-1]:
                                for kcd1, vcd1 in vcd.items():
                                    if 'ontologyTerm' in vcd1:
                                        dict_types[key]['type']='ontologyTerm.json'
                                    elif kcd1 == 'type':
                                        dict_types[key]['type']=vcd1
                    elif 'beaconCommonComponents' in v:
                        v_splitted = v.split('/')
                        for kcd, vcd in commonComponents.items():
                            if kcd == v_splitted[-1]:
                                for kcd1, vcd1 in vcd.items():
                                    if 'ontologyTerm' in vcd1:
                                        dict_types[key]['type']='ontologyTerm.json'
                                    elif kcd1 == 'type':
                                        dict_types[key]['type']=vcd1
                elif k == 'items':
                    for kcd, vcd in v.items():
                        if kcd == '$ref':
                            vcd_splitted = vcd.split('/')
                            dict_types[key]['items']=vcd_splitted[-1]
                            vcd_file = open(vcd_splitted[-1])
                            data_vcd = json.load(vcd_file) 
                            for keyv, itemv in data_vcd.items():
                                if keyv == 'properties':
                                    vcd_dict = itemv
                                elif keyv == 'required':
                                    dict_types[key]['required']=itemv
                                    #print(vcd_dict)
                            for key2, item2 in vcd_dict.items():
                                for keyd, itemd in item2.items():
                                    if keyd == "type":
                                        if itemd=='array':
                                            pass
                                        else:
                                            dict_types[key][key2]=itemd
                                    elif keyd == "items":
                                        if isinstance(itemd, dict):
                                            for ki, vi in itemd.items():
                                                if ki =='$ref':
                                                    dict_types[key][key2]={}
                                                    vi_splitted = vi.split('/')
                                                    dict_types[key][key2]['arraytype']=vi_splitted[-1]
                                    elif keyd == '$ref':
                                        if '.json' in itemd:
                                            item_splitted = itemd.split('/')
                                            dict_types[key][key2]=item_splitted[-1]
                                        elif 'commonDefinitions' in itemd:
                                            v_splitted = itemd.split('/')
                                            for kcd, vcd in commonDefinitions.items():
                                                if kcd == v_splitted[-1]:
                                                    for kcd1, vcd1 in vcd.items():
                                                        if 'ontologyTerm' in vcd1:
                                                            dict_types[key][key2]='ontologyTerm.json'
                                                        elif kcd1 == 'type':
                                                            dict_types[key][key2]=vcd1
                                    elif 'oneOf' in keyd:
                                        dict_types[key][key2]=itemd
    elif kprinc == 'required':
        dict_types[kprinc]=vprinc

        




def subtypes(file):
    age = open(file) 
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

subdict = subtypes('pedigree.json')

#print(subdict)

response = {}

for key, value in dict_types.items():
    if key != 'required':
        for k, v in value.items():
            if k == 'type':
                if v == 'string':
                    response[key]=""
                elif v == 'array':
                    response[key]=[]
                elif v == 'object':
                    response[key]={}
                elif v == 'ontologyTerm.json':
                    response[key]={}



for key, value in dict_types.items():
    if key != 'required':
        for k, v in value.items():
            if k != 'required':
                if k == 'items':
                    element = subtypes(v)
                    if isinstance(response[key], list):
                        response[key].append(element)
                    elif isinstance(response[key], dict):
                        response[key][k]={}
                elif k == 'type':
                    if 'ontologyTerm' in v:
                        response[key]={}
                        response[key]['id']=""
                        response[key]['label']=""



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


        


new_response={}

for key, value in response.items():
    if isinstance(value, list):
        new_list=[]
        new_response[key]=[]
        for item in value:
            dicty={}
            for k, v in item.items():
                dicty[k]={}
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        if k1 == 'oneOf':
                            resposta = oneof_function(v1)
                            dicty[k]=resposta
                        else:
                            dicty[k]=v
                else:
                    dicty[k]=v
            if dicty not in new_list:
                new_list.append(dicty)
        for element in new_list:
            new_response[key].append(element)
    else:
        new_response[key]=value


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

dict_final={}
for key, value in new_response.items():
    if isinstance(value, list):
        dict_final[key]=value[0]
    else:
        dict_final[key]= value


dict_defi={}

for key, value in dict_final.items():
    dict_defi[key]={}
    if isinstance(value, dict):
        for k, v in value.items():
            if 'ontologyTerm' in v:
                dict_defi[key][k]={}
                dict_defi[key][k]["id"]=""
                dict_defi[key][k]["label"]=""
            elif '.json' in v:
                element= subtypes(v)
                dict_defi[key][k]=element
            elif 'string' in v:
                dict_defi[key][k]=""
            elif 'boolean' in v:
                dict_defi[key][k]=True
            elif 'integer' in v:
                dict_defi[key][k]=0
            elif 'number' in v:
                dict_defi[key][k]=0
            elif isinstance(v, list):
                dict_defi[key][k]=v
            elif isinstance(v, dict):
                dict_defi[key][k]={}
                for k1, v1 in v.items():
                    if k1 == 'oneOf':
                        vnew=oneofunc(v1)
                        dict_defi[key][k]=vnew
                    elif 'ontologyTerm' in v1:
                        dict_defi[key][k][k1]={}
                        dict_defi[key][k][k1]["id"]=""
                        dict_defi[key][k][k1]["label"]=""
                    elif '.json' in v1:
                        element= subtypes(v1)
                        dict_defi[key][k][k1]=element
                    elif 'string' in v1:
                        dict_defi[key][k][k1]=""
                    elif 'boolean' in v1:
                        dict_defi[key][k][k1]=True
                    elif 'integer' in v1:
                        dict_defi[key][k][k1]=0
                    elif 'number' in v1:
                        dict_defi[key][k][k1]=0
                    elif isinstance(v1, list):
                        dict_defi[key][k][k1]=v1
                    elif isinstance(v1, dict):
                        dict_defi[key][k][k1]=v1


age = subtypes('age.json')
agerange = subtypes('ageRange.json')





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
                new_value=True
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





def dict_overtypes(element):
    superovertypes={}
    for key, value in element.items():
        if isinstance(value, dict):
            superovertypes[key]={}
            for k, v in value.items():
                if 'CURIE' in v:
                    superovertypes[key][k]=''
                elif 'string' in v:
                    superovertypes[key][k]=''
                elif '.json' in v:
                    superovertypes[key][k]=subtypes(v)
                elif 'boolean' in v:
                    superovertypes[key][k]=True
                elif 'oneOf' in k:
                    superovertypes[key][k]=overtypes(v)
                elif k == 'items':
                    list_items=[]
                    list_items.append(v)
                    superovertypes[key]=list_items
        else:
            superovertypes[key]=value
    return superovertypes




def super_overtypes(element):
    superovertypes={}
    for key, value in element.items():
        if isinstance(value, dict):
            superovertypes[key]={}
            for k, v in value.items():
                if isinstance(v, dict):
                    superovertypes[key][k]={}
                    for k1, v1 in v.items():
                        if 'CURIE' in v1:
                            superovertypes[key][k][k1]=""
                        elif 'string' in v1:
                            superovertypes[key][k][k1]=""
                        elif '.json' in v1:
                            superovertypes[key][k]=subtypes(v1)
                        elif 'oneOf' in k1:
                            superovertypes[key][k]=oneofunc(v1)
                        elif 'number' in v1:
                            superovertypes[key][k][k1]=0
                else:
                    superovertypes[key][k]=v
        else:
            superovertypes[key]=value
    return superovertypes




def megaovertypes(element):
    superovertypes={}
    for key, value in element.items():
        if isinstance(value, dict):
            superovertypes[key]={}
            for k, v in value.items():
                if k == 'items':
                    list_items=[]
                    list_items.append(v)
                    superovertypes[key]=list_items
                else:
                    superovertypes[key][k]=v
        else:
            superovertypes[key]=value
    return superovertypes






#print(oneofunc(['age.json', 'ageRange.json', 'gestationalAge.json', 'Timestamp', 'timeInterval.json', 'ontologyTerm.json']))






#print(subtypes('timeInterval.json'))

                            

                        

    
                
                        




                            





        






            
#print(dict_types)



                



def disease():          
    element=subtypes('disease.json')
    element=overtypes(element)
    element=overtypes(element)
    element=dict_overtypes(element)
    return element

def measure():          
    element=subtypes('measurement.json')
    element=overtypes(element)
    element=overtypes(element)
    element=dict_overtypes(element)
    element=super_overtypes(element)
    return element

def ontologyTerm():
    element=subtypes('ontologyTerm.json')
    element=overtypes(element)
    return element

def exposure():
    element=subtypes('exposure.json')
    element=overtypes(element)
    element=dict_overtypes(element)
    return element

def procedure():
    element=subtypes('procedure.json')
    element=overtypes(element)
    element=overtypes(element)
    element=dict_overtypes(element)
    return element

def pedigree():
    element=subtypes('pedigree.json')
    element=overtypes(element)
    element=dict_overtypes(element)
    element=super_overtypes(element)
    return element 

def phenotypicFeature():
    element=subtypes('phenotypicFeature.json')
    element=overtypes(element)
    element=overtypes(element)
    element=dict_overtypes(element)
    element=super_overtypes(element)
    element=megaovertypes(element)
    return element    

def evidence():
    element=subtypes('evidence.json')
    element=overtypes(element)
    element=dict_overtypes(element)
    return element

def treatment():
    element=subtypes('treatment.json')
    element=overtypes(element)
    element=dict_overtypes(element)
    element=super_overtypes(element)
    element=super_overtypes(element)
    element=megaovertypes(element)
    return element
    
#print(treatment())
            
#print(dict_types)

finaldict={}

for key, value in dict_types.items():
    items_dict={}
    if isinstance(value, dict):
        for k, v in value.items():
            if k == 'items':
                if 'disease' in v:
                    items_dict = disease()
                elif 'measure' in v:
                    items_dict = measure()
                elif 'ontologyTerm' in v:
                    items_dict = ontologyTerm()
                elif 'exposure' in v:
                    items_dict = exposure()
                elif 'procedure' in v:
                    items_dict = procedure()
                elif 'pedigree' in v:
                    items_dict = pedigree()
                elif 'phenotypicFeature' in v:
                    items_dict = phenotypicFeature()
                elif 'evidence' in v:
                    items_dict = evidence()
                elif 'treatment' in v:
                    items_dict = treatment()
            elif k == 'type':
                if v == 'array':
                    list_of_items=[]
                    list_of_items.append(items_dict)
                    finaldict[key]=list_of_items
                elif 'ontologyTerm' in v:
                    items_dict=ontologyTerm()
                    finaldict[key]=items_dict
                elif 'object' in v:
                    items_dict={}
                    finaldict[key]=items_dict
                elif 'string' in v:
                    finaldict[key]=''
            

#print(finaldict)

list_of_excel_items=[]
for key, value in finaldict.items():
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
                                                            new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2 + "_" + k3
                                                            list_of_excel_items.append(new_item)            
                                                    else:
                                                        new_item = ""
                                                        new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2
                                                        list_of_excel_items.append(new_item)                                        
                                            else:
                                                new_item = ""
                                                new_item = key + "_" + ki + "_" + k + "_" + k1
                                                list_of_excel_items.append(new_item)
                                    else:
                                        new_item = ""
                                        new_item = key + "_" + ki + "_" + k
                                        list_of_excel_items.append(new_item)
                    elif isinstance(vi, dict):
                        for ki1, vi1 in vi.items():
                            if isinstance(vi1, dict):
                                for ki2, vi2 in vi1.items():
                                    new_item = ""
                                    new_item = key + "_" + ki + "_" + ki1 + "_" + ki2
                                    list_of_excel_items.append(new_item)     
                            else:
                                new_item = ""
                                new_item = key + "_" + ki + "_" + ki1
                                list_of_excel_items.append(new_item)      
                    else:
                        new_item = ""
                        new_item = key + "_" + ki
                        list_of_excel_items.append(new_item) 
    elif isinstance(value, dict):
        for kd, vd in value.items():
            new_item = ""
            new_item = key + "_" + kd
            list_of_excel_items.append(new_item)
    else:
        new_item = ""
        new_item = key
        list_of_excel_items.append(new_item)

#print(list_of_excel_items) 

wb = xw.Book('individuals.xlsx')

sheet = wb.sheets['Sheet1']

list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                'CA', 'CC', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                'DA', 'DD', 'DD', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                'EA', 'EE', 'EE', 'EE', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
]


i=0
dict_of_properties={}
for element in list_of_excel_items:
    property = list_columns[i]+str(1)
    property_value = sheet[property].value
    number_sheet = list_columns[i]+str(2)
    valor = sheet[number_sheet].value
    if valor:
        dict_of_properties[property_value]=valor
    i+=1


definitivedict={}
for key, value in finaldict.items():
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
                                if subitem_dict not in vi_list:
                                    vi_list.append(subitem_dict)
                        item_dict[ki]=vi_list
                    elif isinstance(vi, dict):
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
                                    item_dict[ki]=vi_dict    
                            else:
                                new_item = ""
                                new_item = key + "_" + ki + "_" + ki1
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        vi_dict={}
                                        vi_dict[ki1]=propv 
                                item_dict[ki]=vi_dict      
                    else:
                        new_item = ""
                        new_item = key + "_" + ki
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                item_dict[ki]=propv
                    if item_dict not in value_list:
                        value_list.append(item_dict)
                definitivedict[key]=value_list       
    elif isinstance(value, dict):
        value_dict={}
        for kd, vd in value.items():
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

print(definitivedict)
   
# Closing file 
f.close() 