// snippets for *work_on_spreadsheets*
// ------------------------------------------------------------
// RENAMING WORKSHEETS - BEGIN
// rename_worksheets(ss, WORKSHEET_NAME_MAP1);
// rename_worksheets(ss, WORKSHEET_NAME_MAP2);
// RENAMING WORKSHEETS - END
//
// SPECIFIC to *00-layout* WORKSHEET - BEGIN
// create_00_layout_worksheet(ss);
// update_00_layout_worksheet_links(ss);
// update_00_layout_worksheet_content(ss);
// update_00_layout_worksheet_photo(ss, ss_org);
// update_00_layout_worksheet_signature(ss, ss_org);
// SPECIFIC to *00-layout* WORKSHEET - END
//
// ALL WORKSHEET FORMATTING - BEGIN
// update_all_worksheets(ss);
// ALL WORKSHEET FORMATTING - END
//
// RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - BEGIN
// resize_columns_in_worksheets(ss, RESUME_WS_SPECS);
// write_column_size_in_worksheets(ss);
// order_worksheets(ss);
// RESIZE WORKSHEET COLUMNS, ORDER WORKSHEETS - END
//
// SPECIFIC to *01-personal* WORKSHEET - BEGIN
// update_01_personal_worksheet_photo(ss, ss_org);
// SPECIFIC to *01-personal* WORKSHEET - END
//
// CREATE SHEETS FROM TEMPLATE - BEGIN
// create_ss_from_template(ss, template_ss, blank_resume_folder);
// CREATE SHEETS FROM TEMPLATE - END
//


// returns a list of ss_data (spreadsheet name + null + an int (1))
function get_spreadsheets_to_work_on(){
  var ss_data_to_work_on = [

    ['pds__BCC-DC', null, 1],
    ['pds__BCC-DC-Expansion', null, 1],
    ['pds__BR-DCDR', null, 1],
    ['pds__NBR-ASYCUDA', null, 1],
    ['pds__BSCCL', null, 1],
    ['pds__BSCCL_KUAKATA', null, 1],
    ['pds__BDREN-DC-Expansion', null, 1],
    ['pds__DSHE-DC', null, 1],
    ['pds__ICBISL', null, 1],
    ['pds__IFIC-DC', null, 1],
    ['pds__MTBL-EBNCDC', null, 1],
    ['pds__NBR-ASYCUDA-SLA', null, 1],
    ['pds__iBAS', null, 1],
    ['pds__BPA-Sardha-Police-Academy', null, 1],
    ['pds__InterCon', null, 1],
    ['pds__BCC-AMC', null, 1],
    ['pds__BCC-AMC-2020', null, 1],
    ['pds__DBBL-DC-tvnl', null, 1],
    ['pds__DBL-LAN-tvnl', null, 1],
    ['pds__EBL-DC-tvnl', null, 1],
    ['pds__Ship-Aichi-DC-tvnl', null, 1],
    ['pds__STSCTG-DC-tvnl', null, 1],
    ['pds__UCBL-DC-tvnl', null, 1],
    ['pds__RHD-BDMS', null, 1],
    ['pds__OCAG-AMMS', null, 1],
    ['pds__UGC-HEMIS', null, 1],
    ['pds__CCC-CSSM', null, 1],
    ['pds__OAGN-NAMS', null, 1],
    ['pds__BB-RTGS', null, 1],
    ['pds__RHD-MIS-consultancy', null, 1],
    ['pds__RHD-MIS-2015', null, 1],
    ['pds__NBR-ASYCUDA-SLA', null, 1],
    ['pds__NBR-ASYCUDA', null, 1],
    ['pds__BCC-CA', null, 1],
    ['pds__ROBI-ROC', null, 1],
    ['pds__SCB-CBRM', null, 1],
    // ['pds__DSHE-DC', null, 1],
    // ['pds__iBAS', null, 1],
    // ['pds__InterCon', null, 1],
    // ['pds__BCC-AMC-2020', null, 1],
    // ['pds__DBBL-DC-UPS-Installation', null, 1],
    // ['pds__DBL-DC-Passive ', null, 1],
    // ['pds__EBL-DC-Setup', null, 1],
    // ['pds__Ship-Aichi-DC', null, 1],
    // ['pds__STS-CTG-DC', null, 1],
    // ['pds__UCBL-DC', null, 1],

    // ['spectrum__pds-index', null, 1],
    // ['pds__blank.template', null, 1],
    // ['pds__ACMELL', null, 1],
    // ['pds__BB-RTGS', null, 1],
    // ['pds__BBA-BPBB', null, 1],
    // ['pds__BCC-AMC', null, 1],
    // ['pds__BCC-Cisco-Renewal', null, 1],
    // ['pds__BCC-DC-Expansion', null, 1],
    // ['pds__BCC-DC', null, 1],
    // ['pds__BCC-DSCOCP', null, 1],
    // ['pds__BCC-HW-Expansion', null, 1],
    // ['pds__BCC-Tier-IV-ServerStorage', null, 1],
    // ['pds__BCC', null, 1],
    // ['pds__BDREN-DC-Expansion', null, 1],
    // ['pds__BDREN-G-13', null, 1],
    // ['pds__BDREN-Network', null, 1],
    // ['pds__Beximco-IT', null, 1],
    // ['pds__BG(DC)', null, 1],
    // ['pds__BPA-Sardha-Police-Academy', null, 1],
    // ['pds__BR-DCDR', null, 1],
    // ['pds__BRP', null, 1],
    // ['pds__BSCCL-SCISCO', null, 1],
    // ['pds__BSCCL', null, 1],
    // ['pds__BSCCL_KUAKATA', null, 1],
    // ['pds__BTCL-NGNCDR', null, 1],
    // ['pds__BTCL', null, 1],
    // ['pds__BTTB', null, 1],
    // ['pds__BWDB', null, 1],
    // ['pds__CCC-WPSD', null, 1],
    // ['pds__CRM', null, 1],
    // ['pds__DBBL-DWDM', null, 1],
    // ['pds__DISWLS', null, 1],
    // ['pds__DMS_UBL', null, 1],
    // ['pds__DSEL', null, 1],
    // ['pds__DSILW(BAF)', null, 1],
    // ['pds__DVSIVSS', null, 1],
    // ['pds__DWASA', null, 1],
    // ['pds__EMS', null, 1],
    // ['pds__FOLC', null, 1],
    // ['pds__GP_CHQ', null, 1],
    // ['pds__GPIGP', null, 1],
    // ['pds__IBBL', null, 1],
    // ['pds__ICBIBL(DR)', null, 1],
    // ['pds__ICBISL', null, 1],
    // ['pds__IFIC-DC', null, 1],
    // ['pds__IOWM', null, 1],
    // ['pds__ITCL', null, 1],
    // ['pds__ITICB', null, 1],
    // ['pds__ITNA', null, 1],
    // ['pds__IUB', null, 1],
    // ['pds__JU', null, 1],
    // ['pds__JUB', null, 1],
    // ['pds__KTAL', null, 1],
    // ['pds__LBBL', null, 1],
    // ['pds__MCICT-SASECIH', null, 1],
    // ['pds__MOS_ICT', null, 1],
    // ['pds__Mosharaf-Group', null, 1],
    // ['pds__MTBL-CCTV', null, 1],
    // ['pds__MTBL-EBNCDC', null, 1],
    // ['pds__NBR-ASYCUDA-SLA', null, 1],
    // ['pds__NL_DC', null, 1],
    // ['pds__OBL', null, 1],
    // ['pds__PHQ-AMC', null, 1],
    // ['pds__REB', null, 1],
    // ['pds__RHD-MIS-consultancy', null, 1],
    // ['pds__RHD-MIS-e-procurement', null, 1],
    // ['pds__RWGH', null, 1],
    // ['pds__SBFI', null, 1],
    // ['pds__SCB', null, 1],
    // ['pds__SIBL(DC)', null, 1],
    // ['pds__SIBL', null, 1],
    // ['pds__SPARRSO-2010', null, 1],
    // ['pds__SPARRSO-2012', null, 1],
    // ['pds__SSF', null, 1],
    // ['pds__SSVPE', null, 1],
    // ['pds__SUST-TC', null, 1],
    // ['pds__TBL', null, 1],
    // ['pds__TDS', null, 1],
    // ['pds__UGCB', null, 1],
    // ['pds__VHA', null, 1],
    // ['pds__WDTGCL', null, 1],
    // ['pds__ABBank-CIB', null, 1],
    // ['pds__AgraniBank-BACPS', null, 1],
    // ['pds__BB-BACPS', null, 1],
    // ['pds__BB-CA', null, 1],
    // ['pds__BCBL-CIB', null, 1],
    // ['pds__BCC-CA', null, 1],
    // ['pds__Bdjobs-MPVCC', null, 1],
    // ['pds__Biman-HelpDeskHR', null, 1],
    // ['pds__Boeing-BangladeshBiman', null, 1],
    // ['pds__BRTA-UniVerge', null, 1],
    // ['pds__BuySight-BizOps', null, 1],
    // ['pds__CapGains-LLC', null, 1],
    // ['pds__CCA-IDS', null, 1],
    // ['pds__CCC-CSSM', null, 1],
    // ['pds__CID-CDMS', null, 1],
    // ['pds__CityBank-CityAgent', null, 1],
    // ['pds__CityCell-NID-V-SA', null, 1],
    // ['pds__ConserveTrack-RDU', null, 1],
    // ['pds__ConserveTrack-WCM', null, 1],
    // ['pds__EAM-CMMS', null, 1],
    // ['pds__GP-HRMS', null, 1],
    // ['pds__GP-ROC', null, 1],
    // ['pds__GP-WBMS', null, 1],
    // ['pds__HabibBank-BACPS', null, 1],
    // ['pds__IslamGarments-rmgPro', null, 1],
    // ['pds__lekhapora.com', null, 1],
    // ['pds__LGED-IPMSRDEC', null, 1],
    // ['pds__MarketSharp-CRM', null, 1],
    // ['pds__MTBL-BACPS', null, 1],
    // ['pds__NBR-ASYCUDA', null, 1],
    // ['pds__Nestle-VATsys', null, 1],
    // ['pds__OAGN-NAMS', null, 1],
    // ['pds__OCAG-AMMS', null, 1],
    // ['pds__Partex-OEBS', null, 1],
    // ['pds__RA-BRPSharePoint', null, 1],
    // ['pds__RA-CWRBS', null, 1],
    // ['pds__RA-SRMS', null, 1],
    // ['pds__Revnx-Journey', null, 1],
    // ['pds__RHD-BDMS', null, 1],
    // ['pds__RHD-MIS-2009', null, 1],
    // ['pds__RHD-MIS-2015', null, 1],
    // ['pds__RHD-MIS-2017', null, 1],
    // ['pds__RHD-MIS', null, 1],
    // ['pds__ROBI-DMS', null, 1],
    // ['pds__ROBI-ROC', null, 1],
    // ['pds__SCB-CBRM', null, 1],
    // ['pds__SCB-OPCCMS', null, 1],
    // ['pds__SCB-RTGS', null, 1],
    // ['pds__SECL-CSB', null, 1],
    // ['pds__SECL-Metrica', null, 1],
    // ['pds__SECL-UniVerge', null, 1],
    // ['pds__SECL-VATsys', null, 1],
    // ['pds__SigmaStream-V2P', null, 1],
    // ['pds__SportsBuddy', null, 1],
    // ['pds__TrustBank-BACPS', null, 1],
    // ['pds__UGC-HEMIS', null, 1],
    // ['pds__Unilever-MFGPRO', null, 1],
  ];

  return ss_data_to_work_on;
};


function message_from_values(row_num){
  var ws = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var ws = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("-toc") ;

  var name = ws.getRange(`B${row_num}`).getValue();
  var resume_cell = ws.getRange(`F${row_num}`).getCell(1, 1);
  var resume_name = resume_cell.getValue();
  var resume_links = resume_cell.getFormula().split('"');
  var qa_report_cell = ws.getRange(`BB${row_num}`).getCell(1, 1);
  var qa_report_name = qa_report_cell.getValue();
  var qa_report_links = qa_report_cell.getFormula().split('"');

  var message = `${name}, Your Résumé *(${resume_name})* can be found at the following location\n
    ${resume_links[1]}\n
    please update your résumé\n
    ------------------------------\n
    see the QA report *(${qa_report_name}) on your résumé and resolve the issues\n
    ${qa_report_links[1]}`;

  return message;
};


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
      var unit_values = data_ws.getRange("X5:X").getValues();

      if (name_values != null && org_values != null){
        // the cell to the right is to be cleared first
        active_cell.offset(0, 1).clearContent().clearDataValidations();

        var selected_org = active_cell.getValue();

        var name_list = [];
        name_values.forEach(function(name, index) {
          // if (org_values[index] == selected_org && unit_values[index] == 'scm') {
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
