# process_all_csv.py
import os
import subprocess
import argparse
# Import the configuration
from conf.conf import csv_folder, output_docs_folder, datasetId

# Define a mapping from CSV filenames to their respective Python scripts
csv_to_script = {
    'biosamples.csv': 'biosamples_csv.py',
    'genomicVariations.csv': 'genomicVariations_csv.py',
    'individuals.csv': 'individuals_csv.py',
    'runs.csv': 'runs_csv.py',
    'cohorts.csv': 'cohorts_csv.py',
    'datasets.csv': 'datasets_csv.py',
    'analyses.csv': 'analyses_csv.py',
}

# Ensure the output directory exists
os.makedirs(output_docs_folder, exist_ok=True)

parser = argparse.ArgumentParser(
                    prog='convertCSVtOBFF',
                    description='This script translates a set of csv to BFF')
parser.add_argument('-o', '--output', default=output_docs_folder)
parser.add_argument('-d', '--datasetId', default=datasetId)
parser.add_argument('-i', '--input', default=csv_folder)

args = parser.parse_args()


# Loop over the files in the CSV folder
for csv_file in os.listdir(csv_folder):
    if csv_file in csv_to_script:
        script_name = csv_to_script[csv_file]
        
        # Run the respective script with the appropriate arguments
        subprocess.run(['python', script_name, '-i', args.input, '-o', args.output, '-d', args.datasetId])