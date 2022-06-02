RESUME_WS_QA = {
  'worksheets': {
    '-toc': {
      'num-columns': 22,
    },
    '-toc-new': {
      'num-columns': 25,
    },
    '00-layout': {
      'num-columns': 10,
      'num-rows': 53,
    },
    '01-personal': {
      'num-columns': 5,
      'num-rows': 14,
      'error-on-blank': {
        'D3': 'MISSING: Full name',
        'D4': 'MISSING: Full name in Bangla',
        'D5': 'MISSING: Date of Birth',
        'D6': 'MISSING: Nationality',
        'D7': 'MISSING: Emails',
        'D8': 'MISSING: Phones',
        'D9': 'MISSING: Skype id',
        'D10': 'MISSING: Address',
        'D11': 'MISSING: Organization',
        'D12': 'MISSING: Designation',
        'D13': 'MISSING: Countries worked in',
        'D14': 'MISSING: National ID Number',
        'E3': 'MISSING: Photo Hyperlink',
      },
    },
    '02-career-highlight': {
      'num-columns': 4,
      'grouped-data': {
        'header-rows': 2,
        'group-range-spec': 'B3:B',
        'min-groups': 3,
        'data-range-spec': 'C3:D',
        'min-data-rows': 5,
      },
    },
    '03-education': {
      'num-columns': 5,
      'data-rows': {
        'range-spec': 'B4:E',
        'header-rows': 3,
        'min-entries': 3,
      },
    },
    '04-managerial-expertise': {
      'num-columns': 4,
      'grouped-data': {
        'header-rows': 3,
        'group-range-spec': 'B4:B',
        'min-groups': 3,
        'data-range-spec': 'C4:D',
        'min-data-rows': 5,
      },
    },
    '05-technical-expertise': {
      'num-columns': 4,
      'grouped-data': {
        'header-rows': 3,
        'group-range-spec': 'B4:B',
        'min-groups': 10,
        'data-range-spec': 'C4:D',
        'min-data-rows': 10,
      },
    },
    '06-job-history': {
      'num-columns': 4,
      'block-data': {
        'header-rows': 2,
        'block-range-spec': 'B3:D',
        'marker-column': 0,
        'marker': 'Organization',
        'blank-rows-between-blocks': 1,
        'min-blocks': 1,
      },
    },
    '07-project-roles': {
      'num-columns': 4,
      'block-data': {
        'header-rows': 2,
        'block-range-spec': 'B3:D',
        'marker-column': 0,
        'marker': 'Project/Product',
        'blank-rows-between-blocks': 1,
        'min-blocks': 1,
      },
    },
    '08-training': {
      'num-columns': 4,
      'data-rows': {
        'range-spec': 'B4:D',
        'header-rows': 3,
        'min-entries': 1,
      },
    },
    '09-certification': {
      'num-columns': 5,
      'data-rows': {
        'range-spec': 'B4:E',
        'header-rows': 3,
        'min-entries': 1,
      },
    },
    '10-membership': {
      'num-columns': 6,
      'data-rows': {
        'range-spec': 'B4:E',
        'header-rows': 3,
        'min-entries': 1,
      },
    },
    '11-language-proficiency': {
      'num-columns': 6,
      'data-rows': {
        'range-spec': 'B4:E',
        'header-rows': 3,
        'min-entries': 2,
      },
    },
    '12-contact': {
      'num-columns': 3,
      'num-rows': 7,
      'error-on-blank': {
        'C3': 'MISSING: Contact Number',
        'C4': 'MISSING: Email',
        'C5': 'MISSING: LinkedIn Page',
        'C6': 'MISSING: GitHub/GitLab Page',
        'C7': 'MISSING: Personal Page',
      },
    },
    '13-educational-certificates': {
      'num-columns': 2,
      'data-rows': {
        'range-spec': 'B3:B',
        'header-rows': 2,
        'min-entries': 6,
      },
    },
    '14-vendor-certificates': {
      'num-columns': 2,
      'data-rows': {
        'range-spec': 'B3:B',
        'header-rows': 2,
        'min-entries': 2,
      },
    },
    '15-institutional-certificates': {
      'num-columns': 2,
      'data-rows': {
        'range-spec': 'B3:B',
        'header-rows': 2,
        'min-entries': 2,
      },
    },
    'z-header': {
      'num-columns': 3,
      'data-rows': {
        'range-spec': 'B3:C',
        'header-rows': 2,
        'min-entries': 1,
      },
    },
    'z-footer': {
      'num-columns': 3,
      'data-rows': {
        'range-spec': 'B3:C',
        'header-rows': 2,
        'min-entries': 1,
      },
    },
  }
};
