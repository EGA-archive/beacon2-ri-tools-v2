import json
import xlwings as xw

xls_Book = '/Users/oriol/Desktop/ri-tools/beacon2-ri-tools/CINECA_synthetic_cohort_EUROPE_UK1/Beacon-v2-Models_CINECA_UK1.xlsx'

wb = xw.Book(xls_Book)

sheet = wb.sheets['individuals']

list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                'CA', 'CC', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                'DA', 'DD', 'DD', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                'EA', 'EE', 'EE', 'EE', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
]

num_rows=2506

j=2

while j < 2506:
    property = list_columns[33]+str(1)
    property_value = sheet[property].value

    value_sheet = list_columns[33]+str(j)
    valor = sheet[value_sheet].value

    valorjson = json.loads(valor)
    newdict={}
    list_values=[]
    list_unitid=[]
    list_unitlabel=[]
    for item in valorjson:
        for key, value in item.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, dict):
                        for k1, v1 in v.items():
                            if k1 == 'id':
                                list_unitid.append(v1)
                            else:
                                list_unitlabel.append(v1)
                    else:
                        list_values.append(v)
    valuestring=''
    valueid=''
    valuelabel=''
    for item in list_values:
        if valuestring == '':
            valuestring = str(item)
        else:
            valuestring = valuestring + ',' + str(item)
    for item in list_unitid:
        if valueid == '':
            valueid = str(item)
        else:
            valueid = valueid + ',' + str(item)
    for item in list_unitlabel:
        if valuelabel == '':
            valuelabel = str(item)
        else:
            valuelabel = valuelabel + ',' + str(item)
    

    val_sheet = list_columns[6]+str(j)
    valx_sheet = sheet[val_sheet]
    id_sheet = list_columns[7]+str(j)
    idx_sheet = sheet[id_sheet]
    label_sheet = list_columns[8]+str(j)
    labelx_sheet = sheet[label_sheet]
    valx_sheet.value = valuestring
    idx_sheet.value = valueid
    labelx_sheet.value = valuelabel

    
        



    j+=1
    print(j)

