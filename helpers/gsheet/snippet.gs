// snippets for *work_on_spreadsheets*
// ------------------------------------------------------------
// ALL WORKSHEET FORMATTING - BEGIN
// update_all_worksheets(ss_name);
// ALL WORKSHEET FORMATTING - END
//
// RENAMING WORKSHEETS - BEGIN
// rename_worksheets(ss_name, WORKSHEET_NAME_MAP1);
// rename_worksheets(ss_name, WORKSHEET_NAME_MAP2);
// RENAMING WORKSHEETS - END
//
// RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - BEGIN
// resize_columns_in_worksheets(ss_name, RESUME_WS_COLUMNS);
// write_column_size_in_worksheets(ss_name);
// order_worksheets(ss_name);
// RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - END
//
// SPECIFIC to *00-layout* WORKSHEET - BEGIN
// create_00_layout_worksheet(ss_name);
// update_00_layout_worksheet_links(ss_name);
// update_00_layout_worksheet_content(ss_name);
// update_00_layout_worksheet_photo(ss_name, ss_org);
// update_00_layout_worksheet_signature(ss_name, ss_org);
// SPECIFIC to *00-layout* WORKSHEET - END
//
// SPECIFIC to *01-personal* WORKSHEET - BEGIN
// update_01_personal_worksheet_photo(ss_name, ss_org);
// SPECIFIC to *01-personal* WORKSHEET - END
//
// CREATE SHEETS FROM TEMPLATE - BEGIN
// create_ss_from_template(ss_name, template_ss, blank_resume_folder);
// CREATE SHEETS FROM TEMPLATE - END
//


INFO_CELL_SPEC = {
  "G9": 0,
  "G10": 24,
  "G11": 25,
  "G12": 27,
  "G13": 29,

  "G17": 32,
  "G18": 33,
  "G19": 34,

  "G23": 35,
  "G24": 36,
  "G25": 37,

  "G29": 38,
  "G30": 39,
  "G31": 40,

  "G35": 41,
  "G36": 42,
  "G37": 43,

  "G41": 44,
  "G42": 45,
  "G43": 46,

  "G47": 47,
  "G48": 48,
  "G49": 49,

  "F53": 53,
};


function clear_info_cells(ws){
  for (const [cell_a1, index] of Object.entries(INFO_CELL_SPEC)) {
    ws.getRange(cell_a1).setValue('');
  };
};


function populate_info_cells(ws, data){
  for (const [cell_a1, index] of Object.entries(INFO_CELL_SPEC)) {
    ws.getRange(cell_a1).setValue(data[index]);
  };
};


function onEdit(){
  var ws = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data_ws = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("-toc") ;

  // if it is the *-todo* worksheet
  if(ws.getSheetName() == "-todo"){
    var active_cell = ws.getActiveCell();

    // only applicable for cell F2
    if (active_cell.getA1Notation() == 'F2') {
      var org_values = data_ws.getRange("V5:V").getValues();
      var name_values = data_ws.getRange("B5:B").getValues();

      if (name_values != null && org_values != null){
        // the cell to the right is to be cleared first
        active_cell.offset(0, 1).clearContent().clearDataValidations();

        var selected_org = active_cell.getValue();

        var name_list = [];
        name_values.forEach(function(name, index) {
          if (org_values[index] == selected_org) {
            name_list.push(name);
          };
        });

        var validation_rule = SpreadsheetApp.newDataValidation().requireValueInList(name_list).build();
        active_cell.offset(0, 1).setDataValidation(validation_rule);
      }
    }
    else if (active_cell.getA1Notation() == 'G2') {
      var selected_org = ws.getRange("F2").getValue();
      var selected_name = ws.getRange("G2").getValue();
      // Logger.log(`${selected_org} : ${selected_name} selected`);
      // get the data for this name
      var data_range_spec = `B5:BC${data_ws.getMaxRows()}`;
      var data_values = data_ws.getRange(data_range_spec).getValues();

      clear_info_cells(ws);
      if (selected_org != '' && selected_name != ''){
        var selected_index = -1;
        for (var i = 0; i < data_values.length; i++){
          // Logger.log(`${data_values[i]}`);
          if (data_values[i][20] == selected_org && data_values[i][0] == selected_name){
            selected_index = i;
            // Logger.log(`data found at ${selected_index}`);
            break;
          };
        };

        if (selected_index != -1){
          // we have got the element where the data is
          var data = data_values[selected_index];
          populate_info_cells(ws, data);
          ws.getRange("F3:G53").activate();
        } else {
          Logger.log(`data not found in range ${data_range_spec}`);
        };
      };
    };
  };
};
