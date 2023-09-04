import pandas as pd
import sys
import os
import profile_datasets as prod

in_dir = sys.argv[1]
out_dir = sys.argv[2]

files = os.listdir(in_dir)

file_formats = []

for i in files: 
    file_formats.append(prod.detect_format(i))

df = pd.DataFrame(file_formats, columns = ['file','format'])

# Get all formats 
formats = df['format'].unique().tolist()

# Get list of files of all formats for logs 
df_grouped = df.groupby('format')

# Combine xls and xlsx formats 
df_xls = df_grouped.get_group('xls').reset_index(drop=True)
df_xlsx = df_grouped.get_group('xlsx').reset_index(drop=True)
df_xl = pd.concat([df_xls,df_xlsx])

# Of the xls or xlsx files, which are workbooks that have multiple pages? 
workbooks = []
xl_files = []

for i in df_xl['file']:
    i_file = ('%s/%s') % (in_dir, i)
    if prod.calc_wb_tab(i_file) == 1:
        workbooks.append(i)
    else:
        xl_files.append(i)

# Create files 
outfile_wb = '%s/xl_workbooks.txt' % out_dir
pd.Series(workbooks).to_csv(outfile_wb, index = False, header = False)

outfile_xl = '%s/xl.txt' % out_dir
pd.Series(xl_files).to_csv(outfile_xl, index = False, header = False)

# Remove excel formats since we deal with those above 
# Remove DS Store if it exists
if 'DS_Store' in formats:
    formats.remove('DS_Store')

for i in ['xls','xlsx']: 
    formats.remove(i)

for i in formats:
    dff = df_grouped.get_group(i)
    file_filtered = dff['file']
    outfile = '%s/%s_files.txt' % (out_dir, i)
    file_filtered.to_csv(outfile, index=False, header=False)


    


