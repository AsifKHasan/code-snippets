#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from helper.utils import *
from helper.logger import *
from pprint import pprint


''' Google worksheet wrapper
'''
class GoogleWorksheet(object):

    ''' constructor
    '''
    def __init__(self, google_service, gspread_worksheet, gsheet):
        self.service = google_service
        self.gspread_worksheet = gspread_worksheet
        self.gsheet = gsheet
        self.id = self.gspread_worksheet.id



    ''' get values
    '''
    def get_col_values(self, col_a1):
        return self.gspread_worksheet.col_values(LETTER_TO_COLUMN[col_a1])



    ''' get values
    '''
    def get_values(self, range, major_dimension):
        return self.gspread_worksheet.get(range, major_dimension=major_dimension, value_render_option=ValueRenderOption.formatted)



    ''' get values in batch
    '''
    def get_values_in_batch(self, ranges, major_dimension):
        return self.gspread_worksheet.batch_get(ranges, major_dimension=major_dimension, value_render_option=ValueRenderOption.formatted)



    ''' update values in batch
    '''
    def update_values_in_batch_old(self, values):
        response = None
        try:
            response = self.gspread_worksheet.batch_update(values, value_input_option=ValueInputOption.user_entered)
        except Exception as e:
            print(e)



    ''' copy worksheet to another gsheet
    '''
    def copy_worksheet_to_gsheet(self, destination_gsheet):
        try:
            info(f"copying worksheet        {self.gspread_worksheet.title} to {destination_gsheet.title}")
            response = self.gspread_worksheet.copy_to(destination_gsheet.id)
            # rename the newly copied worksheet
            if response:
                info(f"copied  worksheet        {self.gspread_worksheet.title} to {destination_gsheet.title}")

                try:
                    new_gspread_worksheet = destination_gsheet.gspread_sheet.worksheet(response['title'])
                    info(f"renaming worksheet [{response['title']}] to [{self.gspread_worksheet.title}]")
                    new_gspread_worksheet.update_title(self.gspread_worksheet.title)
                    info(f"renamed  worksheet [{response['title']}] to [{self.gspread_worksheet.title}]")

                except:
                    warn(f"worksheet [{response['title']}] could not be renamed to [{self.gspread_worksheet.title}]")


        except:
            warn(f"could not copy worksheet {self.gspread_worksheet.title} to {destination_gsheet.title}")



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



    ''' rename a worksheet
    '''
    def rename_worksheet(self, new_worksheet_name):
        old_worksheet_name = self.gspread_worksheet.title
        try:
            info(f"renaming worksheet [{old_worksheet_name}] to [{new_worksheet_name}]")
            self.gspread_worksheet.update_title(new_worksheet_name)
            info(f"renamed  worksheet [{old_worksheet_name}] to [{new_worksheet_name}]")

        except:
            warn(f"worksheet [{old_worksheet_name}] could not be renamed to [{new_worksheet_name}]")



    ''' dimensions add request
    '''
    def dimension_add_request(self, cols_to_add_at=None, cols_to_add=0, rows_to_add_at=None, rows_to_add=0):
        requests = []
        if cols_to_add_at and cols_to_add:
            # columns to be added
            if cols_to_add_at == 'end':
                # columns to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=self.id, dimension='COLUMNS', length=rows_to_add))

            else:
                # columns to be inserted at some index
                requests.append(build_insert_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_add_at]-1, length=cols_to_add, inherit_from_before=False))

        if rows_to_add_at and rows_to_add:
            # rows to be added
            if rows_to_add_at == 'end':
                # rows to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=self.id, dimension='ROWS', length=rows_to_add))

            else:
                # rows to be inserted at some index
                requests.append(build_insert_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_add_at, length=rows_to_add, inherit_from_before=True))

        return requests



    ''' dimensions remove request
    '''
    def dimension_remove_request(self, cols_to_remove_from=None, cols_to_remove_to=None, rows_to_remove_from=None, rows_to_remove_to=None):
        requests = []
        if cols_to_remove_from and cols_to_remove_to:
            # columns to be removed
            if cols_to_remove_to == 'end':
                # columns to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1))

            else:
                # columns to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1, end_index=LETTER_TO_COLUMN[cols_to_remove_to]))

        if rows_to_remove_from and rows_to_remove_to:
            # rows to be removed
            if rows_to_remove_to == 'end':
                # rows to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_remove_from))

            else:
                # rows to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_remove_from, end_index=rows_to_remove_to))

        return requests



    ''' link cells to drive files request where cells values are names of drive files
    '''
    def cell_to_drive_file_link_request(self, range_specs_for_cells_to_link):
        range_work_specs = {}
        for range_spec in range_specs_for_cells_to_link:
            range_to_work_on = self.get_range(range_spec=range_spec)
            for cell in range_to_work_on:
                if cell.value == '':
                    warn(f"cell {cell.address:>5} is empty .. skipping")
                else:
                    info(f"cell {cell.address:>5} to be linked with drive file [{cell.value}]")
                    range_work_specs[cell.address] = {'value': cell.value, 'file-name-to-link': cell.value}

        return self.range_work_request(range_work_specs=range_work_specs)


    ''' get a range from a1 notation
    '''
    def get_range(self, range_spec, try_for=3):
        wait_for = 30
        for try_count in range(1, try_for+1):
            try:
                ws_range = self.gspread_worksheet.range(range_spec)
                debug(f"get range passed in [{try_count}] try", nesting_level=1)
                return ws_range
            except Exception as e:
                print(e)
                warn(f"get range failed in [{try_count}] try, trying again in {wait_for} seconds", nesting_level=1)
                time.sleep(wait_for)

        return None



    ''' link cells to worksheets request where cells values are names of worksheets
    '''
    def cell_to_worksheet_link_request(self, range_specs_for_cells_to_link, worksheet_dict={}):
        range_work_specs = {}
        for range_spec in range_specs_for_cells_to_link:
            range_to_work_on = self.get_range(range_spec=range_spec)
            for cell in range_to_work_on:
                if cell.value == '':
                    warn(f"cell {cell.address:>5} is empty .. skipping")
                else:
                    info(f"cell {cell.address:>5} to be linked with worksheet [{cell.value}]")
                    range_work_specs[cell.address] = {'value': cell.value, 'ws-name-to-link': cell.value}

        return self.range_work_request(range_work_specs=range_work_specs, worksheet_dict=worksheet_dict)



    ''' get start_index of trailing blank rows from the worksheet
    '''
    def trailing_blank_row_start_index(self):
        # we first need to know what is the last row having some value
        values = self.gspread_worksheet.get_values()
        return len(values)



    ''' clear conditional format rules from the worksheet
    '''
    def conditional_formatting_rules_clear_request(self):
        requests = []

        return requests



    ''' find and replace in worksheet
    '''
    def find_and_replace(self, find_replace_patterns):
        find_replace_requests = []
        for pattern in find_replace_patterns:
            search_for = pattern['find']
            replace_with = pattern['replace-with']
            request = build_find_replace_request(worksheet_id=self.id, search_for=search_for, replace_with=replace_with)
            if request:
                find_replace_requests.append(request)

        return find_replace_requests


    ''' put column size in pixels in row 1 for all columns except A
    '''
    def column_pixels_in_top_row(self, column_sizes):
        # for coumns B to end
        range_work_specs = {}
        values = []
        requests = []
        for col_num in range(1, self.col_count()):
            cell_a1 = f"{column_to_letter(col_num + 1)}1"
            column_width = column_sizes[self.gspread_worksheet.title][col_num]
            range_work_specs[cell_a1] = {'value': column_width, 'halign': 'center'}

        return self.range_work_request(range_work_specs=range_work_specs, worksheet_dict={})


    ''' remove trailing blank rows
    '''
    def remove_trailing_blank_rows(self):
        rows_to_remove_from, rows_to_remove_to = self.trailing_blank_row_start_index(), 'end'
        request_list = self.dimension_remove_request(rows_to_remove_from=rows_to_remove_from, rows_to_remove_to=rows_to_remove_to)

        info(f"removing .. rows {rows_to_remove_from}-{rows_to_remove_to}", nesting_level=1)
        if len(request_list):
            self.gsheet.update_in_batch(request_list=request_list)

        info(f"removed  .. rows {rows_to_remove_from}-{rows_to_remove_to}", nesting_level=1)



    ''' conditional formatting request for blank cells
    '''
    def conditional_formatting_for_blank_cells_request(self, range_specs):
        ranges = [a1_range_to_grid_range(range_spec, sheet_id=self.id) for range_spec in range_specs]
        rule = build_conditional_format_rule(ranges=ranges, condition_type="BLANK", condition_values=[], format={"backgroundColor": hex_to_rgba("#fff2cc")})

        return [rule]



    ''' conditional formatting request for blank cells
    '''
    def conditional_formatting_for_review_notes_request(self, num_cols):
        range_spec = f"A3:{COLUMN_TO_LETTER[num_cols]}"
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_conditional_format_rule(ranges=[range], condition_type="CUSTOM_FORMULA", condition_values=["=not(isblank($A:$A))"], format={"backgroundColor": hex_to_rgba("#f4cccc")})

        return [rule]



    ''' data validation from list request
    '''
    def data_validation_from_list_request(self, range_spec, values, input_message=None):
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_data_validation_rule(range=range, condition_type='ONE_OF_LIST', condition_values=values, input_message=input_message)

        return [rule]



    ''' data validation from list request
    '''
    def data_validation_clear_request(self, range_spec):
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_no_data_validation_rule(range=range)

        return [rule]



    ''' work on a range work specs requests for value and format updates
    '''
    def range_work_request(self, range_work_specs={}, worksheet_dict={}):
        formats = []
        values = []
        merges = []
        borders = []
        for range_spec, work_spec in range_work_specs.items():
            # value
            if 'value' in work_spec:
                values.append({'range': f"'{self.gspread_worksheet.title}'!{range_spec}", 'values': [[build_value_from_work_spec(work_spec=work_spec, worksheet_dict=worksheet_dict, google_service=self.service)]]})

            # merge
            merge = False
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

        return values, merges + formats + borders



    ''' resize columns request as per spec
    '''
    def column_resize_request(self, column_specs):
        dimension_update_requests = []
        for key, value in column_specs.items():
            # debug(f".. resizing column {key} to {value['size']}", nesting_level=2)
            # set_column_width(target_ws, key, value['size'])
            # dimension_update_request = build_dimension_size_update_request(sheet_id=worksheet.id, dimension='COLUMN', index=gspread.utils.column_letter_to_index(key), size=value['size'])
            dimension_update_request = build_dimension_size_update_request(sheet_id=self.id, dimension='COLUMNS', index=LETTER_TO_COLUMN[key], size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' resize rows request as per spec
    '''
    def row_resize_request(self, row_specs):
        dimension_update_requests = []
        for key, value in row_specs.items():
            dimension_update_request = build_dimension_size_update_request(sheet_id=self.id, dimension='ROWS', index=int(key), size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' unhide columns request
    '''
    def column_unhide_request(self):
        dimension_update_requests = []
        col_count = self.gspread_worksheet.col_count

        # to unhide all columns we need to know the number of columns
        dimension_update_request = build_dimension_visibility_update_request(sheet_id=self.id, dimension='COLUMNS', start_index=0, end_index=col_count, hide=False)
        dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' hide columns request
    '''
    def column_hide_request(self, column_keys):
        dimension_update_requests = []

        # to unhide all columns we need to know the number of columns
        for key in column_keys:
            end_index = LETTER_TO_COLUMN[key]
            start_index = end_index - 1
            dimension_update_request = build_dimension_visibility_update_request(sheet_id=self.id, dimension='COLUMNS', start_index=start_index, end_index=end_index, hide=True)
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' freeze row and column request
    '''
    def dimension_freeze_request(self, frozen_rows=None, frozen_cols=None):
        requests = []

        if frozen_rows is not None:
            request = build_row_freeze_request(sheet_id=self.id, frozen_rows=frozen_rows)
            requests.append(request)

        if frozen_cols is not None:
            request = build_column_freeze_request(sheet_id=self.id, frozen_cols=frozen_cols)
            requests.append(request)

        return requests



    ''' number of rows and columns of the worksheet
    '''
    def number_of_dimesnions(self):
        return self.gspread_worksheet.row_count, self.gspread_worksheet.col_count



    ''' number of rows of the worksheet
    '''
    def row_count(self):
        row_count, _ = self.number_of_dimesnions()
        return row_count



    ''' number of columns of the worksheet
    '''
    def col_count(self):
        _, col_count = self.number_of_dimesnions()
        return col_count
