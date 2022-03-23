// add one column before the last column, change 3rd last (MET) column, change 2nd last (Reference) column, change last (Section) column
function addFormatResponseColumns(ws) {
    var total_rows = ws.getMaxRows();
    var last_col_with_data = ws.getLastColumn();

    // in which row the value MET is in column (last_col_with_data - 1)
    var tabularDataStartRow = rowOfMatchingValue(ws, last_col_with_data - 1, "MET");
    if (tabularDataStartRow == -1) {
        return;
    }

    ws.insertColumnsAfter(last_col_with_data - 1, 1);

    // 3rd last (MET) column
    var index =  last_col_with_data + 1;

    // width, heading and alignment
    ws.setColumnWidth(index, 150);
    var range = ws.getRange(1, index, total_rows);
    range.setHorizontalAlignment("left");
    range.setWrap(true);
    ws.getRange(tabularDataStartRow, index).setValue("Section");

    // 2nd last (Reference) column
    var index =  last_col_with_data;

    // width, heading and alignment
    ws.setColumnWidth(index, 150);
    var range = ws.getRange(1, index, total_rows);
    range.setHorizontalAlignment("left");
    range.setWrap(true);
    ws.getRange(tabularDataStartRow, index).setValue("Reference");

    // last (Section) column
    var index =  last_col_with_data - 1;

    // width, heading and alignment
    ws.setColumnWidth(index, 300);
    var range = ws.getRange(1, index, total_rows);
    range.setHorizontalAlignment("left");
    range.setWrap(true);
    ws.getRange(tabularDataStartRow, index).setValue("Section");
}


// add Tenderer's Response columns at the end
function addTendererResponseColumnsAtTheEnd(ws) {
  var last_col_with_data = ws.getLastColumn();

  ws.insertColumnsAfter(last_col_with_data, 3);

  formatResponseColumn(ws, last_col_with_data + 1);
  formatBookReferenceColumn(ws, last_col_with_data + 2);
  formatSectionReferenceColumn(ws, last_col_with_data + 3);
};


// format Tenderer's Response column width 400, left, with formatting (blank - Yellow)
function formatResponseColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 400);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Tenderer's Response");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// format Book Reference column width 200, left, with formatting (blank - Yellow)
function formatBookReferenceColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 200);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Book Reference");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// format Section Reference column width 200, left, with formatting (blank - Yellow)
function formatSectionReferenceColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 200);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Section Reference");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// add a 3rd row with heading Requirements
function addRequirementAtThirdRow(ws) {
    ws.insertRowBefore(3);
    ws.getRange(3, 2).setValue("Requirements");

    // merge row 3 from column b to last column
    var total_columns = ws.getMaxColumns();
    var range = ws.getRange(3, 2, 3, total_columns - 1);
    range.mergeAcross();
}


// add conditional formatting for review-notes column
function conditionalFormatingOnReviewNotes(ws) {
    // review notes is column A, data starts from A3
    var total_rows = ws.getMaxRows();
    var total_columns = ws.getMaxColumns();
    var range = ws.getRange(3, 1, total_rows - 2, total_columns);

    // conditional formatting
    var rules = ws.getConditionalFormatRules();
    var rule = SpreadsheetApp.newConditionalFormatRule()
      .setRanges([range])
      .whenFormulaSatisfied("=not(isblank($A:$A))")
      .setBackground('#f4cccc')
      .build();
    rules.push(rule);

    ws.setConditionalFormatRules(rules);

}


// format the second row
function formatSecondRow(ws) {
  var last_col_with_data = ws.getLastColumn();

  // merge b2 across the end
  var range = ws.getRange(2, 2, 1, last_col_with_data - 1);
  range.mergeAcross().setHorizontalAlignment("left").setValue("content");

  var range = ws.getRange(2, 1, 1, last_col_with_data - 1);
  range.setBackground("#d9d9d9");

  // freeze two rows
  ws.setFrozenRows(2);
};


// border from b3 to bottom-right
function setContentBorder(ws) {
  var total_rows = ws.getMaxRows();
  var last_col_with_data = ws.getLastColumn();
  var range = ws.getRange(3, 2, total_rows - 2, last_col_with_data - 1);
  range.setBorder(true, true, true, true, true, true, '#b7b7b7', SpreadsheetApp.BorderStyle.SOLID);
};


// add review-notes column as the first column, width 100, left
function addReviewNotesColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  ws.insertColumns(index);

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

  // conditional formatting
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenCellNotEmpty()
    .setBackground('#fff2cc')
    .build();
  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};


// add compliaance columns at the end
function addComplianceColumnsAtTheEnd(ws) {
  var last_col_with_data = ws.getLastColumn();

  ws.insertColumnsAfter(last_col_with_data, 4);

  formatCompliedColumn(ws, last_col_with_data + 1);
  formatComplianceNoteColumn(ws, last_col_with_data + 2);
  formatReferenceDocumentColumn(ws, last_col_with_data + 3);
  formatSectionColumn(ws, last_col_with_data + 4);
};


// format column Section width 200, left, with formatting (blank - Yellow)
function formatSectionColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 200);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Section");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// format column Reference document width 250, left, with formatting (blank - Yellow)
function formatReferenceDocumentColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 250);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Reference document");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// format column Compliance note width 330, left, with formatting (blank - Yellow)
function formatComplianceNoteColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 330);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("left");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Compliance note");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.clearDataValidations();

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


// format column Complied? width 70, centered, with validation (Yes, No, Partial) and formatting (Yes - Green, Blank/Partial - Yellow, No - Red)
function formatCompliedColumn(ws, index) {
  var total_rows = ws.getMaxRows();

  // width, heading and alignment
  ws.setColumnWidth(index, 70);
  var range = ws.getRange(1, index, total_rows);
  range.setHorizontalAlignment("center");
  range.setWrap(true);
  ws.getRange(3, index).setValue("Complied?");

  // data validation
  ws.getRange(4, index).activate();
  range = ws.getRange(4, index, total_rows - 3);
  range.setDataValidation(SpreadsheetApp.newDataValidation()
    .setAllowInvalid(false)
    .requireValueInList(['Yes', 'No', 'Partial'], true)
    .build());

  // conditional formatting
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenTextEqualTo("Yes")
    .setBackground('#d9ead3')
    .build();
  rules.push(rule);

  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenTextEqualTo("No")
    .setBackground('#f4cccc')
    .build();
  rules.push(rule);

  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenTextEqualTo("Partial")
    .setBackground('#fff2cc')
    .build();
  rules.push(rule);

  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenCellEmpty()
    .setBackground('#fff2cc')
    .build();
  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};
