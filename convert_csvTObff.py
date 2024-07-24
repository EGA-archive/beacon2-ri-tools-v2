# process_all_csv.py
import os
import subprocess

# Import the configuration
from conf.conf import csv_folder, output_docs_folder

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

# Loop over the files in the CSV folder
for csv_file in os.listdir(csv_folder):
    if csv_file in csv_to_script:
        script_name = csv_to_script[csv_file]
        csv_path = os.path.join(csv_folder, csv_file)
        output_path = os.path.join(output_docs_folder, os.path.splitext(csv_file)[0] + '.json')
        
        # Run the respective script with the appropriate arguments
        subprocess.run(['python', script_name, csv_path, output_path])