Choose one collection out of the seven possible beacon collections you want to create data for. These collections are:
* Analyses
* Biosamples
* Cohorts
* Datasets
* Genomic Variations
* Individuals
* Runs

Next step, you need to generate the headers for the .xlsx file for the collection, by writing the next bash script and adding the collection you chose directly to the terminal in the root folder of the repository. For example, if you chose genomic variations:
```bash
python beacon.py -datasheet genomicVariations
```