from cyvcf2 import VCF
import json
from tqdm import tqdm
import glob
import re
import conf.conf as conf
import json
import gc
import gzip
from pymongo.mongo_client import MongoClient
from validators.genomicVariations import GenomicVariations, LegacyVariation, SequenceLocation, SequenceInterval, Number, OntologyTerm, MolecularAttributes, FrequencyInPopulation, PopulationFrequency, Identifiers
from pymongo.errors import BulkWriteError
import hashlib
import argparse
from pydantic import ValidationError
import os
from validators.templates.populations import AllelePopulations, GenotypePopulations

client = MongoClient(
        #"mongodb://127.0.0.1:27017/"
        "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
            conf.database_user,
            conf.database_password,
            conf.database_host,
            conf.database_port,
            conf.database_name,
            conf.database_auth_source,
        )
    )

with open('files/deref_schemas/genomicVariations.json') as json_file:
    dict_properties = json.load(json_file)

with open('pipelines/default/templates/populations.json') as pipeline_file:
    pipeline = json.load(pipeline_file)
    if pipeline["numberOfPopulations"]==0:
        pipeline=None
    else:
        num_of_populations=pipeline["numberOfPopulations"]

if pipeline is not None:
    print("VCF being processed with {} population/s!".format(num_of_populations))
elif pipeline is None:
    print("VCF being processed without allele frequencies!")

if conf.allele_counts == True and pipeline is not None:
    AllelePopulations(**pipeline)
elif pipeline is not None:
    GenotypePopulations(**pipeline)

if pipeline is not None:
    list_of_population_headers=[]
    for population_item in pipeline["populations"]:
        list_of_population_headers.append(population_item["alleleFrequency"])
        list_of_population_headers.append(population_item["alleleCount"])
        list_of_population_headers.append(population_item["alleleNumber"])
        if conf.allele_counts == False:
            list_of_population_headers.append(population_item["genotypeHomozygous"])
            list_of_population_headers.append(population_item["genotypeHeterozygous"])
            list_of_population_headers.append(population_item["genotypeHemizygous"])
        else:
            list_of_population_headers.append(population_item["alleleCountHomozygous"])
            list_of_population_headers.append(population_item["alleleCountHeterozygous"])
            list_of_population_headers.append(population_item["alleleCountHemizygous"])
    list_of_population_headers=list(set(list_of_population_headers))
    list_of_existing_headers=[]

try:
    with open('pipelines/default/templates/template.json') as template_file:
        template = json.load(template_file)
        if template["template"]==False:
            template=None
except Exception:
    template = None

try:
    with open('pipelines/default/templates/molecularEffects.json') as molecularEffects_file:
        moleculareffects_ontologies = json.load(molecularEffects_file)
except Exception:
    moleculareffects_ontologies = []

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def process_alleles(allele_property):
    if allele_property == None:
        pass
    elif isinstance(allele_property, tuple):
        allele_property=list(allele_property)
        allele_property=allele_property[0]
    else:
        allele_property = float(allele_property)
    return allele_property

def generate_molecular_attributes(moleculareffectt):
    list_of_molecular_effects=[]
    if moleculareffectt is not None:
        if  "&" in moleculareffectt:
            moleculareffects=moleculareffectt.split("&")
        else:
            moleculareffects=[moleculareffectt]
        if moleculareffects_ontologies != []:
            for moleculareffect in moleculareffects:
                for ontology in moleculareffects_ontologies:
                    if ontology["label"] == moleculareffect:
                        list_of_molecular_effects.append(OntologyTerm(id=ontology["id"], label=ontology["label"]))
    return list_of_molecular_effects

def append_to_json(file, data):
    chunk = " , " + json.dumps(data) + "]"

    with open(file, 'r+') as f:

        f.seek(0, 2)
        index = f.tell()

        while not f.read().startswith(']'):
            index -= 1
            if index == 0:
                raise ValueError("{} is not a JSON formatted file".format(file))
            f.seek(index)

        f.seek(index)
        f.write(chunk)  

def generate(dict_properties, args):
    total_dict =[]
    number_variants=1
    if args.caseLevelData == True:
        try:
            client.beacon.create_collection(name="targets")
        except Exception:
            pass
        try:
            client.beacon.create_collection(name="caseLevelData")
        except Exception:
            pass
    skipped_counts=0
    for vcf_filename in glob.glob(args.input):
        print(vcf_filename)
        vcf = VCF(vcf_filename, strict_gt=True)
        formatted=False
        for rec in vcf.header_iter():
            d = rec.info()
            try:
                if d['ID'] == 'CSQ' and template == None:
                    format_annotation = d['Description']
                    format_list=format_annotation.split('|')
                    formatted=True
                    w=0
                    for entry in format_list:
                        if 'uploaded_allele' in entry.lower():
                            varianttype_num=w
                        elif entry.lower() == 'symbol':
                            gene_num=w
                        elif 'hgvsp' in entry.lower():
                            protein_num=w
                        elif 'consequence' in entry.lower():
                            moleculareffect_num=w
                        w+=1
            except Exception:
                continue
            if pipeline is not None:
                for population_header in list_of_population_headers:
                    if d['ID'] == population_header:
                        list_of_existing_headers.append(population_header)
        if pipeline is not None:
            non_existing_headers = list(set(list_of_population_headers) - set(list_of_existing_headers))
            if len(non_existing_headers)>0:
                raise Exception("There are properties in the populations.json that don't match the header INFO fields. The problematic INFO fields are: {}".format(non_existing_headers))
            
        if args.caseLevelData == False:
            vcf.set_samples([])
        else:
            my_target_list = vcf.samples
            target_errors=[]
            try:
                dict_target={}
                dict_target["_id"]=get_hash(args.datasetId)
                dict_target["datasetId"]=args.datasetId
                dict_target["biosampleIds"]=my_target_list
                if args.json == False:
                    client.beacon.targets.insert_many([dict_target],ordered=False)
                else:
                    with open(args.output+'targets.json', 'w') as outfile:
                        json.dump([dict_target], outfile)
            except BulkWriteError as BulkError:
                start_point=len("batch op errors occurred, full error:")
                error_stringed=str(BulkError)[start_point:]
                new_string = ''.join("'" if charac == '"' else '"' if charac == "'" else charac for charac in error_stringed)
                new_string=new_string.replace('None', '"None"')
                error_dicted=json.loads(new_string)
                target_errors.append(error_dicted["writeErrors"][0]['op'])
                pass
            if target_errors != []:
                for caught_error in target_errors:
                    target_to_update=client.beacon.targets.find_one({"_id": caught_error["_id"]})
                    if target_to_update != {} and target_to_update != None:
                        biosampleIds_to_update=target_to_update["biosampleIds"]
                        duplicated_ids = []
                        for element in biosampleIds_to_update:
                            if element in caught_error["biosampleIds"]:
                                duplicated_ids.append(element)
                        new_positions = []
                        t = len(biosampleIds_to_update)
                        for bioId in caught_error["biosampleIds"]:
                            if bioId in biosampleIds_to_update:
                                new_positions.append(biosampleIds_to_update.index(bioId))
                            else:
                                new_positions.append(t)
                                t+=1
                        for duplicated_id in duplicated_ids:
                            caught_error["biosampleIds"].remove(duplicated_id)
                        
                        
                        target_to_update["biosampleIds"] = biosampleIds_to_update + caught_error["biosampleIds"]
                        set_dict={}
                        set_dict["$set"]=target_to_update
                        if caught_error["biosampleIds"] != []:
                            client.beacon.targets.update_one({"_id": caught_error["_id"]},set_dict)

        pbar = tqdm(total = args.numRows)

        for v in vcf:
            try:
                molecular_attributes = None
                frequency_in_population = None
                if template != None:
                    varianttype=v.INFO.get(template["variantType"])
                    gene=v.INFO.get(template["geneId"])
                    aminoacidchange=v.INFO.get(template["aminoacidChange"])
                    moleculareffectt=v.INFO.get(template["molecularEffects"])
                    list_of_molecular_effects = generate_molecular_attributes(moleculareffectt)
                    if list_of_molecular_effects != []:
                        molecular_attributes = MolecularAttributes(molecularEffects=list_of_molecular_effects,geneIds=[gene] if gene != '' else None,aminoacidChanges=aminoacidchange if aminoacidchange != '' else None)
                    else:
                        molecular_attributes = None
                elif formatted == True:
                    annotation_list=v.INFO.get('CSQ')
                    if annotation_list != None:
                        annotation_list=annotation_list.split('|')
                        try:
                            varianttype=annotation_list[varianttype_num]
                            if '/' in varianttype:
                                if len(varianttype)> 3:
                                    varianttype='INDEL'
                                else:
                                    varianttype='SNP'
                            else:
                                varianttype='Structural Variant'
                        except Exception:
                            varianttype='UNKNOWN'
                        gene=annotation_list[gene_num]
                        protein=annotation_list[protein_num]
                        if protein != '':
                            protein=protein.split('p.')
                            aminoacidchange=protein[1]
                        moleculareffectt=annotation_list[moleculareffect_num]
                        list_of_molecular_effects = generate_molecular_attributes(moleculareffectt)
                        if list_of_molecular_effects != []:
                            molecular_attributes = MolecularAttributes(molecularEffects=list_of_molecular_effects,geneIds=[gene] if gene != '' else None,aminoacidChanges=[aminoacidchange] if protein != '' else None)
                        else:
                            molecular_attributes = None
                    else:
                        formatted=False
                else:
                    try:
                        varianttype=v.INFO.get('VT')
                    except Exception:
                        varianttype='UNKNOWN'
                try:
                    if varianttype == 'SV': 
                        number_variants+=1
                        pbar.update(1)
                        if args.verbosity==True:
                            ref=v.REF
                            chrom=v.CHROM
                            start=v.start
                            print('variant in chr: {} with start position: {} and reference base: {} skipped because being of type Structural Variant, which is not supported yet'.format(chrom, start, ref))
                        skipped_counts+=1
                        continue
                except Exception:
                    pass

                num_of_populations=0
                frequencies=[]
                allele_frequency=0
                ref=v.REF
                chrom=v.CHROM
                start=v.start
                if pipeline is not None:
                    #Validate pipeline.json
                    num_of_populations=pipeline["numberOfPopulations"]     
                    source=pipeline["source"]
                    source_reference=pipeline["sourceReference"]
                    populations=pipeline["populations"]
                    if num_of_populations != 0:
                        for population in populations:
                            dict_per_population={}
                            allele_frequency=v.INFO.get(population["alleleFrequency"])
                            allele_count=v.INFO.get(population["alleleCount"])
                            allele_number=v.INFO.get(population["alleleNumber"])
                            if conf.allele_counts==False:
                                if population["genotypeHomozygous"] != "":
                                    ac_hom=v.INFO.get(population["genotypeHomozygous"])
                                    ac_hom = process_alleles(ac_hom)
                                else:
                                    ac_hom=None
                                if population["genotypeHeterozygous"] != "":
                                    ac_het=v.INFO.get(population["genotypeHeterozygous"])
                                    ac_het = process_alleles(ac_het)
                                else:
                                    ac_het=None
                                if population["genotypeHemizygous"] != "":
                                    ac_hemi=v.INFO.get(population["genotypeHemizygous"])
                                    ac_hemi = process_alleles(ac_hemi)
                                else:
                                    ac_hemi=None
                            else:
                                if population["alleleCountHomozygous"] != "":
                                    ac_hom=v.INFO.get(population["alleleCountHomozygous"])
                                    ac_hom = process_alleles(ac_hom)
                                else:
                                    ac_hom=None
                                if population["alleleCountHeterozygous"] != "":
                                    ac_het=v.INFO.get(population["alleleCountHeterozygous"])
                                    ac_het = process_alleles(ac_het)
                                else:
                                    ac_het=None
                                if population["alleleCountHemizygous"] != "":
                                    ac_hemi=v.INFO.get(population["alleleCountHemizygous"])
                                    ac_hemi = process_alleles(ac_hemi)
                                else:
                                    ac_hemi=None
                            allele_frequency = process_alleles(allele_frequency)
                            allele_number = process_alleles(allele_number)
                            allele_count = process_alleles(allele_count)
                            
                            if allele_frequency == 0.0 or allele_count == 0.0:
                                continue
                            popu=population["population"]
                            if allele_frequency != 0 or allele_frequency != None:
                                dict_per_population["alleleFrequency"]=allele_frequency
                                if allele_count != None and allele_count != 0:
                                    dict_per_population["alleleCount"]=allele_count
                                    if conf.allele_counts==False:
                                        if ac_hom != None:
                                            dict_per_population["genotypeHomozygous"]=ac_hom
                                        if ac_het != None:
                                            dict_per_population["genotypeHeterozygous"]=ac_het
                                        if ac_hemi != None:
                                            dict_per_population["genotypeHemizygous"]=ac_hemi
                                    else:
                                        if ac_hom != None:
                                            dict_per_population["alleleCountHomozygous"]=ac_hom
                                        if ac_het != None:
                                            dict_per_population["alleleCountHeterozygous"]=ac_het
                                        if ac_hemi != None:
                                            dict_per_population["alleleCountHemizygous"]=ac_hemi                                        
                                if allele_number != None and allele_number != 0:
                                    dict_per_population["alleleNumber"]=allele_number
                                dict_per_population["population"]=popu
                            if dict_per_population != {} and allele_frequency !=None:
                                frequencies.append(dict_per_population)
                                num_of_populations=1

                if frequencies != []:
                    population_frequencies=[]
                    for frequency in frequencies:
                        population_frequency = PopulationFrequency(population=frequency["population"],alleleFrequency=frequency["alleleFrequency"]).model_dump(exclude_none=True)
                        population_frequencies.append(population_frequency)
                    frequency_in_population = FrequencyInPopulation(sourceReference=pipeline["sourceReference"],source=pipeline["source"],frequencies=population_frequencies)
                    population_frequencies=[]
                else:
                    if num_of_populations != 0:
                        number_variants+=1
                        pbar.update(1)
                        if args.verbosity==True:
                            print('variant in chr: {} with start position: {} and reference base: {} skipped because none of the populations had allele frequency greater than 0'.format(chrom, start, ref))
                        skipped_counts+=1
                        continue

                try:
                    end=v.end
                    alt=v.ALT
                except Exception:
                    end=v.INFO.get('END')
                    alt=v.ALT
                if alt != [] and '<' and '>' in alt[0]:
                    number_variants+=1
                    pbar.update(1)
                    if args.verbosity==True:
                        ref=v.REF
                        chrom=v.CHROM
                        start=v.start
                        print('variant in chr: {} with start position: {} and reference base: {} skipped because alternateBases: {} format not supported'.format(ref, chrom, start, alt))
                    skipped_counts+=1
                    continue
                elif alt == []:
                    alt=['N']

                try:
                    if varianttype is None:
                        if len(alt[0]) == len(ref):
                            varianttype='SNP'
                        else:
                            varianttype='INDEL'
                except Exception:
                    varianttype = 'UNKNOWN'


                chromos=re.sub(r"</?\[>", "", chrom)
                chromos=chromos.replace("chr","")
                if 'X' in chrom:
                    chromos = '23'
                elif 'Y' in chrom:
                    chromos = '24'
                if len (str(chromos))>1:
                    rootHGVS='NC_0000'
                else:
                    rootHGVS='NC_00000'
                
                if args.refGen == 'GRCh37':
                    if chromos in ['14', '21']:
                        HGVSId=rootHGVS+str(chromos) + '.8' + ':' + 'g.'
                    elif chromos in ['5', '11', '15', '16', '18', '19', '24']:
                        HGVSId=rootHGVS+str(chromos) + '.9' + ':' + 'g.' 
                    elif chromos in ['1', '8', '10', '13', '17', '20', '22', '23']:
                        HGVSId=rootHGVS+str(chromos) + '.10' + ':' + 'g.' 
                    elif chromos in ['2', '3', '4', '6', '9', '12']:
                        HGVSId=rootHGVS+str(chromos) + '.11' + ':' + 'g.'
                    elif chromos == '7':
                        HGVSId=rootHGVS+str(chromos) + '.13' + ':' + 'g.' 
                elif args.refGen == 'GRCh38':
                    if chromos in ['14', '21']:
                        HGVSId=rootHGVS+str(chromos) + '.9' + ':' + 'g.'
                    elif chromos in ['5', '11', '15', '16', '18', '19', '24']:
                        HGVSId=rootHGVS+str(chromos) + '.10' + ':' + 'g.' 
                    elif chromos in ['1', '8', '10', '13', '17', '20', '22', '23']:
                        HGVSId=rootHGVS+str(chromos) + '.11' + ':' + 'g.' 
                    elif chromos in ['2', '3', '4', '6', '9', '12']:
                        HGVSId=rootHGVS+str(chromos) + '.12' + ':' + 'g.'
                    elif chromos == '7':
                        HGVSId=rootHGVS+str(chromos) + '.14' + ':' + 'g.' 
                elif args.refGen == 'NCBI36':
                    if chromos in ['14', '21']:
                        HGVSId=rootHGVS+str(chromos) + '.7' + ':' + 'g.'
                    elif chromos in ['5', '11', '15', '16', '18', '19', '24']:
                        HGVSId=rootHGVS+str(chromos) + '.8' + ':' + 'g.' 
                    elif chromos in ['1', '8', '10', '13', '17', '20', '22', '23']:
                        HGVSId=rootHGVS+str(chromos) + '.9' + ':' + 'g.' 
                    elif chromos in ['2', '3', '4', '6', '9', '12']:
                        HGVSId=rootHGVS+str(chromos) + '.10' + ':' + 'g.'
                    elif chromos == '7':
                        HGVSId=rootHGVS+str(chromos) + '.12' + ':' + 'g.'

                if chromos == 'MT':
                    HGVSId="NC_012920.1:m."
                
                if reversed(ref) == alt[0]:
                    HGVSId = HGVSId + str(start+1) + '_' + str(start+len(ref)-1) + 'inv'
                    varianttype = 'INV'
                elif len(ref) > len(alt[0]):
                    if ref[-1] == alt[0]:
                        HGVSId = HGVSId + str(start+1) + '_' + str(start+len(ref)-1) + 'del'
                        varianttype = 'DEL'
                    elif len(ref)-len(alt[0])>1:
                        HGVSId = HGVSId + str(start+1) + '_' + str(start+len(ref)) + 'delins' + alt[0]
                        varianttype = 'INDEL'
                    else:
                        HGVSId = HGVSId + str(start+2) + 'del' 
                        varianttype = 'DEL'
                elif len(ref) < len(alt[0]):
                    if len(ref) < len(alt[0]) and len(alt[0])>len(ref)+3:
                        if alt[0][len(ref):len(ref)+2] == alt[0][len(ref)+2:len(ref)+4]:
                            num_of_duplications = len(alt[0])-len(ref)
                            num_of_duplications = num_of_duplications//2
                            for i in range(num_of_duplications):
                                if alt[0][len(ref):len(ref)+2] == alt[0][len(ref)*2*i:len(ref)+2*2*i]:
                                    continue
                                else:
                                    num_of_duplications = 'not a duplication'
                            if num_of_duplications == 'not a duplication':
                                pass
                            elif num_of_duplications == 1:
                                HGVSId = HGVSId + str(start+1)+ 'dup'
                                varianttype = 'DUP'
                            else:
                                HGVSId = HGVSId + str(start+1) + '_' + str(start+1+len(alt[0])-num_of_duplications*2) + 'dup'
                                varianttype = 'DUP'
                    if varianttype != 'DUP':
                        if len(ref) > 1:
                            HGVSId = HGVSId + str(start+1) + '_' + str(start+len(ref)) + 'delins' + alt[0]
                            varianttype = 'INDEL'
                        elif ref[0] == alt[0][0]:
                            varianttype = 'INS'
                            HGVSId = HGVSId + str(start+1) + '_' + str(start+2) + 'ins' + alt[0][1:]
                        else:
                            HGVSId = HGVSId + str(start+1) + 'delins' + alt[0]
                            varianttype = 'INDEL'
                elif len(alt[0])==1 and len(ref)==1:
                    HGVSId = HGVSId + str(start+1) + ref + '>' + alt[0]
                    varianttype = 'SNP'
                else:
                    HGVSId = HGVSId + str(start+1) + ref + '>' + alt[0]

                _id=get_hash(args.datasetId+HGVSId)

                sequence_id="HGVSid:" + str(chrom) + ":g." + str(start) + ref + ">" + alt[0]
                end_range = Number(type="Number",value=int(end))
                start_range = Number(type="Number",value=int(start))
                interval = SequenceInterval(type="SequenceInterval", start=start_range, end=end_range)
                location = SequenceLocation(interval=interval, type="SequenceLocation", sequence_id=sequence_id)
                variation = LegacyVariation(alternateBases=alt[0], referenceBases=ref, variantType=varianttype, location=location)
                ##
                if args.caseLevelData == True:
                    j=0
                    p=0
                    dict_trues={"_id": _id,"id": HGVSId, "datasetId": args.datasetId}
                    for zygo in v.genotypes:
                        try:
                            j = new_positions[p]
                            p+=1
                        except Exception:
                            pass
                        if zygo[0] == 1 and zygo[1]== 1:
                            dict_trues[str(j)]="11"
                            j+=1
                        elif zygo[0] == 1 and zygo[1]== 0:
                            dict_trues[str(j)]="10"
                            j+=1
                        elif zygo[0] == 0 and zygo[1]== 1:
                            dict_trues[str(j)]="01"
                            j+=1
                        else:
                            j+=1
                if num_of_populations != 0:
                    variant = GenomicVariations(variation=variation, variantInternalId=_id, frequencyInPopulations=[frequency_in_population.model_dump(exclude_none=True)], molecularAttributes=molecular_attributes, identifiers=Identifiers(genomicHGVSId=HGVSId))
                else:
                    variant = GenomicVariations(variation=variation, variantInternalId=_id, molecularAttributes=molecular_attributes, identifiers=Identifiers(genomicHGVSId=HGVSId))

                definitivedict = variant.model_dump(exclude_none=True)
                definitivedict["datasetId"]=args.datasetId
                definitivedict["length"]=int(end)-int(start)
                definitivedict["_id"]=_id

                try:
                    if num_of_populations != 0:
                        if frequencies!=[]:
                            definitivedict["frequencyInPopulations"]=[]
                            dictfrequency={}
                            dictfrequency["source"]=source
                            dictfrequency["sourceReference"]=source_reference
                            dictfrequency["frequencies"]=frequencies
                            definitivedict["frequencyInPopulations"].append(dictfrequency)
                except Exception:
                    pass
                total_dict.append(definitivedict)

                pbar.update(1)
                number_variants+=1
                if args.caseLevelData == True and args.json == False:
                    catch_errors=[]
                    try:
                        client.beacon.caseLevelData.insert_many([dict_trues],ordered=False)
                    except BulkWriteError as BulkError:
                        start_point=len("batch op errors occurred, full error:")
                        error_stringed=str(BulkError)[start_point:]
                        new_string = ''.join("'" if charac == '"' else '"' if charac == "'" else charac for charac in error_stringed)
                        new_string=new_string.replace('None', '"None"')
                        error_dicted=json.loads(new_string)
                        catch_errors.append(error_dicted["writeErrors"][0]['op'])
                        pass
                    if catch_errors != []:
                        final_dict={}
                        for caught_error in catch_errors:
                            final_dict=caught_error
                            caseLevelData_to_update=client.beacon.caseLevelData.find_one({"_id": caught_error["_id"]})
                            if caseLevelData_to_update != {} and caseLevelData_to_update != None:
                                for k, v in caseLevelData_to_update.items():
                                    final_dict[k]=v
                                set_dict={}
                                set_dict["$set"]=final_dict
                                client.beacon.caseLevelData.update_one({"_id": caught_error["_id"]},set_dict)
                elif args.caseLevelData == True:
                    try:
                        append_to_json(args.output+'caseLevelData.json', dict_trues)
                    except Exception:
                        with open(args.output+'caseLevelData.json', 'w') as outfile:
                            json.dump([dict_trues], outfile)
                    


                dict_trues={}

                if total_dict != []:
                    if args.json == False:
                        variants_errors=[]
                        if number_variants == args.numRows:
                            try:
                                client.beacon.genomicVariations.insert_many(total_dict, ordered=False)
                            except BulkWriteError as BulkError:
                                start_point=len("batch op errors occurred, full error:")
                                error_stringed=str(BulkError)[start_point:]
                                new_string = ''.join("'" if charac == '"' else '"' if charac == "'" else charac for charac in error_stringed)
                                new_string=new_string.replace('None', '"None"')
                                error_dicted=json.loads(new_string)
                                for error in error_dicted["writeErrors"]:
                                    variants_errors.append(error['op'])
                            break
                        elif (number_variants/10000).is_integer():
                            try:
                                client.beacon.genomicVariations.insert_many(total_dict, ordered=False)
                            except BulkWriteError as BulkError:
                                start_point=len("batch op errors occurred, full error:")
                                #print(BulkError.details)
                                error_stringed=str(BulkError)[start_point:]
                                new_string = ''.join("'" if charac == '"' else '"' if charac == "'" else charac for charac in error_stringed)
                                new_string=new_string.replace('None', '"None"')
                                error_dicted=json.loads(new_string)
                                for error in error_dicted["writeErrors"]:
                                    variants_errors.append(error['op'])

                            del definitivedict
                            del total_dict
                            gc.collect()
                            total_dict=[]
                        for error in variants_errors:
                            if args.verbosity == True:
                                print("following duplicated variant found was skipped: {}".format(error))
                            skipped_counts+=1
                    else:
                        for variantdict in total_dict:
                            try:
                                append_to_json(os.path.join(args.output, 'genomicVariations.json'), variantdict)
                            except Exception:
                                with open(os.path.join(args.output, 'genomicVariations.json'), 'w') as outfile:
                                    json.dump([variantdict], outfile)
            except ValidationError:
                print("Validation error for variant in chr: {} with start position: {} and reference base: {}".format(chrom, start, ref))
                raise
            except Exception:
                raise




    if total_dict != []:
        if args.json == False:
            variants_errors=[]
            if number_variants != args.numRows:
                try:
                    client.beacon.genomicVariations.insert_many(total_dict, ordered=False)
                except BulkWriteError as BulkError:
                    start_point=len("batch op errors occurred, full error:")
                    error_stringed=str(BulkError)[start_point:]
                    new_string = ''.join("'" if charac == '"' else '"' if charac == "'" else charac for charac in error_stringed)
                    new_string=new_string.replace('None', '"None"')
                    error_dicted=json.loads(new_string)
                    for error in error_dicted["writeErrors"]:
                        variants_errors.append(error['op'])
            for error in variants_errors:
                if args.verbosity == True:
                    print("following duplicated variant found was skipped: {}".format(error))
                skipped_counts+=1
        else:
            for variantdict in total_dict:
                try:
                    append_to_json(os.path.join(args.output, 'genomicVariations.json'), variantdict)
                except Exception:
                    with open(os.path.join(args.output, 'genomicVariations.json'), 'w') as outfile:
                        json.dump([variantdict], outfile)


    try:
        pbar.close()
        return number_variants, skipped_counts
    except Exception:
        raise Exception('No vcf.gz file could be found.')


parser = argparse.ArgumentParser(
                    prog='genomicVariationsVCFtoJSON',
                    description='This script translates a vcf of genomic variations to a beaconized json for g_variants')

parser.add_argument('-o', '--output', default=conf.output_docs_folder)
parser.add_argument('-d', '--datasetId', default=conf.datasetId)
parser.add_argument('-r', '--refGen', default=conf.reference_genome)
parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
parser.add_argument('-n', '--numRows', default=conf.num_rows)
parser.add_argument('-v', '--verbosity', default=conf.verbosity, action=argparse.BooleanOptionalAction)
parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('-i', '--input', default="files/vcf/files_to_read/*.vcf.gz")

args = parser.parse_args()

total_i, skipped_variants=generate(dict_properties, args)


if total_i-skipped_variants > 0:
    print('Successfully inserted {} records into beacon'.format(total_i-skipped_variants-1))
    print('A total of {} variants were processed'.format(total_i-1))
    print('A total of {} variants were skipped'.format(skipped_variants))
else:
    print('No registries found.')