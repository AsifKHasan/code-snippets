// do some work on a list of worksheets
function work_on_worksheets(ss=undefined) {
  if(ss == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  }

  var worksheet_names_to_work_on = ['-toc-new'];

  for (var i = 0; i < worksheet_names_to_work_on.length; i++) {
    var ws = ss.getSheetByName(worksheet_names_to_work_on[i]);
    // do some work on the worksheet
    // get_and_write_column_size(ws);
    link_cells(ws, 'F5:F', 'E5:E', null);
  }
};


// link cell to a worksheet, optionally set cell value
function link_cell_to_worksheet(ss, cell, ws_name_to_link) {
    if (ss == null ){
      Logger.log(` .. ERROR .. spreadsheet is null`);
      return;
    }

    if (cell == null ){
      Logger.log(` .. ERROR .. cell is null`);
      return;
    }

    var ws_to_link = ss.getSheetByName(ws_name_to_link);
    if (ws_to_link == null ){
      Logger.log(` .. ERROR .. worksheet ${ws_name_to_link} not found`);
      return;
    }

    // Logger.log(` .. linking ${cell.getA1Notation()} to worksheet : ${ws_name_to_link}`);
    var link = `=HYPERLINK("#gid=${ws_to_link.getSheetId()}","${cell.getValue()}")`;
    cell.setFormula(link);
};


// link cell to a worksheet, optionally set cell value
function link_cell_to_spreadsheet(ss, cell, ss_name_to_link) {
    if (ss == null){
      Logger.log(` .. ERROR .. spreadsheet is null`);
      return;
    }

    if (cell == null ){
      Logger.log(` .. ERROR .. cell is null`);
      return;
    }

    var ss_to_link = open_spreadsheet(ss_name_to_link);
    if (ss_to_link == null ){
      Logger.log(` .. ERROR .. spreadsheet ${ss_name_to_link} not found`);
      return;
    }

    Logger.log(` .. linking ${cell.getA1Notation()} to spreadsheet : ${ss_name_to_link}`);
    var link = `=HYPERLINK("${ss_to_link.getUrl()}","${cell.getValue()}")`;
    cell.setFormula(link);
};


// get a range and link each cell with the spreadsheet/worksheet named in the cell
// if worksheet does not exist create it with a base template
function link_cells(ws, range_spec, helper_range_spec, template_ws_name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  if (template_ws_name != null) {
    var template_ws = ss.getSheetByName(template_ws_name);
  }

  var range = ws.getRange(range_spec);
  var helper_range = ws.getRange(helper_range_spec);
  var numRows = range.getNumRows();
  var numCols = range.getNumColumns();
  for (var i = 1; i <= numRows; i++) {
    for (var j = 1; j <= numCols; j++) {
      var cell = range.getCell(i, j);
      var helper_cell = helper_range.getCell(i, j);
      var cell_value = cell.getValue();
      var helper_cell_value = helper_cell.getValue();

      if (cell_value == ''){
        continue;
      }

      // now the link can be to a spreadsheet or a worksheet, helper_cell_value will tell us
      if (helper_cell_value == 'gsheet'){
        // a spreadsheet is to be linked
        link_cell_to_spreadsheet(ss, cell, cell_value);
      } else if (helper_cell_value == 'table'){
        // a worksheet is to be linked, see if there is a worksheet with cell_value
        var ws_name_to_link = ss.getSheetByName(cellValue);
        if (ws_name_to_link == null && template_ws != null) {
          var ws_to_link = duplicate_worksheet(ss, template_ws, cell_value);
        }

        // do the link
        if (ws_to_link != null) {
          link_cell_to_worksheet(ss, cell, ws_to_link);
        } else {
          Logger.log(` .. ERROR .. worksheet : ${cell_value} could not be linked`);
        };
      };
    };
  };
};


// add review-notes column as the first column, width 100, left
function add_conditional_formatting_for_blank_cells(ws, range_spec_list) {
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


// get column size for each column and write the size in row 1 for that column
// ignores the first column (A - review-notes)
function get_and_write_column_size(ws=undefined) {
  if (ws == undefined){
    var ws = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }

  let start_column = 2;
  let row_index = 1;
  var num_columns = ws.getMaxColumns();
  let range_spec = `${COLUMN_TO_LETTER[start_column]}${row_index}:${COLUMN_TO_LETTER[num_columns]}${row_index}`;
  Logger.log(` .... ${num_columns} columns found, update range ${range_spec}`);

  let column_sizes_in_pixel = [];
  for (var i = start_column; i <= num_columns; i++) {
    column_sizes_in_pixel.push(ws.getColumnWidth(i));
  }
  Logger.log(` .... updating range ${range_spec} with ${column_sizes_in_pixel}`);
  ws.getRange(range_spec).setHorizontalAlignment("center").setNumberFormat("0").setValues([column_sizes_in_pixel]);
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
