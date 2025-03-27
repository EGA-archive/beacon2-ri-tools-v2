# Beacon2 RI Tools v2

This repository contains the new Beacon2 RI Tools v2, a software created with the main goal of generating BFF data from .csv or .vcf (and probably more types of datafiles in the future). This is based on the first beacon ri tools, a previous and different version that you can find here: [Beacon ri tools v1](https://github.com/EGA-archive/beacon2-ri-tools). The new features for beacon v2.0 are:

* Code Language is written in [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* The output gain is schemas that suit the very last version of [Beacon v2](https://github.com/ga4gh-beacon/beacon-v2) specifications, and ready to be deployed in a beacon v2 API compliant.
* This version raises exceptions that serve as a guide for users to know how to fill data correctly into the datasheets, so the final datafiles are correct and compliant with specifications.
* All the possible combinations of docs that are compliant with specifications can be generated, for example, writing a variation either in LegacyVariation, MolecularVariation or SystemicVariation.

## Documentation

Please, go to [B2RI/B2PI docs website](https://b2ri-documentation-demo.ega-archive.org/) to know how to use Beacon RI TOOLS v2.

## Data conversion process

Beacon r.i tools v2.0 is a package of tools designed to simplify the population of a Beacon v2 mongoDB database.  Currently, the supported input formats are VCF, CSV, and Phenopackets. These formats are converted to BFF (Beacon Friendly Format JSON,  following Beacon v2 official specifications) and inserted into a Beacon database. 

To create your own Beacon v2 and learn how to populate it visit the official repo of the beacon v2 PI API where you can download all the necessary resources for free.

![Beacon tools v2 diagram](https://github.com/EGA-archive/beacon-data-tools/blob/main/files/beacon-ri-tools-v2-MAR25.png)

## Installation guide with docker

First of all, clone or download the repository to your computer:
```bash
git clone https://github.com/EGA-archive/beacon-data-tools.git
```

To light up the container with beacon data tools, execute the next command inside the root folder:
```bash
docker-compose up -d --build
```

Once the container is up and running you can start using beacon ri tools v2, congratulations!

## Instruction manual

### Setting configuration and csv file

To start using beacon ri tools v2, you have to edit the configuration file [conf.py](https://github.com/EGA-archive/beacon-data-tools/tree/main/conf/conf.py) that you will find inside [conf](https://github.com/EGA-archive/beacon-data-tools/tree/main/conf). Inside this file you will find the next information:
```bash
#### Input and Output files config parameters ####
csv_folder = './csv/examples/'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
allele_counts=False
reference_genome='GRCh37' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='COVID_pop11_fin_2'
case_level_data=False
exact_heterozygosity=False
num_rows=15000000
verbosity=False
```

Please, remember to make the datasetId match the id for your datasets.csv file.

#### Generic config parameters
The *csv_folder* variable sets the path of a folder containing all the CSVs that will be converted to BFF. 

The *output_docs_folder* variable sets the folder where your final .json files (BFF format) will be saved once execution of beacon tools finishes. This folder should always be located within the folder 'output_docs', but subdirectories can be created inside it. e.g output_docs_folder='./output_docs/test1'


#### VCF conversion config parameters
*reference_genome* must be filled in with the assembly version used to map and call the VCF. Make sure to insert the correct information as beacon r.i tools will use the assembly stated to map the positions and show the correct variants once the beacon database is up.

If you don’t want to include all the variants to your beacon database you can do some filtering with *allele_frequency*. It sets a threshold for the minimum allele frequency a variant has to have to be inserted in beacon. 

*datasetID* field will be used to map the metadata to the variant. Please, make sure that datasetId matches the id stated in datasets.csv or datasets.json file. This way the phenotypic and metadata information will be linked to the variant. 

The *case_level_data* is a boolean parameter (True or False) which will relate your variants to the samples they belong to. In case you set this to true, please, read as well the case level data paragraph below. 

The *num_rows* is an approximation of the number of variants in the VCF. Make sure this is, at least, greater than the total variants expected. 

### Populating a beacon instance from VCF

Populate genomicVaritiatons model from a VCF

#### Annotated VCFs
To ensure minimum information is lost, Beacon RI Tools v2 is also compatible with header annotations. 

By default, it expects headers annotated by VEP. The parameters that are read from the VEP annotations are:

- UPLOADED_ALLELE: setting the variant type
- SYMBOL: gene id
- HGVSp: aminoacid change
- CONSEQUENCE: molecular effects. 

However, if your VCF has been annotated with a different tool and you want to keep this information you’ll need to modify /pipelines/default/templates/template.json. Update the key names so they match the ones in your VCF and activate the template to true. (Note that using template.json TRUE will deactivate reading the VEP headers.) 
This way, once your beacon instance is running, you’ll be able to query it using these fields.


#### VCF pipelines for allele frequencies
To read allele frequency variables, there is the populations.json pipeline inside [pipelines](https://github.com/EGA-archive/beacon-data-tools/tree/main/pipelines/default/templates) folder.
In order to let Beacon2 RI Tools v2 read all the INFO column from your VCF and parse the allele frequency variants entries, you will need to add how are the different entries named for each annotation. You will have to tell how many populations are there in your VCF setting the numberOfPopulations value, if there are no allele frequencies in the VCF, then you will need to set it to 0, and if there are but no specific populations, then fill the populations with a “Total” name. 
You also have the option of populating your beacon with the allele frequency information of your variants. 

In order to let Beacon RI Tools v2 read the INFO column from your VCF and parse the allele frequency variants entries you’ll need to modify [population.json][(/](https://github.com/EGA-archive/beacon-data-tools/tree/main/pipelines/default/templates/population.json). 

Basic example of populations.json:
```bash
{

  "numberOfPopulations": 0,
  
  "source": "The Genome Aggregation Database (gnomAD)",
  
  "sourceReference": "gnomad.broadinstitute.org/",
    
      "populations": [
        
        {
            "population": "Total",
            
            "alleleFrequency": "AF_joint",
            
            "alleleCount": "AC_joint",
            
            "alleleCountHomozygous": "nhomalt_joint",
            
            "alleleCountHeterozygous": "",
            
            "alleleNumber": "AN_joint"
        }
    ]
}
```

With this populations.json you would be adding one population, Total, to the beacon. 

#### Converting data from .vcf.gz file

To convert data from .vcf.gz to .json you will need to copy all the .vcf.gz files you want to convert inside the [files_to_read folder](https://github.com/EGA-archive/beacon-data-tools/tree/main/files/vcf/files_to_read).

```bash
docker exec -it ri-tools python genomicVariations_vcf.py
```
After that, if needed, export your documents from mongoDB to a .json file using one of these two possible commands. 
First option will delete "_id" entries generated by mongoDB:
```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection genomicVariations | sed '/"_id":/s/"_id":[^,]*,//g' > genomicVariations.json
```
The second option, our **recommended one**, will keep the "_id" entries generated by mongoDB:
```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection genomicVariations > genomicVariations.json
```
This will generate the final .json file which is in Beacon Friendly Format (BFF). Bear in mind that this time, the file will be saved in the directory you are located, so if you want to save it in the output_docs folder, add it in the path of the mongoexport.

###  Populating a beacon instance from CSV files

The 7 beacon models can be populated from CSVs files: 

Runs
Datasets
Analyses
Cohorts
Biosamples
Individuals 
genomicVariations

To convert the metadata to BFF or to save the variants information without a VCF you will need to fill in the CSV [templates](https://github.com/EGA-archive/beacon-data-tools/tree/main/csv/templates). 

Please, bear in mind the following statements : 

1. Only “correctly spelled” fields will be inserted into the beacon, respect the column structure and naming of the files inside templates. 
2. Every new row will be appended to the final output file as a new and independent document. e.g 3. If in dataset.csv you have two rows you will be creating two independent datasets. 
If your data needs to be appended to the same document, it will have to be separated by ‘ | ‘ and written in the same row. For example, in genomicVariations, if several samples have the same variant you will need to fill in the caseLevelData as in [UPLOAD REDUCED VERSION CASE LEVEL DATA]. Note that you can leave the pipe empty or write the condition multiple times.
4. The info field for each collection is very generic and can be filled with different data, you will need to fill the column data directly with json type data. For copies and subjects for genomicVariations, json data is also needed.
5. Keep in mind that you don’t need to fill in all the columns. Some are optional, while others belong to specific Beacon specification options and may be incompatible with certain columns. If a column is misfilled, an exception will be raised. Beacon RI Tools v2 will only convert the columns that contain information, the rest can be removed if wanted.
These are the mandatory fields for each collection:
- Analyses: id, analysisDate and pipelineName
- Biosamples: id, biosampleStatus and sampleOriginType
- Cohorts: id, name and cohortType
- Datasets: id and name
- Individuals: id and sex
- Runs: id, biosampleID and runDate
6. The id field in Biosamples must match the samples ids in the VCF header.
7. The id field in Individuals can match or not the samples names in the VCF header. If it doesn’t match the field invidualsId field must be filled in Biosamples, mapping the ids in Individuals and the ids in the VCF.
8. The datasetId in Datasets must match the datasetId field in the conf.py (this requirement applies only in the Beacon Production Implementation environment).
9. Finally, remember that not all the different CSVs for the different collections have to be filled up. If a user does not have information for one collection, Beacon will not complain.

To get all the information about how to populate the CSVs, mandatory fields, descriptions… Please visit the [default schemas](https://github.com/ga4gh-beacon/beacon-v2/tree/main/models/json/beacon-v2-default-model) and [Beacon Specification](https://github.com/ga4gh-beacon/beacon-v2). 


#### Case Level Data conversion

If you are converting with the paramater **case_level_data** to True, this will add data into two collections: **targets** and **caseLevelData**. If you need to export the variants to insert them in another mongoDB, you will need to export these two collections as well, by executing the next commands:

```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection caseLevelData > caseLevelData.json
```
```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection targets > targets.json
```

#### Converting data from CSV files

Before the conversion, please make sure your [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/conf/conf.py), is reading the right .csv document(s). 

Execute the next bash script from the root folder in your terminal. All .csv files contained in the specified csv_folder will be transformed into .json:

```bash
docker exec -it ri-tools python convert_csvTObff.py
```

The Beacon Friendly Format JSONs will be generated in the output_docs folder, with the name of the collection followed by .json extension, e.g. genomicVariations.json. 

These BFF jsons will be used to populate a mongoDB for beacon usage. To know how to import thme into a Beacon v2, please do as described in [Beacon v2 PI api](https://github.com/EGA-archive/beacon2-pi-api).

### Populating a beacon instance from Phenopackets

This option will convert a Phenopacket v2 into Beacon Friendly Format Biosamples and Individuals models while preserving as much information as possible.

For detailed information about the mapping of properties between Phenopackets and Beacon schemas, please refer to this spreadsheet: [Beacon + Phenopackets Schemas](https://docs.google.com/spreadsheets/d/1DfkV5BwXzOggDl53-ofi7obnHT4O7J-rtUrnhZH2BiE/edit?gid=474476020#gid=474476020).

Most of the mapping between the Phenopackets and Beacon models was straightforward. However, some fields in the Phenopacket schema did not have a direct match in the Beacon schema.

Fields containing important metadata that could not be mapped to a specific Beacon property were stored in the additionalInformation (notes) field to preserve as much information as possible.

**Please bear in mind that this is a beta version. If you encounter issues or have questions, feel free to open an issue in the [GitHub repository](https://github.com/EGA-archive/phenopackets-to-BFF/issues).**

#### Specific Mappings

##### Individuals.diseases.notes:

The following Phenopacket fields related to diseases were saved in the notes field:

- resolution
- primary_site
- laterality
- excluded

##### Individuals.info:

The file.individual_to_file_identifiers field from Phenopackets is saved in the info property of the Beacon individual.

##### Biosamples.notes:

The biosamples.description field is stored in the notes field of the Beacon biosample.

#### Handling collectionData

The biosamples.timeOfCollection property in Phenopackets supports various data types, including:

- gestationalAge: Measure of the age of a pregnancy
- Age: Age as an ISO8601 duration (e.g., P40Y10M05D)
- AgeRange: Age within a given range
- OntologyClass: Age as an ontology class
- Timestamp: Specific date and time
- TimeInterval: Time interval

In contrast, the Beacon schema defines biosamples.collectionDate as the "Date of biosample collection in ISO8601 format" and expects a simple string.

To maximize data retention, the tool converts the collectionData from Phenopackets to a string and stores it in the collectionDate property of Beacon. While this approach does not fully align with the intended collectionDate field usage, it ensures valuable data is not lost.

#### Converting data from phenopackets

To convert a phenopacket into Biosamples and Individuals schemas first save the phenopacket in this folder: [phenopackets-to-BFF](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/phenopackets-to-BFF). 

And then run: 

```bash
docker exec phenopackets-to-BFF python working-w-phenopackets.py /usr/src/app/examples/phenopacket.json
```

Bear in mind that the path **/usr/src/app/examples** must remain unchanged. 

You'll find your BFFs in the same folder where you saved the phenopacket, [phenopackets-to-BFF](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/phenopackets-to-BFF).

### Version notes

* Other file names and distribution of folder and files is not supported.

### Acknowledgements

Thanks to all the [EGA archive](https://ega-archive.org/) team, and specially: 
* Jordi Rambla, for guiding, supporting, helping and making possible the development of this tool.
