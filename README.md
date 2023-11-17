# Beacon ri tools v2.0

This repository contains the new Beacon ri tools v2.0, a software created with the main goal of generating BFF data from .xlsx or .vcf (and probably more types of datafiles in the future). This is based on the first beacon ri tools, a previous and different version that you can find here: [Beacon ri tools v1](https://github.com/EGA-archive/beacon2-ri-tools). The new features for beacon v2.0 are:

* Code Language is written in [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* The output gain are schemas that suit the very last version of [Beacon v2](https://github.com/ga4gh-beacon/beacon-v2) specifications, and ready to be deployed in a beacon v2 API compliant.
* This version raises exceptions that serve as a guide for users to know how to fill data correctly into the datasheets, so the final datafiles are correct and compliant with specifications.
* All the possible combinations of docs that are compliant with specifications can be generated, like for example, writing a variation either in LegacyVariation, MolecularVariation or SystemicVariation.

### Installation guide with docker

To light up the container with beacon ri tools v2, execute the next command inside root folder:
```bash
docker-compose up -d --build
```

Once the container is up and running you can start using beacon ri tools v2, congratulations!

### Instruction manual

## Setting configuration and excel file

To start using beacon ri tools v2, you have to edit the configuration file [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf/conf.py) that you will find inside [conf](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf). Inside this file you will find the next information:
```bash
num_registries=4
num_variants_registries=4
num_cohorts_registries=1
num_datasets_registries=1
excel_filename='datasheets/empty_model.xlsx'
vcf_filename='files/vcf/chr22.Test.1000G.phase3.joint.norm.ann.dbnsfp.clinvar.cosmic.vcf.gz'
output_docs_folder='output_docs/empty_model/'
```
The **num_registries**, **num_variants_registries**, **num_cohorts_registries** and **num_datasets_registries** are the variables to set how long is the spreadsheet for your collections, being **num_registries** useful for analyses, biosamples, individuals and runs, **num_variants_registries** for genomicVariations, **num_cohorts_registries** for cohorts and **num_datasets_registries** for datasets. Please, modify this parameter so the scripts will read and parse this amount of data and help to shorten the execution time.
The **excel_filename** variable sets where is the .xlsx file the script will read to write and read data from. This .xlsx file needs to have 7 sheets, one with the name of each beacon collection: analyses, biosamples, cohorts, datasets, genomicVariations, individuals and runs. You have **two options** to do so:
 * (**RECOMMENDED**) Use empty_model.xlsx, rename it and save it inside datasheets directory. Note that the first two columns of each sheet (A and B) must be always empty. 
 * (**NOT RECOMMENDED**) In case you need to create the excel from zero, to update headers or whatever other reason, please follow [generating excel file instructions](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/scripts/datasheet/README.md)
The **vcf_filename** variable sets where is the vcf file (already reannotated) that is going to be read by the vcf script.
Last, **output_docs_folder** sets the folder where your final .json files will be saved once execution of beacon tools finishes. Please, remember to create this folder in case it is not, before executing the different scripts.

## Filling in the excel file

Next step is to fill the .xlsx file writing the records according to the header columns, which indicate the field of the schema that this data will be placed in. Every new row will be appended to the final output file as a new and independent document. The main rules for this datasheet filling are the next ones:
* If you want to write data that needs to be appended in the same document, please write data separated with |, for example if you need to write an id, e.g. HG00001|HG00002 then respect this order for their correlatives in the same document, as for the label of this id, e.g. labelforHG00001|labelforHG00002.
* As the info field for each collection is very generic and can be filled with different data, you will need to fill the cell directly with json type data.
* Please, note that the first two columns must remain in blank and respect the columns like the [empty_model.xlsx file](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/datasheets/empty_model.xlsx), as the script will read only these columns to make it go faster.
* Note that you don't have to write inside all the columns, as some of the columns are optionals and other are part of a possible option of the Beacon specification but incompatible with other columns (an exception will arise in case a column is misfilled).

## Filling genomicVariations excel sheet from .vcf file

In case you want to use a .vcf file to obtain your final .json, this .vcf file needs to be a final .vcf reannotated following the [reannotating .vcf file instructions] (https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/download.sh). 
Once you have the final .vcf, you will have to save the .vcf file in the same path that you wrote in the vcf_filename variable that is inside [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf/conf.py) file. 
After that, please execute the next command from the root folder in your terminal:
```bash
docker exec -it ri-tools python vcf.py
```
This will fill in the genomicVariations excel sheet with the .vcf file you provided.

## Getting .json final documents

Once you have finished filling all data and saved the .xlsx file, please execute the next bash script from the root folder in your terminal (for the collection you have chosen, in this case for genomic Variations):

```bash
docker exec -it ri-tools python genomicVariations.py
```

This will generate the final .json file that is Beacon Friendly Format in the output_docs folder with the name of the collection followed by .json extension, e.g. genomicVariations.json. This file will be able to be directly imported into a mongoDB for beacon usage, for example for the [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).

### Version notes

* Other file names and distribution of folder and files is not supported.


### Acknowlegments

Thanks to the all the [EGA archive](https://ega-archive.org/) team especially Jordi Rambla for supporting, helping and making possible the development of this tool.