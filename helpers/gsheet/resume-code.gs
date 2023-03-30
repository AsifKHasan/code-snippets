// returns a list of ss_data (spreadsheet name + organization) from the *-toc* sheet based on some filtering criteria
function select_resume_spreadsheets_from_toc(ss, ws){
  // get the ss_names based on some criteria from the current spreadsheet *-toc* worksheet
  var toc_data = ws.getRange('A5:AA').getValues();
  var column_map = RESUME_WS_SPECS[ws.getName()]['column-index'];

  var ss_data_list = [];
  toc_data.forEach(function(row, index){
    var row_num = index + 5;
    // we must have a value in link column
    if (row[column_map['link'] - 1] != ''){
      // now we apply custom filters

      // let us select only Spectrum scm employees
      // if (row[column_map['organization'] - 1] == 'Spectrum'){
      // if (row[column_map['organization'] - 1] == 'Spectrum' && row[column_map['unit'] - 1] == 'dc-infra'){
      // if (row[column_map['heading'] - 1] == 'A. S. M. Estiuk Sadick'){
      if (row[column_map['process'] - 1] == 'Yes'){
      // if (row_num >= 100 && row_num < 320){
      // if (true){
        var ss_name = row[column_map['link'] - 1];
        var ss_org = row[column_map['organization'] - 1];
        ss_data_list.push([ss_name, ss_org, row_num])
      };
    };
  });

  return ss_data_list;
};


// update links in *-toc* worksheet
function update_toc_worksheet_links(ss_name=undefined) {
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '-toc';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      link_cells(ws, 'F56:F154', 'E56:E154', null);
    } else {
      Logger.log(` .. ERROR .. Worksheet ${key} not found`);
    }
  };
};


// update *01-personal* worksheet
function update_01_personal_worksheet_photo(ss_name, ss_org){
  var ss = open_spreadsheet(ss_name);
  var org = ss_org.toLowerCase();

  if (ss != null){
    var ws_name = '01-personal';
    var ws = ss.getSheetByName(ws_name);

    if (ws != null){
      // formula is in a specific cell
      var cell_A1 = 'E3';
      var cell = ws.getRange(cell_A1);

      if (cell == null){
        Logger.log(` .. ERROR .. Cell ${cell_A1} not found`);
        return;
      } else {
        // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/photo/spectrum/photo__Khandakar.Asif.Hasan.png", 1)
        var name_without_space = ss_name.replace('Résumé__', '');
        var formula = `=image("https://spectrum-bd.biz/data/artifacts/photo/${org}/photo__${name_without_space}.png", 1)`;
        cell.setFormula(formula);
      }
    } else {
      Logger.log(`.. ERROR .. Worksheet ${ws_name} not found`);
    };
  } else {
    Logger.log(`.. ERROR .. Spreadsheet ${ss_name} not found`);
  };
};


// resize rows and update notes in 13, 14 and 15
function do_miscellaneous_things(ss){
  if (ss != null){
    var ws_name_list = ['13-educational-certificates', '14-vendor-certificates', '15-institutional-certificates'];
    ws_name_list.forEach((ws_name) => {
      var ws = ss.getSheetByName(ws_name);
      if (ws != null){
        var range = ws.getRange('B3:B');
        var num_rows = range.getNumRows();
        Logger.log(`.. worksheet ${ws_name} : ${num_rows + 2} rows`);
        for (i = 1; i <= num_rows; i++){
          var cell = range.getCell(i, 1);
          if (cell.getNote() === '{"new-page": true, "keep-with-next": true}'){
            cell.setNote('{"content": "out-of-cell", "keep-with-next": true}');
          }
          if (ws.getRowHeight(i+2) > 100){
            Logger.log(`.... row ${i + 2} height to be set to 450`);
            ws.setRowHeight(i+2, 450);
          }
        };
      };
    });
  };
};
