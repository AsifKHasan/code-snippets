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
