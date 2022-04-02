// do some work on a list of files
function work_on_files() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var file_names_to_work_on = [];

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
        Logger.log('ERROR .. Could not copy file : ' + file_name + ' to : ' + new_name);
      }
    }
  }
};


// open a sheet from name
function open_spreadsheet(ss_name) {
  var files = DriveApp.searchFiles(`title = "${ss_name}" and mimeType = "${MimeType.GOOGLE_SHEETS}"`);
  if (files.hasNext()) {
    var ss = SpreadsheetApp.open(files.next());
  }

  if (files.hasNext()) {
    Logger.log(`There are more than one file with the name : ${ss_name}`);
  }

  return ss;
};


// copy a file with a new name and location
function copy_file_to(from_file, new_name, destination_folder_id) {
  var new_file = from_file.makeCopy(new_name, destination_folder_id);
  return new_file;
};


// get unique file by name
function get_unique_file_by_name(file_name) {
  var files = DriveApp.getFilesByName(file_name);

  // return the first file if any, else return null
  if (files.hasNext()) {
    var file = files.next();
  } else {
    return null;
  }

  // if there are more files, report duplicate
  if (files.hasNext()) {
    Logger.log(`There are more than one file with the name : ${file_name}`);
    return null;
  }

  return file;
};


// create spreadsheets from a template
function create_ss_from_template(ss_name, template_ss, folder){
  var file = get_unique_file_by_name(ss_name);

  // make sure we do not have any spreadsheet named ss_name
  if (file != null){
    if (file.getMimeType() == 'application/vnd.google-apps.spreadsheet'){
      Logger.log(`ERROR: Spreadsheet ${ss_name} already exists`);
      return null;
    };
  };

  var ss = copy_file_to(template_ss, ss_name, folder);
  if (ss == null){
    Logger.log(`ERROR: Spreadsheet ${ss_name} could not be created`);
  };

  return ss;
};
