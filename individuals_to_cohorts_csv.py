import json
from tqdm import tqdm
import conf.conf as conf
import csv
import sys
from validators.cohorts import Cohorts
import hashlib

with open("files/headers/individuals.txt", "r") as txt_file:
    list_of_headers=txt_file.read().splitlines() 
with open('files/deref_schemas/individuals.json') as json_file:
    dict_properties = json.load(json_file)

csv_filename = "csv/examples/CINECA_synthetic_cohort_EUROPE_UK1/individuals.csv"

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def check(name, list_of_filled_items):
    measures_list_1 = ['measures|measurementValue|referenceRange|high', 'measures|measurementValue|referenceRange|low', 'measures|measurementValue|referenceRange|unit|id', 'measures|measurementValue|referenceRange|unit|label']
    measures_list_2 = ['measures|measurementValue|unit|id', 'measures|measurementValue|unit|label', 'measures|measurementValue|value']
    measures_list_3 = ['measures|measurementValue|typedQuantities|quantity|referenceRange|high', 'measures|measurementValue|typedQuantities|quantity|referenceRange|low', 'measures|measurementValue|typedQuantities|quantity|referenceRange|unit', 'measures|measurementValue|typedQuantities|quantity|unit|id', 'measures|measurementValue|typedQuantities|quantity|unit|label', 'measures|measurementValue|typedQuantities|quantity|value']
    observation_list_1 = ['measures|observationMoment']
    observation_list_2 = ['measures|observationMoment|days', 'measures|observationMoment|weeks']
    observation_list_3 = ['measures|observationMoment|end', 'measures|observationMoment|start']
    observation_list_4 = ['measures|observationMoment|end|iso8601duration', 'measures|observationMoment|start|iso8601duration']
    observation_list_5 = ['measures|observationMoment|iso8601duration']
    observation_list_6 = ['measures|observationMoment|id', 'measures|observationMoment|label']
    ageOfOnset_list_1 = ['diseases|ageOfOnset']
    ageOfOnset_list_2 = ['diseases|ageOfOnset|days', 'diseases|ageOfOnset|weeks']
    ageOfOnset_list_3 = ['diseases|ageOfOnset|end', 'diseases|ageOfOnset|start']
    ageOfOnset_list_4 = ['diseases|ageOfOnset|end|iso8601duration', 'diseases|ageOfOnset|start|iso8601duration']
    ageOfOnset_list_5 = ['diseases|ageOfOnset|iso8601duration']
    ageOfOnset_list_6 = ['diseases|ageOfOnset|id', 'diseases|ageOfOnset|label']
    onset_list_1 = ['phenotypicFeatures|onset']
    onset_list_2 = ['phenotypicFeatures|onset|days', 'phenotypicFeatures|onset|weeks']
    onset_list_3 = ['phenotypicFeatures|onset|end', 'phenotypicFeatures|onset|start']
    onset_list_4 = ['phenotypicFeatures|onset|end|iso8601duration', 'phenotypicFeatures|onset|start|iso8601duration']
    onset_list_5 = ['phenotypicFeatures|onset|iso8601duration']
    onset_list_6 = ['phenotypicFeatures|onset|id', 'phenotypicFeatures|onset|label']
    measure_check=0

    list_of_checks=[]
    i=0
    if name == 'measures':
        for measure in list_of_filled_items:
            if 'measurementValue' in measure:
                if measure in measures_list_1:
                    measure_check+=1
                    measures_list_1=[]
                elif measure in measures_list_2:
                    measure_check+=1
                    measures_list_2=[]
                elif measure in measures_list_3:
                    measure_check+=1
                    measures_list_3=[]
        if measure_check > 1:
            raise Exception(('please, choose only one {} format').format('measurementValue'))
    elif name == 'observations':
        for measure in list_of_filled_items:
            if 'observationMoment' in measure:
                if measure in observation_list_1:
                    measure_check+=1
                    observation_list_1=[]
                elif measure in observation_list_2:
                    measure_check+=1
                    observation_list_2=[]
                elif measure in observation_list_3:
                    measure_check+=1
                    observation_list_3=[]
                elif measure in observation_list_4:
                    measure_check+=1
                    observation_list_4=[]
                elif measure in observation_list_5:
                    measure_check+=1
                    observation_list_5=[]
                elif measure in observation_list_6:
                    measure_check+=1
                    observation_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('observationMoment'))
    elif name == 'procedures':
        for measure in list_of_filled_items:
            if 'ageAtProcedure' in measure:
                if measure in ageAtProcedure_list_1:
                    measure_check+=1
                    ageAtProcedure_list_1=[]
                elif measure in ageAtProcedure_list_2:
                    measure_check+=1
                    ageAtProcedure_list_2=[]
                elif measure in ageAtProcedure_list_3:
                    measure_check+=1
                    ageAtProcedure_list_3=[]
                elif measure in ageAtProcedure_list_4:
                    measure_check+=1
                    ageAtProcedure_list_4=[]
                elif measure in ageAtProcedure_list_5:
                    measure_check+=1
                    ageAtProcedure_list_5=[]
                elif measure in ageAtProcedure_list_6:
                    measure_check+=1
                    ageAtProcedure_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('ageAtProcedure'))
    elif name == 'diseases':
        for measure in list_of_filled_items:
            if 'ageOfOnset' in measure:
                if measure in ageOfOnset_list_1:
                    measure_check+=1
                    ageOfOnset_list_1=[]
                elif measure in ageOfOnset_list_2:
                    measure_check+=1
                    ageOfOnset_list_2=[]
                elif measure in ageOfOnset_list_3:
                    measure_check+=1
                    ageOfOnset_list_3=[]
                elif measure in ageOfOnset_list_4:
                    measure_check+=1
                    ageOfOnset_list_4=[]
                elif measure in ageOfOnset_list_5:
                    measure_check+=1
                    ageOfOnset_list_5=[]
                elif measure in ageOfOnset_list_6:
                    measure_check+=1
                    ageOfOnset_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('ageOfOnset'))
    elif name == 'phenotypic':
        for measure in list_of_filled_items:
            if 'onset' in measure:
                if measure in onset_list_1:
                    measure_check+=1
                    onset_list_1=[]
                elif measure in onset_list_2:
                    measure_check+=1
                    onset_list_2=[]
                elif measure in onset_list_3:
                    measure_check+=1
                    onset_list_3=[]
                elif measure in onset_list_4:
                    measure_check+=1
                    onset_list_4=[]
                elif measure in onset_list_5:
                    measure_check+=1
                    onset_list_5=[]
                elif measure in onset_list_6:
                    measure_check+=1
                    onset_list_6=[]
        if measure_check>1:
                raise Exception(('please, choose only one {} format').format('onset'))

def commas(prova):
    length_iter=0
    array_of_newdicts=[]
    for key, value in prova.items():
        if isinstance(value, str):
            valuesplitted = value.split('|')
            length_iter=len(valuesplitted)
        elif isinstance(value, dict):
            for kval, vval in value.items():
                if isinstance(vval, str):
                    valsplitted = vval.split('|')
                    length_iter=len(valsplitted)
    if length_iter > 0:
        i=0
        while i < length_iter:
            newdict={}
            for key, value in prova.items():
                if isinstance(value, str):
                    valuesplitted = value.split('|')
                    if valuesplitted[i]!='' or valuesplitted[i]!={}:
                        newdict[key]=valuesplitted[i]
                elif isinstance(value, int):
                    valuesplitted = value.split('|')
                    if valuesplitted[i]!='' or valuesplitted[i]!={}:
                        newdict[key]=valuesplitted[i]
                elif isinstance(value, dict):
                    newdict[key]={}
                    for k, v in value.items():
                        if isinstance(v, str):
                            vsplitted = v.split('|')
                            try:
                                if vsplitted[i]!='' or vsplitted[i]!={}:
                                    newdict[key][k]=float(vsplitted[i])
                            except Exception:
                                #print(vsplitted)
                                #print(i)
                                if vsplitted[i]!='' or vsplitted[i]!={}:
                                    newdict[key][k]=vsplitted[i]
                        elif isinstance(v, int):
                            newdict[key][k]=v
                        elif isinstance(v, dict):
                            newdict[key][k]={}
                            for k1, v1 in v.items():
                                if isinstance(v1, str):
                                    v1splitted = v1.split('|')
                                    try:
                                        if v1splitted[i]!='' or v1splitted[i]!={} and len(v1splitted[i])!=0:
                                            newdict[key][k][k1]=v1splitted[i]
                                    except Exception:
                                        pass

                    if newdict[key][k]=={} or newdict[key][k]=="":
                        del newdict[key]
            array_of_newdicts.append(newdict)
            i+=1
    else:
        array_of_newdicts.append(prova)
    return(array_of_newdicts)

def generate(dict_properties, list_of_headers):
    #csv_filename = conf.csv_filename
    with open(csv_filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        num_rows = sum(1 for row in reader)
    
    total_dict =[]

    k=0
    pbar = tqdm(total = num_rows)
    with open(csv_filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        i=1
        definitivedict={}
        definitivedict["id"]='cohortId'
        definitivedict["name"]='cohortName'
        definitivedict["cohortType"]='user-defined'
        definitivedict["collectionEvents"]=[]
        event={}
        event["eventSize"]=num_rows
        for line in reader:
            
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                property_value=property_value.replace('\ufeff', '')
                if property_value not in list_of_headers:
                    raise Exception(('the header {} is not allowed. Please, take a look at csv templates to check the headers allowed.').format(property_value))


                if '|' in vline:
                    valors = vline.split('|')
                else:
                    valors = [vline]

                if i > 0:
                    
                    if vline != '':


                        list_of_filled_items.append(property_value)

                    if valors and vline != '':
                        if 'age' in kline.lower():
                            print(valors)
                            try:
                                event["eventAgeRange"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventAgeRange"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventAgeRange"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventAgeRange"]={}
                                event["eventAgeRange"]["availability"]=True
                                event["eventAgeRange"]["availabilityCount"]=1
                                event["eventAgeRange"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventAgeRange"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventAgeRange"]["distribution"][str(valor)]=1
                        elif kline == 'diseases|diseaseCode|id':
                            try:
                                event["eventDiseases"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventDiseases"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventDiseases"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventDiseases"]={}
                                event["eventDiseases"]["availability"]=True
                                event["eventDiseases"]["availabilityCount"]=1
                                event["eventDiseases"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventDiseases"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventDiseases"]["distribution"][str(valor)]=1
                        elif kline == 'ethnicity|id':
                            try:
                                event["eventEthnicities"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventEthnicities"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventEthnicities"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventEthnicities"]={}
                                event["eventEthnicities"]["availability"]=True
                                event["eventEthnicities"]["availabilityCount"]=1
                                event["eventEthnicities"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventEthnicities"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventEthnicities"]["distribution"][str(valor)]=1
                        elif kline == 'sex|id':
                            try:
                                event["eventGenders"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventGenders"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventGenders"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventGenders"]={}
                                event["eventGenders"]["availability"]=True
                                event["eventGenders"]["availabilityCount"]=1
                                event["eventGenders"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventGenders"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventGenders"]["distribution"][str(valor)]=1
                        elif kline == 'geographicOrigin|id':
                            try:
                                event["eventLocations"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventLocations"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventLocations"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventLocations"]={}
                                event["eventLocations"]["availability"]=True
                                event["eventLocations"]["availabilityCount"]=1
                                event["eventLocations"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventLocations"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventLocations"]["distribution"][str(valor)]=1
                        elif kline == 'phenotypicFeatures|featureType|id':
                            try:
                                event["eventPhenotypes"]["availabilityCount"]+=1
                                for valor in valors:
                                    try:
                                        event["eventPhenotypes"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventPhenotypes"]["distribution"][str(valor)]=1
                            except Exception:
                                event["eventPhenotypes"]={}
                                event["eventPhenotypes"]["availability"]=True
                                event["eventPhenotypes"]["availabilityCount"]=1
                                event["eventPhenotypes"]["distribution"]={}
                                for valor in valors:
                                    try:
                                        event["eventPhenotypes"]["distribution"][str(valor)]+=1
                                    except Exception:
                                        event["eventPhenotypes"]["distribution"][str(valor)]=1




            


            
            pbar.update(1)
            if i > num_rows:
                break
            i+=1
    definitivedict["collectionEvents"].append(event)
    Cohorts(**definitivedict)
    definitivedict["datasetId"]=conf.datasetId
    definitivedict["_id"]=get_hash(conf.datasetId+definitivedict["id"])
    total_dict.append(definitivedict)
    pbar.close()
    return total_dict, i




dict_generado, total_i=generate(dict_properties, list_of_headers)


output = conf.output_docs_folder + 'cohorts.json'

if total_i-1 > 0:

    print('Successfully transformed {} individual registries into a cohort file in {}'.format(total_i-1, output))

else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)

