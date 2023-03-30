LETTER_TO_COLUMN = {
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
};


COLUMN_TO_LETTER = ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];


// ="Résumé__"&de_space(C57)
function de_space(text){
  var without_space = text.replace(/\s+/g, '.').replace(/[.][.]+/g, '.');
  return without_space;
};


function photo_link_from_name(name){
  // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/photo/photo__Khandakar.Asif.Hasan.png", 3)
  var name_without_space = de_space(name);
  var link = `=image("https://spectrum-bd.biz/data/artifacts/photo/photo__${name_without_space}.png", 3)`;
  return link;
};


function signature_link_from_name(name){
  // this is the link we need =image("https://spectrum-bd.biz/data/artifacts/signature/signature__Khandakar.Asif.Hasan.png", 3)
  var name_without_space = de_space(name);
  var link = `=image("https://spectrum-bd.biz/data/signature/artifacts/signature__${name_without_space}.png", 3)`;
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
  if (range.getHeight() === 1 && range.getWidth() === 1){
    merge = false;
  };

  if (merge === true){
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

  // number-format
  if ('format' in work_spec){
    range.setNumberFormat(work_spec['format']);
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
    range.setBorder(true, true, true, true, false, false, work_spec['border-color'], SpreadsheetApp.BorderStyle.SOLID);
  };

  // wrap
  if ('wrap' in work_spec){
    if (work_spec['wrap'] === true) {
      range.setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
    } else {
      range.setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
    }
  };

  // worksheet links
  if ('ws-name-to-link' in work_spec){
    link_cell_to_worksheet(ss, range, work_spec['ws-name-to-link'])
  };

  // note
  if ('note' in work_spec){
    range.setNote(work_spec['note']);
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


// find and replace text within a sheet
function search_replace_texts(ss, serach_for, replace_with){
  var tf = ss.createTextFinder(serach_for);
  tf.matchCase(true);
  tf.matchEntireCell(false);
  tf.ignoreDiacritics(true);
  tf.matchFormulaText(true);

  tf.replaceAllWith(replace_with);
};


// split text into lines and remove spaces and any special character from the begining
function split_and_dress(value) {
  var lines = value.split('\n');
  const regex = /^[-\s•]+/;
  lines = lines.map(s => s.replace(regex, ''));

  return lines;
};


// if the value is a number return a quoted value by prepending a ' before, for string and valid dates return as it is
function quote_number(value) {
  if (!isNaN(value)) {
    // it still can be a date, HACK - if it is date it is a very big number
    if (value > 100000) {
      // Logger.log(`from : Date : ${value}`);
      var val = value;

    } else {
      // Logger.log(`from : Num  : ${value}`);
      var val = `'${value}`;
    };

  } else {
    // Logger.log(`from : NaN  : ${value}`);
    var val = value;

  };

  return val;
};
