import json

vrs = 'ref_schemas/vrs'
file_vrs= vrs + '.json'
new_vrs = open(file_vrs,) 
datavrs = json.load(new_vrs)



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
    list_of_states=[]
    for key,value in new_dict9.items():
        list_of_states.append(value)
    return list_of_states


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
            elif k == 'location':
                new_dict41[key][k]='location'
            else:
                new_dict41[key][k]=v
    #print(new_dict41)
    new_dict42={}
    for key, value in new_dict41.items():
        new_dict42[key]={}
        for k, v in value.items():
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
                                            dictvi[ki]= True
                                        elif vi1 == 'number':
                                            dictvi[ki]= 0
                                        elif vi1 == 'integer':
                                            dictvi[ki]= 0

                        new_dict42[key][k].append(dictvi) 
                              
            elif k == 'location':
                new_dict42[key][k]='location'
            else:
                new_dict42[key][k]=v
    
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
    return list_of_states


state(datavrs)