// return a QA summary on a group data (parent data) and row data (child data)
// output is an array of objects that looks like {'group-name': 'string', 'starts-at': int, 'ends-at': int, 'data-summary': [{'is-row-blank': bool, 'blank-col-count': int, 'data': []}]}
function qa_summary_on_group(group_data, child_data){
  let group_qa_summary = [];

  // first we identify each group from group_data and row ranges for each of them
  // we assume that the first element of the group_data values contains the group name and if it is blank, it is a continuation of the running group
  let running_group_name = '';
  let running_group_start_index = 0;
  let running_group_end_index = 0;
  group_data.forEach((row, row_index) => {
    let group_name_found = row;
    if (row_index == 0){
      running_group_name = group_name_found;
    };

    if (group_name_found != '' && group_name_found != running_group_name){
      // we have got a new group, close the running group
      group_qa_summary.push({'group-name': running_group_name, 'starts-at': running_group_start_index, 'ends-at': running_group_end_index});

      running_group_name = group_name_found;
      running_group_start_index = row_index;
    };

    running_group_end_index = row_index;
  });

  // the last group
  group_qa_summary.push({'group-name': running_group_name, 'starts-at': running_group_start_index, 'ends-at': running_group_end_index});

  // now for each group summarize the child data
  group_qa_summary.forEach((group, index) => {
    let data_start_index = group['starts-at'];
    let data_end_index = group['ends-at'];
    let group_data = child_data.slice(data_start_index, data_end_index + 1);
    let data_qa_summary = qa_summary_on_data(group_data);
    group['data-summary'] = data_qa_summary;
  });

  return group_qa_summary;
};


// return a QA summary on data organized as blocks
// output is an array of objects that looks like {'marker': 'string', 'starts-at': int, 'ends-at': int}
function qa_summary_on_blocks(block_data, block_spec){
  var marker = block_spec['marker'];
  var marker_column = block_spec['marker-column'];
  var blocks = [];
  block_data.forEach((row, index) => {
    // marker to be found in marker-column
    var v = row[marker_column];
    if (v == marker){
      blocks.push({marker: row[1], 'starts-at': index});
    };
  });

  // now we have got the blocks, get further into the blocks
  for (var i = 0 ; i < blocks.length ; i++){
    if (i < (blocks.length - 1)){
      blocks[i]['ends-at'] = blocks[i+1]['starts-at'] - 1;
    } else {
      blocks[i]['ends-at'] = block_data.length - 1;
    };
  };

  // a block ends at the last row having data before the next block
  for (var i = 0; i < blocks.length; i++){
    if (i < (blocks.length - 1)){
      // get the last non-blank data index
      var last_block_row = blocks[i]['ends-at'];
      for (var j = blocks[i]['ends-at']; j >= blocks[i]['starts-at']; j--){
        var is_row_blank = all_elements_empty(block_data[j]);
        if (is_row_blank == false){
          blocks[i]['ends-at'] = j;
          break;
        };
      };
    };
  };

  return blocks;
};


function all_elements_empty(data){
  for (var i = 0; i < data.length; i++){
    if (data[i] != ''){
      return false;
    };
  };

  return true;
};


// return a QA summary on data which is a two dimesional array of rows and columns
// output is an array of objects {'is-row-blank': bool, 'blank-col-count': int, 'data': []}
function qa_summary_on_data(data){
  let data_qa_summary = [];
  data.forEach((row, row_index) => {
    let is_row_blank = true;
    let blank_col_count = 0;
    row.forEach((col, col_index) => {
      if (col == ''){
        blank_col_count++;
      } else {
        is_row_blank = false;
      };
    });

    data_qa_summary.push({'is-row-blank': is_row_blank, 'blank-col-count': blank_col_count, 'data': row});
  });

  return data_qa_summary;
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
    'check_06_job_history_worksheet',
    'check_07_project_roles_worksheet',
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


function qa_error(description, link=null, where=null, location=null){
  return [where, location, 'error', description, link];
};

function qa_warn(description, link=null, where=null, location=null){
  return [where, location, 'warn', description, link];
};

function qa_todo(description, link=null, where=null, location=null){
  return [where, location, 'todo', description, link];
};

function qa_none(description, link=null, where=null, location=null){
  return [where, location, null, description, link];
};
