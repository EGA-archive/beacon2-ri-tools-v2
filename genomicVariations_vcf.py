from cyvcf2 import VCF
import warnings
import json
from tqdm import tqdm
import glob
import re
import conf.conf as conf
import uuid
import json
import gc

with open('files/deref_schemas/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)

def generate(dict_properties):
    byt_combined=b''
    total_dict =[]
    i=1
    l=0
    for vcf_filename in glob.glob("files/vcf/files_to_read/*.vcf.gz"):
        print(vcf_filename)
        vcf = VCF(vcf_filename, strict_gt=True)
        my_target_list = vcf.samples

        num_rows=conf.num_variants
        pbar = tqdm(total = num_rows)
        for v in vcf:
            #print(v)
            dict_to_xls={}
            ref=v.REF
            chrom=v.CHROM
            start=v.start
            end=v.end
            alt=v.ALT
            dict_to_xls['variation|alternateBases'] = alt[0]

            dict_to_xls['variation|referenceBases'] = ref
            dict_to_xls['variation|variantType'] = v.INFO.get('VT')
            #print(v.INFO.get('ANN'))
            if v.INFO.get('ANN') is not None:
                annot = v.INFO.get('ANN')
                annotations = annot.split("|")
                dict_to_xls['molecularAttributes|molecularEffects|label'] = annotations[1]
                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000174"
                dict_to_xls['molecularAttributes|aminoacidChanges'] = "."
                dict_to_xls['molecularAttributes|geneIds'] = annotations[3]
            
            
            zigosity={}
            zigosity['0/1']='GENO:GENO_0000458'
            zigosity['1/0']='GENO:GENO_0000458'
            zigosity['1/1']='GENO:GENO_0000136'
            j=0
            dict_to_xls['caseLevelData|zygosity|id'] =''
            dict_to_xls['caseLevelData|zygosity|label']=''
            for zygo in v.genotypes:
                if dict_to_xls['caseLevelData|zygosity|id'] == '':
                    if zygo[0] == 1 and zygo[1]== 1:
                        dict_to_xls['caseLevelData|zygosity|label'] = '1/1'
                        dict_to_xls['caseLevelData|zygosity|id'] = zigosity['1/1']
                        dict_to_xls['caseLevelData|biosampleId'] = my_target_list[j]
                    elif zygo[0] == 1 and zygo[1]== 0:
                        dict_to_xls['caseLevelData|zygosity|label'] = '1/0'
                        dict_to_xls['caseLevelData|zygosity|id'] = zigosity['1/0']
                        dict_to_xls['caseLevelData|biosampleId'] = my_target_list[j]
                    elif zygo[0] == 0 and zygo[1]== 1:
                        dict_to_xls['caseLevelData|zygosity|label'] = '0/1'
                        dict_to_xls['caseLevelData|zygosity|id'] = zigosity['0/1']
                        dict_to_xls['caseLevelData|biosampleId'] = my_target_list[j]
                else:
                    if zygo[0] == 1 and zygo[1]== 1:
                        dict_to_xls['caseLevelData|zygosity|label'] = dict_to_xls['caseLevelData|zygosity|label'] + '|' + '1/1'
                        dict_to_xls['caseLevelData|zygosity|id'] = dict_to_xls['caseLevelData|zygosity|id'] + '|' + zigosity['1/1']
                        dict_to_xls['caseLevelData|biosampleId'] = dict_to_xls['caseLevelData|biosampleId'] + '|' + my_target_list[j]
                    elif zygo[0] == 1 and zygo[1]== 0:
                        dict_to_xls['caseLevelData|zygosity|label'] = dict_to_xls['caseLevelData|zygosity|label'] + '|' + '1/0'
                        dict_to_xls['caseLevelData|zygosity|id'] = dict_to_xls['caseLevelData|zygosity|id'] + '|' + zigosity['1/0']
                        dict_to_xls['caseLevelData|biosampleId'] = dict_to_xls['caseLevelData|biosampleId'] + '|' + my_target_list[j]
                    elif zygo[0] == 0 and zygo[1]== 1:
                        dict_to_xls['caseLevelData|zygosity|label'] = dict_to_xls['caseLevelData|zygosity|label'] + '|' + '0/1'
                        dict_to_xls['caseLevelData|zygosity|id'] = dict_to_xls['caseLevelData|zygosity|id'] + '|' + zigosity['0/1']
                        dict_to_xls['caseLevelData|biosampleId'] = dict_to_xls['caseLevelData|biosampleId'] + '|' + my_target_list[j]


                j+=1

            chromos=re.sub(r"</?\[>", "", chrom)
            if conf.reference_genome == 'GRCh37':
                dict_to_xls['identifiers|genomicHGVSId'] = 'NC_0000'+str(chromos) + '.10' + ':' + 'g.' + str(start) + ref + '>' + alt[0]
            elif conf.reference_genome == 'GRCh38':
                dict_to_xls['identifiers|genomicHGVSId'] = 'NC_0000'+str(chromos) + '.11' + ':' + 'g.' + str(start) + ref + '>' + alt[0]
            elif conf.reference_genome == 'NCBI36':
                dict_to_xls['identifiers|genomicHGVSId'] = 'NC_0000'+str(chromos) + '.9' + ':' + 'g.' + str(start) + ref + '>' + alt[0]

            dict_to_xls['variation|location|interval|start|value'] = int(start)
            dict_to_xls['variation|location|interval|start|type']="Number"
            dict_to_xls['variation|location|interval|end|value'] = int(end)
            dict_to_xls['variation|location|interval|end|type']="Number"

            dict_to_xls['variation|location|interval|start|value'] = int(start)
            dict_to_xls['variation|location|interval|start|type']="Number"
            dict_to_xls['variation|location|interval|end|value'] = int(end)
            dict_to_xls['variation|location|interval|end|type']="Number"
            dict_to_xls['variation|location|interval|type']="SequenceInterval"
            dict_to_xls['variation|location|type']="SequenceLocation"
            dict_to_xls['variation|location|sequence_id']="HGVSid:" + str(chrom) + ":g." + str(start) + ref + ">" + alt[0]
            dict_to_xls['variantInternalId'] = str(uuid.uuid1())+':' + str(ref) + ':' + str(alt[0])
            

            k=0

            

            dict_of_properties={}
            for kline, vline in dict_to_xls.items():
                property_value = kline

                
                valor = vline

                if valor:
                    dict_of_properties[property_value]=valor
                    

                elif valor == 0:
                    dict_of_properties[property_value]=valor

            
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
                                                if isinstance(v, list):
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
                                                #print(v_array)
                                                #print(v1_array)
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
            
            if i == num_rows:
                s = json.dumps(total_dict)

                s = s.encode('utf-8')
                byt_combined+=s
                pbar.update(1)
                break
            elif (i/20000).is_integer():
                s = json.dumps(total_dict[0:-1])
                s = s.encode('utf-8')
                byt_combined+=s+b','
                del total_dict
                gc.collect()
                total_dict=[]
                pbar.update(1)

            
            pbar.update(1)
            i+=1
    if i != num_rows:
        s = json.dumps(total_dict)
        s = s.encode('utf-8')
        byt_combined+=s

    byt_combined+=b''
    total_dict=json.loads(byt_combined.decode('utf-8'))
    pbar.close()
    return total_dict, i, l

dict_generado, total_i, l=generate(dict_properties)

output = conf.output_docs_folder + 'genomicVariations.json'

if total_i-l > 0:
    print('Successfully converted {} registries into {}'.format(total_i-l, output))
else:
    print('No registries found.')

with open(output, 'w') as f:
    json.dump(dict_generado, f)
