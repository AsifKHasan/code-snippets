#!/usr/bin/env python3

import pandas as pd
import numpy as np; np.random.seed(sum(map(ord, 'calmap')))
import matplotlib.pyplot as plt
import calmap
from datetime import datetime
from calendar import monthrange
from dateutil import parser

def acquire_data():
    # the xlsx file to be used as source, assuming that the xlsx is in the same directory of this script
    ATTENDANCE_XLSX = './attendance-record.xlsx'
    ATTENDANCE_WS_NAME = 'attendance'
    HEADER_ROW = 0

    # read the xlsx (one specfic worksheet) into a pandas dataframe, assuming that the column names are in the row specified
    df = pd.read_excel(ATTENDANCE_XLSX, ATTENDANCE_WS_NAME, HEADER_ROW)

    return df

def prepare_data(raw_attendance_df):
    # discard columns that we do not need
    df = raw_attendance_df[['Department', 'Name', 'Date/Time', 'Status', 'Operation', 'Exception Description', 'Identification Code', 'Identification', 'Device No.']]

    # get the min and max date ()
    min_date = parser.parse(df['Date/Time'].min())
    max_date = parser.parse(df['Date/Time'].max())

    # start from the first day of month and end at last day of month
    min_date = min_date.replace(day=1)
    max_date = max_date.replace(day=monthrange(max_date.year, max_date.month)[1])

    # a series for holding the days in that range so that we can plot them
    all_days = pd.date_range(start=min_date, end=max_date, freq='D')

    # get attendance count for the days
    attendance_count_by_day = count_attendance(df, all_days)

    return attendance_count_by_day

def produce_result(data_df):
    fig, _ = calmap.calendarplot(data_df, monthticks=1, daylabels='MTWTFSS', dayticks=[0, 1, 2, 3, 4, 5, 6], cmap='YlGn', fillcolor='grey', linewidth=1, fig_kws=dict(figsize=(8, 4)))
    fig.savefig('calendar_heatmap.pdf', bbox_inches='tight')

'''
    TODO: this is the function you need to change
    the random numbers should be replaced with actual attendance counts from the raw_atendance_data
'''
def count_attendance(raw_attandance_df, all_days):
    # we just generate some random numbers for attedance count now
    days = np.random.choice(all_days, 1000)
    attendance_count_by_day = pd.Series(np.random.randn(len(days)), index=days)
    
    return attendance_count_by_day

if __name__ == '__main__':
    attendance_df = acquire_data()
    data_df = prepare_data(attendance_df)
    produce_result(data_df)
