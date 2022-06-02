// returns a list of ss_data (spreadsheet name + organization) from the *-toc* sheet based on some filtering criteria
function select_resume_spreadsheets_from_toc(ss, ws){
  // get the ss_names based on some criteria from the current spreadsheet *-toc* worksheet
  var toc_data = ws.getRange('A5:X').getValues();
  var column_map = RESUME_WS_SPECS[ws.getName()]['column-index'];

  var ss_data_list = [];
  toc_data.forEach(function(row, index){
    var row_num = index + 5;
    // we must have a value in link column
    if (row[column_map['link'] - 1] != ''){
      // now we apply custom filters

      // let us select only Spectrum scm employees
      // if (row[column_map['organization'] - 1] == 'Spectrum'){
      // if (row[column_map['organization'] - 1] == 'Spectrum' && row[column_map['unit'] - 1] == 'dc-infra'){
      // if (row[column_map['heading'] - 1] == 'A. S. M. Estiuk Sadick'){
      if (row[column_map['process'] - 1] == 'Yes'){
      // if (row_num >= 100 && row_num < 320){
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


// update *01-personal* worksheet
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
        // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/photo/spectrum/photo__Khandakar.Asif.Hasan.png", 1)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/artifacts/photo/${org}/photo__${name_without_space}.png", 1)`;
        cell.setFormula(formula);
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};


// update *06-job-history* worksheet
function update_06_job_history_worksheet(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss == null){
    return;
  };

  // get the *job-history* worksheet
  var ws_name = '06-job-history';
  var ws = ss.getSheetByName(ws_name);

  // append a row for safety
  ws.insertRowsAfter(ws.getMaxRows(), 1);

  var total_rows = ws.getMaxRows();
  var total_columns = ws.getMaxColumns();

  // we do it only if the worksheet has 7 columns
  if (total_columns != 7){
    Logger.log(` .. worksheet ${ws_name} does not have 7 columns` );
    return;
  }

  ws.clearConditionalFormatRules();

  // unfreeze
  ws.setFrozenRows(0);

  // add columns as defined in RESUME_WS_COLUMNS
  for (const [key, value] of Object.entries(RESUME_WS_SPECS[ws_name]['columns'])) {
    // Logger.log('column ' + key + ' size ' + value);
    var index = LETTER_TO_COLUMN[key];
    ws.insertColumns(index);
    ws.setColumnWidth(index, value);
  };

  // first we create a 4 row gap between entries, each entry starts at column E now, starting at row 4
  var current_row = 4;
  while(1){
    // if there is a value in this row column E, insert 4 rows above
    var column = LETTER_TO_COLUMN['E'];
    var range_spec = `E${current_row}`;
    var values = ws.getRange(range_spec).getValues();
    // Logger.log(`.. cell ${range_spec} : ${values[0][0]}`);
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

  var current_row = 4;
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
    // Logger.log(r);
    var source_range_spec = `E${r[0]}:J${r[1]}`;
    var source_range = ws.getRange(source_range_spec);


    var target_range_spec = `B${r[0] - 3}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    // Logger.log(`preparing range : ${target_range_spec}`);

    target_range.setBorder(true, true, true, true, false, false, "#999999", SpreadsheetApp.BorderStyle.SOLID).setHorizontalAlignment('left');
    // conditional formats
    add_conditional_formatting_for_blank_cells(ws, [target_range_spec]);



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
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('left').setFontWeight("bold");

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


  // review-notes
  range = ws.getRange(3, 1, ws.getMaxRows() - 2, ws.getMaxColumns());
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenFormulaSatisfied("=not(isblank($A:$A))")
    .setBackground('#f4cccc')
    .build();
  rules.push(rule);

  ws.setConditionalFormatRules(rules);


};


// update *07-project-roles* worksheet
function update_07_project_roles_worksheet(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss == null){
    return;
  };

  // get the *07-project-roles* worksheet
  var ws_name = '07-project-roles';
  var ws = ss.getSheetByName(ws_name);

  // append a row for safety
  ws.insertRowsAfter(ws.getMaxRows(), 1);

  var total_rows = ws.getMaxRows();
  var total_columns = ws.getMaxColumns();

  // we do it only if the worksheet has 8 columns
  if (total_columns != 8){
    Logger.log(` .. worksheet ${ws_name} does not have 7 columns` );
    return;
  }

  ws.clearConditionalFormatRules();

  // unfreeze
  ws.setFrozenRows(0);

  // add columns as defined in RESUME_WS_COLUMNS
  for (const [key, value] of Object.entries(RESUME_WS_SPECS[ws_name]['columns'])) {
    // Logger.log('column ' + key + ' size ' + value);
    var index = LETTER_TO_COLUMN[key];
    ws.insertColumns(index);
    ws.setColumnWidth(index, value);
  };

  // first we create a 10 row gap between entries, each entry starts at column E now, starting at row 4
  var current_row = 4;
  while(1){
    // if there is a value in this row column G [Project/Product], insert 10 rows above
    var column = LETTER_TO_COLUMN['E'];
    var range_spec = `E${current_row}`;
    var values = ws.getRange(range_spec).getValues();
    // Logger.log(`.. cell ${range_spec} : ${values[0][0]}`);
    if(values[0][0] != ''){
      ws.insertRowsBefore(current_row, 10);
      current_row = current_row + 11;
    } else {
      current_row++;
    }
    if (current_row >= ws.getMaxRows()){
      break;
    }
  };

  var current_row = 4;
  var rows_starting_data = [];
  while(1){
    // if there is a value in this row column G [Project/Product], insert 4 rows above
    var column = LETTER_TO_COLUMN['G'];
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
      data_row_ranges.push([rows_starting_data[i], rows_starting_data[i+1] - 11]);
    } else {
      data_row_ranges.push([rows_starting_data[i], ws.getMaxRows()]);
    }
  }

  // unmerge everything in range B3:D
  var range = ws.getRange('B3:D');
  range.breakApart();

  const SOURCE_COLUMNS = {
    Project : 1,
    Description : 2,
    Role : 3,
    Activities : 4,
    DateFrom : 6,
    DateTo : 7,
  };

  const TARGET_COLUMNS = {
    A : 1,
    B : 2,
    C : 3,
  };

  // now we have enough space for filling the first three columns
  const OFFSET = 9;
  data_row_ranges.forEach(function(r, i){
    // Logger.log(r);
    var source_range_spec = `E${r[0]}:K${r[1]}`;
    var source_range = ws.getRange(source_range_spec);


    var target_range_spec = `B${r[0] - OFFSET}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    // Logger.log(`preparing range : ${target_range_spec}`);

    target_range.setBorder(true, true, true, true, false, false, "#999999", SpreadsheetApp.BorderStyle.SOLID).setHorizontalAlignment('left');
    // conditional formats
    add_conditional_formatting_for_blank_cells(ws, [target_range_spec]);


    // TODO: process col A, 1st row - Project/Product
    target_cell = target_range.getCell(1, TARGET_COLUMNS.A);
    target_cell.setValue('Project/Product').setFontWeight("bold");

    target_cell = target_range.getCell(1, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Project);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");


    // TODO: process col A, 2nd row - Client
    target_cell = target_range.getCell(2, TARGET_COLUMNS.A);
    target_cell.setValue('Client').setFontWeight("bold");

    target_cell = target_range.getCell(2, TARGET_COLUMNS.B);
    target_cell.setFontWeight("bold");


    // TODO: process col A, 3rd row - Tenure
    target_cell = target_range.getCell(3, TARGET_COLUMNS.A);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.DateFrom)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('right').setFontWeight("bold");

    target_cell = target_range.getCell(3, TARGET_COLUMNS.B);
    target_cell.setValue('-');
    target_cell.setHorizontalAlignment('center').setFontWeight("bold");

    target_cell = target_range.getCell(3, TARGET_COLUMNS.C);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.DateTo)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('left').setFontWeight("bold");


    // TODO: process col A, 4th row - Project Brief
    target_cell = target_range.getCell(4, TARGET_COLUMNS.A);
    target_cell.setValue('Project Brief').setFontWeight("bold");

    target_cell = target_range.getCell(4, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Description);
    target_cell.setValue(source_cell.getValue());

    // row 6 Tools and Technology
    target_cell = target_range.getCell(6, TARGET_COLUMNS.B);
    target_cell.setValue('Tools and Technology').setFontWeight("bold");

    // row 7-8 column C bullet symbol
    target_cell = target_range.getCell(7, TARGET_COLUMNS.B);
    target_cell.setValue('•').setHorizontalAlignment('center');

    target_cell = target_range.getCell(8, TARGET_COLUMNS.B);
    target_cell.setValue('•').setHorizontalAlignment('center');


    // TODO: process col A, 9th row - Role(s) Performed
    target_cell = target_range.getCell(9, TARGET_COLUMNS.A);
    target_cell.setValue('Role(s) Performed').setFontWeight("bold");

    target_cell = target_range.getCell(9, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Role);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");


    // TODO: process col A, 10th row - Activities/Tasks Performed
    target_cell = target_range.getCell(10, TARGET_COLUMNS.A);
    target_cell.setValue('Activities/Tasks Performed').setFontWeight("bold");

    // 10th row to end, column C center aligned
    var target_range_spec = `C${r[0]}:C${r[1]}`;
    var target_range = ws.getRange(target_range_spec);
    target_range.setHorizontalAlignment('center');


    // TODO: process col Activities
    // var source_range_spec = `J${r[0]}:K${r[1]}`;
    var source_range = ws.getRange(r[0], SOURCE_COLUMNS.Activities + 4, r[1]-r[0]+1, 2);

    var target_range_spec = `C${r[0]}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    source_range.copyTo(target_range, {contentsOnly:true});
  });


  // merging
  data_row_ranges.forEach(function(r, i){
    // merge row 1 - [Project/Product] column C and D horizontally
    var range_spec = `C${r[0] - OFFSET}:D${r[0] - OFFSET}`
    // Logger.log(`.. merging ${range_spec} - [Project/Product]`);
    var range = ws.getRange(range_spec);
    range.merge();


    // merge row 2 - [Client] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 1 - OFFSET}:D${r[0] + 1 - OFFSET}`);
    range.merge();


    // merge row 4-6 - [Project Brief] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 3 - OFFSET}:D${r[0] + 5 - OFFSET}`);
    range.mergeAcross();


    // merge row 4-8 - [Project Brief] column B vertically
    var range = ws.getRange(`B${r[0] + 3 - OFFSET}:B${r[0] + 7 - OFFSET}`);
    range.merge();


    // merge row 9 - [Role(s) Performed] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 8 - OFFSET}:D${r[0] + 8 - OFFSET}`);
    range.merge();


    // merge row 10-end - [Activities/Tasks Performed] column B vertically
    var range = ws.getRange(`B${r[0] + 9 - OFFSET}:B${r[1]}`);
    range.merge();
  });


  // *content* in B2 and merge to D2
  var cell = ws.getRange('B2');
  cell.setValue('content');
  var range = ws.getRange('B2:D2');
  range.merge();


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

  // remove column E to K
  ws.deleteColumns(5, 7);


  // review-notes
  range = ws.getRange(3, 1, ws.getMaxRows() - 2, ws.getMaxColumns());
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenFormulaSatisfied("=not(isblank($A:$A))")
    .setBackground('#f4cccc')
    .build();
  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};


// resize rows and update notes in 13, 14 and 15
function do_miscellaneous_things(ss){
  if (ss != null){
    var ws_name_list = ['13-educational-certificates', '14-vendor-certificates', '15-institutional-certificates'];
    ws_name_list.forEach((ws_name) => {
      var ws = ss.getSheetByName(ws_name);
      if (ws != null){
        var range = ws.getRange('B3:B');
        var num_rows = range.getNumRows();
        Logger.log(`.. worksheet ${ws_name} : ${num_rows + 2} rows`);
        for (i = 1; i <= num_rows; i++){
          var cell = range.getCell(i, 1);
          if (cell.getNote() === '{"new-page": true, "keep-with-next": true}'){
            cell.setNote('{"content": "out-of-cell", "keep-with-next": true}');
          }
          if (ws.getRowHeight(i+2) > 100){
            Logger.log(`.... row ${i + 2} height to be set to 450`);
            ws.setRowHeight(i+2, 450);
          }
        };
      };
    });
  };
};
