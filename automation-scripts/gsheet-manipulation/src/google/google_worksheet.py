#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from helper.utils import *
from helper.logger import *


COLUMN_TO_LETTER = ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LETTER_TO_COLUMN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 
    'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26
}


''' Google worksheet wrapper
'''
class GoogleWorksheet(object):

    ''' constructor
    '''
    def __init__(self, gspread_worksheet, gsheet):
        self.gspread_worksheet = gspread_worksheet
        self.gsheet = gsheet
        self.id = self.gspread_worksheet.id



    ''' bulk create multiple worksheets by duplicating this worksheet 
    '''
    def duplicate_worksheet(self, new_worksheet_names):
        request_list = []
        for worksheet_name in new_worksheet_names:
            info(f"duplicating worksheet {self.gspread_worksheet.title} as {worksheet_name}")
            request_list.append(build_duplicate_sheet_request(worksheet_id=self.id, new_worksheet_name=worksheet_name))

        if len(request_list):
            self.gsheet.update_in_batch(request_list=request_list)
            info(f"duplicated  worksheet {self.gspread_worksheet.title} to {len(request_list)} worksheets")
        


    ''' add dimensions
    '''
    def add_dimension(self, worksheet_id, cols_to_add_at=None, cols_to_add=0, rows_to_add_at=None, rows_to_add=0):
        requests = []
        if cols_to_add_at and cols_to_add:
            # columns to be added
            if cols_to_add_at == 'end':
                # columns to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=worksheet_id, dimension='COLUMNS', length=rows_to_add))

            else:
                # columns to be inserted at some index
                requests.append(build_insert_dimension_request(worksheet_id=worksheet_id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_add_at]-1, length=cols_to_add, inherit_from_before=False))

        if rows_to_add_at and rows_to_add:
            # rows to be added
            if rows_to_add_at == 'end':
                # rows to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=worksheet_id, dimension='ROWS', length=rows_to_add))

            else:
                # rows to be inserted at some index
                requests.append(build_insert_dimension_request(worksheet_id=worksheet_id, dimension='ROWS', start_index=rows_to_add_at, length=rows_to_add, inherit_from_before=True))

        if len(requests) > 0:
            self.update_in_batch(requests)



    ''' add dimensions
    '''
    def remove_dimension(self, worksheet_id, cols_to_remove_from=None, cols_to_remove_to=None, rows_to_remove_from=None, rows_to_remove_to=None):
        requests = []
        if cols_to_remove_from and cols_to_remove_to:
            # columns to be removed
            if cols_to_remove_to == 'end':
                # columns to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=worksheet_id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1))

            else:
                # columns to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=worksheet_id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1, end_index=LETTER_TO_COLUMN[cols_to_remove_to]))

        if rows_to_remove_from and rows_to_remove_to:
            # rows to be removed
            if rows_to_remove_to == 'end':
                # rows to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=worksheet_id, dimension='ROWS', start_index=LETTER_TO_COLUMN[rows_to_remove_from]-1))

            else:
                # rows to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=worksheet_id, dimension='ROWS', start_index=LETTER_TO_COLUMN[rows_to_remove_from]-1, end_index=LETTER_TO_COLUMN[rows_to_remove_to]))

        if len(requests) > 0:
            self.update_in_batch(requests)



    ''' rename a worksheet
    '''
    def rename_worksheet(self, new_worksheet_name):
        try:
            info(f"renaming worksheet {self.gspread_worksheet.title} to {new_worksheet_name}")
            self.gspread_worksheet.update_title(new_worksheet_name)
            info(f"renamed  worksheet {self.gspread_worksheet.title} to {new_worksheet_name}")

        except:
            warn(f"worksheet {self.gspread_worksheet.title} could not be renamed to {new_worksheet_name}")
        


    ''' link cells to worksheets where cells values are names of worksheets
    '''
    def link_cells_to_worksheet(self, range_spec_for_cells_to_link, worksheet_dict={}):
        range_to_work_on = self.gspread_worksheet.range(range_spec_for_cells_to_link)
        range_work_specs = {}
        for cell in range_to_work_on:
            if cell.value == '':
                warn(f"cell {cell.address:>5} is empty .. skipping")
            else:
                info(f"cell {cell.address:>5} to be linked with worksheet [{cell.value}]")
                range_work_specs[cell.address] = {'value': cell.value, 'ws-name-to-link': cell.value}

        count = self.work_on_ranges(range_work_specs=range_work_specs, worksheet_dict=worksheet_dict)



    ''' get start_index of trailing blank rows from the worksheet
    '''
    def trailing_blank_row_start_index(self, worksheet):
        # we first need to know what is the last row having some value
        values = worksheet.get_values()
        return len(values)



    ''' clear conditional format rules from the worksheet
    '''
    def clear_conditional_format_rules(self, worksheet):
        rules = get_conditional_format_rules(worksheet)
        rules.clear()
        rules.save()
        
        
        
    ''' conditional formatting for blank cells
    '''
    def add_conditional_formatting_for_blank_cells(self, worksheet, range_specs):
        ranges = [a1_range_to_grid_range(range_spec, sheet_id=worksheet.id) for range_spec in range_specs] 
        rule = build_conditional_format_rule(ranges=ranges, condition_type="BLANK", condition_values=[], format={"backgroundColor": hex_to_rgba("#fff2cc")})
        self.update_in_batch(rule)



    ''' conditional formatting for blank cells
    '''
    def add_conditional_formatting_for_review_notes(self, worksheet, row_count, col_count):
        range_spec = f"A3:{COLUMN_TO_LETTER[col_count]}"
        range = a1_range_to_grid_range(range_spec, sheet_id=worksheet.id)

        rule = build_conditional_format_rule(ranges=[range], condition_type="CUSTOM_FORMULA", condition_values=["=not(isblank($A:$A))"], format={"backgroundColor": hex_to_rgba("#f4cccc")})
        self.update_in_batch(rule)



    ''' work on a range work specs for value and format updates
    '''
    def work_on_ranges(self, range_work_specs={}, worksheet_dict={}):
        count = 0
        formats = []
        values = []
        merges = []
        borders = []
        for range_spec, work_spec in range_work_specs.items():
            # value
            if 'value' in work_spec:
                values.append({'range': range_spec, 'values': [[build_value_from_work_spec(work_spec=work_spec, worksheet_dict=worksheet_dict)]]})

            # merge
            merge = True
            if 'merge' in work_spec:
                merge = work_spec['merge']

            if merge:
                merges.append({'mergeCells': {'range': a1_range_to_grid_range(range_spec, sheet_id=self.id), 'mergeType': 'MERGE_ALL'}})

            # formats
            repeat_cell = build_repeatcell_from_work_spec(a1_range_to_grid_range(range_spec, sheet_id=self.id), work_spec)
            if repeat_cell:
                formats.append(repeat_cell)

            # borders
            if 'border-color' in work_spec:
                broder_object = {'range': a1_range_to_grid_range(range_spec, sheet_id=self.id)}
                borders.append({'updateBorders': {**broder_object, **build_border_around_spec(work_spec['border-color'])}})


            count = count + 1

        # batch update values
        if len(values):
            self.gspread_worksheet.batch_update(values, value_input_option=ValueInputOption.user_entered)

        # batch merges
        if len(merges):
            self.gsheet.update_in_batch(merges)
        
        # batch formats
        if len(formats):
            self.gsheet.update_in_batch(formats)
        
        # batch formats
        if len(borders):
            self.gsheet.update_in_batch(borders)

        return count



    ''' resize columns as per spec
    '''
    def resize_columns(self, worksheet, column_specs):
        dimension_update_requests = []
        for key, value in column_specs.items():
            # debug(f".. resizing column {key} to {value['size']}", nesting_level=2)
            # set_column_width(target_ws, key, value['size'])
            # dimension_update_request = build_dimension_update_request(sheet_id=worksheet.id, dimension='COLUMN', index=gspread.utils.column_letter_to_index(key), size=value['size'])
            dimension_update_request = build_dimension_update_request(sheet_id=worksheet.id, dimension='COLUMNS', index=LETTER_TO_COLUMN[key], size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        # batch dimension updates
        if len(dimension_update_requests):
            self.update_in_batch(dimension_update_requests)
