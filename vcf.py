import vcfpy
import warnings
import re
import openpyxl
from scripts.datasheet.conf import conf
from tqdm import tqdm
import glob
import os
import pandas as pd 


num_variants_registries = conf.num_variants_registries

def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = custom_formatwarning

new_dict_to_xls={}
for vcf_filename in glob.glob("files/vcf/files_to_read/*.vcf.gz"):
    print(vcf_filename)
    vcf = vcfpy.Reader.from_path(vcf_filename)
    i=0
    header_list = ['#CHROM', 'POS' , 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + vcf.header.samples.names

    pbar = tqdm(total = num_variants_registries)
    for v in vcf:
        warning = False
        
        dict_to_xls={}
        try:
            for value in v.ALT:
                ALT = str(value.value)
                TYPE = str(value.type)
                dict_to_xls['variation|variantType']=TYPE
        except Exception as e:
            for value in v.ALT:
                ALT = str(value.value)
                
        line = [v.CHROM, v.POS, v.ID, v.REF, ALT, v.QUAL, v.FILTER, v.INFO, v.FORMAT]
        line += [alt.value for alt in v.ALT]
        line += [call.data.get('GT') or './.' for call in v.calls]
        if TYPE == 'SYMBOLIC':
            warnings.warn('variantType is SV. This type of variant is not supported. The VCF entry with ID: {} will not be converted'.format(line[2]), Warning)
            warning = True
            continue
        if line[3] != '':
            dict_to_xls['variation|alternateBases'] = line[3]
        else:
            warnings.warn('alternateBases NOT FOUND. The VCF entry with ID: {} will not be converted.'.format(line[2]), Warning)
            warning = True
            continue
        dict_to_xls['variation|referenceBases'] = line[4]
        for k,v in line[7].items():
            if k == 'VT':
                if v[0] == 'SV':
                    warnings.warn('variantType is SV. This type of variant is not supported. The VCF entry with ID: {} will not be converted'.format(line[2]), Warning)
                    continue
                else:
                    dict_to_xls['variation|variantType'] = v[0]

            elif k == 'ANN':
                line7splitted = v[0].split("|")
                dict_to_xls['molecularAttributes|molecularEffects|label'] = line7splitted[1]
                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000174"
                dict_to_xls['molecularAttributes|aminoacidChanges'] = "."
                dict_to_xls['molecularAttributes|geneIds'] = line7splitted[3]
        try:
            dict_to_xls['variation|variantType']
        except Exception:
            warnings.warn('VariantType NOT FOUND. The VCF entry with ID: {} will not be converted.'.format(line[2]), Warning)
            warning = True
            i-=1
            continue
        
        dict_to_xls['variantInternalId'] = 'chr' + str(line[0]) + '_' + str(line[1]) + '_' + str(line[3]) + '_' + str(line[4])
        zigosity={}
        zigosity['0/1']='GENO:GENO_0000458'
        zigosity['1/0']='GENO:GENO_0000458'
        zigosity['1/1']='GENO:GENO_0000136'
        j=0
        dict_to_xls['caseLevelData|zygosity|id'] =''
        dict_to_xls['caseLevelData|zygosity|label']=''
        for zygo in line[9:-1]:
            num = 9 + j
            if dict_to_xls['caseLevelData|zygosity|id'] == '':
                if zygo == '1/0' or zygo == '0/1' or zygo== '1/1':
                    dict_to_xls['caseLevelData|zygosity|label'] = zygo
                    dict_to_xls['caseLevelData|zygosity|id'] = zigosity[zygo]
                    dict_to_xls['caseLevelData|biosampleId'] = header_list[num]
            else:
                if zygo == '1/0' or zygo == '0/1' or zygo== '1/1':
                    dict_to_xls['caseLevelData|zygosity|label'] = dict_to_xls['caseLevelData|zygosity|label'] + '|' + zygo
                    dict_to_xls['caseLevelData|zygosity|id'] = dict_to_xls['caseLevelData|zygosity|id'] + '|' + zigosity[zygo]
                    dict_to_xls['caseLevelData|biosampleId'] = dict_to_xls['caseLevelData|biosampleId'] + '|' + header_list[num]
            j+=1
        dict_to_xls['identifiers|genomicHGVSId'] = str(line[0]) + ':' + 'g.' + str(line[1]) + line[4] + '>' + line[3]
        ''' Systemic Variation
        if conf.variation_model == 'SystemicVariation':
            if conf.variation_submodel == 'CopyNumberCount':
                if conf.subject_model == 'ChromosomeLocation':
                    dict_to_xls['variation|subject|type']="ChromosomeLocation"
        '''

        dict_to_xls['variation|location|interval|start|value'] = int(line[1]) -1
        dict_to_xls['variation|location|interval|start|type']="Number"
        dict_to_xls['variation|location|interval|end|value'] = int(line[1])
        dict_to_xls['variation|location|interval|end|type']="Number"

        dict_to_xls['variation|location|interval|start|value'] = int(line[1]) -1
        dict_to_xls['variation|location|interval|start|type']="Number"
        dict_to_xls['variation|location|interval|end|value'] = int(line[1])
        dict_to_xls['variation|location|interval|end|type']="Number"
        dict_to_xls['variation|location|interval|type']="SequenceInterval"
        dict_to_xls['variation|location|type']="SequenceLocation"
        dict_to_xls['variation|location|sequence_id']="HGVSid:" + str(line[0]) + ":g." + str(line[1]) + line[4] + ">" + line[3]





        xls_Book = conf.excel_filename

        wb = openpyxl.load_workbook(xls_Book)

        sheet = wb['genomicVariations']

        list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                        'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                        'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                        'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                        'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
        ]

        dict_columns={}
        i+=1
        
        l=0
        if warning is not True:
            while l < len(list_columns):
                property = list_columns[l]+str(1)
                property_value = sheet[property].value
                if property_value is not None:
                    dict_columns[property]=property_value
                l+=1

            for key, value in dict_to_xls.items():
                for k, v in dict_columns.items():
                    if key == v:
                        result = ''.join([i for i in k if not i.isdigit()])
                        result = result + str(i+1)
                        new_dict_to_xls[result]=value


        pbar.update(1)
        if i == num_variants_registries:
            break

        
    pbar.close()



    for key, value in new_dict_to_xls.items():
        sheet[key].value = value

    wb.save(xls_Book)

read_file = pd.read_excel (conf.excel_filename, 'genomicVariations')
read_file.to_csv ("CINECA.csv",  
                  index = None, 
                  header=True)  
df = pd.DataFrame(pd.read_csv("Test.csv"))

df