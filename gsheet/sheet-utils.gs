// do some work on a list of sheets
function workOnSheets() {
  var sheet_names_to_work_on = ['Résumé__Abdur.Rab.Marjan', 'Résumé__Akeed.Anjum', 'Résumé__Amimul.Ahshan.Avi', 'Résumé__Amiya.Ahmed',
                                'Résumé__Anis.Bulbul', 'Résumé__Anisur.Rahman', 'Résumé__Aqib.Asifur.Rahman', 'Résumé__Arifur.Rahman',
                                'Résumé__Arnab.Kumar.Ghosh', 'Résumé__Ashish.Kumar.Das', 'Résumé__Asma.ul.Husna', 'Résumé__Atiqur.Rahman',
                                'Résumé__Azharul.Islam', 'Résumé__Ekramul.Bari', 'Résumé__Fahim.Shahriar', 'Résumé__G.M.Ataur.Rahman',
                                'Résumé__Ibrahim.Ibna.Md.Liaquat.Ullah', 'Résumé__Kamrun.Nahar', 'Résumé__Karzon.Chowdhury', 'Résumé__Khairul.AN-AM',
                                'Résumé__Laboni.Das', 'Résumé__Lutfunnahar.Lota', 'Résumé__Manzur.Alam', 'Résumé__Mashud.Karim',
                                'Résumé__Md.Abdullah.Al.Mamun', 'Résumé__Md.Ahsanur.Rahman', 'Résumé__Md.Asgor.Ali', 'Résumé__Md.Asheq.Ullah',
                                'Résumé__Md.Atikul.Islam', 'Résumé__Md.Atiqur.Rahman', 'Résumé__Md.Azizul.Hakim', 'Résumé__Md.Hafizur.Rahman',
                                'Résumé__Md.Hasibur.Rahman', 'Résumé__Md.Imtiaz.Morshed.Bin.Zaman', 'Résumé__Md.Jakir.Hossain', 'Résumé__Md.Jamal.Uddin',
                                'Résumé__Md.Kamruzzaman.Tanim', 'Résumé__Md.Kaziul.Islam', 'Résumé__Md.Mahabub.Al-Islam', 'Résumé__Md.Mahasin.Alam',
                                'Résumé__Md.Mazharul.Islam', 'Résumé__Md.Murshadul.Islam', 'Résumé__Md.Murshid.Sarker', 'Résumé__Md.Najib.Hasan',
                                'Résumé__Md.Nazmul.Hasan', 'Résumé__Md.Rabiul.Islam', 'Résumé__Md.Rejwan.Ull.Alam', 'Résumé__Md.Rezaul.Islam',
                                'Résumé__Md.Rezaul.Karim', 'Résumé__Md.Robiul.Awoul', 'Résumé__Md.Rokonuzzaman', 'Résumé__Md.Saidur.Rahman.Shamim',
                                'Résumé__Md.Sajal.Biswas', 'Résumé__Md.Samim.Hosen', 'Résumé__Md.Shahin.Sheikh', 'Résumé__Md.Sharafat.Hossain.Kamal',
                                'Résumé__Md.Sirajul.Islam', 'Résumé__Md.Tuhin.Reza', 'Résumé__Md.Zahidul.Islam', 'Résumé__Mehedi.Hasan',
                                'Résumé__Miskatun.Nahar', 'Résumé__Mohammad.Ashraful.Islam', 'Résumé__Mohammad.Main.Uddin', 'Résumé__Mohammed.Kowsar.Rahman',
                                'Résumé__Monjur.Ahmed', 'Résumé__Muhammad.Aminur.Rahman', 'Résumé__Muhammad.Ashraf.Uddin.Bhuiyan', 'Résumé__Muhsinur.Rahman.Chowdhury',
                                'Résumé__Murshida.Mushfique', 'Résumé__Mushfika.Faria', 'Résumé__Nasima.Aktar', 'Résumé__Nur-E-Asma.Tabassum',
                                'Résumé__Nusrat.Jahan.Mahmud', 'Résumé__Rajib.Chowdhury', 'Résumé__Raqibul.Islam', 'Résumé__Rishad.Ali.Mimo',
                                'Résumé__Sagar.Saha', 'Résumé__Saiful.Islam', 'Résumé__Saleh.Ahammed', 'Résumé__Salman.Hossen',
                                'Résumé__Sanjoy.Kumar.Saha', 'Résumé__Sanmoon.Yasmin', 'Résumé__Shahida.Begum', 'Résumé__Shaikh.Tojibul.Islam',
                                'Résumé__Shajir.Uddin.Haider', 'Résumé__Shariful.Islam', 'Résumé__Shihan.Zaman', 'Résumé__Shohag.Hossain',
                                'Résumé__Syed.Taslimur.Rahaman', 'Résumé__Tanmoy.Chandra.Dhar', 'Résumé__Tofiq.Akbar', 'Résumé__Umme.Rumman.Usha'];

  for (var i = 0; i < sheet_names_to_work_on.length; i++) {
    var sheet_name = sheet_names_to_work_on[i];

    // try to find the file by name
    var file = getUniqueFileByName(sheet_name);
    if (file == null) {
      Logger.log('Could not find sheet : ' + sheet_name);
      continue;
    }

    // try to open the sheet
    var sheet = SpreadsheetApp.open(file);
    if (sheet == null) {
      Logger.log('Could not open sheet : ' + sheet_name);
      continue;
    }

    Logger.log('PROCESSING : ' + sheet_name);

    // do some work on the sheet

//    copyWorksheetToSheetInSpecificIndex(sheet, '-toc', 1);
//    copyWorksheetToSheetInSpecificIndex(sheet, 'wb-resume-layout', 2);

    SpreadsheetApp.setActiveSpreadsheet(sheet);
    updateLinksInToCWorksheet(sheet);
    updateLinksInWbResumeLayoutWorksheet(sheet);

//    workOnPersonalWorksheet(sheet);
//    workOnCareerHighlightWorksheet(sheet);
//    workOnEducationWorksheet(sheet);
//    workOnManagerialExpertiseWorksheet(sheet);
//    workOnTechnicalExpertiseWorksheet(sheet);
//    workOnJobHistoryWorksheet(sheet);
//    workOnProjectRolesWorksheet(sheet);
//    workOnTrainingWorksheet(sheet);
//    workOnCertificationWorksheet(sheet);
//    workOnMembershipWorksheet(sheet);
//    workOnLanguageProficiencyWorksheet(sheet);

//    workOnWorksheets();

    Logger.log('DONE : ' + sheet_name);
  }
};

// update links in -toc worksheet
function updateLinksInToCWorksheet(sheet) {
  var ws_name = '-toc';
  var ws = sheet.getSheetByName(ws_name);

  linkCells(ws, 'F3', null);
};

// update links in wb-resume-layout worksheet
function updateLinksInWbResumeLayoutWorksheet(sheet) {
  var ws_name = 'wb-resume-layout';
  var ws = sheet.getSheetByName(ws_name);

  linkCells(ws, 'D12', null);
  linkCells(ws, 'D13', null);
  linkCells(ws, 'D14', null);
  linkCells(ws, 'D15', null);
  linkCells(ws, 'D16', null);
  linkCells(ws, 'C20', null);
  linkCells(ws, 'C22', null);
  linkCells(ws, 'D23', null);
  linkCells(ws, 'D24', null);

  // copy image link from personal!E3 and put into J7
  var personal_ws = sheet.getSheetByName('personal');
  var formula = personal_ws.getRange('E3').getCell(1, 1).getFormula().replace(', 1)', ', 3)');
  ws.getRange('J7').setFormula(formula);
};


// copy worksheet to another sheet in specific index
function copyWorksheetToSheetInSpecificIndex(copy_to, sheetname_to_copy, index) {
  var thisSheet = SpreadsheetApp.getActiveSpreadsheet();

  var ws = thisSheet.getSheetByName(sheetname_to_copy);
  var copiedWorksheet = ws.copyTo(copy_to);
  copiedWorksheet.setName(sheetname_to_copy);
  copy_to.setActiveSheet(copiedWorksheet);
  copy_to.moveActiveSheet(index);
};

function bulkProcessResumeWorksheets(ws) {
  removeTrailingBlankColumns(ws);
  removeTrailingBlankRows(ws);

  // add 2nd row
  ws.insertRowAfter(1);
  // freeze 2 rows
  ws.setFrozenRows(2);

  // add review-notes column
  addReviewNotesColumn(ws, 1);

  addConditionalFormattingForBlankCells(ws);
  formatSecondRow(ws);
  getAndWriteColumnSizeInFirstRow(ws);
  setContentBorder(ws);
  formatWorksheetFontAndSize(ws);
};

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
