#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from helper.utils import *
from helper.logger import *


COLUMN_TO_LETTER = ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LETTER_COLUMN_TO = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 
    'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

''' Google sheet wrapper
'''
class GoogleSheet(object):

    ''' constructor
    '''
    def __init__(self, google_service):
        self.service = google_service
        self.gspread_sheet = None



    ''' open a gsheet
    '''
    @classmethod
    def open(cls, google_service, gsheet_name):
        c = cls(google_service)
        c.gspread_sheet = c.service.gspread.open(gsheet_name)
        return c



    ''' update spreadsheet in batch
    '''
    def update_in_batch(self, request_body):
        self.gspread_sheet.batch_update(body={'requests': request_body})    



    ''' bulk create multiple worksheets by duplicating a given worksheet 
    '''
    def bulk_duplicate_worksheet(self, worksheet_name_to_duplicate, new_worksheet_names):
        try:
            worksheet_to_duplicate = self.gspread_sheet.worksheet(worksheet_name_to_duplicate)

            for worksheet_name in new_worksheet_names:
                # check existence of the worksheet
                try:
                    ws = self.gspread_sheet.worksheet(worksheet_name)
                    warn(f"worksheet {worksheet_name} already exists")

                except:
                    info(f"duplicating worksheet {worksheet_name_to_duplicate} as {worksheet_name}")
                    worksheet_to_duplicate.duplicate(new_sheet_name=worksheet_name)
                    info(f"duplicated  worksheet {worksheet_name_to_duplicate} as {worksheet_name}")
        
        except WorksheetNotFound as e:
            error(f"worksheet {worksheet_name_to_duplicate} not found")



    ''' order the worksheets of the gsheet alphabetically
    '''
    def order_worksheets(self):
        info(f"ordering worksheets for {self.gspread_sheet.title}")
        reordered_worksheets = sorted(self.gspread_sheet.worksheets(), key=lambda x: x.title, reverse=False)
        self.gspread_sheet.reorder_worksheets(reordered_worksheets)
        info(f"ordered  worksheets for {self.gspread_sheet.title}")



    ''' rename a worksheet
    '''
    def rename_worksheet(self, worksheet_name, new_worksheet_name):
        try:
            worksheet_to_rename = self.gspread_sheet.worksheet(worksheet_name)

            # check existence of the new_worksheet_name
            try:
                ws = self.gspread_sheet.worksheet(new_worksheet_name)
                warn(f"worksheet {worksheet_name} already exists")

            except:
                info(f"renaming worksheet {worksheet_name} to {new_worksheet_name}")
                worksheet_to_rename.update_title(new_worksheet_name)
                info(f"renamed  worksheet {worksheet_name} to {new_worksheet_name}")
        
        except WorksheetNotFound as e:
            error(f"worksheet {worksheet_name} not found")



    ''' link cells to worksheets where cells values are names of worksheets
    '''
    def link_cells_to_worksheet(self, worksheet_name, range_spec_for_cells_to_link):
        try:
            worksheet_to_work_on = self.gspread_sheet.worksheet(worksheet_name)

            # get the cells to link
            range_to_work_on = worksheet_to_work_on.range(range_spec_for_cells_to_link)
            for cell in range_to_work_on:
                if cell.value == '':
                    warn(f"cell {cell.address:>5} is empty .. skipping")
                else:
                    info(f"cell {cell.address:>5} value is [{cell.value}]")
                    # see if the value is the name of any worksheet
                    try:
                        worksheet_to_link_to = self.gspread_sheet.worksheet(cell.value)
                        
                        # it is a valid worksheet, link the cell to this worksheet
                        info(f".. linking {cell.address:>5} to worksheet [{cell.value}]")

                        # TODO: do the linking
                        worksheet_to_work_on.update(cell.address, f'=HYPERLINK("#gid={worksheet_to_link_to.id}", "{cell.value}")', raw=False)

                        info(f".. linked  {cell.address:>5} to worksheet [{cell.value}]")

                    except WorksheetNotFound as e:
                        warn(f".. [{cell.value}] is not a valid worksheet .. skipping")
        
        except WorksheetNotFound as e:
            error(f"worksheet {worksheet_name} not found")



    ''' delete trailing blank rows from the worksheet
    '''
    def remove_trailing_blank_rows(self, worksheet, row_count):
        # we first need to know what is the last row having some value
        values = worksheet.get_values()
        rows_with_value = len(values)

        row_to_delete_from = rows_with_value + 1
        rows_to_delete = row_count - rows_with_value
        debug(f"  .. deleting : {rows_to_delete} rows starting from row {row_to_delete_from}")
        worksheet.delete_rows(row_to_delete_from, row_count)
        debug(f"  .. deleted  : {rows_to_delete} rows starting from row {row_to_delete_from}")



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
    def work_on_ranges(self, worksheet_name=None, worksheet=None, range_work_specs={}):
        if worksheet is None:
            try:
                worksheet = self.gspread_sheet.worksheet(worksheet_name)
            
            except WorksheetNotFound as e:
                error(f"worksheet {worksheet_name} not found")
                return 0

        count = 0
        formats = []
        values = []
        merges = []
        borders = []
        for range_spec, work_spec in range_work_specs.items():
            # value
            if 'value' in work_spec:
                values.append({'range': range_spec, 'values': [[build_value_from_work_spec(work_spec, self.gspread_sheet)]]})

            # merge
            merge = True
            if 'merge' in work_spec:
                merge = work_spec['merge']

            if merge:
                merges.append({'mergeCells': {'range': a1_range_to_grid_range(range_spec, sheet_id=worksheet.id), 'mergeType': 'MERGE_ALL'}})

            # formats
            repeat_cell = build_repeatcell_from_work_spec(a1_range_to_grid_range(range_spec, sheet_id=worksheet.id), work_spec)
            if repeat_cell:
                formats.append(repeat_cell)

            # borders
            if 'border-color' in work_spec:
                broder_object = {'range': a1_range_to_grid_range(range_spec, sheet_id=worksheet.id)}
                borders.append({'updateBorders': {**broder_object, **build_border_around_spec(work_spec['border-color'])}})


            count = count + 1

        # batch update values
        if len(values):
            worksheet.batch_update(values, value_input_option=ValueInputOption.user_entered)

        # batch merges
        if len(merges):
            self.update_in_batch(merges)
        
        # batch formats
        if len(formats):
            self.update_in_batch(formats)
        
        # batch formats
        if len(borders):
            self.update_in_batch(borders)

        return count



    ''' resize columns as per spec
    '''
    def resize_columns(self, worksheet, column_specs):
        dimension_update_requests = []
        for key, value in column_specs.items():
            # debug(f".. resizing column {key} to {value['size']}", nesting_level=2)
            # set_column_width(target_ws, key, value['size'])
            # dimension_update_request = build_dimension_update_request(sheet_id=worksheet.id, dimension='COLUMN', index=gspread.utils.column_letter_to_index(key), size=value['size'])
            dimension_update_request = build_dimension_update_request(sheet_id=worksheet.id, dimension='COLUMNS', index=LETTER_COLUMN_TO[key], size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        # batch dimension updates
        if len(dimension_update_requests):
            self.update_in_batch(dimension_update_requests)
