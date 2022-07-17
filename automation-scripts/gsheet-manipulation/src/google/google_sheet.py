#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from google.google_worksheet import GoogleWorksheet

from helper.utils import *
from helper.logger import *


''' Google sheet wrapper
'''
class GoogleSheet(object):

    ''' constructor
    '''
    def __init__(self, google_service, gspread_sheet):
        self.service = google_service
        self.gspread_sheet = gspread_sheet



    ''' update spreadsheet in batch
    '''
    def update_in_batch(self, request_list):
        self.gspread_sheet.batch_update(body={'requests': request_list})    



    ''' get worksheet by name
    '''
    def worksheet_by_name(self, worksheet_name):
        try:
            ws = self.gspread_sheet.worksheet(worksheet_name)
            return GoogleWorksheet(gspread_worksheet=ws, gsheet=self)

        except:
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
    def remove_worksheet(self, worksheet_name):
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



    ''' link cells of a worksheet to worksheets where cells values are names of worksheets
    '''
    def link_cells_to_worksheet(self, worksheet_name, range_spec_for_cells_to_link):
        worksheet_to_work_on = self.worksheet_by_name(worksheet_name)
        if worksheet_to_work_on:
            worksheet_dict = self.worksheets_as_dict()
            worksheet_to_work_on.link_cells_to_worksheet(range_spec_for_cells_to_link=range_spec_for_cells_to_link, worksheet_dict=worksheet_dict)



    ''' work on a worksheet's range of work specs for value and format updates
    '''
    def work_on_ranges(self, worksheet_name, range_work_specs={}):
        worksheet_to_work_on = self.worksheet_by_name(worksheet_name)
        if worksheet_to_work_on:
            worksheet_dict = self.worksheets_as_dict()
            info(f"formatting .. {len(range_work_specs.keys())} ranges", nesting_level=1)
            count = worksheet_to_work_on.work_on_ranges(range_work_specs=range_work_specs, worksheet_dict=worksheet_dict)
            info(f"formatted  .. {count} ranges", nesting_level=1)
