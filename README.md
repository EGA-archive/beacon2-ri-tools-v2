# Beacon ri tools v2.0

This repository contains the new Beacon ri tools v2.0, a software created with the main goal of generating BFF data from .xlsx or .vcf (and probably more types of datafiles in the future). This is based on the first beacon ri tools, a previous and different version that you can find here: [Beacon ri tools v1](https://github.com/EGA-archive/beacon2-ri-tools). The new features for beacon v2.0 are:

* Code Language is written in [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* The output gain are schemas that suit the very last version of [Beacon v2](https://github.com/ga4gh-beacon/beacon-v2) specifications, and ready to be deployed in a beacon v2 API compliant.
* This version raises exceptions that serve as a guide for users to know how to fill data correctly into the datasheets, so the final datafiles are correct and compliant with specifications.
* All the possible combinations of docs that are compliant with specifications can be generated, like for example, writing a variation either in LegacyVariation, MolecularVariation or SystemicVariation.

## Data conversion process

The main goal of Beacon ri tools v2.0 is to obtain a BFF (json following Beacon v2 official specifications) file that can be injected to a beacon v2 mongoDB database. To obtain a beacon v2 with its mongodb and see how to inject this BFF files, you can check it out and download yours for free at the official repo of [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).
To get this json file, you can either convert your data from a vcf file or from a .xlsx file that you will later convert to .csv file. Please, see instruction manual to follow the right steps to do the data conversion. At the end, you will end completing one of the possible conversion processes that is shown in the next diagram:
![Beacon tools v2 diagram](https://github.com/EGA-archive/beacon-ri-tools-v2/blob/main/files/beacontoolsv2.png)

## Installation guide with docker

To light up the container with beacon ri tools v2, execute the next command inside root folder:
```bash
docker-compose up -d --build
```

Once the container is up and running you can start using beacon ri tools v2, congratulations!

## Instruction manual

### Setting configuration and excel file

To start using beacon ri tools v2, you have to edit the configuration file [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf/conf.py) that you will find inside [conf](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf). Inside this file you will find the next information:
```bash
num_registries=2504
num_variants_registries=1004
num_cohorts_registries=1
num_datasets_registries=1
excel_filename='datasheets/allele.xlsx'
csv_filename='csv/genomicVariations.csv'
collection='genomicVariations'
vcf_folder='files/vcf/files_to_read/'
output_docs_folder='output_docs/allele/'
```
The **num_registries**, **num_variants_registries**, **num_cohorts_registries** and **num_datasets_registries** are the variables to set how long is the spreadsheet for your collections, being **num_registries** useful for analyses, biosamples, individuals and runs, **num_variants_registries** for genomicVariations, **num_cohorts_registries** for cohorts and **num_datasets_registries** for datasets. Please, modify this parameter so the scripts will read and parse this amount of data and help to shorten the execution time.
The **excel_filename** variable sets where is the .xlsx file the script will read to write and read data from. This .xlsx file needs to have 7 sheets, one with the name of each beacon collection: analyses, biosamples, cohorts, datasets, genomicVariations, individuals and runs (the **collection** variable sets which is the collection of beacon you are working on, **this is the variable you have to fill first before executing any script**). You have **two options** to do so:
 * (**RECOMMENDED**) Use empty_model.xlsx, rename it and save it inside datasheets directory. Note that the first two columns of each sheet (A and B) must be always empty. 
 * (**NOT RECOMMENDED**) In case you need to create the excel from zero, to update headers or whatever other reason, please follow [generating excel file instructions](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/scripts/datasheet/README.md)
The **csv_filename** variable sets where is the csv file that is going to be read by the scripts. 
The **vcf_folder** variable sets where is the folder with all the vcf files that are going to be converted to json. Bear in mind that the **num_variants_registries** will limit the total number of variants that will be read, no matter how many files are inside the folder.
Lastly, **output_docs_folder** sets the folder where your final .json files will be saved once execution of beacon tools finishes. Please, remember to create this folder in case it is not, before executing the different scripts.

### Converting data from .vcf or .vcf.gz file

To convert data from .vcf (or .vcf.gz) to .json, you will have to copy all the files you want to convert inside the [files_to_read folder](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/files/vcf/files_to_read).
```bash
docker exec -it ri-tools python genomicVariations_vcf.py
```
This will generate the final .json file that is Beacon Friendly Format in the output_docs folder with the name of the collection followed by .json extension, e.g. genomicVariations.json. 
You can also copy it to your localhost directory by using this command:
```bash
docker cp ri-tools:usr/src/app/output_docs/empty_model/genomicVariations.json .
```

### Filling in the excel file (if metadata or not having a vcf file for genomicVariations)

If you want to convert metadata into BFF or fill a genomicVariations spreadsheet to convert to json, you will have to fill in the .xlsx file writing the records according to the header columns, which indicate the field of the schema that this data will be placed in. Every new row will be appended to the final output file as a new and independent document. 
First, copy the excel file to your host machine so you can then edit it with Excel, by executing the following command:
```bash
docker cp ri-tools:usr/src/app/datasheets/empty_model.xlsx .
```
After that, fill in the datasheets, following the next rules:
* If you want to write data that needs to be appended in the same document, please write data separated with |, for example if you need to write an id, e.g. HG00001|HG00002 then respect this order for their correlatives in the same document, as for the label of this id, e.g. labelforHG00001|labelforHG00002.
* As the info field for each collection is very generic and can be filled with different data, you will need to fill the cell directly with json type data. For copies and subjects, json data is also needed.
* Please, respect the columns like the [empty_model.xlsx file](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/datasheets/empty_model.xlsx), as the script will read only these columns to make it go faster.
* Note that you don't have to write inside all the columns, as some of the columns are optionals and other are part of a possible option of the Beacon specification but incompatible with other columns (an exception will raise in case a column is misfilled).

Once you have correctly filled in the excel file, please, copy it back again to the datasheets folder, using this command:
```bash
docker cp empty_model.xlsx ri-tools:usr/src/app/datasheets/empty_model.xlsx
```

### Getting .json final documents

Once you have finished filling all data and saved the .xlsx file, you will have to convert the .xlsx spreadsheet into a .csv file. Before that, please make sure yor [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/scripts/datasheet/conf/conf.py) file contains the correct file and folder paths (for the .csv file that will be output is **csv_filename**). If you are good with the paths, execute then the .xlsx to .csv converter:
```bash
docker exec -it ri-tools python csv_converter.py
```
After that, execute the next bash script from the root folder in your terminal (for the collection you have chosen, in this case for genomic Variations):
```bash
docker exec -it ri-tools python genomicVariations_csv.py
```

This will generate the final .json file that is Beacon Friendly Format in the output_docs folder with the name of the collection followed by .json extension, e.g. genomicVariations.json. 
You can also copy it to your localhost directory by using this command:
```bash
docker cp ri-tools:usr/src/app/output_docs/empty_model/genomicVariations.json .
```

This file will be able to be directly imported into a mongoDB for beacon usage, for example, as described in [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).

### Version notes

* Other file names and distribution of folder and files is not supported.

### Acknowlegments

Thanks to all the [EGA archive](https://ega-archive.org/) team especially Jordi Rambla for supporting, helping and making possible the development of this tool.