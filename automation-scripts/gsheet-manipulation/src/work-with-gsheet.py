#!/usr/bin/env python3

import argparse

from gsheet.gsheet_util import *
from helper.logger import *

def do_something(gsheet):
    worksheets = gsheet.worksheets()
    for ws in worksheets:
        info(ws.title)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gsheet", required=True, help="gsheet name to work with")
    args = vars(ap.parse_args())

    gsheet = open_gsheet(gsheet_name=args["gsheet"])
    if gsheet:
        do_something(gsheet)
