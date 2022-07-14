#!/usr/bin/env python3

import gspread
from gspread.exceptions import *

from helper.logger import *


''' open a gsheet
'''
def open_gsheet(gsheet_name):
    gc = gspread.service_account(filename='../conf/credential.json')
    sh = gc.open(gsheet_name)
    return sh



''' work on a range as per work specification
'''
def work_on_range(range, work_spec):
    pass