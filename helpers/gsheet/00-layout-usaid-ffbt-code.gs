LAYOUT_SPECS = {
  'num-columns': 4,
  'columns': {'B': 30, 'C': 370, 'D': 400, },
  'ranges': {
    'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'left'},
    'B7': {'value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'note': '{"content": "free"}'},
    'B10': {'value': '03-education', 'ws-name-to-link': '03-education', 'note': '{"content": "free"}'},
    'B13': {'value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "free"}'},
    'B16': {'value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'note': '{"content": "free"}'},
    'B19': {'value': '16-references', 'ws-name-to-link': '16-references', 'note': '{"content": "free"}'},

  },

  'cell-empty-markers': [
  ],
};

// update *00-layout_nbr_bsw* worksheet
function update_worksheet_00_layout_USAID_FFBT(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '00-layout-USAID-FFBT';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      // iterate over ranges and apply specs
      for (const [key, value] of Object.entries(LAYOUT_SPECS['ranges'])) {
        var range = ws.getRange(key);
        if (range === null){
          Logger.log(`ERROR: Range ${key} not found`);
          continue;
        } else {
          Logger.log(`.. Range ${key} found`);
          work_on_range(ss=ss, range=range, work_spec=value);
        }
      };
    } else {
      Logger.log(`.. ERROR: worksheet ${ws_name} not found`);
    }
  };
};
