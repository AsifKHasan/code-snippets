// add review-notes column as the first column, width 100, left
function addConditionalFormattingForBlankCells(ws, range_spec_list) {
  // get the ranges
  var range_list = [];
  for (i = 0; i < range_spec_list.length; i++) {
    range_list.push(ws.getRange(range_spec_list[i]));
  };

  // conditional formatting
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges(range_list)
    .whenCellEmpty()
    .setBackground('#fff2cc')
    .build();

  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};

// add review-notes column as the first column, width 100, left
function add_review_notes_column(ws, index=1) {
  ws.insertColumns(index);

  var total_rows = ws.getMaxRows();
  var total_columns = ws.getMaxColumns();

  // width, heading and alignment
  ws.setColumnWidth(index, 100);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(2, index).setValue("review-notes").setFontWeight("bold");

  // data validation
  // ws.getRange(3, total_columns).activate();
  range = ws.getRange(3, index, total_rows - 2, total_columns);
  // range.clearDataValidations();

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


// link cell to an worksheet, optionally set cell value
function link_cell_to_worksheet(ss, cell, ws_name_to_link) {
    if (ss == null ){
      Logger.log(`ERROR: spreadsheet is null`);
      return;
    }

    if (cell == null ){
      Logger.log(`ERROR: cell is null`);
      return;
    }

    var ws_to_link = ss.getSheetByName(ws_name_to_link);
    if (ws_to_link == null ){
      Logger.log(`worksheet ${ws_name_to_link} not found`);
      return;
    }

    var link = `=HYPERLINK("#gid=${ws_to_link.getSheetId()}","${cell.getValue()}")`;
    cell.setFormula(link);
};


// get column size for each column and write the size in row 1 for that column
// ignores the first column (A - review-notes)
function get_and_write_column_size(ws=undefined) {
  if (ws == undefined){
    var ws = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }

  var numColumns = ws.getMaxColumns();
  for (i = 2; i <= numColumns; i++) {
    var column_size_pixel = ws.getColumnWidth(i);
    // put the value in the first row of that column
    cell = ws.getRange(1, i);
    cell.setHorizontalAlignment("center").setNumberFormat("0").setValue(column_size_pixel);
  }
};


// for resizing columns based on size mentioned in the top row
// ignores the first column (A - review-notes)
function resize_columns_with_sizes_in_first_row() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ws = ss.getActiveSheet();
  numColumns = ws.getMaxColumns();

  for (i = 2; i <= numColumns; i++) {
    cell = ws.getRange(1, i);
    ws.setColumnWidth(i, cell.getValue());
  }
};


// for calculating the sizes of each column in a table layout in inches
// ignores the first column (A - review-notes) and assumes that pages are 6.77 inches wide excluding margins and gutters
function get_and_write_column_width_in_inches() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ws = ss.getActiveSheet();
  var width_in = 6.77

  numColumns = ws.getMaxColumns();
  sumOfColumnSizes = 0;
  for (i = 2; i <= numColumns; i++) {
    sumOfColumnSizes += ws.getColumnWidth(i);
  }

  // calculate size of each column in inches
  for (i = 2; i <= numColumns; i++) {
    column_size_in = (ws.getColumnWidth(i) / sumOfColumnSizes) * width_in;
    // put the value in the first row of that column
    cell = ws.getRange(1, i);
    cell.setHorizontalAlignment("center");
    cell.setNumberFormat("0.00");
    cell.setValue(column_size_in);
  }
};


// get a range and link each cell with the worksheet named in the cell
// if worksheet does not exit create it with a base template
function link_cells(ws, range_spec, template_worksheet_name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  if (template_worksheet_name != null) {
    var template_ws = ss.getSheetByName(template_worksheet_name);
  }

  var range = ws.getRange(range_spec);
  var numRows = range.getNumRows();
  var numCols = range.getNumColumns();
  for (var i = 1; i <= numRows; i++) {
    for (var j = 1; j <= numCols; j++) {
      var cell = range.getCell(i, j);
      var cellValue = cell.getValue();
      Logger.log(cell.getA1Notation() + ': row = ' + i + ', col = ' + j + ', value = ' + cellValue);
      // see if there is a worksheet with cellValue
      var worksheet_to_link = ss.getSheetByName(cellValue);
      if (worksheet_to_link == null && template_worksheet_name != null) {
        var worksheet_to_link = duplicateWorksheet(ss, template_ws, cellValue);
      }

      // do the link
      if (worksheet_to_link != null) {
        linkToWorksheet(cell, worksheet_to_link);
      } else {
        Logger.log('worksheet : ' + cellValue + ' could not be linked');
      }
    }
  }
};


// remove columns from a worksheet where all cells are blank
function remove_trailing_blank_columns(ws) {
  var total_cols = ws.getMaxColumns();
  var last_col_with_data = ws.getLastColumn();
  // Logger.log("out of %s cols, last col with data is %s", total_cols, last_col_with_data);
  // Cols start at "1"
  if (total_cols > last_col_with_data) {
    ws.deleteColumns(last_col_with_data + 1, total_cols - last_col_with_data);
  }
};

// remove all trailing rows from a worksheet where all cells are blank
function remove_trailing_blank_rows(ws) {
  var total_rows = ws.getMaxRows();
  var last_row_with_data = ws.getLastRow();
  // Logger.log("out of %s rows, last row with data is %s", total_rows, last_row_with_data);
  // Rows start at "1"
  if (total_rows > last_row_with_data) {
    ws.deleteRows(last_row_with_data + 1, total_rows - last_row_with_data);
  }
};


// merge cells Across for a given range
function merge_cells_across(range_spec) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ws = ss.getActiveSheet();

    range = ws.getRange(range_spec);
    range.mergeAcross();
};
