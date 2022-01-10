// do some Arbitrary work
function doSomething() {
  linkCells("F3:F3", "blank-template");

};

// do some work on a list of worksheets
function workOnWorksheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var worksheet_names_to_work_on = ['personal', 'career-highlight', 'education', 'managerial-expertise', 'technical-expertise', 'job-history', 'project-roles', 'training', 'certification', 'membership', 'language-proficiency'];
//  var worksheet_names_to_work_on = ['language-proficiency'];

  for (var i = 0; i < worksheet_names_to_work_on.length; i++) {
    var ws = ss.getSheetByName(worksheet_names_to_work_on[i]);
    // do some work on the worksheet
    bulkProcessResumeWorksheets(ws);
  }
};

// get a range and link each cell with the worksheet named in the cell
// if worksheet does not exit create it with a base template
function linkCells(ws, range_spec, template_worksheet_name) {
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

// duplicate a worksheet and give it a new name
function duplicateWorksheet(from_sheet, from_worksheet, new_worksheet_name) {
    copied_sheet = from_worksheet.copyTo(from_sheet).setName(new_worksheet_name);
    return copied_sheet;
};

function linkToWorksheet(cell, worksheet_to_link) {
    var link = '=HYPERLINK("#gid=' + worksheet_to_link.getSheetId() + '","' + cell.getValue() + '")'
    cell.setFormula(link);
};

// for ordering worksheets in a Google sheet
function orderWorksheets() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheetNameArray = [];
    var sheets = ss.getSheets();

    for (var i = 0; i < sheets.length; i++) {
        sheetNameArray.push(sheets[i].getName());
    }

    sheetNameArray.sort();

    sheetNameArray.forEach(function(e, i) {
        Logger.log(i + ' worksheet : ' + e);
        ss.setActiveSheet(ss.getSheetByName(e));
        ss.moveActiveSheet(i + 1);
    });
};

// copy worksheets from one sheet to another
function copyWorksheetsBetweenSheets(copy_to) {
    var thisSheet = SpreadsheetApp.getActiveSpreadsheet();

    var otherSheet = openSheet(copy_to);
    if (otherSheet == null) {
      Logger.log('Can not open sheet : ' + copy_to);
      return null;
    }

    sheetnames_to_copy = [];

    for (var i = 0; i < sheetnames_to_copy.length; i++) {
        var ws = thisSheet.getSheetByName(sheetnames_to_copy[i]);
        var copiedWorksheet = ws.copyTo(otherSheet);
        copiedWorksheet.setName(sheetnames_to_copy[i]);
    }
};

// copy certain worksheets to multiple destinations and manage links
function copySheets() {
  var worksheetToCopy = "header-coverpage";
  var destinations = ["1B-MTV7BGmmS400z0pQn3OAN5gNYk7FAdYvyAG3k_p8Y", "1gsxA2IEAAm3BZK36AGvwBX8avlnn2hwa9DeuKq3ZP7o", "1k1y8SkqwvHWgagwUHtJQvApdcjtga1y8KVX6ho262KU", "1sEiMT0KBa1msXsvV1qJTRh_GLFdW7YOC1yNpAIIN24E", "1ZWgcJ81m7VdJvceHBG8qFbw73833scDto1a5Is07xlc", "1XdzFmk4Ins7u2X87er3V9tF1xWybwZKkr5ppWGZ8QDw", "1Dmd6-YTH9HKxAIT6SM3Fjq2OqH-0gGY02gptNLMI3Co", "1Nat1XemN0fAAwSrWz-2TIH-omSZ-I1UiNH008ED4Y0s", "13RQPMP-7LSJhhhicfLykNidZfqiJSYE8ZUSX8o8870M", "1MVMw9DavzJPPz7Twt4C86qHIEV-528ub2_RaA19-4gw", "13cB4aZHWPKCh5x5ICGXiYpmYhoHzZgOQoZomd132evQ", "1oE3VX3GdeOrPiVYNd1xGxFJ1CIaMdTeKjM0L0xaYjHI", "1cd8Y76r2cg0uvCdRTuvGEgirnlNmZlyJiSWd4KHcbbQ"];

  //var ss = SpreadsheetApp.getActiveSpreadsheet();
  //var sheetToCopy = ss.getSheetByName(worksheetToCopy);

  destinations.forEach(function(d) {
    var destination = SpreadsheetApp.openById(d);
    //sheetToCopy.copyTo(destination);
    // rename destination worksheet
    //var sheet = destination.getSheetByName("Copy of " + worksheetToCopy);
    //sheet.setName(worksheetToCopy);
    var linkedSheet = destination.getSheetByName(worksheetToCopy);
    var linkedSheetId = linkedSheet.getSheetId();

    var sheet = destination.getSheetByName("-toc");
    sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).activate();
    destination.getActiveRangeList().setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
    destination.getRange('L3').activate();
    destination.getCurrentCell().setValue('header-coverpage');
    destination.getActiveRangeList().setShowHyperlink(true);
    destination.getCurrentCell().setFormula('=HYPERLINK("#gid=' + linkedSheetId + '","header-coverpage")');

  });
};

// remove columns from a worksheet where all cells are blank
function removeTrailingBlankColumns(ws) {
  var total_cols = ws.getMaxColumns();
  var last_col_with_data = ws.getLastColumn();
  // Logger.log("out of %s cols, last col with data is %s", total_cols, last_col_with_data);
  // Cols start at "1"
  if (total_cols > last_col_with_data) {
    ws.deleteColumns(last_col_with_data + 1, total_cols - last_col_with_data);
  }
};

// remove all trailing rows from a worksheet where all cells are blank
function removeTrailingBlankRows(ws) {
  var total_rows = ws.getMaxRows();
  var last_row_with_data = ws.getLastRow();
  // Logger.log("out of %s rows, last row with data is %s", total_rows, last_row_with_data);
  // Rows start at "1"
  if (total_rows > last_row_with_data) {
    ws.deleteRows(last_row_with_data + 1, total_rows - last_row_with_data);
  }
};

// move a sheet to End
function moveWorksheetToEnd(ws_name) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ws = ss.getSheetByName(ws_name);
    var sheet_count = ss.getNumSheets();

    ss.setActiveSheet(ws);
    ss.moveActiveSheet(sheet_count);
};

// merge cells Across for a given range
function mergeCellsAcross(range_spec) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ws = ss.getActiveSheet();

    range = ws.getRange(range_spec);
    range.mergeAcross();
};
