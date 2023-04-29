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
            'J': {'halign': 'center', 'size':  80, 'label': 'margin-spec'        , 'validation-list': ['wide', 'medium', 'narrow', 'none']},
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
        'index': 1,
        'num-rows': 34,
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,

        'columns': {
            'A': {'size': 100, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True},
            'B': {'size': 200, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True},
            'C': {'size': 200, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True},
            'D': {'size': 400, 'halign': 'left', 'valign': 'middle', 'font-family': 'Calibri', 'fomt-size': 10, 'weight': 'normal', 'wrap': True},
        },

        'review-notes': True,

        'ranges': {
            'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new'},
            'A2': {'value': 'review-notes', 'weight': 'bold'},
            'B2:D2': {'value': 'content', 'weight': 'bold', 'merge': True},

            'B3:C3': {'value': 'Assignment Name:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D3': {'value': 'Country:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B4:C4': {'value': "='01-summary'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True},
            'D4': {'value': "='01-summary'!C4", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B5:C5': {'value': 'Location within Country:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D5': {'value': 'Duration of assignment (months):', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B6:C6': {'value': "='01-summary'!C5", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True},
            'D6': {'value': "='01-summary'!C6", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B7:C7': {'value': 'Name of Client:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D7': {'value': 'Approximate value of the Project (In BDT):', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B8:C8': {'value': "='01-summary'!C7", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True},
            'D8': {'value': "='02-revenue'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B9:C9': {'value': 'Address', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D9': {'value': 'Approx. value of the services provided by your firm under the contract:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B10:C10': {'value': "='01-summary'!C8", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"keep-line-breaks": true}'},
            'D10': {'value': "='02-revenue'!C3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B11': {'value': 'Start Date (Month/Year):', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},
            'C11': {'value': 'Completion Date (Month/Year):', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},
            'D11': {'value': 'No. of person-months of the assignment:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B12': {'value': "='01-summary'!C11", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},
            'C12': {'value': "='01-summary'!C12", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},
            'D12': {'value': "='01-summary'!C10", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B13:C13': {'value': 'Name of joint venture partner or sub-consultants, if any:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D13': {'value': 'No. of months of Professional Staff Provided by your firm under the contract:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B14:C14': {'value': '04-joint-venture', 'ws-name-to-link': '04-joint-venture', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True},
            'D14': {'value': "='01-summary'!C10", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B15:D15': {'merge': True},

            'B16:D16': {'value': 'Name of Senior Staff (Project Director/Coordinator, Team Leader) Involved and Functions Performed:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},
            'B17:D17': {'value': '05-people', 'ws-name-to-link': '05-people', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},

            'B18:D18': {'merge': True},

            'B19:D19': {'value': 'Narrative Description of Project:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free", "new-page": true}'},
            'B20:D20': {'value': 'Project Description', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'B21:D21': {'value': '06-description', 'ws-name-to-link': '06-description', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},

            'B22:D22': {'merge': True},

            'B23:D23': {'value': 'Functionality', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'B24:D24': {'value': '07-functionality', 'ws-name-to-link': '07-functionality', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},

            'B25:D25': {'merge': True},

            'B26:D26': {'value': 'Technology', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'B27:D27': {'value': '08-technology', 'ws-name-to-link': '08-technology', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},

            'B28:D28': {'merge': True},

            'B29:D29': {'value': 'Narrative Descriptions of works performed by your organization:', 'font-size': 11, 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free", "new-page": true}'},
            'B30:D30': {'value': 'Services Provided', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'B31:D31': {'value': '09-services', 'ws-name-to-link': '09-services', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},

            'B32:D32': {'merge': True},

            'B33:D33': {'value': 'Processes Adopted', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'B34:D34': {'value': '10-process', 'ws-name-to-link': '10-process', 'weight': 'normal', 'border-color': '#b7b7b7', 'merge': True, 'note': '{"content": "free"}'},
        },

        'cell-empty-markers': [
            'B3:D14',
            'B16:D17',
            'B19:D21',
            'B23:D24',
            'B26:D27',
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

            'B3:C3': {'value': 'Name:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'merge': True},
            'D3': {'value': 'Proposed Position:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7'},

            'B4': {'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},
            'C4': {'value': "='01-personal'!D3", 'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7', 'merge': True},
            'D4': {'weight': 'normal', 'fgcolor': '#434343', 'border-color': '#b7b7b7'},

            'B5:D5': {'merge': True, 'font-size': 4},

            'B6:D6': {'value': 'Summary of personnel experience', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#ffffff', 'merge': True, 'note': '{"content": "free"}'},
            'B7:D7': {'value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'merge': True, 'note': '{"content": "free"}'},

            'B8:D8': {'merge': True, 'font-size': 4},

            'B9:D9': {'value': 'EDUCATION:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#ffffff', 'merge': True, 'note': '{"content": "free"}'},
            'B10:D10': {'value': '03-education', 'ws-name-to-link': '03-education', 'merge': True, 'note': '{"content": "free"}'},

            'B11:D11': {'merge': True, 'font-size': 4},

            'B12:D12': {'value': 'PROFESSIONAL EXPERIENCE:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#ffffff', 'merge': True, 'note': '{"content": "free", "new-page": true}'},
            'B13:D13': {'value': '06-job-history-USAID-FFBT', 'ws-name-to-link': '06-job-history-USAID-FFBT', 'merge': True, 'note': '{"content": "free"}'},

            'B14:D14': {'merge': True, 'font-size': 4},

            'B15:D15': {'value': 'LANGUAGE:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#ffffff', 'merge': True, 'note': '{"content": "free"}'},
            'B16:D16': {'value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'merge': True, 'note': '{"content": "free"}'},

            'B17:D17': {'merge': True, 'font-size': 4},

            'B18:D18': {'value': 'REFERENCES:', 'weight': 'bold', 'fgcolor': '#666666', 'bgcolor': '#ffffff', 'merge': True, 'note': '{"content": "free"}'},
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
        },
        'review-notes': True,
        'ranges': {
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
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '03-education': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '04-managerial-expertise': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '05-technical-expertise': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '06-job-history': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
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
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '08-training': {
        'num-columns': 4,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '09-certification': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '10-membership': {
        'num-columns': 6,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '11-language-proficiency': {
        'num-columns': 5,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
            'B3:F3' : {'border-color': '#b7b7b7', 'wrap': True, 'bgcolor': '#f3f3f3'},
            'B4:F' : {'border-color': '#b7b7b7', 'wrap': True, 'bgcolor': '#ffffff'},
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
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z4',
        ],
    },
    '13-educational-certificates': {
        'num-columns': 2,
        'frozen-rows': 2,
        'frozen-columns': 0,
        'columns': {
            'A': {'size': 100, 'halign': 'left', 'wrap': True},
        },
        'review-notes': True,
        'ranges': {
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
        },
        'review-notes': True,
        'ranges': {
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
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
    '16-references': {
        'num-columns': 6,
        'frozen-rows': 2,
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
            'B3:F3' : {'border-color': '#b7b7b7', 'wrap': True, 'bgcolor': '#f3f3f3'},
            'B4:F6' : {'border-color': '#b7b7b7', 'wrap': True, 'bgcolor': '#ffffff'},
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
        },
        'review-notes': True,
        'ranges': {
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
        },
        'review-notes': True,
        'ranges': {
        },
        'cell-empty-markers': [
            'B3:Z',
        ],
    },
}

# which structure we are using
WORKSHEET_STRUCTURE = WORKSHEET_STRUCTURE_RESUME
