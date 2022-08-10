#!/usr/bin/env python3

import gspread
from gspread.exceptions import *
from gspread_formatting import *

from pprint import pprint

from helper.utils import *
from helper.logger import *


WORKSHEET_STRUCTURE = {
    '00-layout': {
        'index': 1,
        'num-rows': 34,
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,

        'columns': {
            'A': {'size': 100, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True}, 
            'B': {'size': 200, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True}, 
            'C': {'size': 200, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True}, 
            'D': {'size': 400, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True}, 
        },

        'review-notes': True,

        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new'},
            'A2': {'value': 'review-notes', 'weight': 'bold'},
            'B2:D2': {'value': 'content', 'weight': 'bold', 'merge': True},

            'B3:C3': {'value': 'Assignment Name:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D3': {'value': 'Country:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B4:C4': {'value': "='01-summary'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True},
            'D4': {'value': "='01-summary'!C4", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},


        },

        'cell-empty-markers': [
            'B3:D18'
        ], 
    },
}


WORKSHEET_SPECS = {
    '06-job-history': {
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
    },
    '-toc-new': {
        'frozen-rows': 2,
        'frozen-columns': 0,

        'columns': {
            'A': {'halign': 'center', 'size':  60, 'label': 'section'            , },
            'B': {'halign': 'left',   'size': 200, 'label': 'heading'            , },
            'C': {'halign': 'center', 'size':  80, 'label': 'process'            , 'validation-list': ['Yes']},
            'D': {'halign': 'center', 'size':  80, 'label': 'level'              , 'validation-list': ['0', '1', '2', '3', '4', '5', '6']},
            'E': {'halign': 'center', 'size':  80, 'label': 'content-type'       , 'validation-list': ['docx', 'gsheet', 'lof', 'lot', 'pdf', 'table', 'toc']},
            'F': {'halign': 'left',   'size': 200, 'label': 'link'               , },
            'G': {'halign': 'center', 'size':  80, 'label': 'break'              , 'validation-list': ['page', 'section']},
            'H': {'halign': 'center', 'size':  80, 'label': 'landscape'          , 'validation-list': ['Yes']},
            'I': {'halign': 'center', 'size':  80, 'label': 'page-spec'          , 'validation-list': ['A4', 'A3', 'Letter', 'Legal']},
            'J': {'halign': 'center', 'size':  80, 'label': 'margin-spec'        , 'validation-list': ['wide', 'medium', 'narrow', 'none']},
            'K': {'halign': 'center', 'size':  80, 'label': 'hide-pageno'        , 'validation-list': ['Yes']},
            'L': {'halign': 'center', 'size':  80, 'label': 'hide-heading'       , 'validation-list': ['Yes']},
            'M': {'halign': 'center', 'size':  80, 'label': 'different-firstpage', 'validation-list': ['Yes']},
            'N': {'halign': 'left',   'size':  80, 'label': 'header-first'       , },
            'O': {'halign': 'left',   'size':  80, 'label': 'header-odd'         , },
            'P': {'halign': 'left',   'size':  80, 'label': 'header-even'        , },
            'Q': {'halign': 'left',   'size':  80, 'label': 'footer-first'       , },
            'R': {'halign': 'left',   'size':  80, 'label': 'footer-odd'         , },
            'S': {'halign': 'left',   'size':  80, 'label': 'footer-even'        , },
            'T': {'halign': 'center', 'size':  80, 'label': 'override-header'    , 'validation-list': ['Yes']},
            'U': {'halign': 'center', 'size':  80, 'label': 'override-footer'    , 'validation-list': ['Yes']},
            'V': {'halign': 'left',   'size':  80, 'label': 'responsible'        , },
            'W': {'halign': 'left',   'size':  80, 'label': 'reviewer'           , },
            'X': {'halign': 'left',   'size': 160, 'label': 'status'             , 'validation-list': ['pending', 'under-documentation', 'ready-for-review', 'under-review', 'finalized']},
        },

        'cell-empty-markers': [
            'V3:W'
        ], 

    }    
}



''' create worksheets according to spec defined in WORKSHEET_STRUCTURE
'''
def create_worksheets(g_sheet, worksheet_name_list):
    for ws_name in worksheet_name_list:
        if (ws_name in WORKSHEET_STRUCTURE):
            info(f"creating worksheet {ws_name}", nesting_level=1)
          
            worksheet_created = create_worksheet(g_sheet=g_sheet, worksheet_name=ws_name, worksheet_struct=WORKSHEET_STRUCTURE[ws_name])  
            if worksheet_created:
                info(f"created  worksheet {ws_name}", nesting_level=1)
            
            else:
                info(f"worksheet {ws_name} already exists", nesting_level=1)

        else:
            warn(f"worksheet {ws_name} : structure not defined", nesting_level=1)



''' format worksheets according to spec defined in WORKSHEET_STRUCTURE
'''
def format_worksheets(g_sheet, worksheet_name_list):
    for ws_name in worksheet_name_list:
        if (ws_name in WORKSHEET_STRUCTURE):
            info(f"formatting worksheet {ws_name}", nesting_level=1)
          
            worksheet_formatted = format_worksheet(g_sheet=g_sheet, worksheet_name=ws_name, worksheet_struct=WORKSHEET_STRUCTURE[ws_name])  
            if worksheet_formatted:
                info(f"formatted  worksheet {ws_name}", nesting_level=1)
            
            else:
                info(f"worksheet {ws_name} could not be formatted", nesting_level=1)

        else:
            warn(f"worksheet {ws_name} : structure not defined", nesting_level=1)



''' create a worksheet according to spec defined in WORKSHEET_STRUCTURE
'''
def create_worksheet(g_sheet, worksheet_name, worksheet_struct):
    # the worksheet might exist
    worksheet = g_sheet.worksheet_by_name(worksheet_name=worksheet_name, suppress_log=True)
    if worksheet:
        return False


    # create the worksheet with right dimensions and in the right place with right freezing
    request = build_add_sheet_request(worksheet_name=worksheet_name, sheet_index=worksheet_struct['index'], num_rows=worksheet_struct['num-rows'], num_cols=worksheet_struct['num-columns'], frozen_rows=worksheet_struct['frozen-rows'], frozen_cols=worksheet_struct['frozen-columns'])

    g_sheet.update_in_batch(request_list=[request])


    # get the worksheet
    worksheet = g_sheet.worksheet_by_name(worksheet_name=worksheet_name)
    if not worksheet:
        return False


    # work on the columns - size, alignemnts, fonts and wrapping
    range_work_specs = {}

    # requests for column resizing
    column_resize_requests = worksheet.column_resize_request(column_specs=worksheet_struct['columns'])

    #  requests for column formatting
    for col_a1, work_spec in worksheet_struct['columns'].items():
        range_spec = f"{col_a1}:{col_a1}"
        range_work_specs[range_spec] = work_spec

    values, format_requests = worksheet.range_work_request(range_work_specs=range_work_specs)


    # will there be review-notes in the worksheet
    if worksheet_struct['review-notes']:
        conditional_format_requests = worksheet.conditional_formatting_for_review_notes_request(num_cols=worksheet_struct['num-columns'])
    else:
        conditional_format_requests = []


    # finally update in batch
    g_sheet.update_in_batch(request_list=column_resize_requests+format_requests+conditional_format_requests)


    return True



''' format a worksheet according to spec defined in WORKSHEET_STRUCTURE
'''
def format_worksheet(g_sheet, worksheet_name, worksheet_struct):
    # get the worksheet
    worksheet = g_sheet.worksheet_by_name(worksheet_name=worksheet_name)
    if not worksheet:
        return False


    # get the ranges and formatting requests
    worksheet_dict = g_sheet.worksheets_as_dict()
    values, format_requests = worksheet.range_work_request(range_work_specs=worksheet_struct['ranges'], worksheet_dict=worksheet_dict)


    # conditional formatting for blank cells
    conditional_format_requests = worksheet.conditional_formatting_for_blank_cells_request(range_specs=worksheet_struct['cell-empty-markers'])


    # update formats in batch
    g_sheet.update_in_batch(request_list=format_requests+conditional_format_requests)


    # update values in batch
    worksheet.update_values_in_batch(values=values)


    return True



''' modify 06-job-history to new format
'''
def create_06_job_history_new(gsheet):
    # get job-histories data from 06-job-history
    job_history_ws_name = '06-job-history'
    job_history_ws = gsheet.gspread_sheet.worksheet(job_history_ws_name)
    if job_history_ws is None:
        error(f"worksheet {job_history_ws_name} not found", nesting_level=1)
        return

    WORKSHEET_SPEC = WORKSHEET_SPECS['06-job-history']

    # get the job-history list
    job_histories = job_history_from_06_job_history(job_history_ws)

    # duplicate the *06-job-history* as *06-job-history-NEW* worksheet
    target_ws_name = '06-job-history-NEW'
    info(f"duplicating .. worksheet {job_history_ws_name} as {target_ws_name}", nesting_level=1)
    target_ws = job_history_ws.duplicate(new_sheet_name=target_ws_name)
    if target_ws:
        info(f"duplicated  .. worksheet {job_history_ws_name} as {target_ws_name}", nesting_level=1)
    else:
        error(f"could not duplicate   {job_history_ws_name} as {target_ws_name}", nesting_level=1)
        return

    col_count = target_ws.col_count
    row_count = target_ws.row_count


    # add 4 new columns at the end (after D) E, F, G, H and add job_histories.count * 3 + rows at the end
    # HACK - for safety add 1000 rows at the end
    cols_to_add_at, cols_to_add, rows_to_add_at, rows_to_add = 'B', 4, 'end', 1000
    info(f"adding .. {cols_to_add} new columns at {cols_to_add_at} and {rows_to_add} new rows at {rows_to_add_at}", nesting_level=1)
    gsheet.add_dimension(worksheet_id=target_ws.id, cols_to_add_at=cols_to_add_at, cols_to_add=cols_to_add, rows_to_add_at=rows_to_add_at, rows_to_add=rows_to_add)
    info(f"added  .. {cols_to_add} new columns at {cols_to_add_at} and {rows_to_add} new rows at {rows_to_add_at}", nesting_level=1)

    col_count = col_count + 4
    row_count = row_count + 1000


    # add 4 new columns at the end (after D) E, F, G, H
    # info(f"adding .. 4 new columns at E-H", nesting_level=1)
    # target_ws.insert_cols([[], [], [], []], 2)
    # col_count = col_count + 4
    # info(f"added  .. 4 new columns at E-H", nesting_level=1)


    # add job_histories.count * 3 + rows at the end
    # HACK - for safety add 1000 rows at the end
    # target_ws.add_rows(job_histories.length * 3 + 1)
    # info(f"adding .. 1000 new rows at the end", nesting_level=1)
    # target_ws.add_rows(1000)
    # row_count = row_count + 1000
    # info(f"added  .. 1000 new rows at the end", nesting_level=1)


    info(f"resizing .. columns", nesting_level=1)
    target_ws.resize_columns(WORKSHEET_SPEC['columns'])
    info(f"resized  .. columns", nesting_level=1)


    # iterate job-histories and create range_work_specs
    range_work_specs = {}
    current_row = 4
    index = 0
    info(f"generating .. dynamic ranges", nesting_level=1)
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


    info(f"generated  .. {index} dynamic ranges", nesting_level=1)

    # iterate over ranges and apply specs
    info(f"formatting .. ranges", nesting_level=1)
    count = gsheet.work_on_ranges(worksheet=target_ws, range_work_specs={**WORKSHEET_SPEC['ranges'], **range_work_specs})
    info(f"formatted  .. {count} ranges", nesting_level=1)


    # remove last 3 columns and trailing blank rows
    cols_to_remove_from, cols_to_remove_to = 'F', 'end'
    rows_to_remove_from, rows_to_remove_to = gsheet.trailing_blank_row_start_index(worksheet=target_ws), 'end'
    info(f"removing .. columns {cols_to_remove_from}-{cols_to_remove_to} and rows {rows_to_remove_from}-{rows_to_remove_to}", nesting_level=1)
    gsheet.remove_dimension(worksheet_id=target_ws.id, cols_to_remove_from=cols_to_remove_from, cols_to_remove_to=cols_to_remove_to, rows_to_remove_from=rows_to_remove_from, rows_to_remove_to=rows_to_remove_to)
    info(f"removed  .. columns {cols_to_remove_from}-{cols_to_remove_to} and rows {rows_to_remove_from}-{rows_to_remove_to}", nesting_level=1)


    # # remove last 3 columns
    # info(f"removing .. last 3 columns", nesting_level=1)
    # target_ws.delete_columns(6, 8)
    # col_count = col_count - 3
    # info(f"removed  .. last 3 columns", nesting_level=1)

    # # remove all trailing blank rows
    # info(f"removing .. trailing blank rows", nesting_level=1)
    # gsheet.remove_trailing_blank_rows(target_ws, row_count)
    # info(f"removed  .. trailing blank rows", nesting_level=1)


    # clear conditional formatting
    info(f"clearing .. all conditional formatting", nesting_level=1)
    gsheet.clear_conditional_format_rules(target_ws)
    info(f"cleared  .. all conditional formatting", nesting_level=1)


    # conditional formatting for blank cells
    info(f"adding .. conditional formatting for blank cells", nesting_level=1)
    gsheet.add_conditional_formatting_for_blank_cells(target_ws, WORKSHEET_SPEC['cell-empty-markers'])
    info(f"added  .. conditional formatting for blank cells", nesting_level=1)


    # conditional formatting review-notes
    info(f"adding .. conditional formatting for review-notes", nesting_level=1)
    gsheet.add_conditional_formatting_for_review_notes(target_ws, row_count, col_count)
    info(f"added  .. conditional formatting for review-notes", nesting_level=1)


    info(f"freezing .. {WORKSHEET_SPEC['frozen-rows']} rows and {WORKSHEET_SPEC['frozen-columns']} columns", nesting_level=1)
    try:
        target_ws.freeze(WORKSHEET_SPEC['frozen-rows'], WORKSHEET_SPEC['frozen-columns'])
        info(f"freezed  .. {WORKSHEET_SPEC['frozen-rows']} rows and {WORKSHEET_SPEC['frozen-columns']} columns", nesting_level=1)
    except Exception as e:
        warn(str(e))

    

''' get job-histories data from '06-job-history'
'''
def job_history_from_06_job_history(job_history_ws):
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
                group_value_index = GROUP_VALUE_INDEX[current_group]
                if len(row) > group_value_index:
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
                    group_value_index = GROUP_VALUE_INDEX[current_group]
                    if len(row) > group_value_index:
                        value = row[group_value_index]
                        if value != '':
                            job_history[current_group] = job_history[current_group] + split_and_dress(value)

                else:
                    # this must be the from value
                    job_history['from'] = new_group_label
                    if len(row) >= 3:
                        job_history['to'] = row[2]
                    else:
                        job_history['to'] = ''


        # we should have at least one entry for each groups
        if len(job_history['name']) == 0:
            job_history['name'].append('')

        if len(job_history['position']) == 0:
            job_history['position'].append('')

        if len(job_history['summary']) == 0:
            job_history['summary'].append('')

        if True:
            debug(f"project {job_history_index}", nesting_level=2)
            debug(f".. from     : {job_history['from']}", nesting_level=2)
            debug(f".. to       : {job_history['to']}", nesting_level=2)

            debug(f".. name     : {job_history['name'][0]}", nesting_level=2)
            for name in job_history['name'][1:]:
                debug(f"..          : {name}", nesting_level=2)

            debug(f".. position : {job_history['position'][0]}", nesting_level=2)
            for position in job_history['position'][1:]:
                debug(f"..          : {position}", nesting_level=2)

            debug(f".. summary  : {job_history['summary'][0]}", nesting_level=2)
            for summary in job_history['summary'][1:]:
                debug(f"..          : {summary}", nesting_level=2)

        job_history_index = job_history_index + 1


    return job_histories



''' create worksheet *-new-toc* from *-toc* worksheet
'''
def new_toc_from_toc(gsheet):
    # duplicate the *-toc* as *-toc-new* worksheet
    toc_ws_name = '-toc'
    toc_new_ws_name = '-toc-new'
    gsheet.duplicate_worksheet(worksheet_name_to_duplicate=toc_ws_name, new_worksheet_names=[toc_new_ws_name])

    # get the -toc-new worksheet
    toc_new_ws = gsheet.worksheet_by_name(toc_new_ws_name)
    if toc_new_ws is None:
        return

    requests = []

    # unhide all columns
    requests = requests + toc_new_ws.column_unhide_request()

    # if there are 20 columns in -toc-new, insert two columns at position 16 (Q) (override-header and override-footer)
    if (toc_new_ws.col_count() == 20):
        requests = requests + toc_new_ws.dimension_add_request(cols_to_add_at='Q', cols_to_add=2)


    # add 3 new columns after G - 'landscape', 'page-spec', 'margin-spec'. Column G we will use for 'break'
    requests = requests + toc_new_ws.dimension_add_request(cols_to_add_at='H', cols_to_add=3)

    WORKSHEET_SPEC = WORKSHEET_SPECS['-toc-new']


    #  resize columns
    requests = requests + toc_new_ws.column_resize_request(WORKSHEET_SPEC['columns'])


    # batch the requests
    gsheet.update_in_batch(request_list=requests)


    # for each column
    range_work_specs = {}
    requests = []
    info(f"generating .. dynamic ranges", nesting_level=1)
    for col_a1, col_data in WORKSHEET_SPEC['columns'].items():
        # change the labels in row 2
        if ('label' in col_data):
            range_spec = f"{col_a1}2"
            range_work_specs[range_spec] = {'value': col_data['label']}

        # set horizontal alignments
        if ('halign' in col_data):
            range_spec = f"{col_a1}:{col_a1}"
            range_work_specs[range_spec] = {'halign': col_data['halign']}

        # set validation rules
        range_spec = f"{col_a1}3:{col_a1}"
        requests = requests + toc_new_ws.data_validation_clear_request(range_spec)
        if ('validation-list' in col_data):
            requests = requests + toc_new_ws.data_validation_from_list_request(range_spec, col_data['validation-list'])


    # get the work range requests
    values, formats = toc_new_ws.range_work_request(range_work_specs=range_work_specs)
    requests = requests + formats


    range_spec = 'C3:U'
    vals_list = toc_new_ws.get_values(range=range_spec, major_dimension='ROWS')
    for row in vals_list:
        row_len = len(row)

        # for column C (process) (range C3:C), change values to blank if it is -
        col_idx = LETTER_TO_COLUMN['C'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''

        # for column I (page-spec) (range I3:I), change values to A4
        col_idx = LETTER_TO_COLUMN['I'] - 3
        if (col_idx < row_len):
            row[col_idx] = 'A4'


        # for column J (margin-spec) (range J3:J), change values to narrow
        col_idx = LETTER_TO_COLUMN['J'] - 3
        if (col_idx < row_len):
            row[col_idx] = 'narrow'

        # for column K (hide-pageno) (range K3:K), change values to Yes if it is No
        col_idx = LETTER_TO_COLUMN['K'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''
            elif (row[col_idx] == 'No'):
                row[col_idx] = 'Yes'


        # for column L (hide-heading) (range L3:L), change values to blank if it is -
        col_idx = LETTER_TO_COLUMN['L'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''

        # for column M (different-firstpage) (range M3:M), change values to blank if it is -
        col_idx = LETTER_TO_COLUMN['M'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''

        # for column T (override-header) (range T3:T), change values to blank if it is -
        col_idx = LETTER_TO_COLUMN['T'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''

        # for column U (override-footer) (range U3:U), change values to blank if it is -
        col_idx = LETTER_TO_COLUMN['U'] - 3
        if (col_idx < row_len):
            if (row[col_idx] == '-'):
                row[col_idx] = ''

        # for column H (landscape) (range H3:H), change values to Yes if column G contains landscape
        # for column G (break) (range G3:G), change values to blank if it is -, change to section if it contains newpage
        col_idx_g = LETTER_TO_COLUMN['G'] - 3
        col_idx_h = LETTER_TO_COLUMN['H'] - 3
        if (col_idx_h < row_len):
            if (row[col_idx_g] == '-'):
                row[col_idx_g] = ''

            elif (row[col_idx_g].endswith('_landscape')):
                row[col_idx_h] = 'Yes'

            if (row[col_idx_g].startswith('newpage_')):
                row[col_idx_g] = 'section'

            if (row[col_idx_g].startswith('continuous_')):
                row[col_idx_g] = ''


    values.append({'range': range_spec, 'values': vals_list})

    # clear conditional formatting
    requests = requests + toc_new_ws.conditional_formatting_rules_clear_request()

    # conditional formatting for blank cells
    requests = requests + toc_new_ws.conditional_formatting_for_blank_cells_request(WORKSHEET_SPEC['cell-empty-markers'])

    #  freeze rows and columns
    requests = requests + toc_new_ws.dimension_freeze_request(frozen_rows=WORKSHEET_SPEC['frozen-rows'], frozen_cols=WORKSHEET_SPEC['frozen-columns'])


    value_count = len(values)
    format_count = len(requests)

    info(f"generated  .. {value_count} dynamic values", nesting_level=1)
    info(f"generated  .. {format_count} dynamic formats", nesting_level=1)

    info(f"formatting .. ranges", nesting_level=1)
    gsheet.update_in_batch(request_list=requests)
    info(f"formatted  .. {format_count} ranges", nesting_level=1)

    info(f"updating   .. ranges", nesting_level=1)
    toc_new_ws.update_values_in_batch(values=values)
    info(f"updated    .. {value_count} ranges", nesting_level=1)
