#!/usr/bin/env python3

import argparse

from google.google_service import GoogleService
from google.google_sheet import GoogleSheet

from task.resume_tasks import *

from helper.logger import *

def do_something(gsheet):
    # bulk_duplicate_worksheet(gsheet)
    # order_worksheets(gsheet)
    # link_cells_to_worksheet(gsheet)

    # BEGIN resume related
    create_06_job_history_new(gsheet)
    # END   resume related


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gsheet", required=True, help="gsheet name to work with")
    args = vars(ap.parse_args())

    google_service = GoogleService('../conf/credential.json')
    gsheet = GoogleSheet.open(google_service, gsheet_name=args["gsheet"])
    if gsheet:
        do_something(gsheet)
