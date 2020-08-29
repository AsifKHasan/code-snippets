// do some work on a list of worksheets
function workOnWorksheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var sheetnames_to_work_on = ['G.5.2-operational-acceptance-tests-(oat)', 'G.6-training-(trn)'];
//  var sheetnames_to_work_on = ['0-coverpage', 'header-coverpage', 'header-odd', 'footer-odd'];
//  var sheetnames_to_work_on = ['A.1-br-organization', 'A.2-br-organogram', 'A.3-vision-&-mission-statement-of-br', 'A.4-current-status-of-ticketing-&-reservation', 'A.5-brits-stakeholders', 'A.6-objectives-of-project', 'A.7-scope-of-work', 'A.8-human-resource-&-logistic-supports-from-br', 'A.9-acronyms-used-in-technical-requirements', 'B.1-introduction', 'B.2-centralized-databased-system', 'B.3-n-tier-architecture', 'B.4-brits-interface-architecture', 'B.5-brits-network-architecture', 'B.6-integration-with-internal-&-external-systems', 'C-general-philosophy-for-implementation-of-brits', 'D.1-requirements-definition', 'F-minimum-technology-(non-functional)-requirements', 'G-project-management-requirements', 'G.5-testing-&-quality-assurance-requirement'];
  // var sheetnames_to_work_on = ['E.1-general-business-rules-for-tickets-(gr)', 'E.2-passenger-registration-with-brits-(pr)', 'E.3-ticket-quota-allotment-(ta)', 'E.4-counter-tickets-(ctickets)-(ct)', 'E.5-electronic-tickets-(etickets)-(et)', 'E.6-portable-point-of-sales-ticket-(ptickets)-(pt)', 'E.7-ticket-vending-machine-(vtickets)-(vt)', 'E.8-payment-&-collection-(pc)', 'E.9-giant-screen-displays-train-tracker-(gps)-&-analytics-(gs)', 'E.10-br-portal-(bp)', 'E.11-br-mobile-apps-(ma)', 'E.12-service-kiosks-(sk)', 'E.13-call-centre-(cc)', 'E.14-reports-requirements-(rt)', 'E.15-br-work-admin-center', 'F.1-basic-characteristics-of-software-architecture-(csa)', 'F.2-operational-business-rules-configuration-(brc)', 'F.3-language-dates-&-numbers-(ldn)', 'F.4-graphical-user-interface-requirements-(gui)', 'F.S-access-&-authentication-requirements-(acc)', 'F.6-server-workstation-os-software-requirements-(sws)', 'F.7-software-coding-convention-(scc)', 'F.8-database-requirements-&-optimization-(dro)', 'F.9-storage-requirements-(sto)', 'F.10-integration-requirements-(int)', 'F.11-reporting-visualization-&-dashboard-(rvd)', 'F.12-message-&-notification-technology-(mnt)', 'F.13-system-management-&-monitoring-(smm)', 'F.14-security-requirements-(sec)', 'F.15-hardware-requirements-(hwr)', 'F.16-sizing-&-performance-requirements-(per)', 'G.1-implementation-planning-(imp)', 'G.2-use-project-management-tools-(pmt)', 'G.2-documentation-requirements-(doc)', 'G.3-management-&-maintenance-(mam)', 'G.4-reports-(rpt)', 'G.5.1-user-acceptance-tests-(uat)', 'G.5.2-operational-acceptance-tests-(oat)', 'G.6-training-(trn)', 'G.7-terms-&-conditions-of-application-software-(tcs)', 'G.8-team-qualifications-&-experience-(tea)', 'G.9-other-avenues-for-revenue-generation-(rev)'];

  for (var i = 0; i < sheetnames_to_work_on.length; i++) {
    var ws = ss.getSheetByName(sheetnames_to_work_on[i]);
    // do some work on the worksheet

    // addRequirementAtThirdRow(ws);

    // conditionalFormatingOnReviewNotes(ws);

    // removeTrailingBlankRows(ws);
    // removeTrailingBlankColumns(ws);
    //
    // addComplianceColumnsAtTheEnd(ws);
    //
    // addReviewNotesColumn(ws, 1);


    // addTendererResponseColumnsAtTheEnd(ws);

    addFormatResponseColumns(ws);

    //
    // formatSecondRow(ws);
    // setContentBorder(ws);
  }
};

function rowOfMatchingValue(ws, column, value){
  var data = ws.getDataRange().getValues();
  for (var i = 0; i < data.length; i++) {
    if (data[i][column - 1] == value) {
      return i + 1;
    }
  }

  return -1;
}

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
