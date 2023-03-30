// do some work on a list of sheets
function work_on_spreadsheets() {
  var this_ss = SpreadsheetApp.getActiveSpreadsheet();
  var toc_ws_name = '-toc-new';
  var toc_ws = this_ss.getSheetByName(toc_ws_name);

  // link_cells(toc_ws, 'F102:F', 'E102:E', null)
  // return;

  // get sheets to work on
  // var ss_data_to_work_on = select_resume_spreadsheets_from_toc(this_ss, toc_ws);
  var ss_data_to_work_on = get_spreadsheets_to_work_on();

  // var template_ss = get_unique_file_by_name('Résumé__template');
  // var target_resume_folder = DriveApp.getFolderById('19qaw26Oq_i1t_sK2lcU5gLeNVszc8Pch');

  // get worksheet to import
  var ss_to_import_from = open_spreadsheet('celloscope__résumé__template')
  // var ws_to_import = ss_to_import_from.getSheetByName('16-references');
  var ws_to_import = ss_to_import_from.getSheetByName('00-layout-USAID-FFBT');

  ss_data_to_work_on.forEach(function(ss_data, index){
    var ss_name = ss_data[0];
    var ss_org = ss_data[1];
    var row_num = ss_data[2];
    Logger.log(`PROCESSING ${index} : ${row_num} .. ${ss_org} : ${ss_name}`);

    var ss = open_spreadsheet(ss_name);
    if (ss == null){
      Logger.log(` .. ERROR .. ${index} : Spreadsheet ${ss_name} not found`);
      return;
    }


    // do_miscellaneous_things(ss);
    // search_replace_texts(ss, 'https://spectrum-bd.biz/data/artifacts/signature/signature', 'https://spectrum-bd.biz/data/artifacts/signature/spectrum/signature');
    // search_replace_texts(ss, 'https://spectrum-bd.biz/data/i', 'https://spectrum-bd.biz/data/artifacts/i');
    // search_replace_texts(ss, 'https://spectrum-bd.biz/data/s', 'https://spectrum-bd.biz/data/artifacts/s');
    // search_replace_texts(ss, 'https://spectrum-bd.biz/data/p', 'https://spectrum-bd.biz/data/artifacts/p');
    // search_replace_texts(ss, '.png", 3)', '.png", 1)');


    // CREATE Resume gsheet - BEGIN
    // create_ss_from_template(ss_name, template_ss, target_resume_folder)
    // CREATE Resume gsheet - BEGIN


    // RENAME worksheets - BEGIN
    // rename_worksheets(ss, {'07-project-roles-NBR-BSW': '07-project-roles'});
    // RENAME worksheets - END

    // MOVE worksheet - BEGIN
    // move_worksheet_to_end(ss, '-toc');
    // MOVE worksheet - END

    // work on *-toc-new* - BEGIN
    // new_toc_from_toc(ss);
    // update_new_toc(ss);
    // update_new_toc_links(ss);
    // update_toc_new_worksheet_links(ss_name);
    // work on *-new-toc* - END

    // REMOVE named worksheet - BEGIN
    // remove_worksheet(ss, ws_name_to_remove='-toc-new');
    // REMOVE named worksheet - END

    // IMPORT worksheets into ss to a specific location - BEGIN
    // import_worksheet(ss, ws_to_import=ws_to_import, index=3);
    // IMPORT worksheets into ss to a specific location - END
    //
    // ALL WORKSHEET FORMATTING - BEGIN
    // update_all_worksheets(ss);
    // ALL WORKSHEET FORMATTING - END
    //
    // RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - BEGIN
    // resize_columns_in_worksheets(ss, RESUME_WS_SPECS);
    // write_column_size_in_worksheets(ss);
    // order_worksheets(ss);
    // RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - END
    //
    // SPECIFIC to *00-layout* WORKSHEET - BEGIN
    // update_00_layout_worksheet_structure(ss)
    // update_00_layout_worksheet_photo(ss_name, ss_org);
    // update_00_layout_worksheet_signature(ss_name, ss_org);
    // update_00_layout_worksheet_links(ss_name);
    // SPECIFIC to *01-personal* WORKSHEET - END
    //
    // SPECIFIC to *00-layout-USAID_FFBT* WORKSHEET - BEGIN
    update_worksheet_00_layout_USAID_FFBT(ss_name);
    // SPECIFIC to *00-layout-USAID_FFBT* WORKSHEET - END
    //
    // SPECIFIC to *01-personal* WORKSHEET - BEGIN
    // update_01_personal_worksheet_photo(ss_name, ss_org);
    // SPECIFIC to *01-personal* WORKSHEET - END

    // SPECIFIC to *06-job-history* WORKSHEET - BEGIN
    // update_06_job_history_worksheet(ss_name);
    // SPECIFIC to *06-job-history* WORKSHEET - END

    // SPECIFIC to *01-project-roles* WORKSHEET - BEGIN
    // update_07_project_roles_worksheet(ss_name);
    // create_07_project_roles_nbr_bsw_worksheet(ss_name);
    // SPECIFIC to *01-project-roles* WORKSHEET - END

    Logger.log(`DONE ..... ${index} : ${row_num} .. ${ss_org} : ${ss_name}`);
  });
};


// update all worksheets with the given spec
function update_all_worksheets(ss){
  var update_spec = {'font-family': 'Calibri', 'font-size': 10, 'valign': 'top', 'merge': false};

  // get all the worksheets
  ss.getSheets().forEach(function(ws){
    var range = ws.getRange(1, 1, ws.getMaxRows(), ws.getMaxColumns());
    work_on_range(ss, range, update_spec)
    Logger.log(` .. Worksheet ${ws.getName()} updated`);
  });
};


// resize columns in each worksheet as per spec
function resize_columns_in_worksheets(ss, ws_column_specs){
  // get all the worksheets
  ss.getSheets().forEach(function(ws){
    let ws_name = ws.getName();
    if (ws_name in ws_column_specs){
      let ws_column_spec = ws_column_specs[ws_name];
      if ('num-columns' in ws_column_spec){
        // see if the number of columns matches
        if (ws_column_spec['num-columns'] == ws.getMaxColumns()) {
          for (const [key, value] of Object.entries(ws_column_spec['columns'])) {
            let index = LETTER_TO_COLUMN[key];
            ws.setColumnWidth(index, value);
          };
        } else {
          Logger.log(` .. WARN .. ${ws_name} expected ${ws_column_spec['num-columns']} columns, found ${ws.getMaxColumns()} columns`);
        };
      };
    };
  });
};


// write column sizes for each worksheet
function write_column_size_in_worksheets(ss){
  // get all the worksheets
  var ws_list = ss.getSheets();
  for (var i = 0; i < ws_list.length; i++) {
    Logger.log(` .. PROCESSING .. Worksheet ${ws_list[i].getName()}`);
    get_and_write_column_size(ws_list[i]);
    Logger.log(` .. DONE ........ Worksheet ${ws_list[i].getName()}`);
  };

};


// create a Worksheet in the specific position with specified parameters
function create_worksheet(ss, ws_name, ws_index=undefined, ws_rows, ws_columns, ws_column_sizes=undefined){
  // check if the worksheet already exists or not
  var ws = ss.getSheetByName(ws_name);
  if (ws != null){
    Logger.log(`ERROR: Worksheet ${ws_name} already exists in Spreadsheet ${ss.getName()}`);
    return;
  };

  // if index was not specified, default it as the 2nd worksheet
  if (ws_index == undefined){
    ws_index = 1;
  };

  // create the Worksheet
  var ws = ss.insertSheet(ws_name, ws_index);

  // limit rows
  var rows_to_delete = ws.getMaxRows() - ws_rows;
  ws.deleteRows(ws_rows + 1, rows_to_delete);

  // limit columns
  var columns_to_delete = ws.getMaxColumns() - ws_columns;
  ws.deleteColumns(ws_columns + 1, columns_to_delete);

  // resize columns as specified
  if (ws_column_sizes != undefined){
    for (var i = 0; i < ws_column_sizes.length; i++) {
      var column_size = ws_column_sizes[i];
      ws.setColumnWidth(i+1, column_size);
    };
  }

  return ws;
};


// rename Worksheets of a Spreadsheet - the name map is a dict
function rename_worksheets(ss, name_map){
  for (const [key, value] of Object.entries(name_map)) {
    var ws = ss.getSheetByName(key);
    if (ws != null){
      ws.setName(value);
      Logger.log(`Worksheet ${key} renamed to ${value}`);
    } else {
      Logger.log(`Worksheet ${key} not found`);
    }
  };
};


// list all worksheet
function list_worksheets(ss){
  var ws_name_list = [];
  var ws_list = ss.getSheets();

  for (var i = 0; i < ws_list.length; i++) {
    ws_name_list.push(ws_list[i].getName());
  };

  // return ws_name_list;
  ws_name_list_str = ws_name_list.join('\n');
  Logger.log(ws_name_list_str);
};


// for ordering worksheets in a Google sheet
function order_worksheets(ss) {
  var ws_name_list = [];
  var ws_list = ss.getSheets();

  for (var i = 0; i < ws_list.length; i++) {
    ws_name_list.push(ws_list[i].getName());
  }

  ws_name_list.sort();

  ws_name_list.forEach(function(e, i){
    // Logger.log(i + ' worksheet : ' + e);
    ss.setActiveSheet(ss.getSheetByName(e));
    ss.moveActiveSheet(i+1);
  });
};


// duplicate a Worksheet
function duplicate_worksheet(ss, ws_name, duplicate_ws_name){
  // get the worksheet to duplicate
  var ws = ss.getSheetByName(ws_name);
  if (ws === null){
    Logger.log(`ERROR: ${ws_name} not found`);
    return null;
  }

  var ws_pos = ws.getIndex();

  // duplicate the worksheet, see if the worksheet already exists or not
  var duplicate_ws = ss.getSheetByName(duplicate_ws_name);
  if (duplicate_ws != null){
    Logger.log(`WARN: ${duplicate_ws_name} already exists`);
    return null;
  }

  // now do the duplication
  var duplicate_ws = ws.copyTo(ss).setName(duplicate_ws_name);
  duplicate_ws.activate();
  ss.moveActiveSheet(ws_pos+1);

  return duplicate_ws;
};


// import ws_to_import into *ss* in position *index*
function import_worksheet(ss, ws_to_import, index=-1){
  // first check whether the worksheet already exists or not
  var ws_name_to_import = ws_to_import.getName();
  var ws = ss.getSheetByName(ws_name_to_import);
  if (ws != null){
    Logger.log(`.. WARN : worksheet ${ws_name_to_import} EXISTS`)
    return;
  }

  Logger.log(`.. INFO : importing worksheet ${ws_name_to_import}`)
  var ws = ws_to_import.copyTo(ss);
  ws.setName(ws_to_import.getName());
  ss.setActiveSheet(ws);
  if (index != -1){
    ss.moveActiveSheet(index);
  }
};


// remove worksheet by name
function remove_worksheet(ss, ws_name_to_remove){
  var ws_to_remove = ss.getSheetByName(ws_name_to_remove);
  if (ws_to_remove != null){
    ss.deleteSheet(ws_to_remove);
  }
};


// copy worksheets from one sheet to another
function copy_worksheets_between_sheets(copy_to) {
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
function copy_sheets() {
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


// move a sheet to End
function move_worksheet_to_end(ss, ws_name) {
    var ws = ss.getSheetByName(ws_name);
    var sheet_count = ss.getNumSheets();

    ss.setActiveSheet(ws);
    ss.moveActiveSheet(sheet_count);
};
