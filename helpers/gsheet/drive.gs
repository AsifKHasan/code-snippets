// open a sheet from name
function open_spreadsheet(ss_name) {
  var files = DriveApp.searchFiles(`title = "${ss_name}" and mimeType = "${MimeType.GOOGLE_SHEETS}"`);
  if (files.hasNext()) {
    var ss = SpreadsheetApp.open(files.next());
  }

  if (files.hasNext()) {
    Logger.log(`There are more than one file with the name : ${file_name}`);
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
