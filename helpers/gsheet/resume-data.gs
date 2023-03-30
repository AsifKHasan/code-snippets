RESUME_WS_SPECS = {
  '-toc-new' : {
    'column-index': {
      'section': 1,
      'heading': 2,
      'process': 3,
      'link': 6,
      'responsible': 22,
      'reviewer': 23,
      'status': 24,
      'organization': 25,
      'existing': 26,
      'unit': 27,
    },
  },
  '00-layout' : {
    'num-columns': 10,
    'columns': {'B': 40, 'C': 200, 'D': 40, 'E': 30, 'F': 40, 'G': 30, 'H': 150, 'I': 150, 'J': 320, },
    'cell-links': {
      // 'B13': {'cell-value': '10-membership', 'ws-name-to-link': '10-membership', 'note': '{"content": "out-of-cell"}'},
      // 'B16': {'cell-value': '03-education', 'ws-name-to-link': '03-education', 'note': '{"content": "out-of-cell"}'},
      // 'B19': {'cell-value': '08-training', 'ws-name-to-link': '08-training', 'note': '{"content": "out-of-cell"}'},
      // 'B21': {'cell-value': '09-certification', 'ws-name-to-link': '09-certification', 'note': '{"content": "out-of-cell"}'},
      // 'B24': {'cell-value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'note': '{"content": "out-of-cell"}'},
      'B29': {'cell-value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "out-of-cell"}'},
      'B31': {'cell-value': '07-project-roles', 'ws-name-to-link': '07-project-roles', 'note': '{"content": "out-of-cell"}'},
      // 'B34': {'cell-value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'note': '{"content": "out-of-cell"}'},
      // 'B37': {'cell-value': '05-technical-expertise', 'ws-name-to-link': '05-technical-expertise', 'note': '{"content": "out-of-cell"}'},
      // 'H39': {'cell-value': '12-contact', 'ws-name-to-link': '12-contact'},
      // 'B41': {'note': '{"content": "out-of-cell"}'},
    },
    'cell-contents': {
      // Name of the Firm
      'H3': {'cell-value': 'Spectrum Engineering Consortium Ltd.'},
      // EoI/RFP Reference
      'H4': {'cell-value': '123-456-789-987-654-321'},
      // Name of the Client
      'H5': {'cell-value': 'National Board of Revenue'},
      // Date of Signing - Day / Month / Year
      'I51': {'cell-value': '23 / 03 / 2022'},
    },
    'cell-formats': {
      'A1': {'value': '-toc', 'ws-link': '-toc', 'halign': 'center'},
      'B2:J2': {'value': 'content', 'weight': 'bold'},

      // top table
      'B3:G3': {'value': 'Name of the Firm', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H3:J3': {'weight': 'bold'},
      'B4:G4': {'value': 'EoI/RFP Reference', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H4:J4': {},
      'B5:G5': {'value': 'Name of the Client', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H5:J5': {},
      'B3:J5': {'border-color': '#b7b7b7'},

      // blank row
      'B6:J6': {},

      // info table
      'B7': {'value': '1', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C7:G7': {'value': 'PROPOSED POSITION FOR THIS PROJECT', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H7:I7': {},
      'B8': {'value': '2', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C8:G8': {'value': 'NAME OF STAFF', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H8:I8': {'formula': "='01-personal'!D3"},
      'B9': {'value': '3', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C9:G9': {'value': 'DATE OF BIRTH', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H9:I9': {'formula': "='01-personal'!D5", 'halign': 'left'},
      'B10': {'value': '4', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C10:G10': {'value': 'NATIONALITY', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H10:I10': {'formula': "='01-personal'!D6"},
      'J7:J10': {'halign': 'center'},
      'B7:J10': {'border-color': '#b7b7b7'},

      // blank row
      'B11:J11' : {},

      // 5 - Membership
      'B12': {'value': '5', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C12:J12': {'value': 'MEMBERSHIP IN PROFESSIONAL SOCIETIES', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B13:J13': {'value': '10-membership', 'ws-link': '10-membership', 'notes': '{"content": "out-of-cell"}'},
      'B12:J13': {'border-color': '#b7b7b7'},

      // blank row
      'B14:J14': {},

      // 6 - Education
      'B15': {'value': '6', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C15:J15': {'value': 'EDUCATION', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B16:J16': {'value': '03-education', 'ws-link': '03-education', 'notes': '{"content": "out-of-cell"}'},
      'B15:J16': {'border-color': '#b7b7b7'},

      // blank row
      'B17:J17': {},

      // 7 - Other Training
      'B18': {'value': '7', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C18:J18': {'value': 'OTHER TRAINING', 'weight': 'bold', 'bgcolor': '#f3f3f3'},

      'B19:J19': {'value': '08-training', 'ws-link': '08-training', 'notes': '{"content": "out-of-cell"}'},

      // blank row
      'B20:J20': {},

      'B21:J21': {'value': '09-certification', 'ws-link': '09-certification', 'notes': '{"content": "out-of-cell"}'},
      'B18:J21': {'border-color': '#b7b7b7'},

      // blank row
      'B22:J22': {},

      // 8 - Language Proficiency
      'B23': {'value': '8', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C23:J23': {'value': 'LANGUAGES & DEGREE OF PROFICIENCY', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B24:J24': {'value': '11-language-proficiency', 'ws-link': '11-language-proficiency', 'notes': '{"content": "out-of-cell"}'},
      'B23:J24': {'border-color': '#b7b7b7'},

      // blank row
      'B25:J25': {},

      // 9 - Countries of Experience
      'B26': {'value': '9', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C26:G26': {'value': 'COUNTRIES OF WORK EXPERIENCE', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H26:J26': {'formula': "='01-personal'!D13"},
      'B26:J26': {'border-color': '#b7b7b7'},

      // blank row
      'B27:J27': {},

      // 10 - Employment
      'B28': {'value': '10', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C28:J28': {'value': 'EMPLOYMENT RECORD', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B29:J29': {'value': '06-job-history', 'ws-link': '06-job-history', 'notes': '{"content": "out-of-cell"}'},
      'B28:J29': {'border-color': '#b7b7b7'},

      'B30:J30': {},

      'B31:J31': {'value': '07-project-roles', 'ws-link': '07-project-roles', 'notes': '{"content": "out-of-cell"}', 'border-color': '#b7b7b7'},

      // blank row
      'B32:J32': {},

      // 11 - Jobs Undertaken
      'B33': {'value': '11', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C33:J33': {'value': 'WORK UNDERTAKEN THAT BEST ILLUSTRATES YOUR CAPABILITY TO HANDLE THIS ASSIGNMENT', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B34:J34': {'value': '02-career-highlight', 'ws-link': '02-career-highlight', 'notes': '{"content": "out-of-cell"}'},
      'B33:J34': {'border-color': '#b7b7b7'},

      // blank row
      'B35:J35': {},

      // 12 - Computer Skill
      'B36': {'value': '12', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C36:J36': {'value': 'COMPUTER SKILLS', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'B37:J37': {'value': '05-technical-expertise', 'ws-link': '05-technical-expertise', 'notes': '{"content": "out-of-cell"}'},
      'B36:J37': {'border-color': '#b7b7b7'},

      // blank row
      'B38:J38': {},

      // 13 - Contact
      'B39': {'value': '13', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left'},
      'C39:G39': {'value': 'CONTACT AND WEB INFORMATION', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
      'H39:J39': {'value': '12-contact', 'ws-link': '12-contact'},
      'B39:J39': {'border-color': '#b7b7b7'},

      // blank row
      'B40:J40': {},

      // certification
      'B41:J41': {'value': 'CERTIFICATION [do not amend this certification]', 'notes': '{"content": "out-of-cell"}'},

      // blank row
      'B42:J42': {},

      'B43:J43': {'value': 'I, the undersigned, certify that (i) I was not a former employee of the Client immediately before submission of this Proposal, (ii) I have not offered my CV to be proposed by a Firm other than this Software Firm for this assignment and, (iii) to the best of my knowledge and belief, this CV correctly describes myself, my qualifications, and my experience. I also understand that any willful misstatement described herein may lead to my disqualification or dismissal, if engaged.'},

      // blank row
      'B44:J44': {},

      'B45:J45': {'value': 'I have been employed by [FIRM NAME] continuously for the last twelve (12) months as regular full-time staff. Indicate "Yes" or "No" in the boxes below:'},

      // blank row
      'B46:J46': {},


      // confirmation and signature
      'D47': {'value': 'Yes', 'halign': 'right'},
      'E47': {'value': '✔', 'border-color': '#b7b7b7', 'halign': 'center'},
      'F47': {'value': 'No', 'halign': 'right'},
      'G47': {'border-color': '#b7b7b7', 'halign': 'center'},

      'H49': {'value': 'Signature', 'halign': 'right'},
      'H53': {'value': 'Date of Signing', 'halign': 'right'},

      'I47:J51': {'border-color': '#b7b7b7', 'halign': 'center'},
      'I52:J52': {'halign': 'center'},
      'I53:J53': {'value': 'Day / Month / Year', 'halign': 'center'},
      'I52:J53': {'border-color': '#b7b7b7'},

      // review notes
      'A45': {'value': 'change FIRM NAME'},
      'A52': {'value': 'fill correctly'},
    },
    'cell-empty-markers': [
      'B3:J5', 'B7:J10', 'B12:J13', 'B15:J16', 'B18:J19', 'B21:J21', 'B23:J24', 'B26:J26', 'B28:J29', 'B31:J31', 'B33:J34', 'B36:J37', 'B39:J39',
      'D47', 'E47', 'F47', 'H49', 'H53', 'I47:J51', 'I52:J52', 'I53:J53'
    ],
  },
  '01-personal' : {
    'num-columns': 5,
    'columns': {'B': 40, 'C': 130, 'D': 330, 'E': 400, },
  },
  '02-career-highlight' : {
    'num-columns': 4,
    'columns': {'B': 150, 'C': 30, 'D': 800, },
  },
  '03-education' : {
    'num-columns': 5,
    'columns': {'B': 100, 'C': 200, 'D': 300, 'E': 300, },
  },
  '04-managerial-expertise' : {
    'num-columns': 4,
    'columns': {'B': 170, 'C': 30, 'D': 800, },
  },
  '05-technical-expertise' : {
    'num-columns': 4,
    'columns': {'B': 170, 'C': 30, 'D': 800, },
  },
  '06-job-history' : {
    'num-columns': 4,
    'columns': {'B': 170, 'C': 30, 'D': 700, },
  },
  '07-project-roles' : {
    'num-columns': 4,
    'columns': {'B': 170, 'C': 30, 'D': 700, },
  },
  '08-training' : {
    'num-columns': 4,
    'columns': {'B': 100, 'C': 550, 'D': 350, },
  },
  '09-certification' : {
    'num-columns': 5,
    'columns': {'B': 100, 'C': 200, 'D': 300, 'E': 400,},
  },
  '10-membership' : {
    'num-columns': 6,
    'columns': {'B': 300, 'C': 150, 'D': 150, 'E': 150, 'F': 250, },
  },
  '11-language-proficiency' : {
    'num-columns': 6,
    'columns': {'B': 80, 'C': 270, 'D': 270, 'E': 270, 'F': 210, },
  },
  '12-contact' : {
    'num-columns': 3,
    'columns': {'B': 200, 'C': 600, },
  },
  '13-educational-certificates' : {
    'num-columns': 2,
    'columns': {'B': 1000, },
  },
  '14-vendor-certificates' : {
    'num-columns': 2,
    'columns': {'B': 1000, },
  },
  '15-institutional-certificates' : {
    'num-columns': 2,
    'columns': {'B': 1000, },
  },
};
