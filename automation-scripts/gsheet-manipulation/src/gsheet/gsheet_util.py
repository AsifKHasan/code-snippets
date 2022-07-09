#!/usr/bin/env python3

import gspread

from helper.logger import *

''' open a gsheet
'''
def open_gsheet(gsheet_name):
    gc = gspread.service_account(filename='../conf/credential.json')
    sh = gc.open(gsheet_name)
    return sh


