// do some work on a list of sheets
function work_on_spreadsheets() {
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
        let msg = `${ws_spec['mum-columns']} required, but found ${ws.getMaxColumns()} columns`;
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
          let msg = `Cell ${cell_a1} NOT FOUND`;
          logs.push(qa_error(msg, ws_url, ws_name));
          continue;
        };

        // if the cell is blank
        if (ws.getRange(cell_a1).getValue() == ''){
          let msg = `Cell ${cell_a1} - ${error}`;
          logs.push(qa_error(msg, ws_url, ws_name));
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
            let msg = `Row ${row_num} : NO DATA`;
          logs.push(qa_error(msg, ws_url, ws_name));
        } else {
          data_rows_found++;

          // if one or more column is blank
          if (row[1] > 0){
            let msg = `Row ${row_num} : some coumns are missing values`;
            logs.push(qa_error(msg, ws_url, ws_name));
          };
        };
      });

      if (data_rows_expected > data_rows_found){
        let msg = `At least ${data_rows_expected} expected, found ${data_rows_found} data entries`;
        logs.push(qa_error(msg, ws_url, ws_name));
      };
    };


  };

  return logs;
};


// generate QA report for the resume
function prepare_qa_report(ss_name, qa_report_folder_id){
  var current_time = new Date();
  var qa_report_name = `${ss_name.replace('Résumé__', 'résumé-qa-report__')}__${current_time.toISOString().slice(0, 10)}`;
  var qa_report_template_name = 'résumé-qa-report-template';

  if (ss_name != undefined){
    var ss = open_spreadsheet(ss_name);
  };

  if (ss == null){
    return;
  }
  var qa_logs = [];

  // each qa log is a list {where, location, kind, description}
  // check the sheet and everything and get the logs
  var check_function_name_list = [
    'check_resume_spreadsheet',
  ];

  check_function_name_list.forEach(function(func){
    Logger.log(`.. running .... ${func}`);
    var logs = this[func](ss);
    qa_logs.push(...logs);
    Logger.log(`.. finished ... ${func}`);
  });

  // write qa logs, create the qa-report gsheet first
  var template_ss = get_unique_file_by_name(qa_report_template_name);
  var folder = DriveApp.getFolderById(qa_report_folder_id);
  if (template_ss != null){
    var qa_report_file = create_ss_from_template(qa_report_name, template_ss, folder);
  } else {
    Logger.log(`.. ERROR : QA log template ${qa_report_template_name} could not be opened`);
    return;
  };

  //write the logs in the *resume-qa-report* worksheet
  var qa_report_ss = SpreadsheetApp.open(qa_report_file);
  var ws = qa_report_ss.getSheetByName('resume-qa-report');
  var start_row = 3;
  var num_rows = qa_logs.length;
  var start_col = 2;
  var num_cols = 5;

  // make sure we have enough rows for writing the logs
  if (ws.getMaxRows() < (qa_logs.length + 3)){
    // insert rows after row 3
    var rows_to_insert = (qa_logs.length + 3) - ws.getMaxRows() - 1;
    if (rows_to_insert > 0){
      ws.insertRowsAfter(3, rows_to_insert);
    }
  };

  var range = ws.getRange(start_row, start_col, num_rows, num_cols);
  range.setValues(qa_logs);

  // get error and warning counts
  var error_count = 0;
  var warning_count = 0;
  qa_logs.forEach(function(log){
    if (log[2] == 'error'){
      error_count = error_count + 1;
    };
    if (log[2] == 'warning'){
      warning_count = warning_count + 1;
    };
  });

  Logger.log(`.. QA report ${qa_report_name} prepared`);
  return {'error-count': error_count, 'warning-count': warning_count, 'qa-report-name': qa_report_file};
};
