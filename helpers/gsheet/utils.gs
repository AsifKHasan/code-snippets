// ="Résumé__"&de_space(C57)
function de_space(text){
  var without_space = text.replace(/\s+/g, '.').replace(/[.][.]+/g, '.');
  return without_space;
};

function photo_link_from_name(name){
  // this is the link we need =image("https://spectrum-bd.biz/data/photo/photo__Khandakar.Asif.Hasan.png", 3)
  var name_without_space = de_space(name);
  var link = `=image("https://spectrum-bd.biz/data/photo/photo__${name_without_space}.png", 3)`;
  return link;
};

function signature_link_from_name(name){
  // this is the link we need =image("https://spectrum-bd.biz/data/signature/signature__Khandakar.Asif.Hasan.png", 3)
  var name_without_space = de_space(name);
  var link = `=image("https://spectrum-bd.biz/data/signature/signature__${name_without_space}.png", 3)`;
  return link;
};

function run_test(){
  var link = signatureLinkFromName('Abdullah-Al-Hossain Bin Sarwar');
  Logger.log(link);
};

// work on a range - merge, value, formula, alignment, bgcolor, border, notes etc.
function work_on_range(ss, range, work_spec){
  // see if the range is to be merged
  var merge = true;
  if ('merge' in work_spec){
    merge = work_spec['merge'];
  };

  // see if it is a single cell or a range
  if (range.getHeight() == 1 || range.getWidth() == 1){
    merge = false;
  };

  if (merge == true){
    if (range.isPartOfMerge() == false){
      range.merge();
    };
  };

  // value
  if ('value' in work_spec){
    range.setValue(work_spec['value']);
  };

  // formula
  if ('formula' in work_spec){
    range.setFormula(work_spec['formula']);
  };

  // halign
  if ('halign' in work_spec){
    range.setHorizontalAlignment(work_spec['halign']);
  };

  // valign
  if ('valign' in work_spec){
    range.setVerticalAlignment(work_spec['valign']);
  };

  // font-family
  if ('font-family' in work_spec){
    range.setFontFamily(work_spec['font-family']);
  };

  // font-size
  if ('font-size' in work_spec){
    range.setFontSize(work_spec['font-size']);
  };

  // weight
  if ('weight' in work_spec){
    range.setFontWeight(work_spec['weight']);
  };

  // bgcolor
  if ('bgcolor' in work_spec){
    range.setBackground(work_spec['bgcolor']);
  };

  // border-color
  if ('border-color' in work_spec){
    range.setBorder(true, true, true, true, true, true, work_spec['border-color'], SpreadsheetApp.BorderStyle.SOLID);
  };

  // ws-link
  if ('ws-link' in work_spec){
    link_cell_to_worksheet(ss, range, work_spec['ws-link'])
  };

  // notes
  if ('notes' in work_spec){
    range.setNote(work_spec['notes']);
  };

};

function show_html() {
  var t = HtmlService.createTemplateFromFile('index');
  t.data = list_worksheets();
  t.evaluate();
  var ui = SpreadsheetApp.getUi();
  ui.showSidebar(t);
};


function row_of_matching_value(ws, column, value){
  var data = ws.getDataRange().getValues();
  for (var i = 0; i < data.length; i++) {
    if (data[i][column - 1] == value) {
      return i + 1;
    }
  }

  return -1;
};

// return a QA summary on data which is a two dimesional array of rows and columns
// output is an array of rows containing array [is_row_blank, blank_col_count]
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

    data_qa_summary.push([is_row_blank, blank_col_count]);
  });

  return data_qa_summary;
};
