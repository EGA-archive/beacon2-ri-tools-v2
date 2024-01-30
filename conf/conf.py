#### Input and Output files config parameters ####
csv_filename='./csv/examples/cohorts.csv'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
num_variants=1000000
reference_genome='GRCh38' # Choose one between NCBI36, GRCh37, GRCh38
chromosome=['1'] # This variable is an array of chromosomes you want to convert from you vcf.gz file. Write the cromosomes the same exact way they are written in the vcf file, e.g. 'chr22', '22', ...
genomic_start_position=1
genomic_end_position=1394436



