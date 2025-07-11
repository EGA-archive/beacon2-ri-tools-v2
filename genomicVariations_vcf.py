from cyvcf2 import VCF
import json
from tqdm import tqdm
import glob
import re
import conf.conf as conf
import uuid
import json
import gc
import gzip
from pymongo.mongo_client import MongoClient
from validators.genomicVariations import GenomicVariations

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

try:
    with open('pipelines/default/templates/populations.json') as pipeline_file:
        pipeline = json.load(pipeline_file)
except Exception:
    pipeline = None

try:
    with open('pipelines/default/templates/template.json') as template_file:
        template = json.load(template_file)
        if template["template"]==False:
            template=None
except Exception:
    template = None

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
                    try:
                        newdict[key]=valuesplitted[i]
                    except Exception:
                        newdict[key]=valuesplitted[0]
                elif isinstance(value, int):
                    valuesplitted = value.split('|')
                    newdict[key]=valuesplitted[i]
                elif isinstance(value, dict):
                    newdict[key]={}
                    for k, v in value.items():
                        if isinstance(v, str):
                            vsplitted = v.split('|')
                            try:
                                newdict[key][k]=float(vsplitted[i])
                                newdict[key][k]="unknown"
                            except Exception:
                                newdict[key][k]=vsplitted[i]
                        elif isinstance(v, int):
                            newdict[key][k]=v
                        elif isinstance(v, dict):
                            newdict[key][k]={}
                            for k1, v1 in v.items():
                                if isinstance(v1, str):
                                    v1splitted = v1.split('|')
                                    newdict[key][k][k1]=v1splitted[i]
            array_of_newdicts.append(newdict)
            i+=1
    else:
        array_of_newdicts.append(prova)
    return(array_of_newdicts)

def num_rows_in_vcf_files():
    total_lines = 0
    for vcf_filename in glob.glob("files/vcf/files_to_read/*.vcf.gz"):
        with gzip.open(vcf_filename, 'rt') as f:
            total_lines += sum(1 for line in f if not line.startswith('#'))
    return total_lines

num_rows = conf.num_rows

def generate(dict_properties):
    total_dict =[]
    total_dict2 =[]
    dict_true={}
    i=1
    l=0
    if conf.case_level_data == True:
        try:
            client.beacon.create_collection(name="caseLevelData")
        except Exception:
            pass
    
    for vcf_filename in glob.glob("files/vcf/files_to_read/*.vcf.gz"):
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
        if conf.case_level_data == False:
            vcf.set_samples([])
        else:
            my_target_list = vcf.samples
            try:
                client.beacon.create_collection(name="targets")
                found_item=client.beacon.targets.find_one({"datasetId": conf.datasetId})
                if found_item == None:
                    dict_target={}
                    dict_target["datasetId"]=conf.datasetId
                    dict_target["biosampleIds"]=my_target_list
                    target_list=[dict_target]
                    client.beacon.targets.insert_many(target_list)
            except Exception:
                dict_target={}
                dict_target["datasetId"]=conf.datasetId
                dict_target["biosampleIds"]=my_target_list
                target_list=[dict_target]
                client.beacon.targets.insert_many(target_list)

        skipped_counts=0

        pbar = tqdm(total = num_rows)

        for v in vcf:
            dict_to_xls={}
            if template != None:
                varianttype=v.INFO.get(template["variantType"])
                gene=v.INFO.get(template["geneId"])
                aminoacidchange=v.INFO.get(template["aminoacidChange"])
                moleculareffectt=v.INFO.get(template["molecularEffects"])
                if moleculareffectt is not None:
                    if  "&" in moleculareffectt:
                        moleculareffects=moleculareffectt.split("&")
                        dict_to_xls['molecularAttributes|molecularEffects|id']=""
                    else:
                        moleculareffects=[moleculareffectt]
                        dict_to_xls['molecularAttributes|molecularEffects|id']=""
                    for moleculareffect in moleculareffects:
                        if dict_to_xls['molecularAttributes|molecularEffects|id']=="":
                            if moleculareffect == 'missense_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000150"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'intron_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000161"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'upstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001631"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '5_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001623"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'synonymous_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001819"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'downstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001632"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'non_coding_transcript_exon_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001792"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '5_prime_UTR_premature_start_codon_gain_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001988"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_region_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001630"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'intergenic_region':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0000605"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_donor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001575"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '3_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001624"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_acceptor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001574"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'stop_retained_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001567"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'coding_sequence_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id']="SO:0001580"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                        else:
                            if moleculareffect == 'missense_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "ENSGLOSSARY:0000150"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'intron_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "ENSGLOSSARY:0000161"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'upstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001631"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '5_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001623"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'synonymous_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001819"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'downstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001632"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'non_coding_transcript_exon_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001792"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '5_prime_UTR_premature_start_codon_gain_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001988"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_region_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001630"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'intergenic_region':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0000605"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_donor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001575"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '3_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001624"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_acceptor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001574"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'stop_retained_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001567"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'coding_sequence_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id']+= "|"+ "SO:0001580"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect

                if gene != '':
                    dict_to_xls['molecularAttributes|geneIds']=gene
                if aminoacidchange!='':
                    dict_to_xls['molecularAttributes|aminoacidChanges']=aminoacidchange
            elif formatted == True:
                annotation_list=v.INFO.get('CSQ')
                if annotation_list != None:
                    annotation_list=annotation_list.split('|')
                    #print(annotation_list)
                    #print(varianttype_num)
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
                    #print(varianttype)
                    gene=annotation_list[gene_num]
                    if gene != '':
                        dict_to_xls['molecularAttributes|geneIds']=gene
                    protein=annotation_list[protein_num]
                    #print(protein)
                    if protein != '':
                        protein=protein.split('p.')
                        aminoacidchange=protein[1]
                        dict_to_xls['molecularAttributes|aminoacidChanges']=aminoacidchange
                    moleculareffectt=annotation_list[moleculareffect_num]
                    
                    if "&" in moleculareffectt:
                        moleculareffects=moleculareffectt.split("&")
                        dict_to_xls['molecularAttributes|molecularEffects|id']=""
                    else:
                        moleculareffects=[moleculareffectt]
                        dict_to_xls['molecularAttributes|molecularEffects|id']=""
                    for moleculareffect in moleculareffects:
                        if dict_to_xls['molecularAttributes|molecularEffects|id']=="":
                            if moleculareffect == 'missense_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000150"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'intron_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "ENSGLOSSARY:0000161"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'upstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001631"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '5_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001623"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'synonymous_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001819"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'downstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001632"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'non_coding_transcript_exon_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001792"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '5_prime_UTR_premature_start_codon_gain_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001988"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_region_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001630"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'intergenic_region':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0000605"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_donor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001575"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == '3_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001624"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'splice_acceptor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001574"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'stop_retained_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] = "SO:0001567"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                            elif moleculareffect == 'coding_sequence_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id']="SO:0001580"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] = moleculareffect
                        else:
                            if moleculareffect == 'missense_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "ENSGLOSSARY:0000150"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'intron_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "ENSGLOSSARY:0000161"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'upstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001631"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '5_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001623"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'synonymous_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001819"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'downstream_gene_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001632"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'non_coding_transcript_exon_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001792"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '5_prime_UTR_premature_start_codon_gain_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001988"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_region_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001630"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'intergenic_region':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0000605"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_donor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001575"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == '3_prime_UTR_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001624"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'splice_acceptor_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001574"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'stop_retained_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id'] += "|"+ "SO:0001567"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                            elif moleculareffect == 'coding_sequence_variant':
                                dict_to_xls['molecularAttributes|molecularEffects|id']+= "|"+ "SO:0001580"
                                dict_to_xls['molecularAttributes|molecularEffects|label'] += "|"+  moleculareffect
                        #print(dict_to_xls['molecularAttributes|molecularEffects|id'])
                else:
                    formatted=False



            else:
                try:
                    varianttype=v.INFO.get('VT')
                except Exception:
                    varianttype='UNKNOWN'
                

            
            
            try:
                if varianttype == 'SV': 
                    i+=1
                    pbar.update(1)
                    if conf.verbosity==True:
                        ref=v.REF
                        chrom=v.CHROM
                        start=v.start
                        print('variant in chr: {} with start position: {} and reference base: {} skipped because being of type Structural Variant, which is not supported yet'.format(chrom, start, ref))
                    skipped_counts+=1
                    continue
            except Exception:
                pass
            try:
                num_of_populations=0
                frequencies=[]
                allele_frequency=0
                if pipeline is not None:
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
                            ac_hom=v.INFO.get(population["alleleCountHomozygous"])
                            ac_het=v.INFO.get(population["alleleCountHeterozygous"])
                            if allele_frequency == None:
                                pass
                            if isinstance(allele_frequency, tuple):
                                allele_frequency=list(allele_frequency)
                                allele_frequency=allele_frequency[0]
                            else:
                                allele_frequency = float(allele_frequency)
                            if allele_frequency == 0.0:
                                continue
                            if allele_number == None:
                                pass
                            elif isinstance(allele_number, tuple):
                                allele_number=list(allele_number)
                                allele_number=allele_number[0]
                            else:
                                allele_number = int(allele_number)
                            if allele_count == None:
                                pass
                            elif isinstance(allele_count, tuple):
                                allele_count=list(allele_count)
                                allele_count=allele_count[0]
                            else:
                                allele_count = int(allele_count)
                            if allele_count == 0:
                                continue
                            if ac_hom == None:
                                pass
                            elif isinstance(ac_hom, tuple):
                                ac_hom=list(ac_hom)
                                ac_hom=ac_hom[0]
                            else:
                                ac_hom = int(ac_hom)

                            if ac_het == None:
                                pass
                            elif isinstance(ac_het, tuple):
                                ac_het=list(ac_het)
                                ac_het=ac_het[0]
                            else:
                                ac_het = int(ac_het)
                            if allele_frequency != 0 or allele_frequency != None:
                                if allele_count != 0 or allele_count != None:
                                    if ac_hom == None and ac_het != None and allele_count != None:
                                        ac_hom = allele_count - ac_het
                                    elif ac_het == None and ac_hom != None and allele_count != None:
                                        ac_het = allele_count - ac_hom
                            popu=population["population"]
                            if allele_frequency != 0 or allele_frequency != None:
                                dict_per_population["alleleFrequency"]=allele_frequency
                                if allele_count != None and allele_count != 0:
                                    dict_per_population["alleleCount"]=allele_count
                                    dict_per_population["alleleCountHomozygous"]=ac_hom
                                    dict_per_population["alleleCountHeterozygous"]=ac_het
                                if allele_number != None and allele_number != 0:
                                    dict_per_population["alleleNumber"]=allele_number
                                dict_per_population["population"]=popu
                            if dict_per_population != {} and allele_frequency !=None:
                                frequencies.append(dict_per_population)
                if pipeline is None or num_of_populations == 0:
                    allele_frequency=v.INFO.get('AF')
                    if allele_frequency == None:
                        pass
                    if isinstance(allele_frequency, tuple):
                        allele_frequency=list(allele_frequency)
                        allele_frequency=allele_frequency[0]
                    else:
                        allele_frequency = float(allele_frequency)
                    if allele_frequency == 0.0:
                        i+=1
                        pbar.update(1)
                        if conf.verbosity==True:
                            ref=v.REF
                            chrom=v.CHROM
                            start=v.start
                            print('variant in chr: {} with start position: {} and reference base: {} skipped because its allele frequency is 0'.format(chrom, start, ref))
                        skipped_counts+=1
                        continue
                    allele_number=v.INFO.get('AN')
                    if allele_number == None:
                        pass
                    elif isinstance(allele_number, tuple):
                        allele_number=list(allele_number)
                        allele_number=allele_number[0]
                    else:
                        allele_number = float(allele_number)
                    allele_count=v.INFO.get('AC')
                    if allele_count == None:
                        pass
                    elif isinstance(allele_count, tuple):
                        allele_count=list(allele_count)
                        allele_count=allele_count[0]
                    else:
                        allele_count = float(allele_count)
                    if allele_count == 0.0:
                        i+=1
                        pbar.update(1)
                        if conf.verbosity==True:
                            ref=v.REF
                            chrom=v.CHROM
                            start=v.start
                            print('variant in chr: {} with start position: {} and reference base: {} skipped because its allele count is 0'.format(chrom, start, ref))
                        skipped_counts+=1
                        continue
                    ac_hom=v.INFO.get('AC_Hom')
                    if ac_hom == None:
                        pass
                    elif isinstance(ac_hom, tuple):
                        ac_hom=list(ac_hom)
                        ac_hom=ac_hom[0]
                    else:
                        ac_hom = float(v.INFO.get('AC_Hom'))
                    ac_het=v.INFO.get('AC_Het')
                    if ac_het == None:
                        pass
                    elif isinstance(ac_het, tuple):
                        ac_het=list(ac_het)
                        ac_het=ac_het[0]
                    else:
                        ac_het = float(v.INFO.get('AC_Het'))
                if conf.allele_counts == True:
                    if allele_frequency == 0 or allele_frequency == 0.0 or allele_frequency is None:
                        i+=1
                        pbar.update(1)
                        if conf.verbosity==True:
                            ref=v.REF
                            chrom=v.CHROM
                            start=v.start
                            print('variant in chr: {} with start position: {} and reference base: {} skipped because its allele frequency is 0'.format(chrom, start, ref))
                        skipped_counts+=1
                        continue

                if allele_frequency is not None:
                    dict_to_xls['frequencyInPopulations|sourceReference']=pipeline["frequencyInPopulations|sourceReference"]
                    dict_to_xls['frequencyInPopulations|source']=pipeline["frequencyInPopulations|source"]
                    dict_to_xls['frequencyInPopulations|frequencies|population']="Total"
                    dict_to_xls['frequencyInPopulations|frequencies|alleleFrequency']=allele_frequency
                    if allele_frequency != 0 or allele_frequency != None:
                        dict_per_population["alleleFrequency"]=allele_frequency
                        if allele_count != None and allele_count != 0:
                            dict_per_population["alleleCount"]=allele_count
                            dict_per_population["alleleCountHomozygous"]=ac_hom
                            dict_per_population["alleleCountHeterozygous"]=ac_het
                        if allele_number != None and allele_number != 0:
                            dict_per_population["alleleNumber"]=allele_number
                        dict_per_population["population"]=popu
                    if dict_per_population != {} and allele_frequency !=None:
                        frequencies.append(dict_per_population)
                        num_of_populations=1


            except Exception as e:
                pass
            #print(allele_frequency)
            if frequencies == []:
                if num_of_populations != 0:
                    i+=1
                    pbar.update(1)
                    if conf.verbosity==True:
                        ref=v.REF
                        chrom=v.CHROM
                        start=v.start
                        print('variant in chr: {} with start position: {} and reference base: {} skipped because none of the populations had allele frequency greater than 0'.format(chrom, start, ref))
                    skipped_counts+=1
                    continue

            #print(v)
            try:
                ref=v.REF
                chrom=v.CHROM
                start=v.start
                end=v.end
                alt=v.ALT
            except Exception:
                chrom=v.CHROM
                start=v.start
                ref=v.REF
                end=v.INFO.get('END')
                alt=v.ALT
            if alt != [] and '<' and '>' in alt[0]:
                i+=1
                pbar.update(1)
                if conf.verbosity==True:
                    ref=v.REF
                    chrom=v.CHROM
                    start=v.start
                    print('variant in chr: {} with start position: {} and reference base: {} skipped because alternateBases: {} format not supported'.format(ref, chrom, start, alt))
                skipped_counts+=1
                continue
            elif alt == []:
                alt=['N']
            dict_to_xls['variation|alternateBases'] = alt[0]

            dict_to_xls['variation|referenceBases'] = ref
            try:
                dict_to_xls['variation|variantType'] = varianttype
                if varianttype is None:
                    if len(alt[0]) == len(ref):
                        dict_to_xls['variation|variantType']='SNP'
                    else:
                        dict_to_xls['variation|variantType']='INDEL'
            except Exception:
                dict_to_xls['variation|variantType']='UNKNOWN'


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
            if conf.reference_genome == 'GRCh37':
                HGVSId=rootHGVS+str(chromos) + '.10' + ':' + 'g.' + str(start+1) + ref + '>' + alt[0]
                dict_to_xls['identifiers|genomicHGVSId'] = HGVSId
            elif conf.reference_genome == 'GRCh38':
                HGVSId=rootHGVS+str(chromos) + '.11' + ':' + 'g.' + str(start+1) + ref + '>' + alt[0]
                dict_to_xls['identifiers|genomicHGVSId'] = HGVSId
            elif conf.reference_genome == 'NCBI36':
                HGVSId=rootHGVS+str(chromos) + '.9' + ':' + 'g.' + str(start+1) + ref + '>' + alt[0]
                dict_to_xls['identifiers|genomicHGVSId'] = HGVSId

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
            
            

            if conf.case_level_data == True:
                if conf.exact_heterozygosity == False:
                    j=0
                    dict_trues={"id": HGVSId, "datasetId": conf.datasetId}
                    for zygo in v.gt_types:
                        if zygo==1:
                            dict_trues[str(j)]="y"
                            j+=1
                        elif zygo ==3:
                            dict_trues[str(j)]="11"
                            j+=1
                        else:
                            j+=1
                elif conf.exact_heterozygosity == True:
                    j=0
                    dict_trues={"id": HGVSId, "datasetId": conf.datasetId}
                    for zygo in v.genotypes:
                        if zygo[0] == 1 and zygo[1]== 1:
                            dict_trues[str(j)]="11"
                            j+=1
                        elif zygo[0] == 1 and zygo[1]== 0:
                            dict_trues[str(j)]="10"
                            j+=1
                        elif zygo[0] == 0 and zygo[1]== 1:
                            dict_trues[str(j)]="01"
                            j+=1

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
                                                if isinstance(v, dict):
                                                    for k1, v1 in v.items():
                                                        new_item = ""
                                                        new_item = key + "|" + ki + "|" + k + "|" + k1
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                try:
                                                                    subitem_dict[k][k1]=propv
                                                                except Exception:
                                                                    subitem_dict[k]={}
                                                                    subitem_dict[k][k1]=propv
                                                else:
                                                    new_item = ""
                                                    new_item = key + "|" + ki + "|" + k
                                                    for propk, propv in dict_of_properties.items():
                                                        if propk == new_item:


                                                            try:
                                                                if ki == 'clinicalInterpretations':
                                                                    pass
                                                                else:
                                                                    propv = re.sub(r'\s', '', propv)
                                                                respropv = json.loads(propv) 
                                                                subitem_dict[k]=respropv
                                                            except Exception:
                                                                subitem_dict[k]=propv


                                        if subitem_dict != {}:
                                            if subitem_dict not in vi_list and subitem_dict != {}:


                                                vi_list.append(subitem_dict)

                                            if ki == 'clinicalInterpretations':
                                                for itemvl in vi_list:
                                                    list_to_def=commas(itemvl)
                                                    for itemldf in list_to_def:
                                                        try:
                                                            if itemldf not in item_dict[ki]:
                                                                item_dict[ki].append(itemldf)
                                                        except Exception:
                                                            item_dict[ki]=[]
                                                            item_dict[ki].append(itemldf)
                                            elif ki == 'frequencies':
                                                item_dict[ki]=vi_list
                                            else:
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
                                    if key == 'caseLevelData' or key=='frequencyInPopulations':
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
                                    list_mol=[]
                                    for kd1, vd1 in itemvd.items():

                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                if '|' in propv:
                                                    propv_splitted = propv.split('|')
                                                    propv_splitted=list(dict.fromkeys(propv_splitted))
                                                    t=0


                                                    while t < len(propv_splitted):
                                                        dict_mol={}
                                                        try:
                                                            dict_mol[kd1]=propv_splitted[t]

                                                        except Exception:

                                                            dict_mol[kd1]=propv_splitted[t]

                                                        t+=1
                                                        list_mol.append(dict_mol)

                                                    t=0
                                                    u=0
                                                    if kd1 == 'label':
                                                        try:
                                                            if len(list_mol) == 2:
                                                                dict_mol_2={}
                                                                dict_mol_2['id']=list_mol[t]['id']
                                                                dict_mol_2['label']=list_mol[t+1]['label']
                                                                try:
                                                                    value_dict[kd].append(dict_mol_2)
                                                                except Exception:
                                                                    value_dict[kd]=[]
                                                                    value_dict[kd].append(dict_mol_2)
                                                        except Exception:
                                                            pass
                                                        else:
                                                            try:
                                                                while u < len(list_mol):
                                                                    dict_mol_2={}
                                                                    dict_mol_2['id']=list_mol[t]['id']
                                                                    indice = int(len(list_mol)/2)
                                                                    dict_mol_2['label']=list_mol[t+indice]['label']
                                                                    try:
                                                                        value_dict[kd].append(dict_mol_2)
                                                                    except Exception:
                                                                        value_dict[kd]=[]
                                                                        value_dict[kd].append(dict_mol_2)
                                                                    t+=1
                                                                    u+=2
                                                            except Exception:
                                                                pass

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

                                    #print(list_mol)



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

            GenomicVariations(**definitivedict)
            definitivedict["datasetId"]=conf.datasetId
            definitivedict["length"]=int(end)-int(start)
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
            i+=1

            if conf.case_level_data == True:
                client.beacon.caseLevelData.insert_one(dict_trues)
            dict_trues={}

            if total_dict != []:
                if i == num_rows:
                    client.beacon.genomicVariations.insert_many(total_dict)
                    #pbar.update(1)
                    break
                elif (i/10000).is_integer():
                    client.beacon.genomicVariations.insert_many(total_dict)
                    del definitivedict
                    del total_dict
                    gc.collect()
                    total_dict=[]
                    #pbar.update(1)  




    if total_dict != []:
        if i != num_rows:
            client.beacon.genomicVariations.insert_many(total_dict)
    if conf.case_level_data == True:
        if total_dict2 != []:
            if i != num_rows:
                client.beacon.caseLevelData.insert_many(total_dict2)



    pbar.close()
    return i, skipped_counts

total_i, skipped_variants=generate(dict_properties)


if total_i-skipped_variants > 0:
    print('Successfully inserted {} records into beacon'.format(total_i-skipped_variants-1))
    print('A total of {} variants were processed'.format(total_i-1))
    print('A total of {} variants were skipped'.format(skipped_variants))
else:
    print('No registries found.')