#!/usr/bin/env python3

import pandas as pd

# the xlsx file to be used as source, assuming that the xlsx is in the same directory of this script
ATTENDANCE_XLSX = './attendance-record.xlsx'
ATTENDANCE_WS_NAME = 'attendance'
HEADER_ROW = 0

# read the xlsx (one specfic worksheet) into a pandas dataframe, assuming that the column names are in the row specified
attendance_df = pd.read_excel(ATTENDANCE_XLSX, ATTENDANCE_WS_NAME, HEADER_ROW)

# how many rows (attendance entry) are there?
# there are multiple methods, we can take the shape (dimensions of the df) which is a touple of integers (rows, columns)
attendance_entry_count = attendance_df.shape[0]
print('total {0} attendance found'.format(attendance_entry_count))

# the shape returns physical rows even empty rows if there is any, so we use count which actually counts only rows value is not blank or NA
# count can give a count for each column as a Series
# we assume that valid entry means User ID column is not blank or NA
valid_entry_count = attendance_df.count()['User ID']
print('total {0} valid attendance found'.format(valid_entry_count))
