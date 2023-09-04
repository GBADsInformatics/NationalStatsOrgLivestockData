## The purpose of this script is to get information about which countries we have data for 

import pandas as pd
import sys 
import os

# Get list of files in the data dir 
files = os.listdir('../raw_data')

# Number of files 
n_files = len(files)
print('There were %d files collected' % n_files)

countries = []
# Number of countries 
for i in files: 
    country = i.split('_')[1]
    countries.append(country)

# Get number of unique countries 
countries = pd.Series(countries)

u_countries = countries.unique()
n_countries = len(u_countries)

print('Data for %d countries was collected: %s' % (n_countries, u_countries))

# Types of file formats 
file_format = []

for i in files: 
    format = i.split('.')[1]
    file_format.append(format)

file_format = pd.Series(file_format)

u_file_format = file_format.unique()
n_file_format = len(u_file_format)

print('There are %d unique file formats including: %s' % (n_file_format, u_file_format))
