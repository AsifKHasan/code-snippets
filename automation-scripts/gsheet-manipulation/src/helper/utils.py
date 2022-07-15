#!/usr/bin/env python3

import re


'''split text into lines and remove spaces and any special character from the begining
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



''' build a repeatCell from work_spec
''' 
def repeatcell_from_work_spec(range, work_spec):
    fields = []

    # formula
    formula = None
    if 'formula' in work_spec:
        # range.setFormula(work_spec['formula'])
        pass


    # halign
    halign = None
    if 'halign' in work_spec:
        halign = work_spec['halign']
        fields.append('userEnteredFormat.horizontalAlignment')


    # valign
    valign = None
    if 'valign' in work_spec:
        valign = work_spec['valign']
        fields.append('userEnteredFormat.verticalAlignment')


    # number-format
    number_format = None
    if 'date-format' in work_spec:
        number_format = {'type': 'DATE', 'pattern': work_spec['date-format']}
        fields.append('userEnteredFormat.numberFormat')


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
    

    # fgcolor
    fg_color = None
    if 'fgcolor' in work_spec:
        fg_color = work_spec['fgcolor']
        fields.append('userEnteredFormat.textFormat.foregroundColor')


    # bgcolor
    bg_color = None
    if 'bgcolor' in work_spec:
        bg_color = work_spec['bgcolor']
        fields.append('userEnteredFormat.backgroundColor')


    # border-color
    border_color = None
    if 'border-color' in work_spec:
        # range.setBorder(true, true, true, true, false, false, work_spec['border-color'], SpreadsheetApp.BorderStyle.SOLID)
        # fields.append('userEnteredFormat.borders')
        pass


    # wrap
    wrap_strategy = None
    if 'wrap' in work_spec:
        if work_spec['wrap'] == True:
            wrap_strategy = 'WRAP'
        else:
            wrap_strategy = 'CLIP'

        fields.append('userEnteredFormat.wrapStrategy')

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
            # 'borders': borders,
            'textFormat': {
              'foregroundColor': None if fg_color is None else hex_to_rgba(fg_color),
              'fontFamily': font_family,
              'fontSize': font_size,
              'bold': bold
            }
          }
        },
        'fields': ','.join(fields)
      }
    }



''' build a boolean conditional format rule
    ranges is a list
    condition_type is enum (https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#ConditionType)
    condition_values is a list of strings
    format is a dict
''' 
def conditional_format_rule(ranges, condition_type, condition_values, format):
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
    
