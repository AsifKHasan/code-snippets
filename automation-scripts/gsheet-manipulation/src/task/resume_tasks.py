#!/usr/bin/env python3

import gspread
from gspread.exceptions import *
from gspread_formatting import *

from pprint import pprint

from helper.utils import *
from helper.logger import *


LABEL_TO_GROUP = {
  'Organization': 'name',
  'Position': 'position',
  'Job Summary': 'summary',
}

GROUP_SUBGROUP = {
}

GROUP_VALUE_INDEX = {
  'name': 1,
  'position': 1,
  'summary': 2,
}

JOB_HISTORY_NEW_WS_SPECS = {
  'num-columns': 5,
  'frozen-rows': 3,
  'frozen-columns': 0,

  'columns': {
    'A': {'size': 100}, 
    'B': {'size': 65}, 
    'C': {'size': 65}, 
    'D': {'size': 30}, 
    'E': {'size': 640}, 
  },

  'ranges': {
    'B1:B': {'weight': 'normal', 'halign': 'center', 'merge': False},
    'C1:C': {'weight': 'normal', 'halign': 'center', 'merge': False},
    'D1:D': {'weight': 'normal', 'halign': 'center', 'merge': False},
    'E1:E': {'weight': 'normal', 'halign': 'left', 'merge': False},

    'B3:B': {'date-format': 'yyyy-mmm', 'merge': False, 'weight': 'bold'},
    'C3:C': {'date-format': 'yyyy-mmm', 'merge': False, 'weight': 'bold'},

    'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new'},
    'B2:E2': {'value': 'content', 'weight': 'bold', 'halign': 'left'},

    'A3:H': {'valign': 'top', 'merge': False, 'wrap': True},

    'B3': {'value': 'From', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'weight': 'bold', 'note': '{"repeat-rows": 1}'},
    'C3': {'value': 'To', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'weight': 'bold'},
    'D3:E3': {'value': 'Employment history', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'halign': 'left', 'weight': 'bold'},

  },

  'cell-empty-markers': [
    'B3:E'
  ], 
}



''' modify 06-job-history to new format
'''
def create_06_job_history_new(gsheet):
    # get job-histories data from 06-job-history
    job_history_ws_name = '06-job-history'
    job_history_ws = gsheet.gspread_sheet.worksheet(job_history_ws_name)
    if job_history_ws is None:
        error(f".. worksheet {job_history_ws_name} not found")
        return

    # get the job-history list
    job_histories = job_history_from_06_job_history(job_history_ws)

    # duplicate the *06-job-history* as *06-job-history-NEW* worksheet
    target_ws_name = '06-job-history-NEW'
    info(f"duplicating .. worksheet {job_history_ws_name} as {target_ws_name}")
    target_ws = job_history_ws.duplicate(new_sheet_name=target_ws_name)
    if target_ws:
        info(f"duplicated  .. worksheet {job_history_ws_name} as {target_ws_name}")
    else:
        error(f"could not duplicate   {job_history_ws_name} as {target_ws_name}")
        return

    col_count = target_ws.col_count
    row_count = target_ws.row_count

    # add 4 new columns at the end (after D) E, F, G, H
    info(f"adding .. 4 new columns at E-H")
    target_ws.insert_cols([[], [], [], []], 2)
    col_count = col_count + 3
    info(f"added  .. 4 new columns at E-H")


    # add job_histories.count * 3 + rows at the end
    # HACK - for safety add 1000 rows at the end
    # target_ws.add_rows(job_histories.length * 3 + 1)
    info(f"adding .. 1000 new rows at the end")
    target_ws.add_rows(1000)
    row_count = row_count + 1000
    info(f"added  .. 1000 new rows at the end")


    # for each column
    info(f"resizing .. columns")
    for key, value in JOB_HISTORY_NEW_WS_SPECS['columns'].items():
        # resize the columns
        debug(f".. resizing column {key} to {value['size']}")
        set_column_width(target_ws, key, value['size'])

    info(f"resized  .. columns")


    # iterate over ranges and apply specs
    info(f"formatting .. pre-defined ranges")
    count = gsheet.work_on_ranges(target_ws, range_work_specs=JOB_HISTORY_NEW_WS_SPECS['ranges'])
    info(f"formatted  .. {count} pre-defined ranges")


    # iterate job-histories and create range_work_specs
    range_work_specs = {}
    current_row = 4
    index = 0
    info(f"generating .. dynamic ranges")
    for job_history in job_histories:
        block_start_row = current_row

        range_spec = ''

        # Organization - label
        range_spec = f"D{current_row}:E{current_row}"
        range_work_specs[range_spec] = {'value': 'Organization', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'}

        current_row = current_row + 1

        for s in job_history['name']:
            range_spec = f"D{current_row}:E{current_row}"
            range_work_specs[range_spec] = {'value': s, 'halign': 'left', 'weight': 'normal'}
            current_row = current_row + 1

        # Position - label
        range_spec = f"D{current_row}:E{current_row}"
        range_work_specs[range_spec] = {'value': 'Position', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'}

        current_row = current_row + 1

        for s in job_history['position']:
            range_spec = f"D{current_row}:E{current_row}"
            range_work_specs[range_spec] = {'value': s, 'halign': 'left', 'weight': 'normal'}
            current_row = current_row + 1

        # Job Summary - label
        range_spec = f"D{current_row}:E{current_row}"
        range_work_specs[range_spec] = {'value': 'Job Summary', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'}

        current_row = current_row + 1

        for s in job_history['summary']:
            range_spec = f"D{current_row}"
            range_work_specs[range_spec] = {'value': '•', 'halign': 'center'}
            range_spec = f"E{current_row}"
            range_work_specs[range_spec] = {'value': s, 'halign': 'left', 'weight': 'normal'}
            current_row = current_row + 1


        # job-history finished
        block_end_row = current_row - 1
        
        # From
        range_spec = f"B{block_start_row}:B{block_end_row}"
        # val = quote_number(job_history['from'])
        val = job_history['from']
        # debug(f".. From : {job_history['from']} -> {val}")
        range_work_specs[range_spec] = {'value': val, 'border-color': '#b7b7b7'}

        # To 
        range_spec = f"C{block_start_row}:C{block_end_row}"
        # val = quote_number(job_history['to'])
        val = job_history['to']
        # debug(f".. To   : {job_history['to']} -> {val}")
        range_work_specs[range_spec] = {'value': val, 'border-color': '#b7b7b7'}

        # border around column D and E
        range_spec = f"D{block_start_row}:E{block_end_row}"
        range_work_specs[range_spec] = {'border-color': '#b7b7b7', 'merge': False}

        index = index + 1


    info(f"generated  .. {index} dynamic ranges")

    # iterate over ranges and apply specs
    info(f"formatting .. dynamic ranges")
    count = gsheet.work_on_ranges(target_ws, range_work_specs=range_work_specs)
    info(f"formatted  .. {count} dynamic ranges")

    # remove last 3 columns
    info(f"removing .. last 3 columns")
    target_ws.delete_columns(6, 8)
    col_count = col_count - 3
    info(f"removed  .. last 3 columns")

    # remove all trailing blank rows
    info(f"removing .. trailing blank rows")
    gsheet.remove_trailing_blank_rows(target_ws, row_count)
    info(f"removed  .. trailing blank rows")

    # clear conditional formatting
    info(f"clearing .. all conditional formatting")
    gsheet.clear_conditional_format_rules(target_ws)
    info(f"cleared  .. all conditional formatting")

    # conditional formatting for blank cells
    info(f"adding .. conditional formatting for blank cells")
    gsheet.add_conditional_formatting_for_blank_cells(target_ws, JOB_HISTORY_NEW_WS_SPECS['cell-empty-markers'])
    info(f"added  .. conditional formatting for blank cells")

    # conditional formatting review-notes
    info(f"adding .. conditional formatting for review-notes")
    gsheet.add_conditional_formatting_for_review_notes(target_ws, row_count, col_count)
    info(f"added  .. conditional formatting for review-notes")

    info(f"freezing .. {JOB_HISTORY_NEW_WS_SPECS['frozen-rows']} rows and {JOB_HISTORY_NEW_WS_SPECS['frozen-columns']} columns")
    try:
        target_ws.freeze(JOB_HISTORY_NEW_WS_SPECS['frozen-rows'], JOB_HISTORY_NEW_WS_SPECS['frozen-columns'])
        info(f"freezed  .. {JOB_HISTORY_NEW_WS_SPECS['frozen-rows']} rows and {JOB_HISTORY_NEW_WS_SPECS['frozen-columns']} columns")
    except Exception as e:
        warn(str(e))

    

''' get job-histories data from '06-job-history'
'''
def job_history_from_06_job_history(job_history_ws):
    source_values = job_history_ws.get('B3:D')

    num_rows = len(source_values)
    current_row_index = 0
    job_histories = []
    new_job_history_found = False
    job_history = {}

    # loop until we have eaten up all rows
    while num_rows > current_row_index:
        current_row = source_values[current_row_index]
        # pprint(f"{current_row_index} : {current_row}")

        if len(current_row) > 0 and current_row[0] == 'Organization':
            # we have found the start of a new job-history

            # there may be a running job-history
            if len(job_history.keys()) != 0:
                job_history['end-row'] = current_row_index - 1
                job_histories.append(job_history)
                job_history = {}

            job_history['start-row'] = current_row_index

        current_row_index = current_row_index + 1

    # there may be a pending job-history
    if len(job_history.keys()) != 0:
        job_history['end-row'] = current_row_index - 1
        job_histories.append(job_history)

    # now we have a list of job-histories
    job_history_index = 0
    for job_history in job_histories:
        job_history['name'] = []
        job_history['position'] = []
        job_history['from'] = ''
        job_history['to'] = ''
        job_history['summary'] = []
        current_group = 'name'
        for i in range(job_history['start-row'], job_history['end-row'] + 1):
            row = source_values[i]

            # the row may be empty
            if len(row) == 0:
                continue

            # the group is the first value
            new_group_label = row[0]
            new_group_label = new_group_label.strip()

            if new_group_label == '':
                # previous group continuing
                value = row[GROUP_VALUE_INDEX[current_group]]

                # group may have subgroups
                if current_group in GROUP_SUBGROUP:
                    if value in GROUP_SUBGROUP[current_group]:
                        # the value is not value for the group rather it starts a subgroup
                        current_group = GROUP_SUBGROUP[current_group][value]

                    else:
                        # this is not a subgroup, append value
                        if value != '':
                            job_history[current_group] = job_history[current_group] + split_and_dress(value)

                else:
                    # the group does not have any subgroups, append value
                    if value != '':
                        job_history[current_group] = job_history[current_group] + split_and_dress(value)

            else:
                # a new group has started, get the group
                if new_group_label in LABEL_TO_GROUP:
                    current_group = LABEL_TO_GROUP[new_group_label]

                    # append value into the group
                    value = row[GROUP_VALUE_INDEX[current_group]]
                    if value != '':
                        job_history[current_group] = job_history[current_group] + split_and_dress(value)

                else:
                    # this must be the from value
                    job_history['from'] = new_group_label
                    job_history['to'] = row[2]


        # we should have at least one entry for each groups
        if len(job_history['name']) == 0:
            job_history['name'].append('')

        if len(job_history['position']) == 0:
            job_history['client'].append('')

        if len(job_history['summary']) == 0:
            job_history['task'].append('')

        if True:
            debug(f"project {job_history_index}")
            debug(f".. from     : {job_history['from']}")
            debug(f".. to       : {job_history['to']}")

            debug(f".. name     : {job_history['name'][0]}")
            for name in job_history['name'][1:]:
                debug(f"..          : {name}")

            debug(f".. position : {job_history['position'][0]}")
            for position in job_history['position'][1:]:
                debug(f"..          : {position}")

            debug(f".. summary  : {job_history['summary'][0]}")
            for summary in job_history['summary'][1:]:
                debug(f"..          : {summary}")

        job_history_index = job_history_index + 1


    return job_histories
