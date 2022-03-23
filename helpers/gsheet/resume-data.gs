WS_WARN_IF_BLANK = {
  '00-layout': [
    'B3:J5', 'B7:J10', 'B12:J13', 'B15:J16', 'B18:J20', 'B22:J23', 'B25:J25', 'B27:J28', 'B30:J30', 'B32:J33', 'B35:J36', 'B38:J38',
    'D44', 'E44', 'F44', 'H46', 'H50', 'I44:J48', 'I49:J49', 'I50:J50'
  ],
};

WS_FORMAT = {
  '00-layout': {
    'A1': {'value': '-toc', 'ws-link': '-toc', 'halign': 'center'},
    'B2:J2': {'value': 'content', 'weight': 'bold'},

    // top table
    'B3:G3': {'value': 'Name of the Firm', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H3:J3': {'weight': 'bold'},
    'B4:G4': {'value': 'EoI/RFP Reference', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H4:J4': {},
    'B5:G5': {'value': 'Name of the Client', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H5:J5': {},
    'B3:J5': {'border-color': '#b7b7b7'},

    // blank row
    'B6:J6': {},

    // info table
    'B7': {'value': '1', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C7:G7': {'value': 'PROPOSED POSITION FOR THIS PROJECT', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H7:I7': {},
    'B8': {'value': '2', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C8:G8': {'value': 'NAME OF STAFF', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H8:I8': {'formula': "='01-personal'!D3"},
    'B9': {'value': '3', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C9:G9': {'value': 'DATE OF BIRTH', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H9:I9': {'formula': "='01-personal'!D5", 'halign': 'left'},
    'B10': {'value': '4', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C10:G10': {'value': 'NATIONALITY', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H10:I10': {'formula': "='01-personal'!D6"},
    'J7:J10': {},
    'B7:J10': {'border-color': '#b7b7b7'},

    // blank row
    'B11:J11' : {},

    // 5 - Membership
    'B12': {'value': '5', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C12:J12': {'value': 'MEMBERSHIP IN PROFESSIONAL SOCIETIES', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B13:J13': {'value': '10-membership', 'ws-link': '10-membership', 'notes': '{"content": "out-of-cell"}'},
    'B12:J13': {'border-color': '#b7b7b7'},

    // blank row
    'B14:J14': {},

    // 6 - Education
    'B15': {'value': '6', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C15:J15': {'value': 'EDUCATION', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B16:J16': {'value': '03-education', 'ws-link': '03-education', 'notes': '{"content": "out-of-cell"}'},
    'B15:J16': {'border-color': '#b7b7b7'},

    // blank row
    'B17:J17': {},

    // 7 - Other Training
    'B18': {'value': '7', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C18:J18': {'value': 'OTHER TRAINING', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B19:J19': {'value': '08-training', 'ws-link': '08-training', 'notes': '{"content": "out-of-cell"}'},
    'B20:J20': {'value': '09-certification', 'ws-link': '09-certification', 'notes': '{"content": "out-of-cell"}'},
    'B18:J20': {'border-color': '#b7b7b7'},

    // blank row
    'B21:J21': {},

    // 8 - Language Proficiency
    'B22': {'value': '8', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C22:J22': {'value': 'LANGUAGES & DEGREE OF PROFICIENCY', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B23:J23': {'value': '11-language-proficiency', 'ws-link': '11-language-proficiency', 'notes': '{"content": "out-of-cell"}'},
    'B22:J23': {'border-color': '#b7b7b7'},

    // blank row
    'B24:J24': {},

    // 9 - Countries of Experience
    'B25': {'value': '9', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C25:G25': {'value': 'COUNTRIES OF WORK EXPERIENCE', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H25:J25': {'formula': "='01-personal'!D13"},
    'B25:J25': {'border-color': '#b7b7b7'},

    // blank row
    'B26:J26': {},

    // 10 - Employment
    'B27': {'value': '10', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C27:J27': {'value': 'EMPLOYMENT RECORD', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B28:J28': {'value': '06-job-history', 'ws-link': '06-job-history', 'notes': '{"content": "out-of-cell"}'},
    'B27:J28': {'border-color': '#b7b7b7'},

    'B29:J29': {},

    'B30:J30': {'value': '07-project-roles', 'ws-link': '07-project-roles', 'notes': '{"content": "out-of-cell"}', 'border-color': '#b7b7b7'},

    // blank row
    'B31:J31': {},

    // 11 - Jobs Undertaken
    'B32': {'value': '11', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C32:J32': {'value': 'WORK UNDERTAKEN THAT BEST ILLUSTRATES YOUR CAPABILITY TO HANDLE THIS ASSIGNMENT', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B33:J33': {'value': '02-career-highlight', 'ws-link': '02-career-highlight', 'notes': '{"content": "out-of-cell"}'},
    'B32:J33': {'border-color': '#b7b7b7'},

    // blank row
    'B34:J34': {},

    // 12 - Computer Skill
    'B35': {'value': '12', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C35:J35': {'value': 'COMPUTER SKILLS', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'B36:J36': {'value': '05-technical-expertise', 'ws-link': '05-technical-expertise', 'notes': '{"content": "out-of-cell"}'},
    'B35:J36': {'border-color': '#b7b7b7'},

    // blank row
    'B37:J37': {},

    // 13 - Contact
    'B38': {'value': '13', 'weight': 'bold', 'bgcolor': '#f3f3f3', 'halign': 'center'},
    'C38:G38': {'value': 'CONTACT AND WEB INFORMATION', 'weight': 'bold', 'bgcolor': '#f3f3f3'},
    'H38:J38': {'value': '12-contact', 'ws-link': '12-contact'},
    'B38:J38': {'border-color': '#b7b7b7'},

    // blank row
    'B39:J39': {'notes': '{"content": "out-of-cell"}'},

    // certification
    'B40:J40': {'value': 'CERTIFICATION [do not amend this certification]'},
    'B41:J41': {'value': 'I, the undersigned, certify that (i) I was not a former employee of the Client immediately before submission of this Proposal, (ii) I have not offered my CV to be proposed by a Firm other than this Software Firm for this assignment and, (iii) to the best of my knowledge and belief, this CV correctly describes myself, my qualifications, and my experience. I also understand that any willful misstatement described herein may lead to my disqualification or dismissal, if engaged.'},
    'B42:J42': {'value': 'I have been employed by [FIRM NAME] continuously for the last twelve (12) months as regular full-time staff. Indicate "Yes" or "No" in the boxes below:'},
    'B43:J43': {'value': ''},

    // confirmation and signature
    'D44': {'value': 'Yes', 'halign': 'right'},
    'E44': {'value': '✔', 'border-color': '#b7b7b7', 'halign': 'center'},
    'F44': {'value': 'No', 'halign': 'right'},
    'G44': {'border-color': '#b7b7b7', 'halign': 'center'},

    'H46': {'value': 'Signature', 'halign': 'right'},
    'H50': {'value': 'Date of Signing', 'halign': 'right'},

    'I44:J48': {'border-color': '#b7b7b7', 'halign': 'center'},
    'I49:J49': {'halign': 'center'},
    'I50:J50': {'value': 'Day / Month / Year', 'halign': 'center'},
    'I49:J50': {'border-color': '#b7b7b7'},

    // review notes
    'A42': {'value': 'change FIRM NAME'},
    'A49': {'value': 'fill correctly'},

  }
};

SS_NAMES_TO_WORK_ON = [
  // 'Résumé__template',

  // AEL
  // 'Résumé__Abdullah-Al-Hossain.Bin.Sarwar',
  // 'Résumé__Asadul.Haque',
  // 'Résumé__Asif.Yusuf',
  // 'Résumé__Asaduzzaman',
  // 'Résumé__Dipankar.Kumar.Biswas',
  // 'Résumé__Iqbal.Yusuf',
  // 'Résumé__Md.Nasir.Uddin',
  // 'Résumé__Md.Ahsan.Habib.Rocky',
  // 'Résumé__Md.Atikur.Zaman',
  // 'Résumé__Md.Faisal.Hossain',
  // 'Résumé__Md.Mijanur.Rahman',
  // 'Résumé__Md.Nahidul.Islam.Siddique',
  // 'Résumé__Md.Sohel.Rana',
  // 'Résumé__Md.Yousuf.Ali',
  // 'Résumé__Mir.Earfan.Elahi',
  // 'Résumé__Mohammad.Kamrul.Hasan',
  // 'Résumé__Salman.Ahmed.Firoz',
  // 'Résumé__Suday.Kumer.Ghosh',
  // 'Résumé__Tanvir.Rahman',
  // 'Résumé__Tufaha.Ashfaque',

  // Celloscope
  'Résumé__Alif.Arfab',
  'Résumé__Altaf.Hossain',
  'Résumé__Amimul.Ahshan.Avi',
  'Résumé__Amiya.Ahmed',
  'Résumé__Anis.Bulbul',
  'Résumé__Arnab.Basak',
  'Résumé__Asif.Khan.Taj',
  'Résumé__Farhana.Naz',
  'Résumé__Kamrun.Nahar',
  'Résumé__Khondoker.Tanvir.Hossain',
  'Résumé__Laboni.Das',
  'Résumé__Mainur.Rahman',
  'Résumé__Maly.Mohsem',
  'Résumé__Md.Azfar.Inan',
  'Résumé__Md.Ehtesham-Ul-Haque',
  'Résumé__MD.Fuad.Hasan.Chowdhury',
  'Résumé__Md.Hafizur.Rahman',
  'Résumé__Md.Jamal.Uddin',
  'Résumé__Md.Kamruzzaman.Tanim',
  'Résumé__Md.Shariar.Kabir',
  'Résumé__Md.Tofiq.Akbar',
  'Résumé__Mehedi.Hasan',
  'Résumé__Mohammad.Ashraful.Islam',
  'Résumé__Mohammad.Mashud.Karim',
  'Résumé__Mohammed.Kowsar.Rahman.Bhuiyan',
  'Résumé__Moshiur.Rahman',
  'Résumé__Mst.Lutfunnahar.Lota',
  'Résumé__Muhammad.Ashraf.Uddin.Bhuiyan',
  'Résumé__Murshida.Mushfique',
  'Résumé__Mushfika.Faria',
  'Résumé__Nafis.Ahmed.Fuad',
  'Résumé__Naim.Reza',
  'Résumé__Nasima.Aktar',
  'Résumé__Shafayat.Ahmed',
  'Résumé__Syed.Mostofa.Monsur',
  'Résumé__Syed.Taslimur.Rahaman',
  'Résumé__Umme.Rumman.Usha',
  'Résumé__Wakib.Hasan',

  // DOER
  'Résumé__Abdullah.Al.Maruf',
  'Résumé__Arun.Chakraborty',
  'Résumé__Ayesha.Siddika',
  'Résumé__Bony.Tasnim',
  'Résumé__Gaffar.Khan',
  'Résumé__Golam.Kibria',
  'Résumé__Imran.Hossain.Pappu',
  'Résumé__Imran.Howlader',
  'Résumé__Imtiaz.Mahmood',
  'Résumé__Israt.Fatima',
  'Résumé__Jahin.Khan.Shourov',
  'Résumé__Kamrul.Hasan.Komol',
  'Résumé__Kazi.Noor.Jahan',
  'Résumé__Mahmudul.Hasan',
  'Résumé__Maria.Nurjahanara.Bhuiaya',
  'Résumé__Md.Masud.Rana.Tuhin',
  'Résumé__Md.Mokaddes.Ali',
  'Résumé__Md.Motaher.Hossain',
  'Résumé__Md.Andalib.Emdad',
  'Résumé__Md.Bodrul.Alam',
  'Résumé__Md.Habibur.Rahman.Tusher',
  'Résumé__Md.Jahangir.Alam',
  'Résumé__Md.Jahidul.Islam',
  'Résumé__Md.Kamrul.Hasan',
  'Résumé__Md.Kamruzzaman',
  'Résumé__Md.Mainul.Islam',
  'Résumé__MD.Masud.Rana-(BDEX)',
  'Résumé__MD.Masud.Rana-(BDO)',
  'Résumé__Md.Mehrab.Hossain',
  'Résumé__MD.Monirul.Islam.Tipu',
  'Résumé__Md.Moshiur.Rahman',
  'Résumé__Md.Nazmul.Hasan.Masum',
  'Résumé__Md.Noor-E-Alom.Siddique',
  'Résumé__Md.Rafaz.Uddin',
  'Résumé__Md.Rasel.Molla',
  'Résumé__Md.Sohan.Kabir',
  'Résumé__Mokul.Arfan.Dito',
  'Résumé__Nahid.Kamal',
  'Résumé__Ommul.Khair.Musammat.Tahera',
  'Résumé__Palash.Kumar.Sinha',
  'Résumé__Rafiqul.Islam.Reyad',
  'Résumé__Rajib.Gupta',
  'Résumé__Redwan.Al.Rashed',
  'Résumé__Rezaul.Karim',
  'Résumé__S.M.Al-Amin',
  'Résumé__Sadia.Yasmin',
  'Résumé__Saikat.Barua',
  'Résumé__Salma.Afrose',
  'Résumé__Sathe.Khan.Majlish',
  'Résumé__Sayada.Sultana',
  'Résumé__Saythe.Kaniz.Fatema',
  'Résumé__Shahadat.Hossain',
  'Résumé__Shanawaz.Durjoy',
  'Résumé__Sharmin.Ferdowsi.Shormi',
  'Résumé__Siam.Samad.Prantik',
  'Résumé__Sohag.Ali',
  'Résumé__Sufia.Khanom',
  'Résumé__Suman.Miah',
  'Résumé__Sumshur.Rahman',
  'Résumé__Suraiya.Binte.Ali',
  'Résumé__Swpan.Kumar.Shill',
  'Résumé__Syed.Ahmad.Mahdi',
  'Résumé__Syed.Ahmad.Rasul',
  'Résumé__Tania.Akter',
  'Résumé__Tanvir.Ahmed',
  'Résumé__Tauhidul.Islam',
  'Résumé__Ziaul.Hoq',
  'Résumé__Zillur.Rahman',

  // SSCL
  'Résumé__Abed.Bin.Hossain',
  'Résumé__Ahmed.Saquib',
  'Résumé__Hasib.Mahmud',
  'Résumé__Jumana.Ahmed',
  'Résumé__Md.Faizul.Bari',

  // Spectrum
  'Résumé__A.K.M.Rakibul.Hasan',
  'Résumé__A.S.M.Estiuk.Sadick',
  'Résumé__Aabid.Rahman',
  'Résumé__Abdur.Rab.Marjan',
  'Résumé__Abdur.Rahman',
  'Résumé__Abdur.Rahman.Sagor',
  'Résumé__Abu.Muhammad.Rashed.Mujib.Noman',
  'Résumé__Adiat.Islam.Sahih',
  'Résumé__Ahmed.Jahin.Akif',
  'Résumé__Airin.Sultana',
  'Résumé__Akeed.Anjum',
  'Résumé__Anan.Aiman.Tuba',
  'Résumé__Aqib.Asifur.Rahman',
  'Résumé__Ashish.Kumar.Das',
  'Résumé__Asma.Ul.Husna',
  'Résumé__Atiqur.Rahman',
  'Résumé__Dipika.Debnath',
  'Résumé__Fahim.Shahriar',
  'Résumé__Faius.Mojumder.Nahin',
  'Résumé__Ferdous.Rahman',
  'Résumé__G.M.Ataur.Rahman',
  'Résumé__Hasib.Ahmed.Prince',
  'Résumé__Ibrahim.Ibna.Md.Liaquat.Ullah',
  'Résumé__Joy.Kabiraj',
  'Résumé__Jyoti.Basu.Chakma',
  'Résumé__K.M.Zabir.Tarique',
  'Résumé__Kamrul.Islam.Sarek',
  'Résumé__Karzon.Chowdhury',
  'Résumé__Kazi.Rakibur.Rahman',
  'Résumé__Khaja.Ajijul.Haque.(Mithu)',
  'Résumé__Khandakar.Asif.Hasan',
  'Résumé__Khandakar.Rashed.Hassan',
  'Résumé__Lubna.Saha',
  'Résumé__Mahim.Jahan.Mim',
  'Résumé__Manzur.Alam',
  'Résumé__Md.Farhad.Bhuiyan',
  'Résumé__Md.Abdullah.Al.Mamun',
  'Résumé__Md.Ahsanur.Rahman',
  'Résumé__Md.Al-Shahariar',
  'Résumé__Md.Anamul.Haque',
  'Résumé__Md.Anisur.Rahman',
  'Résumé__Md.Apon.Reza',
  'Résumé__Md.Arifur.Rahman.Bhuiyan',
  'Résumé__Md.Asgor.Ali',
  'Résumé__Md.Asheq.Ullah',
  'Résumé__Md.Ashraful.Hossain',
  'Résumé__Md.Atikul.Islam',
  'Résumé__Md.Atiqur.Rahman',
  'Résumé__Md.Azizul.Hakim',
  'Résumé__Md.Ekramul.Bari',
  'Résumé__Md.Ferdous.Mahmud',
  'Résumé__Md.Hasibur.Rahman',
  'Résumé__Md.Humayun.Kabir',
  'Résumé__Md.Ibrahim.Hossain',
  'Résumé__Md.Ibrahim.Ullah',
  'Résumé__Md.Istiyak.Ahmed.Milon',
  'Résumé__Md.Jakir.Hossain',
  'Résumé__Md.Jubaer.Hossain',
  'Résumé__Md.Kamruzzaman-(SECL)',
  'Résumé__Md.Kaziul.Islam',
  'Résumé__Md.Khalid.Saifullah.Gazi',
  'Résumé__Md.Mahabub.Al-Islam',
  'Résumé__Md.Mahasin.Alam',
  'Résumé__Md.Mahmudul.Hasan',
  'Résumé__Md.Mashrurul.Hakim',
  'Résumé__Md.Mazharul.Islam',
  'Résumé__Md.Mobusshar.Islam',
  'Résumé__Md.Mominul.Islam',
  'Résumé__Md.Murshadul.Islam',
  'Résumé__Md.Murshid.Sarker',
  'Résumé__Md.Najmul.Hasan.Sharon',
  'Résumé__Md.Nazmul.Hasan',
  'Résumé__Md.Nazmul.Hossain',
  'Résumé__Md.Rabiul.Islam',
  'Résumé__Md.Raqibul.Islam',
  'Résumé__Md.Rejuanul.Haque',
  'Résumé__Md.Rejwan.Ull.Alam',
  'Résumé__Md.Rezaul.Islam',
  'Résumé__Md.Rezaul.Karim',
  'Résumé__Md.Robiul.Awoul',
  'Résumé__Md.Rokonuzzaman',
  'Résumé__Md.Saidur.Rahman.Shamim',
  'Résumé__Md.Saiful.Islam',
  'Résumé__Md.Sajal.Biswas',
  'Résumé__Md.Salman.Hossen',
  'Résumé__Md.Samim.Hosen',
  'Résumé__Md.Sayeem.Khan',
  'Résumé__Md.Shahin.Sheikh',
  'Résumé__Md.Sharafat.Hossain.Kamal',
  'Résumé__Md.Shariful.Islam',
  'Résumé__Md.Shidratul.Islam.Rifat',
  'Résumé__Md.Sirajul.Islam',
  'Résumé__Md.Tuhin.Reza',
  'Résumé__Md.Zahidul.Islam',
  'Résumé__Miskatun.Nahar',
  'Résumé__Mohammad.Main.Uddin',
  'Résumé__Mohammad.Nazmul.Hasan',
  'Résumé__Mohammad.Saiful.Islam',
  'Résumé__Mohammad.Shamsur.Rahman',
  'Résumé__Monjur.Ahmed',
  'Résumé__Muhammad.Aminur.Rahman',
  'Résumé__Muhammad.Myanuddin',
  'Résumé__Muhsinur.Rahman.Chowdhury',
  'Résumé__Nur-E-Asma.Tabassum',
  'Résumé__Nusrat.Jahan.Mahmud',
  'Résumé__Raihan.Ur.Rashid',
  'Résumé__Rajib.Chowdhury',
  'Résumé__Rifat.Ara.Swarna',
  'Résumé__Rishad.Ali.Mimo',
  'Résumé__S.M.Azharul.Islam',
  'Résumé__Sagar.Saha',
  'Résumé__Saiful.Islam',
  'Résumé__Saiful.Islam.Sonnet',
  'Résumé__Sakib.Ibn.Abdullah',
  'Résumé__Saleh.Ahammed',
  'Résumé__Samin.Tawsib.Tanjim',
  'Résumé__Sanjoy.Kumar.Saha',
  'Résumé__Sanmoon.Yasmin',
  'Résumé__Sarkar.Abul.Kalam.Azad',
  'Résumé__Sayeda.Fatema.Ferdousi',
  'Résumé__Sayeda.Tanjila',
  'Résumé__Shahida.Begum',
  'Résumé__Shaikh.Tojibul.Islam',
  'Résumé__Shajir.Uddin.Haider',
  'Résumé__Shihan.Zaman',
  'Résumé__Shohag.Hossain',
  'Résumé__Shuvo.Das',
  'Résumé__SK.Maruf.Hosen',
  'Résumé__Sonjoy.Kumar',
  'Résumé__Soumen.Sikder.Shuvo',
  'Résumé__Syed.Shah.Md.Adib',
  'Résumé__Tanmoy.Chandra.Dhar',
  'Résumé__Tasnim.Kabir.Ratul',
  'Résumé__Tridib.Biswas',

  // External
  'Résumé__Arnab.Kumar.Ghosh',
  'Résumé__Khairul.AN-AM',
  'Résumé__Md.Asif.Atick',
  'Résumé__Md.Imtiaz.Morshed.Bin.Zaman',
  'Résumé__Md.Monirul.Islam',
  'Résumé__Md.Najib.Hasan',
  'Résumé__Saleh.Ahammed.Masum.Khan',

];


WORKKSHEET_CONTENTS = {
  '00-layout': {
    // Name of the Firm
    'H3': {'cell-value': 'Spectrum Engineering Consortium Ltd.'},
    // EoI/RFP Reference
    'H4': {'cell-value': '123-456-789-987-654-321'},
    // Name of the Client
    'H5': {'cell-value': 'National Board of Revenue'},
    // Date of Signing - Day / Month / Year
    'I49': {'cell-value': '23 / 03 / 2022'},
  },
};

WORKKSHEET_LINKS = {
  '00-layout': {
    'B13': {'cell-value': '10-membership', 'ws-name-to-link': '10-membership', 'notes': '{"content": "out-of-cell"}'},
    'B16': {'cell-value': '03-education', 'ws-name-to-link': '03-education', 'notes': '{"content": "out-of-cell"}'},
    'B19': {'cell-value': '08-training', 'ws-name-to-link': '08-training', 'notes': '{"content": "out-of-cell"}'},
    'B20': {'cell-value': '09-certification', 'ws-name-to-link': '09-certification', 'notes': '{"content": "out-of-cell"}'},
    'B23': {'cell-value': '11-language-proficiency', 'ws-name-to-link': '11-language-proficiency', 'notes': '{"content": "out-of-cell"}'},
    'B28': {'cell-value': '06-job-history', 'ws-name-to-link': '06-job-history', 'notes': '{"content": "out-of-cell"}'},
    'B30': {'cell-value': '07-project-roles', 'ws-name-to-link': '07-project-roles', 'notes': '{"content": "out-of-cell"}'},
    'B34': {'cell-value': '02-career-highlight', 'ws-name-to-link': '02-career-highlight', 'notes': '{"content": "out-of-cell"}'},
    'B37': {'cell-value': '05-technical-expertise', 'ws-name-to-link': '05-technical-expertise', 'notes': '{"content": "out-of-cell"}'},
    'H39': {'cell-value': '12-contact', 'ws-name-to-link': '12-contact'},
    'B40': {'notes': '{"content": "out-of-cell"}'},
  },
};

RESUME_WS_COLUMNS = {
  '-toc' : {
  },
  '00-layout' : {
    'B': 40, 'C': 200, 'D': 40, 'E': 30, 'F': 40, 'G': 30, 'H': 150, 'I': 150, 'J': 320,
  },
  '01-personal' : {
    'B': 40, 'C': 130, 'D': 330, 'E': 400,
  },
  '02-career-highlight' : {
    'B': 150, 'C': 30, 'D': 800,
  },
  '03-education' : {
    'B': 100, 'C': 200, 'D': 300, 'E': 300,
  },
  '04-managerial-expertise' : {
    'B': 170, 'C': 30, 'D': 800,
  },
  '05-technical-expertise' : {
    'B': 170, 'C': 30, 'D': 800,
  },
  // '06-job-history' : {
  //   'B': 170, 'C': 30, 'D': 1000,
  // },
  // '07-project-roles' : {
  //   'B': 170, 'C': 30, 'D': 700,
  // },
  '08-training' : {
    'B': 100, 'C': 550, 'D': 350,
  },
  '09-certification' : {
    'B': 100, 'C': 200, 'D': 300, 'E': 400,
  },
  '10-membership' : {
    'B': 300, 'C': 150, 'D': 150, 'E': 150, 'F': 250,
  },
  '11-language-proficiency' : {
    'B': 80, 'C': 270, 'D': 270, 'E': 270, 'F': 210,
  },
  '12-contact' : {
    'B': 200, 'C': 600,
  },
  '13-educational-certificates' : {
    'B': 1000,
  },
  '14-vendor-certificates' : {
    'B': 1000,
  },
  '15-institutional-certificates' : {
    'B': 1000,
  },
};


WORKSHEET_NAME_MAP1 = {
  'idra-wb-resume-layout' : 'layout-IDRA',
  'idra-resume-layout-wb' : 'layout-IDRA',
  'idra-wb-resume-layout-wb' : 'layout-IDRA',
  'Idra-resume-layout-wb' : 'layout-IDRA',
  'Idra-wb-resume-layout' : 'layout-IDRA',
  'wb-idra-resume-layout' : 'layout-IDRA',
  'wb-idra-resume-layout-wb' : 'layout-IDRA',

  'wb-resume-layout-wb' : 'layout-WB-WB',
  'wb-resume-layout' : 'layout-WB',

  'DWASA-wb-resume-layout' : 'layout-DWASA',

  'nbr-bmap-resume-layout' : 'layout-NBR-BMAP',
  'nbr-bmap-wb-resume-layout' : 'layout-NBR-BMAP',

  'pg5-bhp-layout' : 'layout-PG5-BHP',
  'BHP-resume-layout' : 'layout-PG5-BHP',

  'idra-job-history' : 'job-history-IDRA',
  'nbr-bmap-job-history' : 'job-history-NBR-BMAP',

  'idra-project-roles' : 'project-roles-IDRA',
  'nbr-bmap-project-roles' : 'project-roles-NBR-BMAP',

  'nbr-bmap-technical-expertise' : 'technical-expertise-NBR-BMAP',
};


WORKSHEET_NAME_MAP2 = {
  'layout-DWASA': '00-layout-DWASA',
  'layout-IDRA': '00-layout-IDRA',
  'layout-NBR-BMAP': '00-layout-NBR-BMAP',
  'layout-PG5-BHP': '00-layout-PG5-BHP',
  'layout-WB-WB': '00-layout-WB-WB',
  'layout-WB': '00-layout-WB',

  'personal': '01-personal',
  'career-highlight': '02-career-highlight',
  'education': '03-education',
  'managerial-expertise': '04-managerial-expertise',

  'technical-expertise': '05-technical-expertise',
  'technical-expertise-NBR-BMAP': '05-technical-expertise-NBR-BMAP',

  'job-history': '06-job-history',
  'job-history-IDRA': '06-job-history-IDRA',
  'job-history-NBR-BMAP': '06-job-history-NBR-BMAP',

  'project-roles': '07-project-roles',
  'project-roles-IDRA': '07-project-roles-IDRA',
  'project-roles-NBR-BMAP': '07-project-roles-NBR-BMAP',

  'training': '08-training',
  'certification': '09-certification',
  'membership': '10-membership',
  'language-proficiency': '11-language-proficiency',
  'contact': '12-contact',
  'educational-certificates': '13-educational-certificates',
  'vendor-certificates': '14-vendor-certificates',
  'institutional-certificates': '15-institutional-certificates',
};


RESUME_WS_NAMES = [
  '-toc', '00-layout', '01-personal', '02-career-highlight', '03-education', '04-managerial-expertise', '05-technical-expertise', '06-job-history', '07-project-roles', '08-training',
  '09-certification', '10-membership', '11-language-proficiency', '12-contact', '13-educational-certificates', '14-vendor-certificates', '15-institutional-certificates'
];


LETTER_TO_COLUMN = {
  'A' : 1,
  'B' : 2,
  'C' : 3,
  'D' : 4,
  'E' : 5,
  'F' : 6,
  'G' : 7,
  'H' : 8,
  'I' : 9,
  'J' : 10,
  'K' : 11,
  'L' : 12,
  'M' : 13,
  'N' : 14,
  'O' : 15,
  'P' : 16,
  'Q' : 17,
  'R' : 18,
  'S' : 19,
  'T' : 20,
  'U' : 21,
  'V' : 22,
  'W' : 23,
  'X' : 24,
  'Y' : 25,
  'Z' : 26,
};
