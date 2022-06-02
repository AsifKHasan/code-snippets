// do some work on a list of sheets
function qa_work_on_spreadsheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var toc_ws_name = '-toc';
  var ws = ss.getSheetByName(toc_ws_name);

  // get sheets to work on
  var ss_data_to_work_on = select_resume_spreadsheets_from_toc(ss, ws);

  var qa_report_folder_id = '12egQ35QkqEf1eh9B_JTPDiTjgEWTV6Z8';

  ss_data_to_work_on.forEach(function(ss_data){
    var ss_name = ss_data[0];
    var ss_org = ss_data[1];
    var row_num = ss_data[2];
    Logger.log(`PROCESSING ${row_num} .. ${ss_org} : ${ss_name}`);

    // QA REPORT GENERATION - BEGIN
    // update column AZ and BA with counts
    var counts = prepare_qa_report(ss_name, qa_report_folder_id);
    var error_count = counts['error-count'];
    var warning_count = counts['warning-count'];
    var qa_report_name = counts['qa-report-name'];

    var error_count_cell = ws.getRange(`AZ${row_num}`);
    var warning_count_cell = ws.getRange(`BA${row_num}`);
    var link_cell = ws.getRange(`BB${row_num}`);

    error_count_cell.setValue(error_count);
    warning_count_cell.setValue(warning_count);
    link_cell.setValue(qa_report_name);
    link_cell_to_spreadsheet(ss, link_cell, qa_report_name);
    // QA REPORT GENERATION - END

    Logger.log(`DONE ..... ${row_num} .. ${ss_org} : ${ss_name}`);
  });
};


// check 06-job-history worksheet
function check_06_job_history_worksheet(ss){
  var ws_name = '06-job-history';
  var logs = [];
  var ss_url = ss.getUrl();
  var ws = ss.getSheetByName(ws_name);

  if (ws == null){
    let msg = `worksheet ${ws_name} not found`;
    logs.push(qa_error(msg, ss_url));
    return logs;
  }

  // no point in going forward if column count does not match
  if (ws.getMaxColumns() != RESUME_WS_QA['worksheets'][ws_name]['column-count']){
    return logs;
  }

  var ws_url = `${ss_url}#gid=${ws.getSheetId()}`;

  if (!('block-data' in RESUME_WS_QA['worksheets'][ws_name])){
    return logs;
  };

  var block_spec = RESUME_WS_QA['worksheets'][ws_name]['block-data'];
  var block_range_spec = block_spec['block-range-spec'];
  var header_row_count = block_spec['header-rows'];
  var marker_column = block_spec['marker-column'];
  var marker = block_spec['marker'];
  var blank_rows_between_blocks = block_spec['blank-rows-between-blocks'];
  var min_blocks = block_spec['min-blocks'];

  var block_data = ws.getRange(block_range_spec).getValues();
  // identify the blocks by finding the markers, blocks starts at the markers
  var blocks = qa_summary_on_blocks(block_data, block_spec);

  blocks.forEach((block, index) => {
    // the data is in groups, group data is in first column, the other columns are child data
    var block_start_row = block['starts-at'] + header_row_count + 1;
    var block_end_row = block['ends-at'] + header_row_count + 1;
    var data = block_data.slice(block['starts-at'], block['ends-at'] + 1);
    var group_data = data.map(d => d[0]);
    var child_data = data.map(d => d.slice(1));
    var groups = qa_summary_on_group(group_data, child_data);

    // check for gaps between blocks
    if (index < (blocks.length - 1)){
      var row_gaps_with_next_block = blocks[index+1]['starts-at'] - blocks[index]['ends-at'] - 1;
      if (blank_rows_between_blocks != row_gaps_with_next_block){
        let msg = `Blocks should have ${blank_rows_between_blocks} empty row(s) between them, found ${row_gaps_with_next_block} empty row(s) between blocks ${index} and ${index+1}]`;
        logs.push(qa_warn(msg, ws_url, ws_name));
      }
    };

    // the end-index of the last group is the block's end-index
    block['range'] = `B${block_start_row}:D${block_end_row}`;
    Logger.log(` .. block ${index} found at ${block['range']}`)

    groups.forEach((group, index) => {
      var range_a1 = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      Logger.log(` .... ${group['group-name']} found at ${range_a1}`);
    });

    // now do the specific QA checks
    // number of groups
    var groups_expected = 4;
    var group_names_expected = ['Organization', 'Position', 'YYYY-Mon','Job Summary'];
    var group_names_found = groups.map(d => d[0]).join(', ');
    if (groups.length != groups_expected){
      let msg = `Block expected to have ${groups_expected} groups [${group_names_expected}], but has ${groups.length} groups [${group_names_found}]`;
      logs.push(qa_error(msg, ws_url, ws_name, block['range']));
    };

    // ------------------------------------------------------------------------
    // the first group Organization
    if (groups.length > 0){
      var group = groups[0];
      var expected_group_name = 'Organization';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The first group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} name missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the first group Organization
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the second group Position
    if (groups.length > 1){
      var group = groups[1];
      var expected_group_name = 'Position';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The second group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} name missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the second group Position
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the third group Date
    if (groups.length > 2){
      var group = groups[2];
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      var group_name = group['group-name'];

      // the group name must be a valid data
      if (isNaN(Date.parse(group_name))){
        let msg = `The third group must be a valid date, found ${group_name}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let group_data_found = group['data-summary'].length;
      let min_data_rows_expected = 1;
      if (min_data_rows_expected > group_data_found){
        let msg = `Group ${group_name} : At least ${min_data_rows_expected} expected, found ${group_data_found} child entries`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // if the row is blank
        if (data_row['is-row-blank'] == true){
            let msg = `NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (data_row['blank-col-count'] > 0){
            let msg = `some columns are missing values`;
            logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
          };
        };
      });
    };
    // the third group Date
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the fourth group Job Summary
    if (groups.length > 3){
      var group = groups[3];
      var expected_group_name = 'Job Summary';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      var group_name = group['group-name'];
      if (group_name != expected_group_name){
        let msg = `The fourth group must be ${expected_group_name}, found ${group_name}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let group_data_found = group['data-summary'].length;
      let min_data_rows_expected = 10;
      if (min_data_rows_expected > group_data_found){
        let msg = `Group ${group_name} : At least ${min_data_rows_expected} expected, found ${group_data_found} child entries`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // if the row is blank
        if (data_row['is-row-blank'] == true){
            let msg = `NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (data_row['blank-col-count'] > 0){
            let msg = `some columns are missing values`;
            logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
          };
        };
      });
    };
    // the fourth group Job Summary
    // ------------------------------------------------------------------------
  });

  return logs;
};


// check 07-project-roles worksheet
function check_07_project_roles_worksheet(ss){
  var ws_name = '07-project-roles';
  var logs = [];
  var ss_url = ss.getUrl();
  var ws = ss.getSheetByName(ws_name);

  if (ws == null){
    let msg = `worksheet ${ws_name} not found`;
    logs.push(qa_error(msg, ss_url));
    return logs;
  }

  // no point in going forward if column count does not match
  if (ws.getMaxColumns() != RESUME_WS_QA['worksheets'][ws_name]['column-count']){
    return logs;
  }

  var ws_url = `${ss_url}#gid=${ws.getSheetId()}`;

  if (!('block-data' in RESUME_WS_QA['worksheets'][ws_name])){
    return logs;
  };

  var block_spec = RESUME_WS_QA['worksheets'][ws_name]['block-data'];
  var block_range_spec = block_spec['block-range-spec'];
  var header_row_count = block_spec['header-rows'];
  var marker_column = block_spec['marker-column'];
  var marker = block_spec['marker'];
  var blank_rows_between_blocks = block_spec['blank-rows-between-blocks'];
  var min_blocks = block_spec['min-blocks'];

  var block_data = ws.getRange(block_range_spec).getValues();
  var blocks = qa_summary_on_blocks(block_data, block_spec);

  blocks.forEach((block, index) => {
    // the data is in groups, group data is in first column, the other columns are child data
    var block_start_row = block['starts-at'] + header_row_count + 1;
    var block_end_row = block['ends-at'] + header_row_count + 1;
    var data = block_data.slice(block['starts-at'], block['ends-at'] + 1);
    var group_data = data.map(d => d[0]);
    var child_data = data.map(d => d.slice(1));
    var groups = qa_summary_on_group(group_data, child_data);

    // check for gaps between blocks
    if (index < (blocks.length - 1)){
      var row_gaps_with_next_block = blocks[index+1]['starts-at'] - blocks[index]['ends-at'] - 1;
      if (blank_rows_between_blocks != row_gaps_with_next_block){
        let msg = `Blocks should have ${blank_rows_between_blocks} empty row(s) between them, found ${row_gaps_with_next_block} empty row(s) between blocks ${index} and ${index+1}]`;
        logs.push(qa_warn(msg, ws_url, ws_name));
      }
    };

    // the end-index of the last group is the block's end-index
    block['range'] = `B${block_start_row}:D${block_end_row}`;
    Logger.log(` .. block ${index} found at ${block['range']}`)

    groups.forEach((group, index) => {
      var range_a1 = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      Logger.log(` .... ${group['group-name']} found at ${range_a1}`);
    });

    // now do the specific QA checks
    // number of groups
    var groups_expected = 6;
    var group_names_expected = ['Project/Product', 'Client', 'YYYY-Mon', 'Project Brief', 'Role(s) Performed', 'Activities/Tasks Performed'];
    var group_names_found = groups.map(d => d[0]).join(', ');
    if (groups.length != groups_expected){
      let msg = `Block expected to have ${groups_expected} groups [${group_names_expected}], but has ${groups.length} groups [${group_names_found}]`;
      logs.push(qa_error(msg, ws_url, ws_name, block['range']));
    };

    // ------------------------------------------------------------------------
    // the first group Project/Product
    if (groups.length > 0){
      var group = groups[0];
      var expected_group_name = 'Project/Product';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The first group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} name missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the first group Project/Product
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the second group Client
    if (groups.length > 1){
      var group = groups[1];
      var expected_group_name = 'Client';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The second group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} name missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the second group Client
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the third group Date
    if (groups.length > 2){
      var group = groups[2];
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      var group_name = group['group-name'];

      // the group name must be a valid data
      if (isNaN(Date.parse(group_name))){
        let msg = `The third group must be a valid date, found ${group_name}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let group_data_found = group['data-summary'].length;
      let min_data_rows_expected = 1;
      if (min_data_rows_expected > group_data_found){
        let msg = `Group ${group_name} : At least ${min_data_rows_expected} expected, found ${group_data_found} child entries`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // if the row is blank
        if (data_row['is-row-blank'] == true){
            let msg = `NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (data_row['blank-col-count'] > 0){
            let msg = `some columns are missing values`;
            logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
          };
        };
      });
    };
    // the third group Date
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the fourth group Project Brief
    if (groups.length > 3){
      var group = groups[3];
      var expected_group_name = 'Project Brief';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The fourth group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the fourth group Project Brief
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the fifth group Role(s) Performed
    if (groups.length >= 4){
      var group = groups[4];
      var expected_group_name = 'Role(s) Performed';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      if (group['group-name'] != expected_group_name){
        let msg = `The fifth group must be ${expected_group_name}, found ${group['group-name']}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // first data column can not be blank
        if (data_row['data'][0] == ''){
          let msg = `${expected_group_name} missing`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        };
      });
    };
    // the fifth group Role(s) Performed
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // the sixth group Activities/Tasks Performed
    if (groups.length >= 5){
      var group = groups[5];
      var expected_group_name = 'Activities/Tasks Performed';
      var group_range = `B${block_start_row + group['starts-at']}:D${block_start_row + group['ends-at']}`;
      var group_name = group['group-name'];
      if (group_name != expected_group_name){
        let msg = `The sixth group must be ${expected_group_name}, found ${group_name}`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let group_data_found = group['data-summary'].length;
      let min_data_rows_expected = 10;
      if (min_data_rows_expected > group_data_found){
        let msg = `Group ${group_name} : At least ${min_data_rows_expected} expected, found ${group_data_found} child entries`;
        logs.push(qa_error(msg, ws_url, ws_name, group_range));
      };

      let data_rows_found = 0;
      group['data-summary'].forEach((data_row, data_row_index) => {
        let row_num = block_start_row + group['starts-at'] + data_row_index;

        // if the row is blank
        if (data_row['is-row-blank'] == true){
            let msg = `NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (data_row['blank-col-count'] > 0){
            let msg = `some columns are missing values`;
            logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
          };
        };
      });
    };
    // the sixth group Activities/Tasks Performed
    // ------------------------------------------------------------------------
  });

  return logs;
};


// check resume spreadsheet
function check_resume_spreadsheet(ss){
  var logs = [];
  var ss_url = ss.getUrl();

  // check if the ss has min number of worksheets required
  var min_num_of_worksheets = Object.keys(RESUME_WS_QA['worksheets']).length;
  if (ss.getNumSheets() < min_num_of_worksheets){
    let msg = `spreadsheet ${ss.getName()} should have at least ${min_num_of_worksheets} worksheets, but actually has ${ss.getNumSheets()} worksheets`;
    logs.push(qa_error(msg, ss_url));
  } else {
    let msg = `spreadsheet ${ss.getName()} has ${ss.getNumSheets()} worksheets satisfying the min ${min_num_of_worksheets} worksheets requirement`;
    logs.push(qa_none(msg, ss_url));
  }

  // now check each worksheet
  for (const [ws_name, ws_spec] of Object.entries(RESUME_WS_QA['worksheets'])) {
    Logger.log(`.... checking ${ws_name}`);
    var ws = ss.getSheetByName(ws_name);
    if (ws == null){
      let msg = `worksheet ${ws_name} not found`;
      logs.push(qa_error(msg, ss_url));
      continue;
    }

    var ws_url = `${ss_url}#gid=${ws.getSheetId()}`;

    // check whether column count is as specified or not
    if ('num-columns' in ws_spec){
      Logger.log(`...... checking for num-columns`);
      if (ws_spec['num-columns'] != ws.getMaxColumns()){
        let msg = `${ws_spec['num-columns']} required, but found ${ws.getMaxColumns()} columns`;
        logs.push(qa_error(msg, ws_url, ws_name));

        // if column cound does not match, we do not do further QA on this worksheet
        continue;
      };
    };

    // check whether row count is as specified or not
    if ('num-rows' in ws_spec){
      Logger.log(`...... checking for num-rows`);
      if (ws_spec['num-rows'] != ws.getMaxRows()){
        let msg = `${ws_spec['mum-rows']} required, but found ${ws.getMaxRows()} rows`;
        logs.push(qa_error(msg, ws_url, ws_name));
      };
    };

    // check for cells that should not be blank
    if ('error-on-blank' in ws_spec){
      Logger.log(`...... checking for error-on-blank`);
      for (const [cell_a1, error] of Object.entries(ws_spec['error-on-blank'])){
        let cell = ws.getRange(cell_a1);
        if (cell == null){
          let msg = `Cell NOT FOUND`;
          logs.push(qa_error(msg, ws_url, ws_name, cell_a1));
          continue;
        };

        // if the cell is blank
        if (ws.getRange(cell_a1).getValue() == ''){
          let msg = `${error}`;
          logs.push(qa_error(msg, ws_url, ws_name, cell_a1));
        };
      };
    };

    // check for data row existence
    if ('data-rows' in ws_spec){
      Logger.log(`...... checking for data-rows`);
      let data_row_spec = ws_spec['data-rows'];
      let header_row_count = data_row_spec['header-rows'];
      let data_rows_expected = data_row_spec['min-entries'];
      let data_qa_summary = qa_summary_on_data(ws.getRange(data_row_spec['range-spec']).getValues());

      let data_rows_found = 0;
      data_qa_summary.forEach((row, row_index) =>{
        let row_num = row_index + header_row_count + 1;

        // if the row is blank
        if (row[0] == true){
            let msg = `NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (row[1] > 0){
            let msg = `some columns are missing values`;
            logs.push(qa_warn(msg, ws_url, ws_name, `Row ${row_num}`));
          };
        };
      });

      if (data_rows_expected > data_rows_found){
        let msg = `At least ${data_rows_expected} expected, found ${data_rows_found} data entries`;
        logs.push(qa_error(msg, ws_url, ws_name));
      };
    };


    // check for grouped data (parent-child)
    if ('grouped-data' in ws_spec){
      Logger.log(`...... checking for grouped-data`);
      let grouped_data_spec = ws_spec['grouped-data'];
      let header_row_count = grouped_data_spec['header-rows'];

      let group_range_spec = grouped_data_spec['group-range-spec'];
      let min_groups_expected = grouped_data_spec['min-groups'];

      let data_range_spec = grouped_data_spec['data-range-spec'];
      let min_data_rows_expected = grouped_data_spec['min-data-rows'];

      let group_qa_summary = qa_summary_on_group(ws.getRange(group_range_spec).getValues(), ws.getRange(data_range_spec).getValues());
      // Logger.log(group_qa_summary);

      let groups_found = group_qa_summary.length;
      if (min_groups_expected > groups_found){
        let msg = `At least ${min_groups_expected} expected, found ${groups_found} groups`;
        logs.push(qa_error(msg, ws_url, ws_name));
      };

      group_qa_summary.forEach((group, group_index) => {
        let group_name = group['group-name'];
        let group_data_found = group['data-summary'].length;

        if (min_data_rows_expected > group_data_found){
          let msg = `Group ${group_name} : At least ${min_data_rows_expected} expected, found ${group_data_found} child entries`;
          logs.push(qa_warn(msg, ws_url, ws_name));
        };

        let data_rows_found = 0;
        group['data-summary'].forEach((data_row, data_row_index) => {
          let row_num = group['starts-at'] + data_row_index + header_row_count + 1;

          // if the row is blank
          if (data_row['is-row-blank'] == true){
              let msg = `NO DATA`;
            logs.push(qa_error(msg, ws_url, ws_name, `Row ${row_num}`));
          } else {
            data_rows_found++;

            // if one or more column is blank
            if (data_row['blank-col-count'] > 0){
              let msg = `some columns are missing values`;
              logs.push(qa_warn(msg, ws_url, ws_name, `Row ${row_num}`));
            };
          };
        });
      });
    };

  };

  return logs;
};
