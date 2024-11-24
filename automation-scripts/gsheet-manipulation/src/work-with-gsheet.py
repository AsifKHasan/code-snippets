#!/usr/bin/env python3

import json
import yaml
import time
import argparse

from ggle.google_service import GoogleService

from helper.logger import *

from task.common_tasks import *
from task.resume_tasks import *

final_list = []

def execute_gsheet_tasks(g_sheet, g_service, gsheet_tasks=[], worksheet_names=[], destination_gsheet_names=[], work_specs={}, find_replace_patterns=[]):
    for gsheet_task_def in gsheet_tasks:
        task_name = gsheet_task_def['task']
        if hasattr(g_sheet, task_name) and callable(getattr(g_sheet, task_name)):
            # arguments
            args_dict = {}
            for k, v in gsheet_task_def.items():
                if k == 'task':
                    pass

                elif k == 'worksheet_names' and v == True:
                    args_dict[k] = worksheet_names

                elif k == 'destination_gsheet_names' and v == True:
                    args_dict[k] = destination_gsheet_names

                elif k == 'work_specs' and v == True:
                    args_dict[k] = work_specs

                elif k == 'find_replace_patterns' and v == True:
                    args_dict[k] = find_replace_patterns

                else:
                    args_dict[k] = v


            # execute the task
            try:
                task = getattr(g_sheet, task_name)
                debug(f"executing task [{task_name}]")
                task(**args_dict)
                debug(f"executed  task [{task_name}]")
            except Exception as e:
                error(str(e))

        else:
            error(f"g_sheet has no method [{task_name}]")



def work_on_gsheet(g_sheet, g_service, worksheet_names=[], destination_gsheet_names=[], work_specs={}, find_replace_patterns=[]):

    # BEGIN work on worksheet dimensions
    # -----------------------------------------------------------------------------------

    # add rows
    for worksheet_name in worksheet_names:
        # worksheet = g_sheet.worksheet_by_name(worksheet_name=worksheet_name, suppress_log=True)
        # num_rows, num_cols = worksheet.number_of_dimesnions()
        # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name, suppress_log=True)

        # if num_rows == 5:
        #     g_sheet.add_rows(worksheet_name=worksheet_name, rows_to_add_at='end', rows_to_add=1)
        # else:
        #     print(f"[{g_sheet.title:<50}]: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")
        #     pass

        pass

    # add columns
    for worksheet_name in worksheet_names:
        # worksheet = g_sheet.worksheet_by_name(worksheet_name=worksheet_name, suppress_log=True)
        # num_rows, num_cols = worksheet.number_of_dimesnions()
        # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name, suppress_log=True)

        # if num_cols == 5:
        #     g_sheet.add_columns(worksheet_name=worksheet_name, cols_to_add_at='end', cols_to_add=1)
        # else:
        #     print(f"[{g_sheet.title:<50}]: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")
        #     pass

        pass

    # -----------------------------------------------------------------------------------
    # END   work on worksheet dimensions

    # global final_list
    # final_list = list(set(final_list) | set(g_sheet.list_worksheets()))
    # print(final_list)

    # g_sheet.format_worksheets(worksheet_names=worksheet_names)
    # g_sheet.create_worksheets(worksheet_names=worksheet_names)

    # BEGIN common tasks
    # new_toc_from_toc(g_sheet)
    # END   common tasks

    # BEGIN adhoc tasks
    # populate_range(g_sheet=g_sheet)
    # insert_a_row_with_values(g_sheet=g_sheet)
    # END   adhoc tasks

    # BEGIN resume specific tasks
    # border_and_merge_based_on_column(g_sheet=g_sheet, worksheet_names=['02-career-highlight'], range_spec='B3:Z', grouping_columns=1)
    # border_and_merge_based_on_column(g_sheet=g_sheet, worksheet_names=['04-managerial-expertise', '05-technical-expertise'], range_spec='B4:Z', grouping_columns=1)
    # border_and_merge_based_on_column(g_sheet=g_sheet, worksheet_names=['06-job-history', '07-project-roles', '07-project-roles-RHD-TMC'], range_spec='B4:Z', grouping_columns=2)
    # END   resume specific tasks

    # BEGIN PDS specific tasks
    # border_and_merge_based_on_column(g_sheet=g_sheet, worksheet_names=['06-description', '07-functionality', '08-technology', '09-services', '10-process'], range_spec='B3:Z', grouping_columns=1)
    # border_and_merge_based_on_column(g_sheet=g_sheet, worksheet_names=['05-people'], range_spec='B3:Z', grouping_columns=2)
    # END   PDS specific tasks

    # BEGIN drive/file related
    # g_sheet.share(email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # END   drive/file related

    pass


def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related

    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')

    # END   drive file related
    pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with", default=argparse.SUPPRESS)
    args = vars(ap.parse_args())

    # read config.yml to get the list of gsheets and other data
    config = yaml.load(open('../conf/data.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    if 'gsheet' in args and args["gsheet"] != '':
        gsheet_names = [args["gsheet"]]
    else:
        gsheet_names = config['gsheets']

    credential_json = config['credential-json']
    destination_gsheet_names = config.get('destination-gsheet-names', [])
    gsheet_tasks = config.get('gsheet-tasks', [])
    worksheet_names = config.get('worksheet-names', [])
    work_specs = config.get('work-specs', {})
    find_replace_patterns = config.get('find-replace-patterns', [])

    g_service = GoogleService(credential_json)

    count = 0
    num_gsheets = len(gsheet_names)
    for gsheet_name in gsheet_names:
        count = count + 1
        try:
            info(f"processing {count:>4}/{num_gsheets} gsheet {gsheet_name}")
            g_sheet = g_service.open(gsheet_name=gsheet_name)
        except Exception as e:
            g_sheet = None
            warn(str(e))
            # raise e

        if g_sheet:
            execute_gsheet_tasks(g_sheet=g_sheet, g_service=g_service, gsheet_tasks=gsheet_tasks, worksheet_names=worksheet_names, destination_gsheet_names=destination_gsheet_names, work_specs=work_specs, find_replace_patterns=find_replace_patterns)
            # work_on_gsheet(g_sheet=g_sheet, g_service=g_service, worksheet_names=worksheet_names, destination_gsheet_names=destination_gsheet_names, work_specs=work_specs, find_replace_patterns=find_replace_patterns)
            # work_on_drive(g_service=g_service, g_sheet=g_sheet)
            info(f"processed  {count:>4}/{num_gsheets} gsheet {gsheet_name}\n")

        wait_for = 30
        if count % 500 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)
