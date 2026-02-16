import unittest
from genomicVariations_vcf import generate, client
from remove_dataset import remove_dataset
from csv_to_bff import csv_to_bff
import argparse
from conf import conf
import json

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
        parser.add_argument('-d', '--datasetId', default=conf.datasetId)
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