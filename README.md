# Beacon ri tools v2.0

This repository contains the new Beacon ri tools v2.0, a software for generating BFF data from .xlsx or .vcf (and probably more types of datafiles in the future). This is based on the first beacon ri tools, a previous and different version that you can find here: [Beacon ri tools v1](https://github.com/EGA-archive/beacon2-ri-tools). The new features for beacon v2.0 are:

* Code Language is written in [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* The output gain are schemas that suit the very last version of [Beacon v2](https://github.com/ga4gh-beacon/beacon-v2) specifications, and ready to be deployed in a beacon v2 API compliant.
* This version raises exceptions that will serve as a guide for users to know how to fill data correctly into the datasheets, so the final datafiles are correct and compliant with specifications.

### Installation guide (continuous integration)

Still to be implemented.

### Instruction manual

To start using beacon ri tools v2, you have to choose one collection out of the seven possible beacon collections you want to create data for. These collections are:
* Analyses
* Biosamples
* Cohorts
* Datasets
* Genomic Variations
* Individuals
* Runs

Next step, you need to generate the .xlsx file for the collection, by writing the next bash script and adding the collection you chose directly to the terminal in the root folder of the repository. For example, if you chose genomic variations:

```bash
python beacon.py -datasheet genomicVariations
```
After this, a new .xlsx file will be generated inside dataasheets folder with the genomicVariations.xlsl name.

Next step is to fill the .xlsx file writing the records according to the header columns, which indicate the field of the schema that this data will be placed in. Every new row will be appended to the final output file as a new and independent document. The main rules for this datasheet filling are the next ones:
* If you write a value that is a float number, please remember to write it with dot and not with comma, e.g. 2.5.
* If you want to write data that needs to be appended in the same document, please write data separated with commas, for example if you need to write an id, e.g. HG00001,HG00002 then respect this order for their correlatives in the same document, as for the label of this id, e.g. labelforHG00001,labelforHG00002.
* As the info field for each collection is very generic and can be filled with different data, you will need to fill the cell directly with json type data.

Once you have finished filling all data and saved the .xlsx file with the collection name, e.g. genomicVariations.xlsx inside datasheets folder, please execute the next bash script from the root folder in your terminal:

```bash
python genomicVariations.py
```

This will generate the final .json file that is Beacon Friendly Format in the output_schemas folder with the name of the collection followed by .json extension, e.g. genomicVariations.json. This file will be able to be directly imported into a mongoDB for beacon usage, for example for the [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).

### Version notes

* Other file names and distribution of folder and files is not supported.


### Acknowlegments

Thanks to the all the [EGA archive](https://ega-archive.org/) team especially Jordi Rambla for supporting, helping and making possible the development of this tool.