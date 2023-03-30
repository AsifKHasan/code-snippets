// create worksheet *00-layout-new*
function create_00_layout_worksheet(ss_name=undefined){
  var ws_name = '00-layout';
  var ws_index = 1;
  var ws_rows = 50;
  var ws_columns = 9;
  var ws_column_sizes = [];

  for (const [key, value] of Object.entries(RESUME_WS_COLUMNS['00-layout'])) {
    ws_column_sizes.push(value);
  };

  // create worksheet
  var ws = create_worksheet(ss_name, ws_name, ws_index, ws_rows, ws_columns, ws_column_sizes);
  if (ws == null){
    return;
  }

  ws.activate();

  // add review note column
  add_review_notes_column(ws);

  // freeze two rows
  ws.setFrozenRows(2);

  // set font, size and vertical alignment for whole worksheet
  var range = ws.getRange(1, 1, ws.getMaxRows(), ws.getMaxColumns());
  range.setFontFamily('Calibri').setFontSize(10).setVerticalAlignment('top');

  // set wrapping
  range.setWrap(true);

  // write column sizes in top row
  get_and_write_column_size(ws);

  // apply range spec on ranges
  for (const [key, value] of Object.entries(WS_FORMAT['00-layout'])) {
    var range = ws.getRange(key);
    work_on_range(ws.getParent(), range, value);
  };

  // apply blank warning to ranges
  add_conditional_formatting_for_blank_cells(ws, WS_WARN_IF_BLANK['00-layout']);

};


// update *00-layout* worksheet structure
function update_00_layout_worksheet_structure(ss){
  if (ss != null){
    var ws_name = '00-layout';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      ws.clearConditionalFormatRules();

      var total_rows = ws.getMaxRows();
      var total_columns = ws.getMaxColumns();

      // conditional formats
      range = ws.getRange(3, 1, total_rows - 2, total_columns);

      // conditional formatting
      add_conditional_formatting_for_blank_cells(ws, RESUME_WS_SPECS[ws_name]['cell-empty-markers']);

      // review-notes
      var rules = ws.getConditionalFormatRules();
      var rule = SpreadsheetApp.newConditionalFormatRule()
        .setRanges([range])
        .whenFormulaSatisfied("=not(isblank($A:$A))")
        .setBackground('#f4cccc')
        .build();
      rules.push(rule);

      ws.setConditionalFormatRules(rules);

    } else {
      Logger.log(`.. ERROR: worksheet ${ws_name} not found`);
    }
  };
};


// update *00-layout* worksheet
function update_00_layout_worksheet_links(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '00-layout';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      // check if the worksheet has at least 53 rows having content
      var min_rows_that_must_have_content = 52;
      var rows_with_content = ws.getLastRow();
      if(rows_with_content < min_rows_that_must_have_content){
        Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
        return;
      }

      // iterate over LAYOUT_WORKKSHEET_LINKS to get cell values, links and notes
      for (const [key, value] of Object.entries(RESUME_WS_SPECS[ws_name]['cell-links'])) {

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


// update *00-layout* worksheet contents
function update_00_layout_worksheet_content(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '00-layout';
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
      for (const [key, value] of Object.entries(WORKKSHEET_CONTENTS[ws_name])) {
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


// update *00-layout* worksheet photo
function update_00_layout_worksheet_photo(ss_name, ss_org){
  var ss = open_spreadsheet(ss_name);
  var org = ss_org.toLowerCase();

  if (ss != null){
    var ws_name = '00-layout';
    var ws = ss.getSheetByName(ws_name);

    if (ws != null){
      // check if the worksheet has at least 50 rows having content
      var min_rows_that_must_have_content = 50;
      var rows_with_content = ws.getLastRow();
      if(rows_with_content < min_rows_that_must_have_content){
        Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
        return;
      }

      // formula is in a specific cell
      var cell_A1 = 'J7';
      var cell = ws.getRange(cell_A1);

      if (cell == null){
        Logger.log(` .. ERROR .. Cell ${cell_A1} not found`);
        return;
      } else {
        // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/photo/spectrum/photo__Khandakar.Asif.Hasan.png", 1)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/artifacts/photo/${org}/photo__${name_without_space}.png", 1)`;
        cell.setFormula(formula);
        cell.setHorizontalAlignment('center');
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};


// update *00-layout* worksheet signature
function update_00_layout_worksheet_signature(ss_name, ss_org){
  var ss = open_spreadsheet(ss_name);
  var org = ss_org.toLowerCase();

  if (ss != null){
    var ws_name = '00-layout';
    var ws = ss.getSheetByName(ws_name);

    if (ws != null){
      // check if the worksheet has at least 50 rows having content
      var min_rows_that_must_have_content = 50;
      var rows_with_content = ws.getLastRow();
      if(rows_with_content < min_rows_that_must_have_content){
        Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
        return;
      }

      // formula is in a specific cell
      var cell_A1 = 'I47';
      var cell = ws.getRange(cell_A1);

      if (cell == null){
        Logger.log(` .. ERROR .. Cell ${cell_A1} not found`);
        return;
      } else {
        // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/signature/spectrum/signature__Khandakar.Asif.Hasan.png", 1)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/artifacts/signature/${org}/signature__${name_without_space}.png", 1)`;
        cell.setFormula(formula);
        cell.setHorizontalAlignment('center');
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};
