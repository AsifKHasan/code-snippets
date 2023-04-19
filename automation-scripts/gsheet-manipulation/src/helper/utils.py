#!/usr/bin/env python3

import re

from helper.logger import *


''' addSheetRequest builder
'''
def build_add_sheet_request(worksheet_name, sheet_index, num_rows, num_cols, frozen_rows, frozen_cols):
    return {
        'addSheet': {
            'properties': {
                'title': worksheet_name,
                'index': sheet_index,
                'gridProperties': {
                    'rowCount': num_rows,
                    'columnCount': num_cols,
                    'frozenRowCount': frozen_rows,
                    'frozenColumnCount': frozen_cols,
                },
            }
        }
    }



''' build a repeatCell from work_spec
'''
def build_repeatcell_from_work_spec(range, work_spec):
    fields = []

    # valign
    valign = None
    if 'valign' in work_spec:
        valign = work_spec['valign']
        fields.append('userEnteredFormat.verticalAlignment')


    # halign
    halign = None
    if 'halign' in work_spec:
        halign = work_spec['halign']
        fields.append('userEnteredFormat.horizontalAlignment')


    # wrap
    wrap_strategy = None
    if 'wrap' in work_spec:
        if work_spec['wrap'] == True:
            wrap_strategy = 'WRAP'
        else:
            wrap_strategy = 'CLIP'

        fields.append('userEnteredFormat.wrapStrategy')


    # number-format
    number_format = None
    if 'date-format' in work_spec:
        number_format = {'type': 'DATE', 'pattern': work_spec['date-format']}
        fields.append('userEnteredFormat.numberFormat')


    # bgcolor
    bg_color = None
    if 'bgcolor' in work_spec:
        bg_color = work_spec['bgcolor']
        fields.append('userEnteredFormat.backgroundColor')


    # fgcolor
    fg_color = None
    if 'fgcolor' in work_spec:
        fg_color = work_spec['fgcolor']
        fields.append('userEnteredFormat.textFormat.foregroundColor')


    # font-family
    font_family = None
    if 'font-family' in work_spec:
        font_family = work_spec['font-family']
        fields.append('userEnteredFormat.textFormat.fontFamily')


    # font-size
    font_size = None
    if 'font-size' in work_spec:
        font_size = work_spec['font-size']
        fields.append('userEnteredFormat.textFormat.fontSize')


    # weight
    bold = False
    if 'weight' in work_spec:
        if work_spec['weight'] == 'bold':
            bold = True

        fields.append('userEnteredFormat.textFormat.bold')


    # note
    note = None
    if 'note' in work_spec:
        note = work_spec['note']
        fields.append('note')



    if len(fields) == 0:
        return None

    return {
      'repeatCell': {
        'range': range,
        'cell': {
            'userEnteredFormat': {
                'verticalAlignment': valign,
                'horizontalAlignment': halign,
                'wrapStrategy': wrap_strategy,
                'numberFormat': number_format,
                'backgroundColor': None if bg_color is None else hex_to_rgba(bg_color),
                'textFormat': {
                    'foregroundColor': None if fg_color is None else hex_to_rgba(fg_color),
                    'fontFamily': font_family,
                    'fontSize': font_size,
                    'bold': bold
                },
            },
            'note': note,
        },
        'fields': ','.join(fields)
      }
    }



''' appendDimensionRequest builder
'''
def build_append_dimension_request(worksheet_id, dimension, length):
    return {'appendDimension': {'sheetId': worksheet_id, 'dimension': dimension, 'length': length}}



''' insertDimensionRequest builder
'''
def build_insert_dimension_request(worksheet_id, dimension, start_index, length, inherit_from_before):
    range = {'sheetId': worksheet_id, 'dimension': dimension, 'startIndex': start_index, 'endIndex': start_index + length}
    return {'insertDimension': {'range': range, 'inheritFromBefore': inherit_from_before}}



''' deleteDimensionRequest builder
'''
def build_delete_dimension_request(worksheet_id, dimension, start_index, end_index=None):
    range = {'sheetId': worksheet_id, 'dimension': dimension, 'startIndex': start_index}
    if end_index:
        range['endIndex'] = end_index

    return {'deleteDimension': {'range': range}}



''' gsheet border spec for border around a range
'''
def build_duplicate_sheet_request(worksheet_id, new_worksheet_name, new_worksheet_index=None):
    request_body = {
        "duplicateSheet": {
            "sourceSheetId": worksheet_id,
            "newSheetName": new_worksheet_name
        }
    }

    if new_worksheet_index:
        request_body['duplicateSheet'][insertSheetIndex] = new_worksheet_index

    return request_body



''' gsheet border spec for border around a range
'''
def build_border_around_spec(border_color, border_style='SOLID'):
    color = hex_to_rgba(border_color)
    border = {
        "style": border_style,
        # "color": color,
        "colorStyle": {
            "rgbColor": color
        }
    }

    borders = {
        "top": border,
        "bottom": border,
        "left": border,
        "right": border,
        "innerHorizontal": border,
        "innerVertical": border,
    }

    return borders



''' build a boolean conditional format rule
    ranges is a list
    condition_type is enum (https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#ConditionType)
    condition_values is a list of strings
    format is a dict
'''
def build_conditional_format_rule(ranges, condition_type, condition_values, format):
    rule = {"addConditionalFormatRule": {
                "rule": {
                    "ranges" : ranges,
                    "booleanRule": {
                        "condition": {
                            "type": condition_type,
                            "values": [{"userEnteredValue": v} for v in condition_values]
                        },
                        "format": format
                    }
                },
                "index": 0
            }
        }

    return rule



''' build a data validation rule
    condition_values is a list of strings
'''
def build_data_validation_rule(range, condition_type, condition_values, input_message=None):
    values = [{'userEnteredValue': v} for v in condition_values]
    rule = {"setDataValidation": {
                "range" : range,
                "rule": {
                    "condition": {
                        "type": condition_type,
                        "values": values,
                    },
                    "inputMessage": input_message,
                    "strict": True,
                    "showCustomUi": True
                }
            }
        }

    return rule



''' build a no data validation rule
'''
def build_no_data_validation_rule(range):
    rule = {"setDataValidation": {
                "range" : range,
                "rule": None
            }
        }

    return rule



''' gets the value from workspec
'''
def build_value_from_work_spec(work_spec, worksheet_dict={}, google_service=None):
    value = ''
    if 'value' in work_spec:
        value = work_spec['value']

    if value != '':
        # it may be hyperlink to another worksheet
        if 'ws-name-to-link' in work_spec:
            # is it a valid worksheet
            if work_spec['ws-name-to-link'] in worksheet_dict:
                value = f'=HYPERLINK("#gid={worksheet_dict[work_spec["ws-name-to-link"]]}", "{value}")'.lstrip("'")
            else:
                warn(f".... No Worksheet named {work_spec['ws-name-to-link']}")

        # it may be hyperlink to another drive file
        elif 'file-name-to-link' in work_spec:
            # we need the id of the drive file
            drive_file = google_service.get_drive_file(drive_file_name=work_spec['file-name-to-link'])
            if drive_file:
                # print(drive_file)
                value = f'=HYPERLINK("{drive_file["webViewLink"]}", "{value}")'.lstrip("'")
            else:
                warn(f".... No Drive File named {work_spec['file-name-to-link']}")

    return value



''' build dimension size update request
    note: index is 0 based
'''
def build_dimension_size_update_request(sheet_id, dimension, index, size):
    range_spec = {
        "sheetId": sheet_id,
        "dimension": dimension,
        "startIndex": index - 1,
        "endIndex": index
    }

    update_dimension_properties = {
      "updateDimensionProperties": {
        "range": range_spec,
        "properties": {
          "pixelSize": size
        },
        "fields": "pixelSize"
      }
    }

    return update_dimension_properties



''' build dimension visibility update request
    note: index is 0 based
'''
def build_dimension_visibility_update_request(sheet_id, dimension, start_index, end_index, hide):
    range_spec = {
        "sheetId": sheet_id,
        "dimension": dimension,
        "startIndex": start_index,
        "endIndex": end_index
    }

    update_dimension_properties = {
      "updateDimensionProperties": {
        "range": range_spec,
        "properties": {
          "hiddenByUser": hide
        },
        "fields": "hiddenByUser"
      }
    }

    return update_dimension_properties



''' build sheet property update request for frozen rows
'''
def build_row_freeze_request(sheet_id, frozen_rows):
    update_sheet_properties = {
      "updateSheetProperties": {
        "properties": {
          "sheetId": sheet_id,
          "gridProperties": {
            "frozenRowCount": frozen_rows,
          }
        },
        "fields": "gridProperties.frozenRowCount"
      }
    }

    return update_sheet_properties



''' build sheet property update request for frozen columns
'''
def build_column_freeze_request(sheet_id, frozen_cols):
    update_sheet_properties = {
      "updateSheetProperties": {
        "properties": {
          "sheetId": sheet_id,
          "gridProperties": {
            "frozenColumnCount": frozen_cols,
          }
        },
        "fields": "gridProperties.frozenColumnCount"
      }
    }

    return update_sheet_properties



''' split text into lines and remove spaces and any special character from the begining
'''
def split_and_dress(value):
    lines = value.split('\n')
    regex = r'^[-\s•]+'
    lines = [re.sub(regex, '', s) for s in lines]
    regex = r'[\s]+$'
    lines = [re.sub(regex, '', s) for s in lines]

    return lines



''' hex string to RGB color tuple
'''
def hex_to_color(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



''' hex string to RGBA
'''
def hex_to_rgba(hex):
    h = hex.lstrip('#')
    if len(h) == 6:
        h = h + '00'

    color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return {"red": color[0]/255, "green": color[1]/255, "blue": color[2]/255, "alpha": color[3]/255}
