# Review of Livestock Population Data and Metadata from National Statistics Organizations 

National Statistics Organizations (NSOs) often collect livestock population data as part of annual or semi-annual surveys and censuses. 

A list of NSOs was collected from the Open Data Watch's [list of NSOs](https://opendatawatch.com/knowledge-partnership/%e2%80%8bnational-statistical-offices-online/). Each URL was visited to and when findable and available in English, livestock population data and metadata was collected.

This repository holds the data cleaning scripts used to harmonize the format of and profile livestock population data and metadata. 

The project is currently under development - more information about scripts and methodology will be added as the project continues.

## Get information about data collected

The `get_info.py` program in the `scripts_data` directory provides information about all the data that was collected including: 

* How many files were collected
* The number of countries we have data from, and how many data files from each 
* The file formats that the data are in, and how many of each

Run `python get_info.py` for all information to be printed in terminal.

## Get file formats

* The first step of preprocessing is to get all file formats: 
`python get_file_formats.py ../raw_data ../logs`

* Then, we figure out which of the excel files are workbooks and which are just one page. For any that are workbooks, we split the files up and place them in the preprocessing directory and create a log `workbooks.txt`

* csv_files.txt, ods_files.txt, pdf_files.txt etc. provide a list of the files that are in a given format

## Handle files 

### ods files

* There was only one ods file in this analysis so it is handled independently in `ods.py`


Author: Kassy Raymond
Email: kraymond@uoguelph.ca