#### Input and Output files config parameters ####
csv_folder = './csv/examples/Mireia/'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
allele_counts=True
reference_genome='GRCh37' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='gnomad_exome_v2.1.1'
case_level_data=False
num_rows= 35474150

### MongoDB parameters ###
database_host = 'mongo'
database_port = 27017
database_user = 'root'
database_password = 'example'
database_name = 'beacon'
database_auth_source = 'admin'
