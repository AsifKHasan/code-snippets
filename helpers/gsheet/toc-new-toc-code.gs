// update *-new-toc* links
function update_new_toc_links(ss=undefined) {
  if(ss == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  }

  var ss_name = ss.getName();

  // get the *-new-toc* worksheet
  var toc_new_ws_name = '-toc-new';
  var toc_new_ws = ss.getSheetByName(toc_new_ws_name);

  // link values in F3:F
  var range = toc_new_ws.getRange('F3:F');
  var values = range.getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      var cell = range.getCell(row_index+1, col_index+1);
      link_cell_to_worksheet(ss, cell, col)
    });
  });

  // link values in O3:O
  var range = toc_new_ws.getRange('O3:O');
  var values = range.getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      var cell = range.getCell(row_index+1, col_index+1);
      var val = col;
      // if (val === ''){
      //   val = 'z-header';
      //   cell.setValue(val);
      // }
      link_cell_to_worksheet(ss, cell, val);
    });
  });

  // link values in R3:R
  var range = toc_new_ws.getRange('R3:R');
  var values = range.getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      var cell = range.getCell(row_index+1, col_index+1);
      var val = col;
      // if (val === ''){
      //   val = 'z-footer';
      //   cell.setValue(val);
      // }
      link_cell_to_worksheet(ss, cell, val);
    });
  });

};


// update *-new-toc*
function update_new_toc(ss=undefined) {
  if(ss == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  }

  var ss_name = ss.getName();

  // get the *-new-toc* worksheet
  var toc_new_ws_name = '-toc-new';
  var toc_new_ws = ss.getSheetByName(toc_new_ws_name);

  // unhide all columns
  var range = toc_new_ws.getRange("A1:X");
  toc_new_ws.unhideColumn(range);

  // for each column
  TOC_NEW_DATA.forEach(function(col_data){
    // resize the columns
    toc_new_ws.setColumnWidth(col_data['col'], col_data['size'])

    // change the labels in row 2
    var range_spec = `${col_data['col_a1']}2`;
    toc_new_ws.getRange(range_spec).setValue(col_data['label']);

    // set vertical alignments and wrapping
    var range_spec = `${col_data['col_a1']}1:${col_data['col_a1']}`;
    toc_new_ws.getRange(range_spec).setHorizontalAlignment(col_data['halign']).setWrap(false);

    // set validation rules
    if ('validation-list' in col_data){
        var validation_rule = SpreadsheetApp.newDataValidation().requireValueInList(col_data['validation-list']).build();
        var range_spec = `${col_data['col_a1']}3:${col_data['col_a1']}`;
        toc_new_ws.getRange(range_spec).setDataValidation(validation_rule);
    }

  });

};


// create worksheet *-new-toc* from *-toc* worksheet
function new_toc_from_toc(ss=undefined) {
  if(ss == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  }

  var ss_name = ss.getName();

  // duplicate the *-toc* as *-new-toc* worksheet
  var toc_ws_name = '-toc';

  // do some necessary work on -toc worksheet
  var toc_ws = ss.getSheetByName(toc_ws_name);

  // unhide all columns
  var range = toc_ws.getRange("A1:T");
  toc_ws.unhideColumn(range);

  // if there are 20 columns in -toc, insert two columns at position 16 (override-header and override-footer)
  if (toc_ws.getMaxColumns() === 20){
    toc_ws.insertColumns(17, 2);
  }

  var toc_new_ws_name = '-toc-new';
  var toc_new_ws = duplicate_worksheet(ss, toc_ws_name, toc_new_ws_name);

  if (toc_new_ws === null){
    return;
  }

  // add 3 new columns after G - 'landscape', 'page-spec', 'margin-spec'. Column G we will use for 'break'
  toc_new_ws.insertColumns(8, 3);

  // for each column
  TOC_NEW_DATA.forEach(function(col_data){
    // resize the columns
    toc_new_ws.setColumnWidth(col_data['col'], col_data['size'])

    // change the labels in row 2
    var range_spec = `${col_data['col_a1']}2`;
    toc_new_ws.getRange(range_spec).setValue(col_data['label']);

    // set vertical alignments and wrapping
    var range_spec = `${col_data['col_a1']}1:${col_data['col_a1']}`;
    toc_new_ws.getRange(range_spec).setHorizontalAlignment(col_data['halign']).setWrap(false);

    // set validation rules
    if ('validation-list' in col_data){
        var validation_rule = SpreadsheetApp.newDataValidation().requireValueInList(col_data['validation-list']).build();
        var range_spec = `${col_data['col_a1']}3:${col_data['col_a1']}`;
        toc_new_ws.getRange(range_spec).setDataValidation(validation_rule);
    }

  });

  // for column C (process) (range C3:C), change values to blank if it is -
  var range_spec = 'C3:C';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column K (hide-pageno) (range K3:K), change values to Yes if it is No
  var range_spec = 'K3:K';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === 'No') {
        values[row_index][col_index] = 'Yes';
      }

      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column L (hide-heading) (range L3:L), change values to blank if it is -
  var range_spec = 'L3:L';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column M (different-firstpage) (range M3:M), change values to blank if it is -
  var range_spec = 'M3:M';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column T (override-header) (range T3:T), change values to blank if it is -
  var range_spec = 'T3:T';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column U (override-footer) (range U3:U), change values to blank if it is -
  var range_spec = 'U3:U';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      if(col === '-') {
        values[row_index][col_index] = '';
      }
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column J (margin-spec) (range J3:J), change values to narrow
  var range_spec = 'J3:J';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      values[row_index][col_index] = 'narrow';
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column I (page-spec) (range I3:I), change values to A4
  var range_spec = 'I3:I';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    row.forEach((col, col_index) => {
      values[row_index][col_index] = 'A4';
    });
  });
  toc_new_ws.getRange(range_spec).setValues(values);

  // for column H (landscape) (range H3:H), change values to Yes if column G contains landscape
  // for column G (break) (range G3:G), change values to blank if it is -, change to section if it contains newpage
  var range_spec = 'G3:H';
  var values = toc_new_ws.getRange(range_spec).getValues();
  values.forEach((row, row_index) => {
    if (row[0].endsWith('_landscape')){
      values[row_index][1] = 'Yes';
    }

    if (row[0] === '-'){
      values[row_index][0] = '';
    }

    if (row[0].startsWith('newpage_')){
      values[row_index][0] = 'section';
    }

    if (row[0].startsWith('continuous_')){
      values[row_index][0] = '';
    }
  });
  toc_new_ws.getRange(range_spec).setValues(values);

};

TOC_NEW_DATA = [
  {'col':  1, 'col_a1': 'A', 'halign': 'center', 'size':  60, 'label': 'section'            , },
  {'col':  2, 'col_a1': 'B', 'halign': 'left',   'size': 200, 'label': 'heading'            , },
  {'col':  3, 'col_a1': 'C', 'halign': 'center', 'size':  80, 'label': 'process'            , 'validation-list': ['Yes']},
  {'col':  4, 'col_a1': 'D', 'halign': 'center', 'size':  80, 'label': 'level'              , 'validation-list': [0, 1, 2, 3, 4, 5, 6]},
  {'col':  5, 'col_a1': 'E', 'halign': 'center', 'size':  80, 'label': 'content-type'       , 'validation-list': ['docx', 'gsheet', 'lof', 'lot', 'pdf', 'table', 'toc']},
  {'col':  6, 'col_a1': 'F', 'halign': 'left',   'size': 200, 'label': 'link'               , },
  {'col':  7, 'col_a1': 'G', 'halign': 'center', 'size':  80, 'label': 'break'              , 'validation-list': ['page', 'section']},
  {'col':  8, 'col_a1': 'H', 'halign': 'center', 'size':  80, 'label': 'landscape'          , 'validation-list': ['Yes']},
  {'col':  9, 'col_a1': 'I', 'halign': 'center', 'size':  80, 'label': 'page-spec'          , 'validation-list': ['A4', 'A3', 'Letter', 'Legal']},
  {'col': 10, 'col_a1': 'J', 'halign': 'center', 'size':  80, 'label': 'margin-spec'        , 'validation-list': ['wide', 'medium', 'narrow', 'none']},
  {'col': 11, 'col_a1': 'K', 'halign': 'center', 'size':  80, 'label': 'hide-pageno'        , 'validation-list': ['Yes']},
  {'col': 12, 'col_a1': 'L', 'halign': 'center', 'size':  80, 'label': 'hide-heading'       , 'validation-list': ['Yes']},
  {'col': 13, 'col_a1': 'M', 'halign': 'center', 'size':  80, 'label': 'different-firstpage', 'validation-list': ['Yes']},
  {'col': 14, 'col_a1': 'N', 'halign': 'left',   'size':  80, 'label': 'header-first'       , },
  {'col': 15, 'col_a1': 'O', 'halign': 'left',   'size':  80, 'label': 'header-odd'         , },
  {'col': 16, 'col_a1': 'P', 'halign': 'left',   'size':  80, 'label': 'header-even'        , },
  {'col': 17, 'col_a1': 'Q', 'halign': 'left',   'size':  80, 'label': 'footer-first'       , },
  {'col': 18, 'col_a1': 'R', 'halign': 'left',   'size':  80, 'label': 'footer-odd'         , },
  {'col': 19, 'col_a1': 'S', 'halign': 'left',   'size':  80, 'label': 'footer-even'        , },
  {'col': 20, 'col_a1': 'T', 'halign': 'center', 'size':  80, 'label': 'override-header'    , 'validation-list': ['Yes']},
  {'col': 21, 'col_a1': 'U', 'halign': 'center', 'size':  80, 'label': 'override-footer'    , 'validation-list': ['Yes']},
  {'col': 22, 'col_a1': 'V', 'halign': 'left',   'size':  80, 'label': 'responsible'        , },
  {'col': 23, 'col_a1': 'W', 'halign': 'left',   'size':  80, 'label': 'reviewer'           , },
  {'col': 24, 'col_a1': 'X', 'halign': 'left',   'size': 160, 'label': 'status'             , 'validation-list': ['pending', 'under-documentation', 'ready-for-review', 'under-review', 'finalized']},
];
