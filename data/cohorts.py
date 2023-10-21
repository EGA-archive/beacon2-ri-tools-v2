import xlwings as xw
import json
import ast
import gzip
 
ws = xw.Book("Beacon-v2-Models_CINECA_UK1.xlsx").sheets['cohorts']

cohorts = {}
cohorts['collectionEvents'] = []
cohorts['cohortDesign'] = {}
cohorts['inclustionCriteria'] = {}
cohorts['inclustionCriteria']['ageRange'] = {}
cohorts['inclustionCriteria']['ageRange']['end'] = {}
cohorts['inclustionCriteria']['ageRange']['start'] = {}
cohorts['ids']={}
data={}
data1={}
total_list=[]

n=2

while n < 3:
    range = str(n)
    first_column = 'A'
    last_column = 'BA'
    cohorts['cohortDataTypes'] = []
    cohorts['collectionEvents'] = []
    data['eventDiseases']={}
    data['eventLocations']={}
    data['eventGenders']={}
    data['eventEthnicities']={}
    cohorts['genders'] = []
    cohorts['locations'] = []

    

    range_v1= first_column + range + ':' + last_column + range

    val1 = ws.range(range_v1).value

    i=1

    for v1 in val1:
        
        if i ==3:
            if v1 is not None:
                cohorts['cohortDesign']['id']=v1
        elif i == 4:
            if v1 is not None:
                cohorts['cohortDesign']['label']=v1
        elif i == 5:
            if v1 is not None:
                cohorts['cohortSize']=v1
        elif i == 6:
            if v1 is not None:
                cohorts['cohortType']=v1
        elif i == 16:
            if v1 is not None:
                data['eventDiseases']['availability']=v1
        elif i == 17:
            if v1 is not None:
                data['eventDiseases']['availabilityCount']=v1
        elif i == 18:
            if v1 is not None:
                print(type(v1))
                print(v1)
                v1 = ast.literal_eval(v1)
                for value in v1:
                    data['eventDiseases']['distribution']=value
        elif i == 19:
            if v1 is not None:
                data['eventEthnicities']['availability']=v1
        elif i == 20:
            if v1 is not None:
                data['eventEthnicities']['availabilityCount']=v1
        elif i == 21:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                for value in v1:
                    data['eventEthnicities']['distribution']=value
        elif i == 22:
            if v1 is not None:
                data['eventGenders']['availability']=v1
        elif i == 23:
            if v1 is not None:
                data['eventGenders']['availabilityCount']=v1
        elif i == 24:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                for value in v1:
                    data['eventGenders']['distribution']=value
        elif i == 25:
            if v1 is not None:
                data['eventLocations']['availability']=v1
        elif i == 26:
            if v1 is not None:
                data['eventLocations']['availabilityCount']=v1
        elif i == 27:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                for value in v1:
                    data['eventLocations']['distribution']=value
            cohorts['collectionEvents'].append(data)
        elif i == 42:
            if v1 is not None:
                cohorts['id']=v1
        elif i == 43:
            if v1 is not None:
                cohorts['inclustionCriteria']['ageRange']['end']['iso8601duration']=v1
        elif i == 44:
            if v1 is not None:
                cohorts['inclustionCriteria']['ageRange']['start']['iso8601duration']=v1
        elif i == 47:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                for value in v1:
                    cohorts['genders'].append(value)
        elif i == 48:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                for value in v1:
                    cohorts['locations'].append(value)
        elif i == 50:
            if v1 is not None:
                cohorts['name']=v1
        elif i == 51:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                cohorts['ids']['individualIds']=v1
        elif i == 53:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                cohorts['ids']['biosampleIds']=v1
        i+=1

    total_list.append(cohorts)

    n+=1

save_file = open("cohorts.json", "w")  
json.dump(total_list, save_file, indent = 0)  
save_file.close()  

'''
with open('cohorts.json', 'w', encoding='utf-8') as f:
    json.dump(total_list, f, ensure_ascii=False, indent=None, separators=(',', ':'))
'''
