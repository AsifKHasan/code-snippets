function main() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  hyperlink_to_file(ss, '-links-doer', 'B10:B20');
};


// get a range and link each cell with the spreadsheet/worksheet named in the cell
function hyperlink_to_file(ss, ws_name, range_spec) {
  var ws = ss.getSheetByName(ws_name);
  var range = ws.getRange(range_spec);
  var numRows = range.getNumRows();
  for (var i = 1; i <= numRows; i++) {
    var cell = range.getCell(i, 1);
    var cell_value = cell.getValue();
    if (cell_value == ''){
      continue;
    };

    // a spreadsheet is to be linked
    link_cell_to_file(cell_value, cell, cell_value);
  };
};


// link cell to a file
function link_cell_to_file(file_name_to_link, cell, link_text) {
    var file_to_link = get_unique_file_by_name(file_name_to_link);
    if (file_to_link == null ){
      Logger.log(` .. ERROR .. file ${file_name_to_link} not found`);
      return;
    }

    Logger.log(`linking ${cell.getA1Notation()} to file : ${file_name_to_link}`);
    var link = `=HYPERLINK("${file_to_link.getUrl()}","${link_text}")`;
    cell.setFormula(link);
};


// get unique file by name
function get_unique_file_by_name(file_name) {
  Logger.log(`finding : ${file_name}`);

  var files = DriveApp.getFilesByName(file_name);

  // return the first file if any, else return null
  if (files.hasNext()) {
    var file = files.next();
  } else {
    Logger.log(` .. ERROR : No file with the name : ${file_name}`);
    return null;
  }

  // if there are more files, report duplicate
  if (files.hasNext()) {
    Logger.log(` .. WARN  : There are more than one file with the name : ${file_name}`);
    return null;
  }

  return file;
};
