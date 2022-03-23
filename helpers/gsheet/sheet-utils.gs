function workOnLanguageProficiencyWorksheet(sheet) {
  var ws_name = 'language-proficiency';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // remove column 2 (#)
  ws.deleteColumn(2);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setValue('content').setHorizontalAlignment("left");

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 200, 270, 270, 270, 300];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnMembershipWorksheet(sheet) {
  var ws_name = 'membership';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // remove column 2 (#)
  ws.deleteColumn(2);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setValue('content').setHorizontalAlignment("left");

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 300, 150, 150, 100, 300];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnCertificationWorksheet(sheet) {
  var ws_name = 'certification';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 5 (Year) to position 2
  var columnSpec = ws.getRange("E1:E1");
  ws.moveColumns(columnSpec, 2);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");

  // remove column 3 (#)
  ws.deleteColumn(3);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 100, 200, 400, 400];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnTrainingWorksheet(sheet) {
  var ws_name = 'training';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 5 (Year) to position 2
  var columnSpec = ws.getRange("E1:E1");
  ws.moveColumns(columnSpec, 2);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");

  // remove column 3 (#)
  ws.deleteColumn(3);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 100, 500, 300];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnProjectRolesWorksheet(sheet) {
  var ws_name = 'project-roles';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 2 (#) to position 6
  var columnSpec = ws.getRange("B1:B1");
  ws.moveColumns(columnSpec, 6);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");

  // merge # and Activities/Tasks Performed
  ws.getRange('e3:f3').merge().setValue('Activities/Tasks Performed	').setHorizontalAlignment('left');

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 200, 200, 200, 40, 400, 120, 120];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnJobHistoryWorksheet(sheet) {
  var ws_name = 'job-history';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 2 (#) to position 5
  var columnSpec = ws.getRange("B1:B1");
  ws.moveColumns(columnSpec, 5);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");

  // merge # and Job Summary
  ws.getRange('d3:e3').merge().setValue('Job Summary').setHorizontalAlignment('left');

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 200, 200, 40, 500, 120, 120];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnTechnicalExpertiseWorksheet(sheet) {
  var ws_name = 'technical-expertise';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // remove column 2 (#)
  ws.deleteColumn(2);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 200, 800];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnManagerialExpertiseWorksheet(sheet) {
  var ws_name = 'managerial-expertise';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // remove column 2 (#)
  ws.deleteColumn(2);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 200, 800];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnEducationWorksheet(sheet) {
  var ws_name = 'education';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 6 (Year) to position 2
  var columnSpec = ws.getRange("F1:F1");
  ws.moveColumns(columnSpec, 2);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");

  // remove column 3 (#)
  ws.deleteColumn(3);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 100, 300, 300, 300];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnCareerHighlightWorksheet(sheet) {
  var ws_name = 'career-highlight';
  var ws = sheet.getSheetByName(ws_name);

  // unmerge b2 (content)
  var range = ws.getRange('b2');
  if (range.isPartOfMerge()) {
    var merged_range = range.getMergedRanges()[0];
    merged_range.breakApart();
  }

  // move column 2 (#) to position 4
  var columnSpec = ws.getRange("B1:B1");
  ws.moveColumns(columnSpec, 4);

  // merge b2 (content) across the end
  var range = ws.getRange(2, 2, 1, ws.getLastColumn() - 1);
  range.mergeAcross().setHorizontalAlignment("left");


  // remove row 3
  ws.deleteRow(3);

  // vertically top-align worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('top');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 150, 30, 800];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

function workOnPersonalWorksheet(sheet) {
  var ws_name = 'personal';
  var ws = sheet.getSheetByName(ws_name);

  // remove row 3
  ws.deleteRow(3);

  // merge e3:e13 and put photo link
  var range = ws.getRange('e3:e13').merge();
  var photo_name = sheet.getName().replace('Résumé__', 'photo__');
  var formula = '=image("https://spectrum-bd.biz/data/photo/' + photo_name + '.png", 1)'
  range.getCell(1, 1).setFormula(formula);

  // vertically center worksheet
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setVerticalAlignment('middle');

  // resize columns and remove extra columns at right
  var column_sizes = [100, 40, 130, 330, 400];
  for (i = 0; i < column_sizes.length; i++) {
    ws.setColumnWidth(i + 1, column_sizes[i]);
  }

  // remove all right columns after specified columns
  var total_columns = ws.getMaxColumns();
  if (total_columns > column_sizes.length) {
    ws.deleteColumns(column_sizes.length + 1, total_columns - column_sizes.length);
  }

  getAndWriteColumnSizeInFirstRow(ws);
};

// open a sheet from name
function openSheet(sheet_name) {
  var files = DriveApp.searchFiles('title = "' + sheet_name + '" and mimeType = "' + MimeType.GOOGLE_SHEETS + '"');
  if (files.hasNext()) {
    var sheet = SpreadsheetApp.open(files.next());
  }

  if (files.hasNext()) {
    Logger.log('There are more than one file with the name : ' + file_name);
  }

  return null;
};

// add review-notes column as the first column, width 100, left
function addConditionalFormattingForBlankCells(ws) {
  var total_rows = ws.getMaxRows();
  var total_columns = ws.getMaxColumns();

  var range = ws.getRange(3, 2, total_rows - 2, total_columns);

  // conditional formatting
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenCellEmpty()
    .setBackground('#fff2cc')
    .build();

  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};

 // add review-notes column as the first column, width 100, left
function addReviewNotesColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  ws.insertColumns(index);

  var total_columns = ws.getMaxColumns();

  // width, heading and alignment
  ws.setColumnWidth(index, 100);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(2, index).setValue("review-notes");

  // data validation
  ws.getRange(3, index).activate();
  range = ws.getRange(3, index, total_rows - 3);
  range.clearDataValidations();
  range.setBackground("#ffffff");

  range = ws.getRange(3, 1, total_rows - 2, total_columns);

  // conditional formatting
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenFormulaSatisfied("=not(isblank($A:$A))")
    .setBackground('#f4cccc')
    .build();

  rules.push(rule);

  ws.setConditionalFormatRules(rules);

};

// format the second row
function formatSecondRow(ws) {
  var last_col_with_data = ws.getLastColumn();

  // merge b2 across the end
  var range = ws.getRange(2, 2, 1, last_col_with_data - 1);
  range.mergeAcross().setHorizontalAlignment("left").setValue("content");

  var range = ws.getRange(2, 1, 1, last_col_with_data - 1);
  range.setBackground("#d9d9d9");
  range.setFontWeight("bold");
};

// get column size for each column and write the size in row 1 for that column
function getAndWriteColumnSizeInFirstRow(ws) {
  var numColumns = ws.getMaxColumns();
  for (i = 1; i <= numColumns; i++) {
    column_size_pixel = ws.getColumnWidth(i);
    // put the value in the first row of that column
    cell = ws.getRange(1, i);
    cell.setHorizontalAlignment("center");
    cell.setNumberFormat("0");
    cell.setValue(column_size_pixel);
  }
};

// border from b3 to bottom-right
function setContentBorder(ws) {
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  var range = ws.getRange(3, 2, total_rows - 2, last_col_with_data - 1);
  range.setBorder(true, true, true, true, true, true, '#b7b7b7', SpreadsheetApp.BorderStyle.SOLID);
};

// full worksheet font to Calibri 10
function formatWorksheetFontAndSize(ws) {
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  var range = ws.getRange(1, 1, total_rows, last_col_with_data);
  range.setFontFamily('Calibri');
  range.setFontSize(10);
};
