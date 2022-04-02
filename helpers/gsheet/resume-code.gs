// returns a list of ss_data (spreadsheet name + organization) from the *-toc* sheet based on some filtering criteria
function select_resume_spreadsheets_from_toc(ss, ws){
  // get the ss_names based on some criteria from the current spreadsheet *-toc* worksheet
  var toc_data = ws.getRange('A5:X').getValues();
  var column_map = RESUME_WS_COLUMN_INDEX[ws.getName()];

  var ss_data_list = [];
  toc_data.forEach(function(row, index){
    var row_num = index + 5;
    // we must have a value in link column
    if (row[column_map['link'] - 1] != ''){
      // now we apply custom filters

      // let us select only Spectrum scm employees
      // if (row[column_map['organization'] - 1] == 'Spectrum'){
      // if (row[column_map['organization'] - 1] == 'Spectrum' && row[column_map['unit'] - 1] == 'dc-infra'){
      // if (row[column_map['heading'] - 1] == 'A.S.M Estiuk Sadick'){
      if (row[column_map['process'] - 1] == 'Yes'){
      // if (row_num >= 248 && row_num <= 288){
      // if (true){
        var ss_name = row[column_map['link'] - 1];
        var ss_org = row[column_map['organization'] - 1];
        ss_data_list.push([ss_name, ss_org, row_num])
      };
    };
  });

  return ss_data_list;
};


// update links in *-toc* worksheet
function update_toc_worksheet_links(ss_name=undefined) {
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '-toc';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      link_cells(ws, 'F56:F154', 'E56:E154', null);
    } else {
      Logger.log(` .. ERROR .. Worksheet ${key} not found`);
    }
  };
};


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
      // check if the worksheet has at least 50 rows having content
      var min_rows_that_must_have_content = 50;
      var rows_with_content = ws.getLastRow();
      if(rows_with_content < min_rows_that_must_have_content){
        Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
        return;
      }

      // iterate over LAYOUT_WORKKSHEET_LINKS to get cell values, links and notes
      for (const [key, value] of Object.entries(WORKKSHEET_LINKS[ws_name])) {

        var cell = ws.getRange(key);
        if (cell == null){
          Logger.log(`ERROR: Cell ${key} not found`);
          return;
        }
        if ('cell-value' in value){
          cell.setValue(value['cell-value']);
        }

        if ('ws-name-to-link' in value){
          link_cell_to_worksheet(ss, cell, value['ws-name-to-link']);
        }

        if ('notes' in value){
          cell.setNote(value['notes']);
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
      // check if the worksheet has at least 50 rows having content
      var min_rows_that_must_have_content = 50;
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
        // this is the link we need =image("https://spectrum-bd.biz/data/photo/spectrum/photo__Khandakar.Asif.Hasan.png", 3)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/photo/${org}/photo__${name_without_space}.png", 3)`;
        cell.setFormula(formula);
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};


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
      var cell_A1 = 'I44';
      var cell = ws.getRange(cell_A1);

      if (cell == null){
        Logger.log(` .. ERROR .. Cell ${cell_A1} not found`);
        return;
      } else {
        // this is the link we need =image("https://spectrum-bd.biz/data/signature/spectrum/signature__Khandakar.Asif.Hasan.png", 3)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/signature/${org}/signature__${name_without_space}.png", 3)`;
        cell.setFormula(formula);
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};


// update *job-history* worksheet
function update_06_job_history_worksheet(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = openSpreadsheet(ss_name);
  };

  if (ss == null){
    return;
  };

  // get the *job-history* worksheet
  var ws_name = 'job-history';
  var ws = ss.getSheetByName(ws_name);
  var ws_pos = ws.getIndex();

  // unfreeze
  ws.setFrozenRows(0);

  // add columns as defined in RESUME_WS_COLUMNS
  for (const [key, value] of Object.entries(RESUME_WS_COLUMNS[ws_name])) {
    // Logger.log('column ' + key + ' size ' + value);
    index = LETTER_TO_COLUMN[key];
    // ws.insertColumns(index);
    // ws.setColumnWidth(index, value);
  };

  // first we create a 4 row gap between entries, eachg entry starts at column E now, starting at row 4
  current_row = 4;
  while(0){
    // if there is a value in this row column E, insert 4 rows above
    var column = LETTER_TO_COLUMN['E'];
    var range = ws.getRange(current_row, column);
    var values = range.getValues();
    if(values[0][0] != ''){
      ws.insertRowsBefore(current_row, 4);
      current_row = current_row + 5;
    } else {
      current_row++;
    }
    if (current_row >= ws.getMaxRows()){
      break;
    }
  };

  current_row = 4;
  var rows_starting_data = [];
  while(1){
    // if there is a value in this row column E, insert 4 rows above
    var column = LETTER_TO_COLUMN['E'];
    var range = ws.getRange(current_row, column);
    var values = range.getValues();
    if(values[0][0] != ''){
      rows_starting_data.push(current_row);
      // Logger.log('at E' + current_row + " found : " + values[0][0]);
    }

    current_row++;

    if (current_row >= ws.getMaxRows()){
      break;
    }
  };

  var data_row_ranges = [];
  for (var i = 0; i < rows_starting_data.length; i++) {
    if(i < rows_starting_data.length - 1){
      data_row_ranges.push([rows_starting_data[i], rows_starting_data[i+1] - 5]);
    } else {
      data_row_ranges.push([rows_starting_data[i], ws.getMaxRows()]);
    }
  }

  // unmerge everything in range B3:D
  var range = ws.getRange('B3:D');
  range.breakApart();

  // now we have enough space for filling the first three columns
  data_row_ranges.forEach(function(r, i){
    var source_range_spec = `E${r[0]}:J${r[1]}`;
    var source_range = ws.getRange(source_range_spec);


    var target_range_spec = `B${r[0] - 3}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    Logger.log(`preparing range : ${target_range_spec}`);

    target_range.setBorder(true, true, true, true, false, false, "#999999", SpreadsheetApp.BorderStyle.SOLID);

    // TODO: process col A, 1st row - Organization
    target_cell = target_range.getCell(1, 1);
    target_cell.setValue('Organization').setFontWeight("bold");

    target_cell = target_range.getCell(1, 3);
    source_cell = source_range.getCell(1, 1);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");

    // TODO: process col A, 2nd row - Position
    target_cell = target_range.getCell(2, 1);
    target_cell.setValue('Position').setFontWeight("bold");

    target_cell = target_range.getCell(2, 3);
    source_cell = source_range.getCell(1, 2);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");

    // TODO: process col A, 3rd row - Tenure
    target_cell = target_range.getCell(3, 1);
    source_cell = source_range.getCell(1, 5)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('right').setFontWeight("bold");

    target_cell = target_range.getCell(3, 2);
    target_cell.setValue('-');
    target_cell.setHorizontalAlignment('center').setFontWeight("bold");

    target_cell = target_range.getCell(3, 3);
    source_cell = source_range.getCell(1, 6)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setFontWeight("bold");

    // TODO: process col A, 4th row - Job Summary
    target_cell = target_range.getCell(4, 1);
    target_cell.setValue('Job Summary').setFontWeight("bold");

    // TODO: process col B and C
    var source_range_spec = `G${r[0]}:H${r[1]}`;
    var source_range = ws.getRange(source_range_spec);

    var target_range_spec = `C${r[0]}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    source_range.copyTo(target_range, {contentsOnly:true});

    // center align column B bullet symbols
    var range_spec = `C${r[0]}:C${r[1]}`;
    var range = ws.getRange(range_spec);
    range.setHorizontalAlignment('center');
  });

  // merging
  data_row_ranges.forEach(function(r, i){
    // merge column B Job Summary vertically
    var range_spec = `B${r[0]}:B${r[1]}`;
    var range = ws.getRange(range_spec);
    range.merge();

    // merge column C and D for organization and position across
    var range_spec = `C${r[0] - 3}:D${r[0] - 2}`;
    Logger.log(`merging across : ${range_spec}`);
    var range = ws.getRange(range_spec);
    range.mergeAcross();
  });

  // *content* in B2 and merge to D2
  var cell = ws.getRange('B2');
  cell.setValue('content');
  var range = ws.getRange('B2:D2');
  range.mergeAcross();

  // remove all rows starting from 3 where column B is empty
  var rows_to_remove = 0;
  for (var i = 3; i < ws.getMaxRows(); i++) {
    var cell = ws.getRange(`B${i}`);
    if (cell.getValue() == ''){
      rows_to_remove++;
    } else {
      break;
    }
  }
  ws.deleteRows(3, rows_to_remove);

  // remove column E to J
  ws.deleteColumns(5, 6);
};


function update_01_personal_worksheet_photo(ss_name, ss_org){
  var ss = open_spreadsheet(ss_name);
  var org = ss_org.toLowerCase();

  if (ss != null){
    var ws_name = '01-personal';
    var ws = ss.getSheetByName(ws_name);

    if (ws != null){
      // formula is in a specific cell
      var cell_A1 = 'E3';
      var cell = ws.getRange(cell_A1);

      if (cell == null){
        Logger.log(` .. ERROR .. Cell ${cell_A1} not found`);
        return;
      } else {
        // this is the link we need =image("https://spectrum-bd.biz/data/photo/spectrum/photo__Khandakar.Asif.Hasan.png", 3)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/photo/${org}/photo__${name_without_space}.png", 3)`;
        cell.setFormula(formula);
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};
