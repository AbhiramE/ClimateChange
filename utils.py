from __future__ import print_function
import pandas as pd
import logging as log

def read_output(file_name, header_row=0, skip_rows=2, delim=r"\s+"):
    '''
    Method to read the output file (fort.22)
    
    ----
    Args:
    file_name: The path to the output file
    header_row: The index of the header_row (index considered
    after the skip_rows have been removed)
    skip_rows: The number of rows from the beginning to skip. It can
    also be a tuple of ints denoting which rows to remove specifically
    delim: The delimiter for the file , default is whitespace
    '''
    df=pd.read_csv(file_name,header=header_row,delimiter=delim, skiprows=skip_rows)
    df=df[:-1] # Remove the last row which contains some summary
    return


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)
