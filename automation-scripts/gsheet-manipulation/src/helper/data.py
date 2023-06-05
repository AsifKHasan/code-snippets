#!/usr/bin/env python3

# Resume structure
WORKSHEET_STRUCTURE_RESUME = {
    '-toc-new': {
        'frozen-rows': 2,
        'frozen-columns': 0,

        'columns': {
            'A': {'halign': 'center', 'size':  60, 'label': 'section'            , },
            'B': {'halign': 'left',   'size': 200, 'label': 'heading'            , },
            'C': {'halign': 'center', 'size':  80, 'label': 'process'            , 'validation-list': ['Yes']},
            'D': {'halign': 'center', 'size':  80, 'label': 'level'              , 'validation-list': ['0', '1', '2', '3', '4', '5', '6']},
            'E': {'halign': 'center', 'size':  80, 'label': 'content-type'       , 'validation-list': ['gsheet', 'lof', 'lot', 'pdf', 'table', 'toc']},
            'F': {'halign': 'left',   'size': 200, 'label': 'link'               , },
            'G': {'halign': 'center', 'size':  80, 'label': 'break'              , 'validation-list': ['page', 'section']},
            'H': {'halign': 'center', 'size':  80, 'label': 'landscape'          , 'validation-list': ['Yes']},
            'I': {'halign': 'center', 'size':  80, 'label': 'page-spec'          , 'validation-list': ['A4', 'A3', 'Letter', 'Legal']},
            'J': {'halign': 'center', 'size': 100, 'label': 'margin-spec'        , 'validation-list': ['wide', 'medium', 'narrow', 'none', 'book-bind', 'secl-pad']},
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
            'V': {'halign': 'left',   'size': 100, 'label': 'background-image'   , },
            'W': {'halign': 'left',   'size':  80, 'label': 'responsible'        , },
            'X': {'halign': 'left',   'size':  80, 'label': 'reviewer'           , },
            'Y': {'halign': 'left',   'size': 160, 'label': 'status'             , 'validation-list': ['pending', 'under-documentation', 'ready-for-review', 'under-review', 'finalized']},
            'Z': {'halign': 'left',   'size': 300, 'label': 'comment'            , },
        },
        'cell-empty-markers': [
            'W3:Y'
        ],
    },
    '00-layout': {
        'num-rows': 27,
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'B': {'size':  30, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'C': {'size': 250, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'D': {'size': 250, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'E': {'size': 270, 'halign': 'center', 'valign': 'top', 'wrap': True},
        },
        'rows': {
            '1': {'size': 21, },
            '2': {'size': 21, },
            '3': {'size': 21, },
            '4': {'size': 21, },
            '5': {'size': 21, },
            '6': {'size': 8, },
            '7': {'size': 21, },
            '8': {'size': 21, },
            '9': {'size': 8, },
            '10': {'size': 21, },
            '11': {'size': 21, },
            '12': {'size': 8, },
            '13': {'size': 21, },
            '14': {'size': 21, },
            '15': {'size': 8, },
            '16': {'size': 21, },
            '17': {'size': 21, },
            '18': {'size': 8, },
            '19': {'size': 21, },
            '20': {'size': 21, },
            '21': {'size': 8, },
            '22': {'size': 21, },
            '23': {'size': 21, },
            '24': {'size': 8, },
            '25': {'size': 21, },
            '26': {'size': 21, },
            '27': {'size': 8, },
            '28': {'size': 21, },
            '29': {'size': 21, },
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },

            'A2': {'value': 'review-notes', 'halign': 'left', 'weight': 'bold', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'weight': 'bold', 'merge': True, },

            'B3': {'value': '1', 'weight': 'bold', },
            'C3': {'value': 'NAME OF RESOURCE', 'weight': 'bold', },
            'D3': {'value': "='01-personal'!D3", },

            'B4': {'value': '2', 'weight': 'bold', },
            'C4': {'value': 'DATE OF BIRTH', 'weight': 'bold', },
            'D4': {'value': "='01-personal'!D5", },

            'B5': {'value': '3', 'weight': 'bold', },
            'C5': {'value': 'NATIONALITY', 'weight': 'bold', },
            'D5': {'value': "='01-personal'!D6", },

            # 'B3:E5': {'border-color': '#B7B7B7', },

            'B6': {'value': '', },
            'B7': {'value': '4', 'weight': 'bold', },
            'C7:E7': {'value': 'SUMMARY OF PROFESSIONAL EXPERIENCE', 'weight': 'bold', 'merge': True, },
            'B8': {'value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'note': '{"content": "free"}', },

            'B9': {'value': '', },
            'B10': {'value': '5', 'weight': 'bold', },
            'C10:E10': {'value': 'EDUCATION', 'weight': 'bold', 'merge': True, },
            'B11': {'value': '03-education', 'ws-name-to-link': '03-education', 'note': '{"content": "free"}', },

            'B12': {'value': '', 'note': '{"content": "free", "new-page": true}', },
            'B13': {'value': '6a', 'weight': 'bold', },
            'C13:E13': {'value': 'EMPLOYMENT RECORD', 'weight': 'bold', 'merge': True, },
            'B14': {'value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "free"}', },

            'B15': {'value': '', 'note': '{"content": "free", "new-page": true}', },
            'B16': {'value': '6b', 'weight': 'bold', },
            'C16:E16': {'value': 'PROFESSIONAL EXPERIENCE', 'weight': 'bold', 'merge': True, },
            'B17': {'value': '07-project-roles', 'ws-name-to-link': '07-project-roles', 'note': '{"content": "free"}', },

            'B18': {'value': '', 'note': '{"content": "free", "new-page": true}', },
            'B19': {'value': '7', 'weight': 'bold', },
            'C19:E19': {'value': 'TECHNICAL EXPERTISE', 'weight': 'bold', 'merge': True, },
            'B20': {'value': '05-technical-expertise', 'ws-name-to-link': '05-technical-expertise', 'note': '{"content": "free"}', },

            'B21': {'value': '', },
            'B22': {'value': '8a', 'weight': 'bold', },
            'C22:E22': {'value': 'PROFESSIONAL TRAINING', 'weight': 'bold', 'merge': True, },
            'B23': {'value': '08-training', 'ws-name-to-link': '08-training', 'note': '{"content": "free"}', },

            'B24': {'value': '', },
            'B25': {'value': '8b', 'weight': 'bold', },
            'C25:E25': {'value': 'PROFESSIONAL CERTIFICATIONS', 'weight': 'bold', 'merge': True, },
            'B26': {'value': '09-certification', 'ws-name-to-link': '09-certification', 'note': '{"content": "free"}', },

            'B27': {'value': '', },
            'B28': {'value': '9', 'weight': 'bold', },
            'C28:E28': {'value': 'LANGUAGES & DEGREE OF PROFICIENCY', 'weight': 'bold', 'merge': True, },
            'B29': {'value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'note': '{"content": "free"}', },
        },
        'cell-empty-markers': [
            'B3:E5',
        ],
    },
    '00-layout-RHD-TMC': {
        'num-rows': 28,
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'B': {'size':  30, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'C': {'size': 250, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'D': {'size': 250, 'halign': 'left', 'valign': 'top', 'wrap': True},
            'E': {'size': 270, 'halign': 'center', 'valign': 'top', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },

            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },

            'B3': {'value': '1', },
            'C3': {'value': 'PROPOSED POSITION', },
            'D3': {'value': "", },

            'B4': {'value': '2', },
            'C4': {'value': 'NAME OF RESOURCE', },
            'D4': {'value': "='01-personal'!D3", },

            'B5': {'value': '3', },
            'C5': {'value': 'DATE OF BIRTH', },
            'D5': {'value': "='01-personal'!D5", },

            'B6': {'value': '4', },
            'C6': {'value': 'NATIONALITY', },
            'D6': {'value': "='01-personal'!D6", },

            # 'B3:E6': {'border-color': '#B7B7B7', },

            'B7': {'value': '', },

            'B8': {'value': '4', },
            'C8:E8': {'value': 'SUMMARY OF PROFESSIONAL EXPERIENCE', 'merge': True, },

            'B9': {'value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'note': '{"content": "free"}', },

            'B10': {'value': '', },

            'B11': {'value': '5', },
            'C11:E11': {'value': 'EDUCATION', 'merge': True, },

            'B12': {'value': '03-education', 'ws-name-to-link': '03-education', 'note': '{"content": "free"}', },

            'B13': {'value': '', 'note': '{"content": "free", "new-page": true}', },

            'B14': {'value': '6', },
            'C14:E14': {'value': 'EMPLOYMENT RECORD', 'merge': True, },

            'B15': {'value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "free"}', },

            'B16': {'value': '', },

            'B17': {'value': '07-project-roles', 'ws-name-to-link': '07-project-roles', 'note': '{"content": "free"}', },

            'B18': {'value': '', 'note': '{"content": "free", "new-page": true}', },

            'B19': {'value': '7', },
            'C19:E19': {'value': 'TECHNICAL EXPERTISE', 'merge': True, },

            'B20': {'value': '05-technical-expertise', 'ws-name-to-link': '05-technical-expertise', 'note': '{"content": "free"}', },

            'B21': {'value': '', },

            'B22': {'value': '8', },
            'C22:E22': {'value': 'TRAINING AND CERTIFICATIONS', 'merge': True, },

            'B23': {'value': '08-training', 'ws-name-to-link': '08-training', 'note': '{"content": "free"}', },

            'B24': {'value': '', },

            'B25': {'value': '09-certification', 'ws-name-to-link': '09-certification', 'note': '{"content": "free"}', },

            'B26': {'value': '', },

            'B27': {'value': '9', },
            'C27:E27': {'value': 'LANGUAGES & DEGREE OF PROFICIENCY', 'merge': True, },

            'B28': {'value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'note': '{"content": "free"}', },
        },
        'cell-empty-markers': [
            'B3:E6',
        ],
    },
    '00-layout-USAID-FFBT': {
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  60},
            'C': {'size': 340},
            'D': {'size': 400},
        },
        'rows': {
            '5': {'size': 10},
            '8': {'size':  10},
            '11': {'size': 10},
            '14': {'size': 10},
            '17': {'size': 10},
        },
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new'},
            'A2': {'value': 'review-notes', 'weight': 'bold'},
            'B2:D2': {'value': 'content', 'weight': 'bold', 'merge': True},

            'B3:C3': {'value': 'Name:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True},
            'D3': {'value': 'Proposed Position:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7'},

            'B4': {'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7'},
            'C4': {'value': "='01-personal'!D3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', 'merge': True},
            'D4': {'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7'},

            'B5:D5': {'merge': True, 'font-size': 4},

            'B6:D6': {'value': 'Summary of personnel experience', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#FFFFFF', 'merge': True, 'note': '{"content": "free"}'},
            'B7:D7': {'value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'merge': True, 'note': '{"content": "free"}'},

            'B8:D8': {'merge': True, 'font-size': 4},

            'B9:D9': {'value': 'EDUCATION:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#FFFFFF', 'merge': True, 'note': '{"content": "free"}'},
            'B10:D10': {'value': '03-education', 'ws-name-to-link': '03-education', 'merge': True, 'note': '{"content": "free"}'},

            'B11:D11': {'merge': True, 'font-size': 4},

            'B12:D12': {'value': 'PROFESSIONAL EXPERIENCE:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#FFFFFF', 'merge': True, 'note': '{"content": "free", "new-page": true}'},
            'B13:D13': {'value': '06-job-history-USAID-FFBT', 'ws-name-to-link': '06-job-history-USAID-FFBT', 'merge': True, 'note': '{"content": "free"}'},

            'B14:D14': {'merge': True, 'font-size': 4},

            'B15:D15': {'value': 'LANGUAGE:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#FFFFFF', 'merge': True, 'note': '{"content": "free"}'},
            'B16:D16': {'value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'merge': True, 'note': '{"content": "free"}'},

            'B17:D17': {'merge': True, 'font-size': 4},

            'B18:D18': {'value': 'REFERENCES:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#FFFFFF', 'merge': True, 'note': '{"content": "free"}'},
            'B19:D19': {'value': '16-references', 'ws-name-to-link': '16-references', 'merge': True, 'note': '{"content": "free"}'},
        },
        'cell-empty-markers': [
            'B4:D4',
        ],
    },
    '01-personal': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  30, 'halign': 'center', 'wrap': True},
            'C': {'size': 130, 'halign': 'left', 'wrap': True},
            'D': {'size': 320, 'halign': 'left', 'wrap': True},
            'E': {'size': 320, 'halign': 'center', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '02-career-highlight': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 150, 'halign': 'left', 'wrap': True},
            'C': {'size':  30, 'halign': 'center', 'wrap': True},
            'D': {'size': 620, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:D1': {'halign': 'center', },
            'B2:D2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '03-education': {
        'num-columns': 5,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  80, 'halign': 'center', 'wrap': True},
            'C': {'size': 210, 'halign': 'left', 'wrap': True},
            'D': {'size': 210, 'halign': 'left', 'wrap': True},
            'E': {'size': 300, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },

            'B3': {'value': 'Year', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Degree', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Subject/Discipline', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'E3': {'value': 'Institute', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '04-managerial-expertise': {
        'num-columns': 4,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 170, 'halign': 'left', 'wrap': True},
            'C': {'size':  30, 'halign': 'center', 'wrap': True},
            'D': {'size': 600, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:D1': {'halign': 'center', },
            'B2:D2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Area', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3:D3': {'value': 'Expertise', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '05-technical-expertise': {
        'num-columns': 4,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 170, 'halign': 'left', 'wrap': True},
            'C': {'size':  30, 'halign': 'center', 'wrap': True},
            'D': {'size': 600, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:D1': {'halign': 'center', },
            'B2:D2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Area', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3:D3': {'value': 'Expertise', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '06-job-history': {
        'num-columns': 5,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  60, 'halign': 'center', 'wrap': True},
            'C': {'size':  60, 'halign': 'center', 'wrap': True},
            'D': {'size':  30, 'wrap': True},
            'E': {'size': 650, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'From', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'To', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3:E3': {'value': 'Employment History', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '06-job-history-USAID-FFBT': {
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  65, 'halign': 'center', 'wrap': True},
            'C': {'size':  65, 'halign': 'center', 'wrap': True},
            'D': {'size':  30, 'wrap': True},
            'E': {'size': 640, 'wrap': True},
        },
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'B1': {'value': '65', 'halign': 'center'},
            'C1': {'value': '65', 'halign': 'center'},
            'D1': {'value': '30', 'halign': 'center'},
            'E1': {'value': '640', 'halign': 'center'},

            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True},

        },
    },
    '07-project-roles': {
        'num-columns': 5,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  60, 'halign': 'center', 'wrap': True},
            'C': {'size':  60, 'halign': 'center', 'wrap': True},
            'D': {'size':  30, 'wrap': True},
            'E': {'size': 650, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'From', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'To', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3:E3': {'value': 'Company/Project/Position/ Relevant Technical and Management Experience', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '08-training': {
        'num-columns': 4,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  80, 'halign': 'center', 'wrap': True},
            'C': {'size': 450, 'halign': 'left', 'wrap': True},
            'D': {'size': 370, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:D1': {'halign': 'center', },
            'B2:D2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Year', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Training', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Institute', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '09-certification': {
        'num-columns': 5,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size':  70, 'halign': 'center', 'wrap': True},
            'C': {'size': 150, 'halign': 'left', 'wrap': True},
            'D': {'size': 280, 'halign': 'left', 'wrap': True},
            'E': {'size': 300, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Year', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Vendor/OEM/ Subject', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Certification', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'E3': {'value': 'Details', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '10-membership': {
        'num-columns': 6,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 250, 'halign': 'left', 'wrap': True},
            'C': {'size': 150, 'halign': 'left', 'wrap': True},
            'D': {'size': 125, 'halign': 'center', 'wrap': True},
            'E': {'size': 125, 'halign': 'center', 'wrap': True},
            'F': {'size': 150, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:F1': {'halign': 'center', },
            'B2:F2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Professional Organization/Society', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Membership Rank/Level', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Membership ID/Number', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'E3': {'value': 'Member Since', 'halign': 'center', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'F3': {'value': 'Details', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '11-language-proficiency': {
        'num-columns': 5,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 110, 'halign': 'left', 'wrap': True},
            'C': {'size': 230, 'halign': 'left', 'wrap': True},
            'D': {'size': 230, 'halign': 'left', 'wrap': True},
            'E': {'size': 230, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:E1': {'halign': 'center', },
            'B2:E2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Language', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Speaking', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Reading', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'E3': {'value': 'Writing', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '12-contact': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 200, 'halign': 'left', 'wrap': True},
            'C': {'size': 600, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:C1': {'halign': 'center', },
            'B2:C2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:C4',
        ],
    },
    '13-educational-certificates': {
        'num-columns': 2,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 800, 'halign': 'center', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1': {'halign': 'center', },
            'B2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '14-vendor-certificates': {
        'num-columns': 2,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 800, 'halign': 'center', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1': {'halign': 'center', },
            'B2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '15-institutional-certificates': {
        'num-columns': 2,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 800, 'halign': 'center', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1': {'halign': 'center', },
            'B2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '16-references': {
        'num-columns': 6,
        'frozen-rows': 3,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 140, 'halign': 'left', 'wrap': True},
            'C': {'size': 150, 'halign': 'left', 'wrap': True},
            'D': {'size': 190, 'halign': 'left', 'wrap': True},
            'E': {'size': 190, 'halign': 'left', 'wrap': True},
            'F': {'size': 130, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:F1': {'halign': 'center', },
            'B2:F2': {'value': 'content', 'halign': 'left', 'merge': True, },
            'B3': {'value': 'Name', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'note': '{"repeat-rows": 1}', },
            'C3': {'value': 'Position', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D3': {'value': 'Company', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'E3': {'value': 'Email', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'F3': {'value': 'Phone Number', 'halign': 'left', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'B4:Z': {'border-color': '#B7B7B7', },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    'z-header': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 600, 'halign': 'left', 'wrap': True},
            'C': {'size': 200, 'halign': 'right', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:C1': {'halign': 'center', },
            'B2:C2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    'z-footer': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 600, 'halign': 'left', 'wrap': True},
            'C': {'size': 200, 'halign': 'right', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:C1': {'halign': 'center', },
            'B2:C2': {'value': 'content', 'halign': 'left', 'merge': True, },
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
}

# Resume structure
WORKSHEET_STRUCTURE_PDS = {
    '00-layout': {
        'num-rows': 34,
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True, },
            'B': {'size': 240, 'halign': 'left', 'wrap': True, },
            'C': {'size': 240, 'halign': 'left', 'wrap': True, },
            'D': {'size': 320, 'halign': 'left', 'wrap': True, },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', },
            'A2': {'value': 'review-notes', 'weight': 'bold', },
            'B1:D1': {'halign': 'center', },
            'B2:D2': {'value': 'content', 'weight': 'bold', 'merge': True, },

            'B3:C3': {'value': 'Assignment Name:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'D3': {'value': 'Country:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B4:C4': {'value': "='01-summary'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', 'merge': True, },
            'D4': {'value': "='01-summary'!C4", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B5:C5': {'value': 'Location within Country:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'D5': {'value': 'Duration of assignment (months):', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B6:C6': {'value': "='01-summary'!C5", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', 'merge': True, },
            'D6': {'value': "='01-summary'!C6", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B7:C7': {'value': 'Name of Client:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'D7': {'value': 'Approximate value of the Project (In BDT):', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B8:C8': {'value': "='01-summary'!C7", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', 'merge': True, },
            'D8': {'value': "='02-revenue'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B9:C9': {'value': 'Address', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'D9': {'value': 'Approx. value of the services provided by your firm under the contract:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B10:C10': {'value': "='01-summary'!C8", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"keep-line-breaks": true}', },
            'D10': {'value': "='02-revenue'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B11': {'value': 'Start Date (Month/Year):', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'C11': {'value': 'Completion Date (Month/Year):', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },
            'D11': {'value': 'No. of person-months of the assignment:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B12': {'value': "='01-summary'!C11", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },
            'C12': {'value': "='01-summary'!C12", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },
            'D12': {'value': "='01-summary'!C10", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B13:C13': {'value': 'Name of joint venture partner or sub-consultants, if any:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'D13': {'value': 'No. of months of Professional Staff Provided by your firm under the contract:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', },

            'B14:C14': {'value': '04-joint-venture', 'ws-name-to-link': '04-joint-venture', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, },
            'D14': {'value': "='01-summary'!C10", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#B7B7B7', },

            'B15:D15': {'merge': True},

            'B16:D16': {'value': 'Name of Senior Staff (Project Director/Coordinator, Team Leader) Involved and Functions Performed:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },
            'B17:D17': {'value': '05-people', 'ws-name-to-link': '05-people', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },

            'B18:D18': {'merge': True, },

            'B19:D19': {'value': 'Narrative Description of Project:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free", "new-page": true}', },
            'B20:D20': {'value': 'Project Description', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'B21:D21': {'value': '06-description', 'ws-name-to-link': '06-description', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },

            'B22:D22': {'merge': True, },

            'B23:D23': {'value': 'Functionality', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'B24:D24': {'value': '07-functionality', 'ws-name-to-link': '07-functionality', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },

            'B25:D25': {'merge': True, },

            'B26:D26': {'value': 'Technology', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'B27:D27': {'value': '08-technology', 'ws-name-to-link': '08-technology', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },

            'B28:D28': {'merge': True, },

            'B29:D29': {'value': 'Narrative Descriptions of works performed by your organization:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free", "new-page": true}', },
            'B30:D30': {'value': 'Services Provided', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'B31:D31': {'value': '09-services', 'ws-name-to-link': '09-services', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },

            'B32:D32': {'merge': True, },

            'B33:D33': {'value': 'Processes Adopted', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#F3F3F3', 'border-color': '#B7B7B7', 'merge': True, },
            'B34:D34': {'value': '10-process', 'ws-name-to-link': '10-process', 'weight': 'normal', 'border-color': '#B7B7B7', 'merge': True, 'note': '{"content": "free"}', },
        },
        'cell-empty-markers': [
            'B3:D14',
            'B16:D17',
            'B19:D21',
            'B23:D24',
            'B26:D27',
            'B29:D31',
            'B33:D34',
        ],
    },
    '01-summary': {
    },
    '02-revenue': {
    },
    '03-contact': {
    },
    '04-joint-venture': {
    },
    '05-people': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left', 'size': 100, 'wrap': True, },
            'B': {'halign': 'left', 'size': 150, 'wrap': True, },
            'C': {'halign': 'left', 'size': 150, 'wrap': True, },
            'D': {'halign': 'left', 'size': 500, 'wrap': True, },
        },
        'review-notes': True,
        'ranges': {
            'A1:Z': {'valign': 'top', 'wrap': True, 'bgcolor': '#FFFFFF', 'border-color': '#B7B7B7', 'no-border': True, },
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left', },
            'A2': {'value': 'review-notes', 'halign': 'left', },
            'B1:C1': {'halign': 'center', },
            'B2:C2': {'value': 'content', 'halign': 'left', 'merge': True, },

            'B2': {'value': 'person'},
            'C2': {'value': 'project-role'},
            'D2': {'value': 'functionalities-performed'},

            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '06-description': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left'  , 'size': 100, },
            'B': {'halign': 'left'  , 'size': 120, },
            'C': {'halign': 'center', 'size':  30, },
            'D': {'halign': 'left'  , 'size': 650, },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'header', 'halign': 'left'},
            'C2:D2': {'value': 'narrative-paragraphs', 'halign': 'left', 'merge': True},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '07-functionality': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left'  , 'size': 100,  },
            'B': {'halign': 'left'  , 'size': 120,  },
            'C': {'halign': 'center', 'size':  30,  },
            'D': {'halign': 'left'  , 'size': 120,  },
            'E': {'halign': 'left'  , 'size': 530,  },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'module', 'halign': 'left'},
            'C2:D2': {'value': 'feature', 'halign': 'left', 'merge': True},
            'E2': {'value': 'process', 'halign': 'left'},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '08-technology': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left'  , 'size': 100,  },
            'B': {'halign': 'left'  , 'size': 120,  },
            'C': {'halign': 'center', 'size':  30,  },
            'D': {'halign': 'left'  , 'size': 650,  },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'area', 'halign': 'left'},
            'C2:D2': {'value': 'technology-tool', 'halign': 'left', 'merge': True},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '09-services': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left'  , 'size': 100,  },
            'B': {'halign': 'left'  , 'size': 120,  },
            'C': {'halign': 'center', 'size':  30,  },
            'D': {'halign': 'left'  , 'size': 650,  },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'area', 'halign': 'left'},
            'C2:D2': {'value': 'services-provided-by-staff', 'halign': 'left', 'merge': True},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '10-process': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left'  , 'size': 100,  },
            'B': {'halign': 'left'  , 'size': 120,  },
            'C': {'halign': 'center', 'size':  30,  },
            'D': {'halign': 'left'  , 'size': 650,  },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'area', 'halign': 'left'},
            'C2:D2': {'value': 'process-description-in-paragraphs-bullets', 'halign': 'left', 'merge': True},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '11-complexity': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'halign': 'left', 'size': 100,  },
            'B': {'halign': 'left', 'size': 200,  },
            'C': {'halign': 'left', 'size': 600,  },
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2': {'value': 'project-complexity', 'halign': 'left'},
            'C2': {'value': 'how-it-was-addressed', 'halign': 'left'},
            'B3:Z': {'border-color': '#B7B7B7'},
        },
        'cell-empty-markers': [
            'B3:Z'
        ],
    },
    '12-screenhots': {
    },
    'z-blank': {
    },
    'z-header': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 600, 'halign': 'left', 'wrap': True},
            'C': {'size': 200, 'halign': 'right', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2:C2': {'value': 'content', 'merge': True, 'halign': 'left'},
            'B3': {'value': 'Project Datasheet', 'halign': 'left'},
            'C3': {'value': '=image("https://spectrum-bd.biz/data/artifacts/res/logo/spectrum-logo-small-111x89.png", 1)', 'halign': 'right'},
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    'z-footer': {
        'num-columns': 3,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
            'B': {'size': 600, 'halign': 'left', 'wrap': True},
            'C': {'size': 200, 'halign': 'right', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
            'A2': {'value': 'review-notes', 'halign': 'left'},
            'B2:C2': {'value': 'content', 'merge': True, 'halign': 'left'},
            'B3': {'value': "='01-summary'!C3", 'halign': 'left'},
            'C3': {'value': 'A', 'note': '{"page-number": "long"}', 'halign': 'right'},
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
}

# which structure we are using
WORKSHEET_STRUCTURE = WORKSHEET_STRUCTURE_PDS
