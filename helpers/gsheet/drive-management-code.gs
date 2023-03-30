// traverse a folder
function start_folder_iteration(){
  // this is SAU-CAS
  var folder_id_to_traverse = '18GGvxjGZFxAW1rLItIAR6CzJHAQh_GX9';
  var folder_to_traverse = DriveApp.getFolderById(folder_id_to_traverse);
  if (folder_to_traverse){
    // get the absolute location
    var parent_path = get_parent_path(folder_to_traverse);
    Logger.log(`traversing folder ${folder_to_traverse.getName()} at ${parent_path}`);

    var object_list = [];
    iterate_folder(folder_to_traverse, parent_path, object_list);

    // persist
    work_on_objects(object_list);

  } else {
    Logger.log(`ERROR: folder ${folder_id_to_traverse} NOT FOUND`);
  };

};


// work on objects
function work_on_objects(object_list){
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var detail_output_ws_name = 'z-file-details';
  var detail_output_ws = ss.getSheetByName(detail_output_ws_name);

  var permission_output_ws_name = 'z-file-permissions';
  var permission_output_ws = ss.getSheetByName(permission_output_ws_name);

  var range_to_clear = detail_output_ws.getRange('A3:M');
  range_to_clear.clearContent();

  var range_to_clear = permission_output_ws.getRange('A3:E');
  range_to_clear.clearContent();


  var detail_output_row_num = 3;
  var permission_output_row_num = 3;
  object_list.forEach(function(entry, index){
    var obj_seq = index;
    var obj_name = entry['object'].getName();
    Logger.log(`PROCESSING ${obj_seq} : ${obj_name}`);

    // get obj data
    var obj_data = get_object_data(entry['object'], entry['is-folder'], entry['parent-path'], obj_seq);

    if (obj_data != null){
      // show/output file data
      // Logger.log(`... parent            : ${obj_data['parent']}`);
      // Logger.log(`... url               : ${obj_data['url']}`);
      // Logger.log(`... type              : ${obj_data['type']}`);
      // Logger.log(`... owner name        : ${obj_data['owner-name']}`);
      // Logger.log(`... owner email       : ${obj_data['owner-email']}`);
      // Logger.log(`... access            : ${obj_data['access']}`);
      // Logger.log(`... worksheets        : ${obj_data['worksheets']}`);
      // Logger.log(`... size              : ${obj_data['size']}KB`);
      // Logger.log(`... created           : ${obj_data['created']}`);
      // Logger.log(`... last-modified     : ${obj_data['last-modified']}`);
      // Logger.log(`... editors-can-share : ${obj_data['editors-can-share']}`);

      // detail output to gsheet
      var values = [obj_data['seq'], obj_data['name'], obj_data['parent'], obj_data['url'], obj_data['type'], obj_data['owner-name'], obj_data['owner-email'],
                    obj_data['access'], obj_data['worksheets'], obj_data['size'], obj_data['created'], obj_data['last-modified'], obj_data['editors-can-share']];

      var range_spec = `A${detail_output_row_num}:M${detail_output_row_num}`;
      var range = detail_output_ws.getRange(range_spec);
      range.setValues([values]);

      detail_output_row_num++;

      // permission output to gsheet
      var permissions = obj_data['permissions'];
      var permission_size = permissions.length;
      var range_spec = `A${permission_output_row_num}:E${permission_output_row_num + permission_size - 1}`;
      var range = permission_output_ws.getRange(range_spec);
      range.setValues(permissions);

      permission_output_row_num = permission_output_row_num + permission_size;

    };

    Logger.log(`DONE       ${obj_seq} : ${obj_name}`);
  });

};

// given an object, return relavant data
function get_object_data(obj, is_folder, parent_folder, seq){
  if (obj === null){
    return null;
  };

  var obj_name = obj.getName();
  var obj_data = {'seq': seq, 'name': obj_name, 'is-folder': is_folder};

  // parent folder
  obj_data['parent'] = parent_folder;

  // url
  obj_data['url'] = obj.getUrl();

  // type
  if (obj_data['is-folder'] === true){
    obj_data['type'] = 'folder';
  } else {
    if (obj.getMimeType() in MIME_TYPES){
      obj_data['type'] = MIME_TYPES[obj.getMimeType()];
    } else {
      obj_data['type'] = obj.getMimeType();
    }
  }

  // owner
  var owner = obj.getOwner();
  obj_data['owner-name'] = owner.getName();
  obj_data['owner-email'] = owner.getEmail();

  // access
  obj_data['access'] = obj.getSharingAccess();

  // worksheets only if it is a gsheet
  // if (file_data['type'] === 'gsheet'){
  //   var ss = open_spreadsheet(file_name);
  //   if (ss != null){
  //     file_data['worksheets'] = ss.getNumSheets();
  //   };
  // };

  // size
  obj_data['size'] = obj.getSize() / 1024;

  // created
  obj_data['created'] = obj.getDateCreated();

  // last-modified
  obj_data['last-modified'] = obj.getLastUpdated();

  // editors-can-share
  if (obj.isShareableByEditors()){
    obj_data['editors-can-share'] = 'Yes';
  } else {
    obj_data['editors-can-share'] = '';
  }

  // permissions
  var permissions = [];
  permissions.push([seq, obj_name, obj_data['owner-name'], obj_data['owner-email'], 'owner']);

  var editors = obj.getEditors();
  editors.forEach(function(user){
    permissions.push([seq, obj_name, user.getName(), user.getEmail(), 'editor']);
  });

  var viewers = obj.getViewers();
  viewers.forEach(function(user){
    permissions.push([seq, obj_name, user.getName(), user.getEmail(), 'viewer']);
  });

  // var commenters = obj.getCommenters();
  // commenters.forEach(function(user){
  //   permissions.push([seq, obj_name, user.getName(), user.getEmail(), 'commenter']);
  // });

  obj_data['permissions'] = permissions;

  return obj_data;
};


// traverse a folder
function iterate_folder(folder_to_traverse, parent_path, object_list){
  object_list.push({'object': folder_to_traverse, 'parent-path': parent_path, 'is-folder': true});
  var this_folder_path = `${parent_path}/${folder_to_traverse.getName()}`;

  // first we iterate files
  var files = folder_to_traverse.getFiles();
  while (files.hasNext()) {
    var file = files.next();
    object_list.push({'object': file, 'parent-path': this_folder_path, 'is-folder': false});
  };

  // first we iterate files
  var folders = folder_to_traverse.getFolders();
  while (folders.hasNext()) {
    var folder = folders.next();
    iterate_folder(folder, this_folder_path, object_list);
  };
};


// get full parent path of a drive file
function get_parent_path(folder){
  var parents = [];
  var parent_iter = folder.getParents();
  while (parent_iter.hasNext()) {
    var folder = parent_iter.next();
    parents.push(folder.getName());
    var parent_iter = folder.getParents();
  };

  parents.reverse();
  parent_path = parents.join('/');

  return parent_path;
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
