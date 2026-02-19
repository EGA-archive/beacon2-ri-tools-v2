import unittest
from genomicVariations_vcf import generate, client
from remove_dataset import remove_dataset
from csv_to_bff import csv_to_bff
from update_record import update_record
from individuals_to_cohorts_csv import individuals_to_cohorts
from genomicVariations_postprocessing import postprocess_variant
import argparse
from conf import conf
import json
import os

class TestGenomicVariationsWithPopulations(unittest.TestCase):
    def test_main_check_AF_reads_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='COVID_FI_subpop_chr21_subset')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/CRG_AFBeacon_GoE_synthetic_dataset_split-multiallelic-GTmasked-variantQC-sampleQC-ploidy_fixed-AF_recalc.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=True, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate({}, args)
        variants = client.beacon.genomicVariations.find({"datasetId": "COVID_FI_subpop_chr21_subset"})
        assert len(list(variants)) == 531
        for variant in variants:
            assert variant["frequencyInPopulations"] in variant
            for population in variant["frequencyInPopulations"]:
                assert population["frequencies"] in population
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] in frequency
                    assert frequency["population"] in frequency
                    assert frequency["alleleFrequency"] >= 0
                    assert isinstance(frequency["population"],str) == True
    def test_main_check_remove_dataset_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-d', '--datasetId', default="COVID_FI_subpop_chr21_subset")
        args = parser.parse_args()
        remove_dataset(args)
        variants = client.beacon.genomicVariations.find({"datasetId": "COVID_FI_subpop_chr21_subset"})
        assert len(list(variants)) == 0
    def test_main_check_AF_reads_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='COVID_FI_subpop_chr21_subset')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/CRG_AFBeacon_GoE_synthetic_dataset_split-multiallelic-GTmasked-variantQC-sampleQC-ploidy_fixed-AF_recalc.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=False, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate({}, args)
        variants = client.beacon.genomicVariations.find({"datasetId": "COVID_FI_subpop_chr21_subset"})
        assert len(list(variants)) == 531
        for variant in variants:
            assert variant["frequencyInPopulations"] in variant
            for population in variant["frequencyInPopulations"]:
                assert population["frequencies"] in population
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] in frequency
                    assert frequency["population"] in frequency
                    assert frequency["alleleFrequency"] >= 0
                    assert isinstance(frequency["population"],str) == True
    def test_main_check_AF_reads_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='COVID_FI_subpop_chr21_subset')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/CRG_AFBeacon_GoE_synthetic_dataset_split-multiallelic-GTmasked-variantQC-sampleQC-ploidy_fixed-AF_recalc.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=conf.only_process_reads_with_allele_frequency, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate({}, args)
        variants = client.beacon.genomicVariations.find({"datasetId": "COVID_FI_subpop_chr21_subset"})
        assert len(list(variants)) == 531
        for variant in variants:
            assert variant["frequencyInPopulations"] in variant
            for population in variant["frequencyInPopulations"]:
                assert population["frequencies"] in population
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] in frequency
                    assert frequency["population"] in frequency
                    assert frequency["alleleFrequency"] >= 0
                    assert isinstance(frequency["population"],str) == True
    def test_main_check_CSV_analyses_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='analyses', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 1
    def test_main_check_CSV_biosamples_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='biosamples', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 20
    def test_main_check_CSV_cohorts_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='cohorts', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 1
    def test_main_check_CSV_datasets_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='datasets', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 1
    def test_main_check_CSV_variants_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='genomicVariations', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 3
    def test_main_check_CSV_individuals_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='individuals', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 20
    def test_main_check_CSV_runs_to_BFF_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='convert_csv_to_bff',
                            description='This script translates a csv to BFF')
        parser.add_argument('-o', '--output', default='./output_docs/')
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-i', '--input', default='./csv/examples/test/')
        parser.add_argument('-e', '--entry_type', default='runs', choices=['analyses', 'biosamples', 'cohorts', 'datasets', 'genomicVariations', 'individuals', 'runs', 'all'])

        args = parser.parse_args()
        with open("files/headers/"+args.entry_type+'.txt', "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/'+args.entry_type+'.json') as json_file:
            dict_properties = json.load(json_file)

        dict_generado, total_i=csv_to_bff(dict_properties, list_of_headers, args)
        assert total_i-1 == 1
    def test_main_check_no_AF_reads_is_working(self):
        with open('pipelines/default/templates/populations.json', 'w') as f:
            json.dump({}, f)
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='test_2')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/CRG_AFBeacon_GoE_synthetic_dataset_split-multiallelic-GTmasked-variantQC-sampleQC-ploidy_fixed-AF_recalc.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=False, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate({}, args)
        variants = client.beacon.genomicVariations.find({"datasetId": "test_2"})
        assert len(list(variants)) == 531
        for variant in variants:
            assert variant["frequencyInPopulations"] not in variant
    def test_main_check_update_records_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='UpdateRecordInMongoDB',
                            description='This script updates a record in MongoDB')
        parser.add_argument('-f', '--file', default=os.path.join(conf.output_docs_folder, 'test.json'))
        parser.add_argument('-r', '--recordType', default=conf.record_type)
        parser.add_argument('-c', '--collection', default=conf.collection_name)
        args = parser.parse_args()
        update_record(args)
        variants = client.beacon.genomicVariations.find({"datasetId": "test_2", "variantInternalId": "3dd4b36613a574231c2b5a69ad3ab847d2187b22ce90ad832c2a03fbf6c8d613"})
        for variant in variants:
            for population in variant["frequencyInPopulations"]:
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] == 1
    def test_main_check_update_records_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='UpdateRecordInMongoDB',
                            description='This script updates a record in MongoDB')
        parser.add_argument('-f', '--file', default=os.path.join(conf.output_docs_folder, 'test.json'))
        parser.add_argument('-r', '--recordType', default=conf.record_type)
        parser.add_argument('-c', '--collection', default=conf.collection_name)
        args = parser.parse_args()
        update_record(args)
        variants = client.beacon.genomicVariations.find({"datasetId": "test_2", "variantInternalId": "3dd4b36613a574231c2b5a69ad3ab847d2187b22ce90ad832c2a03fbf6c8d613"})
        for variant in variants:
            for population in variant["frequencyInPopulations"]:
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] == 1
    def test_main_check_individuals_to_cohorts_is_working(self):
        parser = argparse.ArgumentParser(
                            prog='IndividualsToCohorts',
                            description='This script translates a csv of individuals to a beaconized json of cohorts')

        parser.add_argument('-i', '--input', default='./csv/examples/test/individuals.csv')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default=conf.datasetId)
        parser.add_argument('-c', '--cohortId', default='cohortId')
        parser.add_argument('-n', '--cohortName', default='cohortName')
        parser.add_argument('-t', '--cohortType', default='user-defined')
        args = parser.parse_args()
        with open("files/headers/individuals.txt", "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        dict_generado, total_i=individuals_to_cohorts(list_of_headers, args)
        assert "collectionEvents" in dict_generado[0]
        assert total_i-1 == 20
    def test_main_check_caseLevelData_variants_postprocessing_is_working(self):
        with open("files/headers/genomicVariations.txt", "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/genomicVariations.json') as json_file:
            dict_properties = json.load(json_file)
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/synthetic_usecases_4beacon_testingV4.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=True, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate(dict_properties, args)
        parser = argparse.ArgumentParser(
                            prog='genomicVariations_CaseLevelData_VariantLevelData_postprocessing',
                            description='This script adds caseLevelData or variantLevelData to an existing variant in your database')
        parser.add_argument('-i', '--input', default='./csv/examples/genomicVariations/caseLevelData/')
        parser.add_argument('-d', '--datasetId', default='test')
        args = parser.parse_args()
        dict_generado, total_i=postprocess_variant(dict_properties,list_of_headers, args)
        assert total_i-1==3
        for case_dict in dict_generado:
            assert 'caseLevelData' in case_dict
    def test_main_check_variantLevelData_variants_postprocessing_is_working(self):
        with open("files/headers/genomicVariations.txt", "r") as txt_file:
            list_of_headers=txt_file.read().splitlines() 
        with open('files/deref_schemas/genomicVariations.json') as json_file:
            dict_properties = json.load(json_file)
        parser = argparse.ArgumentParser(
                            prog='genomicVariationsVCFtoJSON',
                            description='This script translates a vcf of genomic variations to a beaconized json for g_variants')
        parser.add_argument('-o', '--output', default=conf.output_docs_folder)
        parser.add_argument('-d', '--datasetId', default='test')
        parser.add_argument('-r', '--refGen', default=conf.reference_genome)
        parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
        parser.add_argument('-n', '--numRows', default=conf.num_rows)
        parser.add_argument('-v', '--verbosity', default=conf.verbosity)
        parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument('-i', '--input', default="files/vcf/files_to_read/synthetic_usecases_4beacon_testingV4.vcf.gz")
        parser.add_argument('-ac', '--alleleCounts', default=conf.populations_by_allele_counts, action=argparse.BooleanOptionalAction)
        parser.add_argument('-af', '--alleleFrequency', default=True, action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        total_i, skipped_variants=generate(dict_properties, args)
        parser = argparse.ArgumentParser(
                            prog='genomicVariations_CaseLevelData_VariantLevelData_postprocessing',
                            description='This script adds caseLevelData or variantLevelData to an existing variant in your database')
        parser.add_argument('-i', '--input', default='./csv/examples/genomicVariations/variantLevelData/')
        parser.add_argument('-d', '--datasetId', default='test')
        args = parser.parse_args()
        dict_generado, total_i=postprocess_variant(dict_properties,list_of_headers, args)
        assert total_i-1==3
        for case_dict in dict_generado:
            assert 'variantLevelData' in case_dict


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestGenomicVariationsWithPopulations))
    #test_suite.addTest(unittest.makeSuite(TestBudget2))
    return test_suite


mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)