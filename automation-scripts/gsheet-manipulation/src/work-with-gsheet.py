#!/usr/bin/env python3

import argparse

from gsheet.gsheet_util import *

from task.gsheet_tasks import *
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

    gsheet = open_gsheet(gsheet_name=args["gsheet"])
    if gsheet:
        do_something(gsheet)
