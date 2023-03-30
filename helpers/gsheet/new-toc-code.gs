LAYOUT_TOC_NEW_WS_SPECS = {
  'num-columns': 24,
  'columns': {'A': 60, 'B': 200, },
  'ranges': {
    'F3': {'cell-value': '00-layout-NBR-BSW', 'ws-name-to-link': '00-layout-NBR-BSW'},
  },
};

// update *-toc-new* worksheet
function update_toc_new_worksheet_links(ss_name=undefined){
if (ss_name == undefined){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
} else {
  var ss = open_spreadsheet(ss_name);
};

if (ss != null){
  var ws_name = '-toc-new';
  var ws = ss.getSheetByName(ws_name);
  if (ws != null){
    // iterate over ranges to get cell values, links and notes
    for (const [key, value] of Object.entries(LAYOUT_TOC_NEW_WS_SPECS['ranges'])) {

      var cell = ws.getRange(key);
      if (cell === null){
        Logger.log(`ERROR: Cell ${key} not found`);
        return;
      } else {
        Logger.log(`.. Cell ${key} found`);
      }

      if ('cell-value' in value){
        cell.setValue(value['cell-value']);
      }

      if ('ws-name-to-link' in value){
        link_cell_to_worksheet(ss, cell, value['ws-name-to-link']);
      }

      if ('note' in value){
        cell.setNote(value['note']);
      }
    }

  } else {
    Logger.log(`ERROR: Worksheet ${ws_name} not found`);
  }
};
};


// update *00-layout_nbr_bsw* worksheet contents
function update_00_layout_nbr_bsw_worksheet_content(ss_name=undefined){
if (ss_name == undefined){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
} else {
  var ss = open_spreadsheet(ss_name);
};

if (ss != null){
  var ws_name = '00-layout-nbr-bsw';
  var ws = ss.getSheetByName(ws_name);
  if (ws != null){
    // check if the worksheet has at least 53 rows having content
    var min_rows_that_must_have_content = 53;
    var rows_with_content = ws.getLastRow();
    if(rows_with_content < min_rows_that_must_have_content){
      Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
      return;
    }

    // iterate over LAYOUT_WORKKSHEET_LINKS to get cell values, links and notes
    for (const [key, value] of Object.entries(LAYOUT_NBR_BSW_WS_SPECS)) {
      var cell = ws.getRange(key);
      if (cell == null){
        Logger.log(`ERROR: Cell ${key} not found`);
        return;
      }
      if ('cell-value' in value){
        cell.setValue(value['cell-value']);
      };
    };
  } else {
    Logger.log(`ERROR: Worksheet ${ws_name} not found`);
  };
};
};
