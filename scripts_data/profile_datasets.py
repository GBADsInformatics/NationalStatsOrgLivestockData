import os
import pandas as pd
import sys
import numpy as np 

def detect_format(file_name):
    """
    detects file format and returns a tuple of the file name and the format
    """
    format = file_name.split('.')[1]

    return(file_name, format)


def detect_excel(files): 
    """
    Detects excel files from a list of files.
    """
    excel = []

    for i in files: 
        format = i.split('.')[1]
        if format == 'xlsx' or format == 'xls':
            excel.append(i)

    return(excel)


def calc_wb_tab(file):
    """
    Calculate the number of tabs in a workbook. Returns 1 if has more than one tab
    """
    df = pd.ExcelFile(file)

    sheets = df.sheet_names

    if len(sheets) > 1: 
        return(1)
    else:
        return(0)
    
def split_tab_save(file, outpath):
    """
    Splits excel sheets that have multiple tabs into multiple files.
    """
    df = pd.ExcelFile(file)

    sheets = df.sheet_names

    in_file = os.path.basename(file)

    nSheets = 0

    for i in sheets:
        nSheets = nSheets + 1
        df = pd.read_excel(open(file, 'rb'),
                      sheet_name=i)
        out_file = outpath + in_file.split('.')[0] + '_' + str(nSheets) + '.csv'
        if not df.empty:
            df.to_csv(out_file, index = False)

def detect_start_end(df):

    """
    Finds the start and end of datasets and potential metadata start/end
    """

    # Find number of values that are not null 
    n_values = np.logical_not(df.isnull()).sum(axis=1)

    # Get max number (number of columns)
    max = n_values.max()

    # Define where table likely starts and ends 
    table_start_end = n_values >= (max-1)

    # Define where metadata might be 
    md_start_end = n_values <= (max-1)

    # Cols to keep 
    indexes = table_start_end[table_start_end].index

    # Potential metadata indices 
    md_indexes = md_start_end[md_start_end].index

    return(indexes, md_indexes)

if __name__ == "__main__":

    if len(sys.argv) != 3: 
        sys.exit('Please provide an input and output path')

    path = sys.argv[1]
    outpath = sys.argv[2]

    files = os.listdir(path)

    excel_files = detect_excel(files)
    
    n_excel_files = len(excel_files)

    files_tabs = []

    # Determine which files have multiple tabs 
    for i in excel_files:
        file = path + i
        if calc_wb_tab(file) == 1:
            files_tabs.append(file)

    print("There are %d excel files" % (n_excel_files))
    print("There are %d excel files with multiple tabs" % len(files_tabs))
    print("The files with multiple tabs include: ")

    for i in files_tabs: 
        print('\n')
        print('%s' % i)
        split_tab_save(i, outpath)
    
