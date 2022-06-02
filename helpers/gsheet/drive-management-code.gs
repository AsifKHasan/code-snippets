// work on files
function work_on_files(){
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var detail_output_ws_name = 'z-file-details';
  var detail_output_ws = ss.getSheetByName(detail_output_ws_name);

  var permission_output_ws_name = 'z-file-permissions';
  var permission_output_ws = ss.getSheetByName(permission_output_ws_name);

  var range_to_clear = detail_output_ws.getRange('A3:M');
  range_to_clear.clearContent();

  var range_to_clear = permission_output_ws.getRange('A3:E');
  range_to_clear.clearContent();


  var file_names_to_work_on = get_file_names_to_work_on();
  var detail_output_row_num = 3;
  var permission_output_row_num = 3;
  file_names_to_work_on.forEach(function(entry){
    var file_seq = entry['seq'];
    var file_name = entry['name'];
    Logger.log(`PROCESSING ${file_seq} : ${file_name}`);

    // get file data
    var file_data = get_file_data(file_name, file_seq);

    if (file_data != null){
      // show/output file data
      Logger.log(`... parent            : ${file_data['parent']}`);
      Logger.log(`... url               : ${file_data['url']}`);
      Logger.log(`... type              : ${file_data['type']}`);
      Logger.log(`... owner name        : ${file_data['owner-name']}`);
      Logger.log(`... owner email       : ${file_data['owner-email']}`);
      Logger.log(`... access            : ${file_data['access']}`);
      Logger.log(`... worksheets        : ${file_data['worksheets']}`);
      Logger.log(`... size              : ${file_data['size']}KB`);
      Logger.log(`... created           : ${file_data['created']}`);
      Logger.log(`... last-modified     : ${file_data['last-modified']}`);
      Logger.log(`... editors-can-share : ${file_data['editors-can-share']}`);

      // detail output to gsheet
      var values = [file_data['seq'], file_data['name'], file_data['parent'], file_data['url'], file_data['type'], file_data['owner-name'], file_data['owner-email'],
                    file_data['access'], file_data['worksheets'], file_data['size'], file_data['created'], file_data['last-modified'], file_data['editors-can-share']];

      var range_spec = `A${detail_output_row_num}:M${detail_output_row_num}`;
      var range = detail_output_ws.getRange(range_spec);
      range.setValues([values]);

      detail_output_row_num++;

      // permission output to gsheet
      var permissions = file_data['permissions'];
      var permission_size = permissions.length;
      var range_spec = `A${permission_output_row_num}:E${permission_output_row_num + permission_size - 1}`;
      var range = permission_output_ws.getRange(range_spec);
      range.setValues(permissions);

      permission_output_row_num = permission_output_row_num + permission_size;

    };

    Logger.log(`DONE       ${file_seq} : ${file_name}`);
  });

};

// given a file name, return relavant data
function get_file_data(file_name, seq){
  var drive_file = get_unique_file_by_name(file_name);
  if (drive_file === null){
    return null;
  };

  var file_data = {'seq': seq, 'name': file_name};

  // parent folder
  var parents = [];
  var parent_iter = drive_file.getParents();
  while (parent_iter.hasNext()) {
    var folder = parent_iter.next();
    // Logger.log(folder.getName());
    parents.push(folder.getName());
    var parent_iter = folder.getParents();
  };

  parents.reverse();
  file_data['parent'] = parents.join('/');

  // url
  file_data['url'] = drive_file.getUrl();

  // type
  file_data['type'] = MIME_TYPES[drive_file.getMimeType()];

  // owner
  var owner = drive_file.getOwner();
  file_data['owner-name'] = owner.getName();
  file_data['owner-email'] = owner.getEmail();

  // access
  file_data['access'] = drive_file.getSharingAccess();

  // worksheets only if it is a gsheet
  if (file_data['type'] === 'gsheet'){
    var ss = open_spreadsheet(file_name);
    if (ss != null){
      file_data['worksheets'] = ss.getNumSheets();
    };
  };

  // size
  file_data['size'] = drive_file.getSize() / 1024;

  // created
  file_data['created'] = drive_file.getDateCreated();

  // last-modified
  file_data['last-modified'] = drive_file.getLastUpdated();

  // editors-can-share
  if (drive_file.isShareableByEditors()){
    file_data['editors-can-share'] = 'Yes';
  } else {
    file_data['editors-can-share'] = '';
  }

  // permissions
  var permissions = [];
  permissions.push([seq, file_name, file_data['owner-name'], file_data['owner-email'], 'owner']);

  var editors = drive_file.getEditors();
  editors.forEach(function(user){
    permissions.push([seq, file_name, user.getName(), user.getEmail(), 'editor']);
  });

  var viewers = drive_file.getViewers();
  viewers.forEach(function(user){
    permissions.push([seq, file_name, user.getName(), user.getEmail(), 'viewer']);
  });

  // var commenters = drive_file.getCommenters();
  // commenters.forEach(function(user){
  //   permissions.push([seq, file_name, user.getName(), user.getEmail(), 'commenter']);
  // });

  file_data['permissions'] = permissions;

  return file_data;
};


// get list of file names to process
function get_file_names_to_work_on() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var name_ws_name = 'z-file-list';
  var name_ws = ss.getSheetByName(name_ws_name);

  var name_data = name_ws.getRange('A3:C').getValues();

  var file_names = [];
  name_data.forEach(function(row, index){
    // we take only the values which has Process Yes
    if (row[NAME_LIST_COLUMNS.Process] === 'Yes'){
      var entry = {'seq': row[NAME_LIST_COLUMNS.Seq], 'name': row[NAME_LIST_COLUMNS.FolderFileName]};
      file_names.push(entry);
    };
  });

  return file_names;
};

const NAME_LIST_COLUMNS = {
  Process: 0,
  Seq: 1,
  FolderFileName: 2,
};

const MIME_TYPES = {
'application/vnd.google-apps.audio'        : 'audio',
'application/vnd.google-apps.document'     : 'gdoc',
'application/vnd.google-apps.drive-sdk'    : 'drive-sdk',
'application/vnd.google-apps.drawing'      : 'gdraw',
'application/vnd.google-apps.file'         : 'file',
'application/vnd.google-apps.folder'       : 'folder',
'application/vnd.google-apps.form'         : 'gform',
'application/vnd.google-apps.fusiontable'  : 'gfusiontable',
'application/vnd.google-apps.jam'          : 'gjamboard',
'application/vnd.google-apps.map'          : 'gmymaps',
'application/vnd.google-apps.photo'        : 'gphoto',
'application/vnd.google-apps.presentation' : 'gslide',
'application/vnd.google-apps.script'       : 'apps-script',
'application/vnd.google-apps.shortcut'     : 'shortcut',
'application/vnd.google-apps.site'         : 'gsite',
'application/vnd.google-apps.spreadsheet'  : 'gsheet',
'application/vnd.google-apps.unknown'      : 'unknown',
'application/vnd.google-apps.video'        : 'video',
};
