// do some work on a list of sheets
function work_on_spreadsheets() {
  var ss_names_to_work_on = SS_NAMES_TO_WORK_ON;

  ss_names_to_work_on.forEach(function(ss_name){
    Logger.log(`PROCESSING : ${ss_name}`);

    // older one time methods, may not be needed anymore
    // rename_worksheets(ss_name, WORKSHEET_NAME_MAP1);
    // rename_worksheets(ss_name, WORKSHEET_NAME_MAP2);

    // for all worksheets
    // resize_columns_in_worksheets(ss_name, RESUME_WS_COLUMNS);
    // write_column_size_in_worksheets(ss_name);
    // order_worksheets(ss_name);

    // var template_ss = get_unique_file_by_name('Résumé__template');
    // var folder = DriveApp.getFolderById('1JltNCjefWmSMZHHQtON_fSTpkHh2W9rP');
    // if (template_ss != null){
    //   create_resumes_from_template(ss_name, template_ss, folder);
    // };

    // specific to *00-layout* worksheet
    // create_00_layout_worksheet(ss_name);
    // update_00_layout_worksheet_links(ss_name);
    // update_00_layout_worksheet_content(ss_name);
    update_00_layout_worksheet_photo(ss_name);
    update_00_layout_worksheet_signature(ss_name);

    Logger.log(`DONE : ${ss_name}`);
  });
};


// do some work on a list of files
function work_on_files() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var file_names_to_work_on = ['Resume__Tanmoy.Chandra.Dhar'];

  for (var i = 0; i < file_names_to_work_on.length; i++) {
    var file_name = file_names_to_work_on[i];
    var file = getUniqueFileByName(file_name);
    var folder_id = '1klZ3h7RmaY7TaPShcfNRseDvk9EeZrqM';
    var folder = DriveApp.getFolderById(folder_id);

    if (file != null) {
      // do some work on the files
      var new_name = file_name.replace('Resume__', 'Résumé__');
      var new_file = copy_file_to(file, new_name, folder);
      if (new_file == null) {
        Logger.log('Could not copy file : ' + file_name + ' to : ' + new_name);
      }
    }
  }
};


// do some work on a list of worksheets
function work_on_worksheets(ss=undefined) {
  if(ss == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  }

  var worksheet_names_to_work_on = RESUME_WS_NAMES;

  for (var i = 0; i < worksheet_names_to_work_on.length; i++) {
    var ws = ss.getSheetByName(worksheet_names_to_work_on[i]);
    // do some work on the worksheet
    get_and_write_column_size(ws);
  }
};
