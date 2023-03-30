PROJECT_ROLE_NBR_BSW_WS_SPECS = {
  'num-columns': 8,
  'frozen-rows': 2,
  'frozen-columns': 0,

  'columns': {
    'A': {'size': 100},
    'B': {'size': 65},
    'C': {'size': 65},
    'D': {'size': 30},
    'E': {'size': 640},
  },

  'ranges': {
    'B1:B': {'weight': 'normal', 'halign': 'center', 'merge': false},
    'C1:C': {'weight': 'normal', 'halign': 'center', 'merge': false},
    'D1:D': {'weight': 'normal', 'halign': 'center', 'merge': false},
    'E1:E': {'weight': 'normal', 'halign': 'left', 'merge': false},

    'B3:B': {'format': 'yyyy-mmm', 'merge': false, 'weight': 'bold'},
    'C3:C': {'format': 'yyyy-mmm', 'merge': false, 'weight': 'bold'},

    'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new'},
    'B2:E2': {'value': 'content', 'weight': 'bold', 'halign': 'left'},

    'A3:H': {'valign': 'top', 'merge': false, 'wrap': true},

    'B3': {'value': 'From', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'weight': 'bold', 'note': '{"repeat-rows": 1}'},
    'C3': {'value': 'To', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'weight': 'bold'},
    'D3:E3': {'value': 'Company/Project/ Position/Relevant technical and management experience', 'bgcolor': '#f3f3f3', 'border-color': '#b7b7b7', 'halign': 'left', 'weight': 'bold'},

  },

  'cell-empty-markers': [
    'B3:E'
  ],
};


// create *07-project-roles-NBR-BSW* worksheet
function create_07_project_roles_nbr_bsw_worksheet(ss_name=undefined){
  // get the spreadsheet
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss == null){
    return;
  };

  var project_roles = project_roles_from_07_project_roles(ss);

  // duplicate the *07-project-roles* as *07-project-roles-NBR-BSW* worksheet
  var source_ws_name = '07-project-roles';
  var source_ws = ss.getSheetByName(source_ws_name);

  var target_ws_name = '07-project-roles-NBR-BSW';
  var target_ws = duplicate_worksheet(ss, source_ws_name, target_ws_name);

  if (target_ws === null){
    return;
  }

  // add 4 new columns after D
  target_ws.insertColumns(2, 4);

  // add project_roles.count * 3 + rows at the end
  // HACk - for safety add 100 rows at the end
  // target_ws.insertRowsAfter(target_ws.getMaxRows(), project_roles.length * 3 + 1);
  target_ws.insertRowsAfter(target_ws.getMaxRows(), 1000);


  // for each column
  for (const [key, value] of Object.entries(PROJECT_ROLE_NBR_BSW_WS_SPECS['columns'])) {
    // resize the columns
    target_ws.setColumnWidth(LETTER_TO_COLUMN[key], value['size'])

  };


  // iterate over ranges and apply specs
  for (const [key, value] of Object.entries(PROJECT_ROLE_NBR_BSW_WS_SPECS['ranges'])) {
    var range = target_ws.getRange(key);
    if (range === null){
      // Logger.log(`ERROR: Range ${key} not found`);
      continue;
    } else {
      // Logger.log(`.. Range ${key} found`);
      work_on_range(ss=ss, range=range, work_spec=value);
    }
  };

  // iterate project-roles and create range_work_specs
  var range_work_specs = {};
  var current_row = 4;
  project_roles.forEach((project_role, index) => {
    var block_start_row = current_row;

    var range_spec = '';

    // Project/Product - label
    var range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Project/Product', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['name'].length; i++){
      range_spec = `D${current_row}:E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['name'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };

    // Client - label
    range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Client', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['client'].length; i++){
      range_spec = `D${current_row}:E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['client'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };

    // Project Brief - label
    range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Project Brief', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['brief'].length; i++){
      range_spec = `D${current_row}:E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['brief'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };

    // Tools and Technology - label
    range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Tools and Technology', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['tool'].length; i++){
      range_spec = `D${current_row}`;
      range_work_specs[range_spec] = {'value': '•', 'halign': 'center'};
      range_spec = `E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['tool'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };

    // Role(s) Performed - label
    range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Role(s) Performed', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['role'].length; i++){
      range_spec = `D${current_row}:E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['role'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };

    // Activities/Tasks Performed - label
    range_spec = `D${current_row}:E${current_row}`;
    range_work_specs[range_spec] = {'value': 'Activities/Tasks Performed', 'halign': 'left', 'bgcolor': '#f3f3f3', 'weight': 'bold'};

    current_row++;

    for (i = 0; i < project_role['task'].length; i++){
      range_spec = `D${current_row}`;
      range_work_specs[range_spec] = {'value': '•', 'halign': 'center'};
      range_spec = `E${current_row}`;
      range_work_specs[range_spec] = {'value': project_role['task'][i], 'halign': 'left', 'weight': 'normal'};
      current_row++;
    };


    // project-role finished
    var block_end_row = current_row - 1;

    // From
    range_spec = `B${block_start_row}:B${block_end_row}`;
    var val = quote_number(project_role.from);
    Logger.log(`.. From : ${project_role.from} -> ${val}`);
    range_work_specs[range_spec] = {'value': val, 'border-color': '#b7b7b7'};

    // To
    range_spec = `C${block_start_row}:C${block_end_row}`;
    var val = quote_number(project_role.to);
    Logger.log(`.. To   : ${project_role.to} -> ${val}`);
    range_work_specs[range_spec] = {'value': val, 'border-color': '#b7b7b7'};

    // border around column D and E
    range_spec = `D${block_start_row}:E${block_end_row}`;
    range_work_specs[range_spec] = {'border-color': '#b7b7b7', 'merge': false};

  });

  // iterate over ranges and apply specs
  for (const [key, value] of Object.entries(range_work_specs)) {
    var range = target_ws.getRange(key);
    if (range === null){
      // Logger.log(`ERROR: Range ${key} not found`);
      continue;
    } else {
      // Logger.log(`.. Range ${key} found`);
      work_on_range(ss=ss, range=range, work_spec=value);
    }
  };

  // remove last 3 columns
  target_ws.deleteColumns(6, 3);

  // remove all trailing blank rows
  remove_trailing_blank_rows(target_ws);

  // clear conditional formatting
  target_ws.clearConditionalFormatRules();

  var total_rows = target_ws.getMaxRows();
  var total_columns = target_ws.getMaxColumns();

  // conditional formats
  var range = target_ws.getRange(3, 1, total_rows - 2, total_columns);

  // conditional formatting
  add_conditional_formatting_for_blank_cells(target_ws, PROJECT_ROLE_NBR_BSW_WS_SPECS['cell-empty-markers']);

  // review-notes
  var rules = target_ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenFormulaSatisfied("=not(isblank($A:$A))")
    .setBackground('#f4cccc')
    .build();
  rules.push(rule);

  target_ws.setConditionalFormatRules(rules);

  target_ws.setFrozenRows(PROJECT_ROLE_NBR_BSW_WS_SPECS['frozen-rows']);
  target_ws.setFrozenColumns(PROJECT_ROLE_NBR_BSW_WS_SPECS['frozen-columns']);

};


// update *07-project-roles* worksheet
function update_07_project_roles_worksheet(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss == null){
    return;
  };

  // get the *07-project-roles* worksheet
  var ws_name = '07-project-roles';
  var ws = ss.getSheetByName(ws_name);

  // append a row for safety
  ws.insertRowsAfter(ws.getMaxRows(), 1);

  var total_rows = ws.getMaxRows();
  var total_columns = ws.getMaxColumns();

  // we do it only if the worksheet has 8 columns
  if (total_columns != 8){
    Logger.log(` .. worksheet ${ws_name} does not have 7 columns` );
    return;
  }

  ws.clearConditionalFormatRules();

  // unfreeze
  ws.setFrozenRows(0);

  // add columns as defined in RESUME_WS_COLUMNS
  for (const [key, value] of Object.entries(RESUME_WS_SPECS[ws_name]['columns'])) {
    // Logger.log('column ' + key + ' size ' + value);
    var index = LETTER_TO_COLUMN[key];
    ws.insertColumns(index);
    ws.setColumnWidth(index, value);
  };

  // first we create a 10 row gap between entries, each entry starts at column E now, starting at row 4
  var current_row = 4;
  while(1){
    // if there is a value in this row column G [Project/Product], insert 10 rows above
    var column = LETTER_TO_COLUMN['E'];
    var range_spec = `E${current_row}`;
    var values = ws.getRange(range_spec).getValues();
    // Logger.log(`.. cell ${range_spec} : ${values[0][0]}`);
    if(values[0][0] != ''){
      ws.insertRowsBefore(current_row, 10);
      current_row = current_row + 11;
    } else {
      current_row++;
    }
    if (current_row >= ws.getMaxRows()){
      break;
    }
  };

  var current_row = 4;
  var rows_starting_data = [];
  while(1){
    // if there is a value in this row column G [Project/Product], insert 4 rows above
    var column = LETTER_TO_COLUMN['G'];
    var range = ws.getRange(current_row, column);
    var values = range.getValues();
    if(values[0][0] != ''){
      rows_starting_data.push(current_row);
      // Logger.log('at E' + current_row + " found : " + values[0][0]);
    }

    current_row++;

    if (current_row >= ws.getMaxRows()){
      break;
    }
  };

  var data_row_ranges = [];
  for (var i = 0; i < rows_starting_data.length; i++) {
    if(i < rows_starting_data.length - 1){
      data_row_ranges.push([rows_starting_data[i], rows_starting_data[i+1] - 11]);
    } else {
      data_row_ranges.push([rows_starting_data[i], ws.getMaxRows()]);
    }
  }

  // unmerge everything in range B3:D
  var range = ws.getRange('B3:D');
  range.breakApart();

  const SOURCE_COLUMNS = {
    Project : 1,
    Description : 2,
    Role : 3,
    Activities : 4,
    DateFrom : 6,
    DateTo : 7,
  };

  const TARGET_COLUMNS = {
    A : 1,
    B : 2,
    C : 3,
  };

  // now we have enough space for filling the first three columns
  const OFFSET = 9;
  data_row_ranges.forEach(function(r, i){
    // Logger.log(r);
    var source_range_spec = `E${r[0]}:K${r[1]}`;
    var source_range = ws.getRange(source_range_spec);


    var target_range_spec = `B${r[0] - OFFSET}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    // Logger.log(`preparing range : ${target_range_spec}`);

    target_range.setBorder(true, true, true, true, false, false, "#999999", SpreadsheetApp.BorderStyle.SOLID).setHorizontalAlignment('left');
    // conditional formats
    add_conditional_formatting_for_blank_cells(ws, [target_range_spec]);


    // TODO: process col A, 1st row - Project/Product
    target_cell = target_range.getCell(1, TARGET_COLUMNS.A);
    target_cell.setValue('Project/Product').setFontWeight("bold");

    target_cell = target_range.getCell(1, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Project);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");


    // TODO: process col A, 2nd row - Client
    target_cell = target_range.getCell(2, TARGET_COLUMNS.A);
    target_cell.setValue('Client').setFontWeight("bold");

    target_cell = target_range.getCell(2, TARGET_COLUMNS.B);
    target_cell.setFontWeight("bold");


    // TODO: process col A, 3rd row - Tenure
    target_cell = target_range.getCell(3, TARGET_COLUMNS.A);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.DateFrom)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('right').setFontWeight("bold");

    target_cell = target_range.getCell(3, TARGET_COLUMNS.B);
    target_cell.setValue('-');
    target_cell.setHorizontalAlignment('center').setFontWeight("bold");

    target_cell = target_range.getCell(3, TARGET_COLUMNS.C);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.DateTo)
    target_cell.setValue(source_cell.getValue()).setNumberFormat('yyyy-MMM').setHorizontalAlignment('left').setFontWeight("bold");


    // TODO: process col A, 4th row - Project Brief
    target_cell = target_range.getCell(4, TARGET_COLUMNS.A);
    target_cell.setValue('Project Brief').setFontWeight("bold");

    target_cell = target_range.getCell(4, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Description);
    target_cell.setValue(source_cell.getValue());

    // row 6 Tools and Technology
    target_cell = target_range.getCell(6, TARGET_COLUMNS.B);
    target_cell.setValue('Tools and Technology').setFontWeight("bold");

    // row 7-8 column C bullet symbol
    target_cell = target_range.getCell(7, TARGET_COLUMNS.B);
    target_cell.setValue('•').setHorizontalAlignment('center');

    target_cell = target_range.getCell(8, TARGET_COLUMNS.B);
    target_cell.setValue('•').setHorizontalAlignment('center');


    // TODO: process col A, 9th row - Role(s) Performed
    target_cell = target_range.getCell(9, TARGET_COLUMNS.A);
    target_cell.setValue('Role(s) Performed').setFontWeight("bold");

    target_cell = target_range.getCell(9, TARGET_COLUMNS.B);
    source_cell = source_range.getCell(1, SOURCE_COLUMNS.Role);
    target_cell.setValue(source_cell.getValue()).setFontWeight("bold");


    // TODO: process col A, 10th row - Activities/Tasks Performed
    target_cell = target_range.getCell(10, TARGET_COLUMNS.A);
    target_cell.setValue('Activities/Tasks Performed').setFontWeight("bold");

    // 10th row to end, column C center aligned
    var target_range_spec = `C${r[0]}:C${r[1]}`;
    var target_range = ws.getRange(target_range_spec);
    target_range.setHorizontalAlignment('center');


    // TODO: process col Activities
    // var source_range_spec = `J${r[0]}:K${r[1]}`;
    var source_range = ws.getRange(r[0], SOURCE_COLUMNS.Activities + 4, r[1]-r[0]+1, 2);

    var target_range_spec = `C${r[0]}:D${r[1]}`;
    var target_range = ws.getRange(target_range_spec);

    source_range.copyTo(target_range, {contentsOnly:true});
  });


  // merging
  data_row_ranges.forEach(function(r, i){
    // merge row 1 - [Project/Product] column C and D horizontally
    var range_spec = `C${r[0] - OFFSET}:D${r[0] - OFFSET}`
    // Logger.log(`.. merging ${range_spec} - [Project/Product]`);
    var range = ws.getRange(range_spec);
    range.merge();


    // merge row 2 - [Client] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 1 - OFFSET}:D${r[0] + 1 - OFFSET}`);
    range.merge();


    // merge row 4-6 - [Project Brief] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 3 - OFFSET}:D${r[0] + 5 - OFFSET}`);
    range.mergeAcross();


    // merge row 4-8 - [Project Brief] column B vertically
    var range = ws.getRange(`B${r[0] + 3 - OFFSET}:B${r[0] + 7 - OFFSET}`);
    range.merge();


    // merge row 9 - [Role(s) Performed] column C and D horizontally
    var range = ws.getRange(`C${r[0] + 8 - OFFSET}:D${r[0] + 8 - OFFSET}`);
    range.merge();


    // merge row 10-end - [Activities/Tasks Performed] column B vertically
    var range = ws.getRange(`B${r[0] + 9 - OFFSET}:B${r[1]}`);
    range.merge();
  });


  // *content* in B2 and merge to D2
  var cell = ws.getRange('B2');
  cell.setValue('content');
  var range = ws.getRange('B2:D2');
  range.merge();


  // remove all rows starting from 3 where column B is empty
  var rows_to_remove = 0;
  for (var i = 3; i < ws.getMaxRows(); i++) {
    var cell = ws.getRange(`B${i}`);
    if (cell.getValue() == ''){
      rows_to_remove++;
    } else {
      break;
    }
  }
  ws.deleteRows(3, rows_to_remove);

  // remove column E to K
  ws.deleteColumns(5, 7);


  // review-notes
  range = ws.getRange(3, 1, ws.getMaxRows() - 2, ws.getMaxColumns());
  var rules = ws.getConditionalFormatRules();
  var rule = SpreadsheetApp.newConditionalFormatRule()
    .setRanges([range])
    .whenFormulaSatisfied("=not(isblank($A:$A))")
    .setBackground('#f4cccc')
    .build();
  rules.push(rule);

  ws.setConditionalFormatRules(rules);
};


// get project-roles *07-project-roles* worksheet
function project_roles_from_07_project_roles(ss){
  if (ss == null){
    return null;
  };

  // get the *07-project-roles* worksheet
  var source_ws_name = '07-project-roles';
  var source_ws = ss.getSheetByName(source_ws_name);

  // get the data (list of project-roles)
  var source_values = source_ws.getRange('B3:D').getValues();

  var num_rows = source_values.length;
  var current_row_index = 0;
  var project_roles = [];
  var new_project_role_found = false;
  var project_role = new Object();

  // loop until we have eaten up all rows
  while (num_rows > current_row_index) {
    var current_row = source_values[current_row_index];

    if (current_row[0] === 'Project/Product'){
      // we have found the start of a new project-role

      // there may be a running project-role
      if (Object.keys(project_role).length != 0){
        project_role.end_row = current_row_index - 1;
        project_roles.push(project_role);
        var project_role = new Object();
      };

      project_role.start_row = current_row_index;

    };

    current_row_index++;
  };

  // there may be a pending project-role
  if (Object.keys(project_role).length != 0){
    project_role.end_row = current_row_index - 1;
    project_roles.push(project_role);
  };

  const regex = /^[.\s]+$/;

  // now we have a list of project-roles
  project_roles.forEach((project_role, index) => {
    project_role['name'] = [];
    project_role['client'] = [];
    project_role.from = '';
    project_role.to = '';
    project_role['brief'] = [];
    project_role['tool'] = [];
    project_role['role'] = [];
    project_role['task'] = [];
    var current_group = 'name';
    for (i = project_role.start_row; i <= project_role.end_row; i++) {
      var row = source_values[i];
      // the group is the first value
      var new_group_label = row[0];
      if (isNaN(new_group_label)) {
        new_group_label = new_group_label.replace(regex, '');
      }

      if (new_group_label === '') {
        // previous group continuing
        var value = row[GROUP_VALUE_INDEX[current_group]];

        // group may have subgroups
        if (current_group in GROUP_SUBGROUP) {
          if (value in GROUP_SUBGROUP[current_group]) {
            // the value is not value for the group rather it starts a subgroup
            current_group = GROUP_SUBGROUP[current_group][value]

          } else {
            // this is not a subgroup, append value
            if (value != '') {
              project_role[current_group] = project_role[current_group].concat(split_and_dress(value));
            };

          };

        } else {
          // the group does not have any subgroups, append value
          if (value != '') {
            project_role[current_group] = project_role[current_group].concat(split_and_dress(value));
          };

        };

      } else {
        // a new group has started, get the group
        if (new_group_label in LABEL_TO_GROUP) {
          current_group = LABEL_TO_GROUP[new_group_label];

          // append value into the group
          var value = row[GROUP_VALUE_INDEX[current_group]];
          if (value != '') {
            project_role[current_group] = project_role[current_group].concat(split_and_dress(value));
          };

        } else {
          // this must be the from value
          project_role.from = new_group_label;
          project_role.to = row[2];
        }
      };

    };

    // we should have at least one entry for each groups
    if (project_role['name'].length === 0) {
      project_role['name'].push('');
    };

    if (project_role['client'].length === 0) {
      project_role['client'].push('');
    };

    if (project_role['brief'].length === 0) {
      project_role['brief'].push('');
    };

    if (project_role['tool'].length === 0) {
      project_role['tool'].push('');
    };

    if (project_role['role'].length === 0) {
      project_role['role'].push('');
    };

    if (project_role['task'].length === 0) {
      project_role['task'].push('');
    };

    if (false) {
      Logger.log(`project ${index}`);
      Logger.log(`.. from  : ${project_role['from']}`);
      Logger.log(`.. to    : ${project_role['to']}`);

      Logger.log(`.. name  : ${project_role['name'][0]}`);
      if (project_role['name'].length > 0) {
        for (i = 1; i < project_role['name'].length; i++) {
          Logger.log(`..       : ${project_role['name'][i]}`);
        };
      }

      Logger.log(`.. client: ${project_role['client'][0]}`);
      if (project_role['client'].length > 0) {
        for (i = 1; i < project_role['client'].length; i++) {
          Logger.log(`..       : ${project_role['client'][i]}`);
        };
      }

      Logger.log(`.. brief : ${project_role['brief'][0]}`);
      if (project_role['brief'].length > 0) {
        for (i = 1; i < project_role['brief'].length; i++) {
          Logger.log(`..       : ${project_role['brief'][i]}`);
        };
      }

      Logger.log(`.. tool  : ${project_role['tool'][0]}`);
      if (project_role['tool'].length > 0) {
        for (i = 1; i < project_role['tool'].length; i++) {
          Logger.log(`..       : ${project_role['tool'][i]}`);
        };
      }

      Logger.log(`.. role  : ${project_role['role'][0]}`);
      if (project_role['role'].length > 0) {
        for (i = 1; i < project_role['role'].length; i++) {
          Logger.log(`..       : ${project_role['role'][i]}`);
        };
      }

      Logger.log(`.. task  : ${project_role['task'][0]}`);
      if (project_role['task'].length > 0) {
        for (i = 1; i < project_role['task'].length; i++) {
          Logger.log(`..       : ${project_role['task'][i]}`);
        };
      }
    };

  });

  return project_roles;

};


LABEL_TO_GROUP = {
  'Project/Product': 'name',
  'Client': 'client',
  'Project Brief': 'brief',
  'Role(s) Performed': 'role',
  'Activities/Tasks Performed': 'task',
};

GROUP_SUBGROUP = {
  'brief': {
    'Tools and Technology': 'tool',
    'Tools and Technologies': 'tool',
    },
};

GROUP_VALUE_INDEX = {
  'name': 1,
  'client': 1,
  'brief': 1,
  'tool': 2,
  'role': 1,
  'task': 2,
};
