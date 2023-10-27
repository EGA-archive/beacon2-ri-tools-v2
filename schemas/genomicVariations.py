import json
import xlwings as xw
from individuals import subtypes, dict_overtypes, overtypes, super_overtypes, megaovertypes, ontologyTerm, measure, exposure, treatment, disease, oneof_function, oneofunc, pedigree, phenotypicFeature, procedure, evidence

file_to_open='genomicVariations.json'
# Opening JSON file 
f = open(file_to_open,) 
   
# returns JSON object as  
# a dictionary 
data = json.load(f) 
   
commonDefinitions = open('commondefinitions.json')
commonDefinitions = json.load(commonDefinitions)
commonComponents = open('beaconcommoncomponents.json')
commonComponents = json.load(commonComponents)

dict_definitions={}
dict_properties={}

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
                print(v)
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
                for kl, vl in dict_definitions.items():
                    if kl == item:
                        new_list.append(vl)
            dict_properties[k]=new_list[0]

for key, value in dict_properties.items():
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, str):
                if v != '':
                    if v == 'Location':
                        dict_properties[key][k]=''
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


print(dict_properties)




