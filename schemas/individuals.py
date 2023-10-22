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
    dict_types[key]=""
    for k, v in value.items():
        if k == "type":
            dict_types[key]=v
        elif k == '$ref':
            dict_types[key]={}
            if 'commonDefinitions' in v:
                v_splitted = v.split('/')
                for kcd, vcd in commonDefinitions.items():
                    if kcd == v_splitted[-1]:
                        for kcd1, vcd1 in vcd.items():
                            if 'ontologyTerm' in vcd1:
                                dict_types[key]='ontologyTerm'
                            elif kcd1 == 'type':
                                dict_types[key]=vcd1
            elif 'beaconCommonComponents' in v:
                v_splitted = v.split('/')
                for kcd, vcd in commonComponents.items():
                    if kcd == v_splitted[-1]:
                        for kcd1, vcd1 in vcd.items():
                            if 'ontologyTerm' in vcd1:
                                dict_types[key]='ontologyTerm'
                            elif kcd1 == 'type':
                                dict_types[key]=vcd1
        


print(dict_types)


   
# Closing file 
f.close() 