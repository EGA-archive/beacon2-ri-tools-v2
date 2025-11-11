import unittest
from genomicVariations_vcf import generate, client
import argparse
from conf import conf

parser = argparse.ArgumentParser(
                    prog='genomicVariationsVCFtoJSON',
                    description='This script translates a vcf of genomic variations to a beaconized json for g_variants')

parser.add_argument('-o', '--output', default=conf.output_docs_folder)
parser.add_argument('-d', '--datasetId', default=conf.datasetId)
parser.add_argument('-r', '--refGen', default=conf.reference_genome)
parser.add_argument('-c', '--caseLevelData', default=conf.case_level_data, action=argparse.BooleanOptionalAction)
parser.add_argument('-n', '--numRows', default=conf.num_rows)
parser.add_argument('-v', '--verbosity', default=conf.verbosity)
parser.add_argument('-j', '--json', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('-i', '--input', default="files/vcf/files_to_read/*.vcf.gz")

args = parser.parse_args()

class TestGenomicVariationsWithPopulations(unittest.TestCase):
    def test_main_check_VCF_to_BFF(self):
        total_i, skipped_variants=generate({}, args)
        variants = client.beacon.genomicVariations.find({})
        assert len(list(variants)) == 40
        for variant in variants:
            assert variant["frequencyInPopulations"] in variant
            for population in variant["frequencyInPopulations"]:
                assert population["frequencies"] in population
                for frequency in population["frequencies"]:
                    assert frequency["alleleFrequency"] in frequency
                    assert frequency["population"] in frequency
                    assert frequency["alleleFrequency"] > 0
                    assert isinstance(frequency["population"],str) == True

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