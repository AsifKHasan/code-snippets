#!/usr/bin/env python

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from ggle.google_worksheet import GoogleWorksheet

from helper.utils import *
from helper.logger import *
import pprint


''' Google sheet wrapper
'''
class GoogleSheet(object):

    ''' constructor
    '''
    def __init__(self, google_service, gspread_sheet):
        self.service = google_service
        self.gspread_sheet = gspread_sheet
        self.id = self.gspread_sheet.id
        self.title = self.gspread_sheet.title


    ''' get column sizes
    '''
    def get_column_sizes(self):
        request = self.service.gsheet_service.spreadsheets().get(spreadsheetId=self.id, includeGridData=False)
        response = request.execute()
        print(response)

        return column_sizes


    ''' copy worksheet to another gsheet
    '''
    def copy_worksheet_to_gsheet(self, destination_gsheet, worksheet_name_to_copy):
        worksheet_to_copy = self.worksheet_by_name(worksheet_name_to_copy)
        if worksheet_to_copy:
            worksheet_to_copy.copy_worksheet_to_gsheet(destination_gsheet)


    ''' update spreadsheet in batch
    '''
    def update_in_batch(self, request_list):
        try:
            self.gspread_sheet.batch_update(body={'requests': request_list})
        except Exception as e:
            print(e)



    ''' share a gsheet
    '''
    def share(self, email, perm_type, role):
        self.gspread_sheet.share(email_address=email, perm_type=perm_type, role=role, notify=False)



    ''' get worksheet by name
    '''
    def worksheet_by_name(self, worksheet_name, suppress_log=False):
        try:
            ws = self.gspread_sheet.worksheet(worksheet_name)
            return GoogleWorksheet(google_service=self.service, gspread_worksheet=ws, gsheet=self)

        except:
            if not suppress_log:
                warn(f"worksheet {worksheet_name} not found", nesting_level=1)

            return None



    ''' returns a dict {worksheet_name, worksheet_id}
    '''
    def worksheets_as_dict(self):
        gspread_worksheets = self.gspread_sheet.worksheets()
        worksheet_dict = { gspread_worksheet.title : gspread_worksheet.id for gspread_worksheet in gspread_worksheets }
        return worksheet_dict



    ''' order the worksheets of the gsheet alphabetically
    '''
    def order_worksheets(self):
        info(f"ordering worksheets for {self.gspread_sheet.title}", nesting_level=1)
        reordered_worksheets = sorted(self.gspread_sheet.worksheets(), key=lambda x: x.title, reverse=False)
        self.gspread_sheet.reorder_worksheets(reordered_worksheets)
        info(f"ordered  worksheets for {self.gspread_sheet.title}", nesting_level=1)



    ''' rename a worksheet
    '''
    def rename_worksheet(self, worksheet_name, new_worksheet_name):
        worksheet_to_rename = self.worksheet_by_name(worksheet_name)
        if worksheet_to_rename:
            worksheet_to_rename.rename_worksheet(new_worksheet_name)



    ''' remove a worksheet
    '''
    def remove_worksheet(self, worksheet_names_to_remove):
        for worksheet_name in worksheet_names_to_remove:
            worksheet_to_remove = self.worksheet_by_name(worksheet_name)
            if worksheet_to_remove:
                try:
                    info(f"removing worksheet {worksheet_name}", nesting_level=1)
                    self.gspread_sheet.del_worksheet(worksheet_to_remove)
                    info(f"removed  worksheet {worksheet_name}", nesting_level=1)

                except:
                    info(f"worksheet {worksheet_name} could not be removed", nesting_level=1)



    ''' bulk create multiple worksheets by duplicating a given worksheet
    '''
    def duplicate_worksheet(self, worksheet_name_to_duplicate, new_worksheet_names):
        worksheet_to_duplicate = self.worksheet_by_name(worksheet_name_to_duplicate)
        if worksheet_to_duplicate:
            worksheet_to_duplicate.duplicate_worksheet(new_worksheet_names)



    ''' link cells of a worksheet to drive files where cells values are names of drive files
    '''
    def link_cells_to_drive_files(self, worksheet_name, range_specs_for_cells_to_link):
        worksheet_to_work_on = self.worksheet_by_name(worksheet_name)
        if worksheet_to_work_on:
            worksheet_to_work_on.link_cells_to_drive_files(range_specs_for_cells_to_link=range_specs_for_cells_to_link)



    ''' link cells of a worksheet to worksheets where cells values are names of worksheets
    '''
    def link_cells_to_worksheet(self, worksheet_name, range_specs_for_cells_to_link):
        worksheet_to_work_on = self.worksheet_by_name(worksheet_name)
        if worksheet_to_work_on:
            worksheet_dict = self.worksheets_as_dict()
            worksheet_to_work_on.link_cells_to_worksheet(range_specs_for_cells_to_link=range_specs_for_cells_to_link, worksheet_dict=worksheet_dict)



    ''' work on a (list of) worksheet's range of work specs for value and format updates
    '''
    def work_on_ranges(self, worksheet_names, range_work_specs={}):
        requests = []
        worksheet_dict = self.worksheets_as_dict()
        for worksheet_name in worksheet_names:
            info(f"working on .. [{len(range_work_specs.keys())}] ranges on [{worksheet_name}]", nesting_level=1)
            worksheet_to_work_on = self.worksheet_by_name(worksheet_name)
            if worksheet_to_work_on:
                values, reqs = worksheet_to_work_on.range_work_request(range_work_specs=range_work_specs, worksheet_dict=worksheet_dict)
                requests = requests + reqs

                if len(values):
                    worksheet_to_work_on.update_values_in_batch(values=values)
                    info(f"updated  .. [{len(values)}] ranges on [{worksheet_name}]", nesting_level=2)

        if len(requests):
            self.update_in_batch(request_list=requests)
            info(f"formatted  .. {len(requests)} ranges", nesting_level=1)



    ''' put column size in pixels in row 1 for all columns except A
    '''
    def column_pixels_in_top_row(self, worksheet_names):
        column_sizes = self.get_column_sizes()
        for worksheet_name in worksheet_names:
            worksheet = self.worksheet_by_name(worksheet_name)
            if worksheet:
                worksheet.column_pixels_in_top_row(column_sizes=column_sizes)



    ''' remove trailing blank rows from a worksheet
    '''
    def remove_trailing_blank_rows(self, worksheet_names):
        for worksheet_name in worksheet_names:
            worksheet = self.worksheet_by_name(worksheet_name)
            if worksheet:
                worksheet.remove_trailing_blank_rows()



    ''' number of rows and columns of a worksheet
    '''
    def number_of_dimesnions(self, worksheet_name):
        worksheet = self.worksheet_by_name(worksheet_name)
        if worksheet:
            return worksheet.number_of_dimesnions()
        else:
            return 0, 0
