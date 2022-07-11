#!/usr/bin/env python3

from gspread.exceptions import *
from gsheet.gsheet_util import *
from helper.logger import *


''' bulk create multiple worksheets by duplicating a given worksheet 
'''
def bulk_duplicate_worksheet(gsheet):
    worksheet_name_to_duplicate = 'z-blank'
    new_worksheet_names = ['04.01-৩১', '04.01-৩২', '04.02-৩৩', '04.02-৩৪', '04.03-৩৫', '04.03-৩৬']

    try:
        worksheet_to_duplicate = gsheet.worksheet(worksheet_name_to_duplicate)

        for worksheet_name in new_worksheet_names:
            # check existence of the worksheet
            try:
                ws = gsheet.worksheet(worksheet_name)
                warn(f"worksheet {worksheet_name} already exists")

            except:
                info(f"duplicating worksheet {worksheet_name_to_duplicate} as {worksheet_name}")
                worksheet_to_duplicate.duplicate(new_sheet_name=worksheet_name)
                info(f"duplicated  worksheet {worksheet_name_to_duplicate} as {worksheet_name}")
    
    except WorksheetNotFound as e:
        error(f"worksheet {worksheet_name_to_duplicate} not found")



''' order the worksheets of the gsheet alphabetically
'''
def order_worksheets(gsheet):
    info(f"ordering worksheets for {gsheet.title}")
    reordered_worksheets = sorted(gsheet.worksheets(), key=lambda x: x.title, reverse=False)
    gsheet.reorder_worksheets(reordered_worksheets)
    info(f"ordered  worksheets for {gsheet.title}")



''' link cells to worksheets where cells values are names of worksheets
'''
def link_cells_to_worksheet(gsheet):
    worksheet_name = '-toc-new'
    range_spec_for_cells_to_link = 'F3:F'

    try:
        worksheet_to_work_on = gsheet.worksheet(worksheet_name)

        # get the cells to link
        range_to_work_on = worksheet_to_work_on.range(range_spec_for_cells_to_link)
        for cell in range_to_work_on:
            if cell.value == '':
                warn(f"cell {cell.address:>5} is empty .. skipping")
            else:
                info(f"cell {cell.address:>5} value is [{cell.value}]")
                # see if the value is the name of any worksheet
                try:
                    worksheet_to_link_to = gsheet.worksheet(cell.value)
                    
                    # it is a valid worksheet, link the cell to this worksheet
                    info(f".. linking {cell.address:>5} to worksheet [{cell.value}]")

                    # TODO: do the linking
                    worksheet_to_work_on.update(cell.address, f'=HYPERLINK("#gid={worksheet_to_link_to.id}", "{cell.value}")', raw=False)

                    info(f".. linked  {cell.address:>5} to worksheet [{cell.value}]")

                except WorksheetNotFound as e:
                    warn(f".. [{cell.value}] is not a valid worksheet .. skipping")




    
    except WorksheetNotFound as e:
        error(f"worksheet {worksheet_name} not found")
