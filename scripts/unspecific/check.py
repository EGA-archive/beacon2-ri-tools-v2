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





