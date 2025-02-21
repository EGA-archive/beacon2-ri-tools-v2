#### Input and Output files config parameters ####
csv_folder = './csv/examples/new_test/'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
allele_counts=False
reference_genome='GRCh38' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='gnomad_joint_v4.1'
case_level_data=False
zygosity=True
num_rows= 1535474150

### MongoDB parameters ###
database_host = 'mongo'
database_port = 27017
database_user = 'root'
database_password = 'example'
database_name = 'beacon'
database_auth_source = 'admin'
