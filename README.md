# Review of Livestock Population Data and Metadata from National Statistics Organizations 

National Statistics Organizations (NSOs) often collect livestock population data as part of annual or semi-annual surveys and censuses. 

A list of NSOs was collected from the Open Data Watch's [list of NSOs](https://opendatawatch.com/knowledge-partnership/%e2%80%8bnational-statistical-offices-online/). Each URL was visited to and when findable and available in English, livestock population data and metadata was collected.

This repository holds the data cleaning scripts used to harmonize the format of and profile livestock population data and metadata. 

The project is currently under development - more information about scripts and methodology will be added as the project continues.

## Get file formats

The first step of preprocessing is to get all file formats: 
`python get_file_formats.py ../raw_data ../logs`

Then, we figure out which of the excel files are workbooks and which are just one page. For any that are workbooks, we split the files up and place them in the preprocessing directory and create a log `workbooks.txt`

Author: Kassy Raymond
Email: kraymond@uoguelph.ca