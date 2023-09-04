import os
import pandas as pd
import sys
import numpy as np 

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
    Calculate the number of tabs in a workbook. Returns names of files that have more than one tab.
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

def parse_excel_sheet(file, sheet_name, threshold=5):
    '''parses multiple tables from an excel sheet into multiple data frame objects. Returns [dfs, df_mds], where dfs is a list of data frames and df_mds their potential associated metadata'''
    xl = pd.ExcelFile(file, sheet_name=sheet_name)
    entire_sheet = xl.parse(sheet_name=sheet_name)

    # count the number of non-Nan cells in each row and then the change in that number between adjacent rows
    n_values = np.logical_not(entire_sheet.isnull()).sum(axis=1)
    n_values_deltas = n_values[1:] - n_values[:-1].values

    # define the beginnings and ends of tables using delta in n_values
    table_beginnings = n_values_deltas > threshold
    table_beginnings = table_beginnings[table_beginnings].index
    table_endings = n_values_deltas < -threshold
    table_endings = table_endings[table_endings].index
    if len(table_beginnings) < len(table_endings) or len(table_beginnings) > len(table_endings)+1:
        raise BaseException('Could not detect equal number of beginnings and ends')

    # look for metadata before the beginnings of tables
    md_beginnings = []
    for start in table_beginnings:
        md_start = n_values.iloc[:start][n_values==0].index[-1] + 1
        md_beginnings.append(md_start)

    # make data frames
    dfs = []
    df_mds = []
    for ind in range(len(table_beginnings)):
        start = table_beginnings[ind]+1
        if ind < len(table_endings):
            stop = table_endings[ind]
        else:
            stop = entire_sheet.shape[0]
        df = xl.parse(sheet_name=sheet_name, skiprows=start, nrows=stop-start)
        dfs.append(df)

        md = xl.parse(sheet_name=sheet_name, skiprows=md_beginnings[ind], nrows=start-md_beginnings[ind]-1).dropna(axis=1)
        df_mds.append(md)
    return dfs, df_mds

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
    
