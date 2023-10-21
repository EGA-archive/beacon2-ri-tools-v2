import xlwings as xw
import json
import ast
import gzip
 
ws = xw.Book("Beacon-v2-Models_CINECA_UK1.xlsx").sheets['individuals']

individuals = {}
individuals['measures'] = []
individuals['interventionsOrProcedures']=[]
individuals['ethnicity'] = {}
individuals['geographicOrigin'] = {}
individuals['info'] = {}
individuals['sex'] = {}



data1={}
data1['measurementValue']={}
data1['assayCode']={}
data2={}
data2['measurementValue']={}
data2['assayCode']={}
data3={}
data3['measurementValue']={}
data3['assayCode']={}
datad={}
datad['diseaseCode']={}
datap={}
datap['procedureCode']={}

total_list=[]

'''
list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                'CA', 'CB', 'CC', 'CD']

i=0

for column in list_columns:
'''
n=2

while n < 2506:
    range = str(n)
    first_column = 'A'
    last_column = 'CD'
    individuals['measures'] = []
    individuals['interventionsOrProcedures']=[]
    range_v1= first_column + range + ':' + last_column + range

    val1 = ws.range(range_v1).value

    i=0

    for v1 in val1:
        
        if i == 0:
            if v1 is not None:
                individuals['diseases']['ageOfOnset']=v1
        elif i == 1:
            if v1 is not None:
                individuals['diseases'] = []
                datad['diseaseCode']['id']=v1
        elif i == 2:
            if v1 is not None:
                datad['diseaseCode']['label']=v1
                individuals['diseases'].append(datad)
        elif i == 9:
            if v1 is not None:
                individuals['ethnicity']['id']=v1
        elif i == 10:
            if v1 is not None:
                individuals['ethnicity']['label']=v1
        elif i == 19:
            if v1 is not None:
                individuals['geographicOrigin']['id']=v1
        elif i == 20:
            if v1 is not None:
                individuals['geographicOrigin']['label']=v1
        elif i == 21:
            if v1 is not None:
                individuals['id']=v1
        elif i == 22:
            if v1 is not None:
                individuals['info']['eid']=v1
        elif i == 27:
            if v1 is not None:
                datap['procedureCode']['id']=v1
        elif i == 28:
            if v1 is not None:
                datap['procedureCode']['label']=v1
            individuals['interventionsOrProcedures'].append(datap)
        elif i == 30:
            if v1 is not None:
                v1_splitted = v1.split(',')
                data1['assayCode']['id']=v1_splitted[0]
                data2['assayCode']['id']=v1_splitted[1]
                data3['assayCode']['id']=v1_splitted[2]
        elif i == 31:
            if v1 is not None:
                v1_splitted = v1.split(',')
                data1['assayCode']['label']=v1_splitted[0]
                data2['assayCode']['label']=v1_splitted[1]
                data3['assayCode']['label']=v1_splitted[2]
        elif i == 32:
            if v1 is not None:
                v1_splitted = v1.split(',')
                data1['date']=v1_splitted[0]
                data2['date']=v1_splitted[1]
                data3['date']=v1_splitted[2]
        elif i == 33:
            if v1 is not None:
                v1 = ast.literal_eval(v1)
                j=0
                for v11 in v1:
                    new_list = []
                    for k, v in v11.items():
                        new_list.append(v)
                    if j == 0:
                        data1['measurementValue'] = new_list[0]
                    if j == 1:
                        data2['measurementValue'] = new_list[0]
                    if j == 2:
                        data3['measurementValue'] = new_list[0]
                    j+=1
            individuals['measures'].append(data1)
            individuals['measures'].append(data2)
            individuals['measures'].append(data3)
        elif i == 68:
            if v1 is not None:
                individuals['sex']['id']=v1
        elif i == 69:
            if v1 is not None:
                individuals['sex']['label']=v1
        i+=1

    total_list.append(individuals)

    n+=1

save_file = open("individuals.json", "w")  
json.dump(total_list, save_file, indent = 0)  
save_file.close()  

'''
with open('individuals.json', 'w', encoding='utf-8') as f:
    json.dump(total_list, f, ensure_ascii=False, indent=None, separators=(',', ':'))
'''
