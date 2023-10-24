import json 
   
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



for key, value in data.items():
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

        


#print(dict_types)



def subtypes(file):
    age = open(file) 
    subdict = {}
    data = json.load(age)
    file_splitted = file.split('.')
    clau = file_splitted[0] 
    subdict[clau]={}
    for key, value in data.items():
        if key == 'properties':
            for k,v in value.items():
                if k == 'required':
                    subdict[clau][k]=v
                else:
                    subdict[clau][k]=""
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        if k1 == 'type':
                            if v1 == 'array':
                                subdict[clau][k]['type']='array'
                            else:
                                subdict[clau][k]=v1
                        elif k1 == '$ref':
                            if 'ontologyTerm' in v1:
                                subdict[clau][k]= 'ontologyTerm.json'
                            elif 'commonDefinitions' in v1:
                                v1_splitted = v1.split('/')
                                for kcd, vcd in commonDefinitions.items():
                                    if kcd == v_splitted[-1]:
                                        for kcd1, vcd1 in vcd.items():
                                            if 'ontologyTerm' in vcd1:
                                                subdict[clau][k]='ontologyTerm.json'
                                            elif kcd1 == 'type':
                                                subdict[clau][k]={}
                                                subdict[clau][k]['type']=vcd1
                            else:
                                v1_splitted = v1.split('/')
                                subdict[clau][k]=v1_splitted[-1]
                        elif k1 == 'items':
                            for k2, v2 in v1.items():
                                if k2 == '$ref':
                                    print(v2)
                                    v2_splitted = v2.split('/')
                                    subdict[clau][k]={}
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
                                                                            subdict[clau][k][k2x]='ontologyTerm.json'
                                                                        else:
                                                                            splitted_v = v3x.split('/')
                                                                            double_split = splitted_v[-1].split('/')
                                                                            subdict[clau][k][k2x]=double_split[-1]
                                                                            
        elif key == 'type':
            subdict[clau]['type']=value
    



    return subdict

subdict = subtypes('timeElement.json')

print(subdict)





   
# Closing file 
f.close() 