import vcfpy
import warnings
import json
from tqdm import tqdm
import glob
import re
from scripts.datasheet.conf import conf
import csv

list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]

with open("files/properties/genomicVariations.txt", "r") as txt_file:
    list_of_properties_required=txt_file.read().splitlines() 
with open("files/headers/genomicVariations.txt", "r") as txt_file:
    list_of_headers_definitions_required=txt_file.read().splitlines()
with open('files/dictionaries/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

def generate(list_of_properties_required, list_of_headers_definitions_required,dict_properties):
    warnings.formatwarning = custom_formatwarning
    total_dict =[]
    new_dict_to_xls={}
    i=1
    for vcf_filename in glob.glob("files/vcf/files_to_read/*"):
        print(vcf_filename)
        vcf = vcfpy.Reader.from_path(vcf_filename)
        
        header_list = ['#CHROM', 'POS' , 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + vcf.header.samples.names
        num_rows=3000
        pbar = tqdm(total = num_rows)
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
            if dict_to_xls['caseLevelData|zygosity|id'] == '':
                zygo=line[10]
                try:
                    if zygo == '1/0' or zygo == '0/1' or zygo== '1/1':
                        dict_to_xls['caseLevelData|zygosity|label'] = zygo
                        dict_to_xls['caseLevelData|zygosity|id'] = zigosity[zygo]
                        dict_to_xls['caseLevelData|biosampleId'] = header_list[num]
                except Exception:
                    pass


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
        
            

            k=0

            

            dict_of_properties={}
            list_of_filled_items=[]
            for kline, vline in dict_to_xls.items():
                property_value = kline

                
                valor = vline

                if i > 0:
                    
                    if valor != '':

                        list_of_filled_items.append(property_value)

                        
                        for header in list_of_headers_definitions_required:
                            header2 = header[0].lower() + header[1:]
                            if header2 in header:
                                if header2 not in list_of_properties_required:
                                    list_of_properties_required.append(header2)
                                for h2 in list_of_definitions_required:
                                    if header in h2:
                                        h2 = h2[0].lower() + h2[1:]
                                        if h2 not in list_of_properties_required:
                                            list_of_properties_required.append(h2)
                    for filled_item in list_of_filled_items:
                        if isinstance(filled_item, str): 
                            if 'variation' in filled_item:
                                try:
                                    list_of_properties_required.remove('variation')
                                except Exception:
                                    pass
                    

                    if valor:
                        dict_of_properties[property_value]=valor
                        

                    elif valor == 0:
                        dict_of_properties[property_value]=valor

                    


            for lispro in list_of_properties_required:
                if lispro not in list_of_filled_items:
                    raise Exception(('error: you are not filling all the required fields. missing field is: {}').format(lispro))
                    

            #print(dict_properties)
            #print(dict_of_properties)
            definitivedict={}
            for key, value in dict_properties.items():
                if isinstance(value, list):
                    value_list=[]
                    item_dict={}
                    for item in value:
                        outcome = 0
                        if isinstance(item, dict):
                            
                            for ki, vi in item.items():
                                if isinstance(vi, list):
                                    vi_list=[]
                                    subitem_dict={}
                                    for subitem in vi:
                                        if isinstance(subitem, dict):
                                            
                                            for k, v in subitem.items():
                                                if isinstance(v, dict):
                                                    
                                                    subitem_dict[k]={}
                                                    for k1, v1 in v.items():
                                                        if isinstance(v1, dict):
                                                            subitem_dict[k][k1]={}
                                                            for k2, v2 in v1.items():
                                                                if isinstance(v2, dict): 
                                                                    subitem_dict[k][k1][k2]={}
                                                                    for k3, v3 in v2.items():
                                                                        new_item = ""
                                                                        new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2 + "|" + k3
                                                                        for propk, propv in dict_of_properties.items():
                                                                            if propk == new_item:
                                                                                subitem_dict[k][k1][k2][k3]=propv
                                                                    if subitem_dict[k][k1][k2]=={}:
                                                                        del subitem_dict[k][k1][k2]
                                                                else:
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            subitem_dict[k][k1][k2]=propv
                                                            if subitem_dict[k][k1]=={}:
                                                                del subitem_dict[k][k1]                                      
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "|" + ki + "|" + k + "|" + k1
                                                            for propk, propv in dict_of_properties.items():
                                                                if propk == new_item:
                                                                    subitem_dict[k][k1]=propv 
                                                    if subitem_dict[k]=={}:
                                                        del subitem_dict[k]  
                                                elif isinstance(v, list):
                                                    listitemv=[]
                                                    vivdict={}
                                                    for itemv in v:
                                                    
                                                        if isinstance(itemv, dict):
                                                            #print('ki is {}'.format(ki))
                                                            #print('k is {}'.format(k))
                                                            #print(itemv)
                                                            
                                                            for kiv, viv in itemv.items():
                                                                

                                                                if isinstance(viv, list):

                                                                    for itemviv in viv:
                                                                        if isinstance(itemviv, dict):
                                                                            
                                                                            for kivi, vivi in itemviv.items():
                                                                                
                                                                                if isinstance(vivi, list):
                                                                                    
                                                                                    for vivitem1 in vivi:
                                                                                        
                                                                                        for kivivi, vivivi in vivitem1.items():
                                                                                            if isinstance(vivivi, dict):
                                                                                                
                                                                                                for kivivi1, vivivi1 in vivivi.items():
                                                                                                    new_item = ""
                                                                                                    new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi + "|" + kivivi1
                                                                                                    for propk, propv in dict_of_properties.items():
                                                                                                        if propk == new_item:
                                                                                                            #print(propk)
                                                                                                            try:
                                                                                                                vivdict[kiv][kivi][kivivi][kivivi1]=propv  
                                                                                                            except Exception:
                                                                                                                vivdict[kiv]={}
                                                                                                                vivdict[kiv][kivi]={}
                                                                                                                vivdict[kiv][kivi][kivivi]={}
                                                                                                                vivdict[kiv][kivi][kivivi][kivivi1]=propv
                                                                                            elif isinstance(vivivi, list):
                                                                                                for vivivitem in vivivi:
                                                                                                    for kivitem, vivitem in vivivitem.items():
                                                                                                        new_item = ""
                                                                                                        new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi + "|" + kivitem
                                                                                                        for propk, propv in dict_of_properties.items():
                                                                                                            if propk == new_item:
                                                                                                                try:
                                                                                                                    vivdict[kiv][kivi][kivivi][kivitem]=propv
                                                                                                                except Exception:
                                                                                                                    vivdict[kiv][kivi]={}
                                                                                                                    vivdict[kiv][kivi][kivivi]={}
                                                                                                                    vivdict[kiv][kivi][kivivi][kivitem]=propv
                                                                                                                    

                                                                                            else:
                                                                                                
                                                                                                new_item = ""
                                                                                                new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi + "|" + kivivi
                                                                                                #print(new_item)
                                                                                                for propk, propv in dict_of_properties.items():
                                                                                                    if propk == new_item:
                                                                                                        try:
                                                                                                            vivdict[kiv][kivi][kivivi]=propv
                                                                                                        except Exception:
                                                                                                            vivdict[kiv]={}
                                                                                                            vivdict[kiv][kivi]={}
                                                                                                            vivdict[kiv][kivi][kivivi]=propv

                                                                                else:
                                                                                    new_item = ""
                                                                                    new_item = key + "|" + ki + "|" + k + "|" + kiv + "|" + kivi
                                                                                    for propk, propv in dict_of_properties.items():
                                                                                        if propk == new_item:
                                                                                            
                                                                                            try:
                                                                                                if 'value' in propk:
                                                                                                    vivdict[kiv][kivi]=int(propv)
                                                                                                else:
                                                                                                    vivdict[kiv][kivi]=propv
                                                                                            except Exception:
                                                                                                vivdict[kiv]={}
                                                                                                vivdict[kiv][kivi]=propv
                                                                                        elif propk == key + "|" + ki + "|" + k + "|" + kiv:
                                                                                            vivdict[kiv]=propv
                                                                                



                                                                                    
                                                            


                                                                else:
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + kiv
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            #print(propk)
                                                                            vivdict[kiv]=propv





                                                            

                                                        if vivdict != {}:
                                                            #print(vivdict)
                                                            subitem_dict[k]=vivdict
                                                elif ki == 'copies':
                                                    new_item = ""
                                                    new_item = key + "|" + ki
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            propv = re.sub(r'\s', '', propv)
                                                            respropv = json.loads(propv) 
                                                            subitem_dict=respropv

                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            try:
                                                                propv = re.sub(r'\s', '', propv)
                                                                respropv = json.loads(propv) 
                                                                subitem_dict[k]=respropv
                                                            except Exception:
                                                                subitem_dict[k]=propv


                                        if subitem_dict != {}:
                                            if subitem_dict not in vi_list and subitem_dict != {}:
                                                vi_list.append(subitem_dict)
                                            
                                            item_dict[ki]=vi_list[0]
                                elif isinstance(vi, dict):

                                    vi_dict={}
                                    for ki1, vi1 in vi.items():
                                        if isinstance(vi1, dict):
                                            vi_dict[ki1]={}
                                            for ki2, vi2 in vi1.items():
                                                new_item = ""
                                                new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        vi_dict[ki1][ki2]=propv
                                                if vi_dict != {}:
                                                    item_dict[ki]=vi_dict
                                            if vi_dict[ki1]=={}:
                                                del vi_dict[ki1]
                                        elif ki1 == 'variation':
                                            vi_dict[ki1]={}
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict[ki1]=propv
                                        elif isinstance(vi1, list):
                                            vi_dict[ki1]=[]
                                            dictkvi={}
                                            for itemvi1 in vi1:
                                                for kvi, vvi in itemvi1.items():
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + ki1 + "|" + kvi
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:
                                                            dictkvi[kvi]=vvi
                                            vi_dict[ki1]=dictkvi
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict[ki1]=propv 
                                                    item_dict[ki]=vi_dict
                                    if vi_dict=={}:
                                        del vi_dict
                                else:
                                    
                                    new_item = ""
                                    new_item = key + "|" + ki
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            if '|' in propv:
                                                outcome +=1
                                                v1_keys=[]
                                            item_dict[ki]=propv

                                if ki == 'members':
                                    new_item = ""
                                    new_item = key + "|" + ki
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            #print(propk)
                                            propv = re.sub(r'\s', '', propv)
                                            respropv = json.loads(propv)  
                                            item_dict[ki]=respropv
        
                            if item_dict != {} and item_dict != [{}]:
                                

                                if outcome > 0:
                                    if item_dict not in value_list:
                                        value_list.append(item_dict)
                                    if value_list != []:
                                        itemdict={}
                                        definitivedict[key]=[]
                                        v_array=[]
                                        for itemvl in value_list:

                                            for kvl, vvl in itemvl.items():
                                                if isinstance(vvl, str):
                                                    if '|' in vvl:
                                                        itemv={}
                                                        v_array = vvl.split('|')
                                                        itemv[kvl]=v_array
                                                        v_key = kvl
                                                elif isinstance(vvl, dict):
                                                    
                                                    v1_array=[]
                                                    itemdict[kvl]={}
                                                    v1_keys = []
                                                    for kvl1, vvl1 in vvl.items():
                                                        itemdict[kvl][kvl1]={}
                                                        if isinstance(vvl1, str) and '|' in vvl1:
                                                            vvl1_array = vvl1.split('|')
                                                            for vvlitem in vvl1_array:
                                                                v1_array.append(vvlitem)
                                                            v1_bigkeys = kvl
                                                            if kvl1 not in v1_keys:
                                                                v1_keys.append(kvl1)

                                        if v1_keys != []:
                                            n=0
                                            list_to_def=[]
                                            half_array_number = len(v1_array)/2
                                            itemdict[v1_bigkeys]={}

                                            while n < int(half_array_number):
                                                newdict={}
                                                newdict[v1_bigkeys]={}
                                                num=int(half_array_number+n)
                                                newdict[v_key]=v_array[n]
                                                newdict[v1_bigkeys][v1_keys[0]]=v1_array[n]
                                                newdict[v1_bigkeys][v1_keys[1]]=v1_array[num]
                                                list_to_def.append(newdict)
                                                n +=1
                                            for itemldf in list_to_def:
                                                definitivedict[key].append(itemldf)
                                        elif len(v_array) > 1:
                                            list_to_def=[]
                                            
                                            for itva in v_array:
                                                newdict={}
                                                newdict[v_key]=itva
                                                list_to_def.append(newdict)
                                            for itemldf in list_to_def:
                                                definitivedict[key].append(itemldf)
                                        else:
                                            for itemvl in value_list:
                                                definitivedict[key].append(itemvl) 
                                else:
                                    if key == 'caseLevelData':
                                        definitivedict[key]=[]
                                        definitivedict[key].append(item_dict)
                                    else:
                                        definitivedict[key]=item_dict
                                    
                elif isinstance(value, dict):
                    value_dict={}
                    for kd, vd in value.items():
                        if isinstance(vd, list):
                            vd_list=[]
                            value_dict[kd]={}
                            for itemvd in vd:
                                if isinstance(itemvd, dict):
                                    dict_mol={}
                                    for kd1, vd1 in itemvd.items():
                                        if isinstance(vd1, dict):
                                            value_dict[kd][kd1]={}
                                            for kd2, vd2 in vd1.items():
                                                new_item = ""
                                                new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        value_dict[kd][kd1][kd2]=propv
                                            if value_dict[kd][kd1]=={}:
                                                del value_dict[kd][kd1]
                                        elif isinstance(vd1, list):
                                            value_dict[kd][kd1]={}
                                            for item in vd1:
                                                for kd2, vd2 in item.items():
                                                    if isinstance(vd2, list):
                                                        value_dict[kd][kd1][kd2]={}
                                                        for itemvd2 in vd2:
                                                            for kd3, vd3 in itemvd2.items():
                                                                new_item = ""
                                                                new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                                                for propk, propv in dict_of_properties.items():
                                                                    if propk == new_item:
                                                                        value_dict[kd][kd1][kd2][kd3]=propv
                                                    else:
                                                        new_item = ""
                                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                value_dict[kd][kd1][kd2]=propv
                                            if value_dict[kd][kd1]=={}:
                                                del value_dict[kd][kd1]
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + kd + "|" + kd1
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    if '|' in propv:
                                                        propv_splitted = propv.split('|')
                                                        for itemsplitted in propv:
                                                            value_dict[kd][kd1]=propv_splitted
                                                            if value_dict not in vd_list:
                                                                vd_list.append(value_dict)
                                                    else:
                                                        if value_dict == {}:
                                                            value_dict[kd]={}
                                                        if 'molecularEffects' in kd:
                                                            try:
                                                                dict_mol[kd1]=propv
                                                                value_dict[kd].append(dict_mol)
                                                            except Exception:
                                                                dict_mol[kd1]=propv
                                                                value_dict[kd]=[]
                                                        else:                                                          
                                                            value_dict[kd][kd1]=propv



                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            value_dict[kd]=[]
                                            value_dict[kd].append(propv)


                                value_dict = {ka:va for ka,va in value_dict.items() if va != {}}
                                if value_dict != {}:
                                    definitivedict[key]=value_dict
                        elif isinstance(vd, dict):
                            value_dict[kd]={}
                            for kd1, vd1 in vd.items():
                                if isinstance(vd1, dict):
                                    value_dict[kd][kd1]={}
                                    for kd2, vd2 in vd1.items():
                                        if isinstance(vd2, dict):
                                            value_dict[kd][kd1][kd2]={}
                                            for kd3, vd3 in vd2.items():
                                                new_item = ""
                                                new_item = key + "|" + kd + "|" + kd1 + "|" + kd2 + "|" + kd3
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        value_dict[kd][kd1][kd2][kd3]=propv
                                                        definitivedict[key]=value_dict
                                        else:
                                            new_item = ""
                                            new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    value_dict[kd][kd1][kd2]=propv
                                                    definitivedict[key]=value_dict
                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd + "|" + kd1
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            value_dict[kd][kd1]=propv
                                            definitivedict[key]=value_dict
                        else:
                            new_item = ""
                            new_item = key + "|" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    value_dict[kd]=propv
                                    definitivedict[key]=value_dict
                    else:
                        new_item = ""
                        new_item = key + "|" + kd
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                value_dict[kd]=propv
                                definitivedict[key]=value_dict
                else:
                    new_item = ""
                    new_item = key
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            definitivedict[key]=propv

            total_dict.append(definitivedict)
            #print(i)
            pbar.update(1)
            
            if i == num_rows:
                i+=1
                break
            i+=1
            
        num_empty=0
        while i+num_empty <= num_rows:
            pbar.update(1)
            num_empty+=1
    pbar.close()
    return total_dict, i, num_empty

    
dict_generado, total_i, num_empty=generate(list_of_properties_required, list_of_headers_definitions_required,dict_properties)


output = conf.output_docs_folder + 'genomicVariations.json'

print('Successfully converted {} registries into {}'.format(total_i-1, output))
print('A total of {} empty registries were encountered'.format(num_empty))

with open(output, 'w') as f:
    json.dump(dict_generado, f)

