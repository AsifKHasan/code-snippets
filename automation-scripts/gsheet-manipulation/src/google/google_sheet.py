#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from helper.utils import *
from helper.logger import *


COLUMN_TO_LETTER = ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

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
    def bulk_duplicate_worksheet(self):
        worksheet_name_to_duplicate = 'z-blank'
        new_worksheet_names = ['04.01-৩১', '04.01-৩২', '04.02-৩৩', '04.02-৩৪', '04.03-৩৫', '04.03-৩৬']

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



    ''' link cells to worksheets where cells values are names of worksheets
    '''
    def link_cells_to_worksheet(self):
        worksheet_name = '-toc-new'
        range_spec_for_cells_to_link = 'F3:F'

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
        debug(f".. deleting : {rows_to_delete} rows starting from row {row_to_delete_from}")
        worksheet.delete_rows(row_to_delete_from, row_count)
        debug(f".. deleted  : {rows_to_delete} rows starting from row {row_to_delete_from}")



    ''' clear conditional format rules from the worksheet
    '''
    def clear_conditional_format_rules(self, worksheet):
        rules = get_conditional_format_rules(worksheet)
        rules.clear()
        rules.save()
        
        
        
    ''' conditional formatting for blank cells
    '''
    def add_conditional_formatting_for_blank_cells(self, worksheet, range_specs):
        pass



    ''' conditional formatting for blank cells
    '''
    def add_conditional_formatting_for_review_notes(self, worksheet, row_count, col_count):
        range_spec = f"A3:{COLUMN_TO_LETTER[col_count]}"
        range = a1_range_to_grid_range(range_spec)

        condition = BooleanCondition('CUSTOM_FORMULA', ['=not(isblank($A:$A))'])
        cell_format = CellFormat(backgroundColor=Color.fromHex('#f4cccc'))
        boolean_rule = BooleanRule(condition=condition, format=cell_format)
        rule = ConditionalFormatRule(ranges=[range], booleanRule=boolean_rule)

        rules = get_conditional_format_rules(worksheet)
        rules.append(rule)
        rules.save()



    ''' work on a range work specs for value and format updates
    '''
    def work_on_ranges(self, worksheet, range_work_specs):
        count = 0
        formats = []
        values = []
        merges = []
        for range_spec, work_spec in range_work_specs.items():
            if 'value' in work_spec:
                values.append({'range': range_spec, 'values': [[work_spec['value']]]})

            merge = True
            if 'merge' in work_spec:
                merge = work_spec['merge']

            if merge:
                merges.append({'mergeCells': {'range': a1_range_to_grid_range(range_spec, sheet_id=worksheet.id), 'mergeType': 'MERGE_ALL'}})

            repeat_cell = repeatcell_from_work_spec(a1_range_to_grid_range(range_spec, sheet_id=worksheet.id), work_spec)
            if repeat_cell:
                formats.append(repeat_cell)

            count = count + 1

        # batch update values
        worksheet.batch_update(values)

        # batch merges
        self.update_in_batch(merges)
        
        # batch formats
        self.update_in_batch(formats)
        
        return count

