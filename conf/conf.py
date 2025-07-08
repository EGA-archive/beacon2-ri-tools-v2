#### Input and Output files config parameters ####
csv_folder = './csv/examples/all-fields/'
output_docs_folder='./output_docs/all-fields/'

#### VCF Conversion config parameters ####
allele_counts=False # Variable still in test, leave it as False for now.
reference_genome='GRCh37' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='test'
case_level_data=True
exact_heterozygosity=True
num_rows=15000000
verbosity=False # This variable, if True, will make the program run slower but give logs about all the skipped variants and the reason why.

### Update record ###
record_type='genomicVariation' # One between analysis, biosample, cohort, dataset, genomicVariation, individual or run
collection_name='genomicVariations'

### MongoDB parameters ###
database_host = 'mongo'
database_port = 27017
database_user = 'root'
database_password = 'example'
database_name = 'beacon'
database_auth_source = 'admin'
