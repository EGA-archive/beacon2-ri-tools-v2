import json

vrs_file = open('ref_schemas/vrs.json')
data_vrs = json.load(vrs_file)

list_subject=[{'$ref': '#/definitions/CURIE'}, {'$ref': '#/definitions/ChromosomeLocation'}, {'$ref': '#/definitions/Gene'}, {'$ref': '#/definitions/SequenceLocation'}]

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




                        



subject(list_subject)

