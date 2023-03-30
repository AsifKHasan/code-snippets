LAYOUT_NBR_BSW_WS_SPECS = {
  'num-columns': 7,
  'columns': {'B': 150, 'C': 350, 'D': 50, 'E': 100, 'F': 50, 'G': 100, },
  'ranges': {
    'A1': {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'halign': 'center'},
    // 'B2:G2': {'value': 'content', 'weight': 'bold'},

    // 'B21': {'note': '{"content": "out-of-cell"}'},
    // 'B22': {'note': '{"keep-with-next": true}'},
    'B23': {'value': '05-technical-expertise', 'ws-name-to-link': '05-technical-expertise', 'note': '{"content": "out-of-cell"}'},

    // 'B25': {'note': '{"keep-with-next": true}'},
    'B26': {'value': '09-certification', 'ws-name-to-link': '09-certification', 'note': '{"content": "out-of-cell"}'},

    // 'B28': {'note': '{"keep-with-next": true}'},
    'B29': {'value': '08-training', 'ws-name-to-link': '08-training', 'note': '{"content": "out-of-cell"}'},

    // 'B31': {'note': '{"keep-with-next": true}'},
    'B32': {'value': '07-project-roles', 'ws-name-to-link': '07-project-roles', 'note': '{"content": "out-of-cell"}'},

    // // Name of Local Representative
    // 'B3:C3': {'value': 'Name of Local Representative', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'left', 'border-color': '#b7b7b7'},
    // 'D3:G3': {'value': 'Spectrum Engineering Consortium Ltd.', 'halign': 'left', 'border-color': '#b7b7b7'},

    // // Name of Employer
    // 'C12': {'value': 'Spectrum Engineering Consortium Ltd.'},

    // // Address of Employer
    // 'C14': {'value': '69/1 Panthapath, Chandrashila Suvastu Tower, 7th Floor, Suite C, DHaka-1205'},

    // // Telephone
    // 'C16': {'value': '+880 96 3863 3633'},

    // // Contact (manager / personnel officer)
    // 'D16': {'value': 'Sayeda Fatema Ferdousi, Assistant Manager, HR'},

    // // Fax
    // 'C18': {'value': '+880 2 9671370'},

    // // Email
    // 'D18': {'value': 'contacts@spectrum-bd.com'},


    // // blank row
    // 'B4:G4': {},

  },

  'cell-empty-markers': [
    'D3:G3',
    'B6:C6',
    'C9',
    'D9:G9',
    'C12:G12',
    'C14:G14',
    'C16',
    'D16:G16',
    'C18',
    'D18:G18',
    'C20',
    'D20:G20',
  ],
};

// update *00-layout_nbr_bsw* worksheet
function update_00_layout_nbr_bsw_worksheet(ss_name=undefined){
  if (ss_name == undefined){
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  } else {
    var ss = open_spreadsheet(ss_name);
  };

  if (ss != null){
    var ws_name = '00-layout-NBR-BSW';
    var ws = ss.getSheetByName(ws_name);
    if (ws != null){
      // check if the worksheet has enough rows having content
      var min_rows_that_must_have_content = 32;
      var rows_with_content = ws.getLastRow();
      if(rows_with_content < min_rows_that_must_have_content){
        Logger.log(`Worksheet ${ws_name} should have at least ${min_rows_that_must_have_content} rows with content, but actually only ${rows_with_content} rows have content`);
        return;
      }

      // iterate over ranges and apply specs
      for (const [key, value] of Object.entries(LAYOUT_NBR_BSW_WS_SPECS['ranges'])) {
        var range = ws.getRange(key);
        if (range === null){
          Logger.log(`ERROR: Range ${key} not found`);
          continue;
        } else {
          Logger.log(`.. Range ${key} found`);
          work_on_range(ss=ss, range=range, work_spec=value);
        }
      };

      if (false) {
        // clear conditional formatting
        ws.clearConditionalFormatRules();

        var total_rows = ws.getMaxRows();
        var total_columns = ws.getMaxColumns();

        // conditional formats
        range = ws.getRange(3, 1, total_rows - 2, total_columns);

        // conditional formatting
        add_conditional_formatting_for_blank_cells(ws, LAYOUT_NBR_BSW_WS_SPECS['cell-empty-markers']);

        // review-notes
        var rules = ws.getConditionalFormatRules();
        var rule = SpreadsheetApp.newConditionalFormatRule()
          .setRanges([range])
          .whenFormulaSatisfied("=not(isblank($A:$A))")
          .setBackground('#f4cccc')
          .build();
        rules.push(rule);

        ws.setConditionalFormatRules(rules);
      };

    } else {
      Logger.log(`.. ERROR: worksheet ${ws_name} not found`);
    }
  };
};
