// do some work on a list of files
function workOnFiles() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

//  var file_names_to_work_on = ['Resume__A.K.M.RakibulHasan', 'Resume__Abdur.Rab.Marjan', 'Resume__Akeed.Anjum', 'Resume__Amimul.Ahshan.Avi', 'Resume__Amiya.Ahmed', 'Resume__Anis.Bulbul', 'Resume__Anisur.Rahman', 'Resume__Aqib.Asifur.Rahman', 'Resume__Arifur.Rahman', 'Resume__Arnab.Kumar.Ghosh', 'Resume__Ashish.Kumar.Das', 'Resume__Asma.ul.Husna', 'Resume__Atiqur.Rahman', 'Resume__Azharul.Islam', 'Resume__Ealham.Al.Musabbir', 'Resume__Ekramul.Bari', 'Resume__Fahim.Shahriar', 'Resume__G.M.Ataur.Rahman', 'Resume__Ibrahim.Ibna.Md.Liaquat.Ullah', 'Resume__Kamrun.Nahar', 'Resume__Karzon.Chowdhury', 'Resume__Khairul.AN-AM', 'Resume__Laboni.Das', 'Resume__Lutfunnahar.Lota', 'Resume__Manzur.Alam', 'Resume__Mashud.Karim', 'Resume__Md.Abdullah.Al.Mamun', 'Resume__Md.Ahsanur.Rahman', 'Resume__Md.Asgor.Ali', 'Resume__Md.Asheq.Ullah', 'Resume__Md.Atikul.Islam', 'Resume__Md.Atiqur.Rahman', 'Resume__Md.Azizul.Hakim', 'Resume__Md.Hafizur.Rahman', 'Resume__Md.Hasibur.Rahman', 'Resume__Md.Imtiaz.Morshed.Bin.Zaman', 'Resume__Md.Jakir.Hossain', 'Resume__Md.Jamal.Uddin', 'Resume__Md.Kamruzzaman.Tanim', 'Resume__Md.Kaziul.Islam', 'Resume__Md.Mahabub.Al-Islam', 'Resume__Md.Mahasin.Alam', 'Resume__Md.Mazharul.Islam', 'Resume__Md.Murshadul.Islam', 'Resume__Md.Murshid.Sarker', 'Resume__Md.Najib.Hasan', 'Resume__Md.Nazmul.Hasan', 'Resume__Md.Rabiul.Islam', 'Resume__Md.Rejwan.Ull.Alam', 'Resume__Md.Rezaul.Islam', 'Resume__Md.Rezaul.Karim', 'Resume__Md.Robiul.Awoul', 'Resume__Md.Rokonuzzaman', 'Resume__Md.Saidur.Rahman.Shamim', 'Resume__Md.Sajal.Biswas', 'Resume__Md.Samim.Hosen', 'Resume__Md.Shahin.Sheikh', 'Resume__Md.Sharafat.Hossain.Kamal', 'Resume__Md.Sirajul.Islam', 'Resume__Md.Tuhin.Reza', 'Resume__Md.Zahidul.Islam', 'Resume__Mehedi.Hasan', 'Resume__Miskatun.Nahar', 'Resume__Mohammad.Ashraful.Islam', 'Resume__Mohammad.Main.Uddin', 'Resume__Mohammed.Kowsar.Rahman', 'Resume__Monjur.Ahmed', 'Resume__Muhammad.Aminur.Rahman', 'Resume__Muhammad.Ashraf.Uddin.Bhuiyan', 'Resume__Muhsinur.Rahman.Chowdhury', 'Resume__Murshida.Mushfique', 'Resume__Mushfika.Faria', 'Resume__Nasima.Aktar', 'Resume__Nur-E-Asma.Tabassum', 'Resume__Nusrat.Jahan.Mahmud', 'Resume__Rajib.Chowdhury', 'Resume__Raqibul.Islam', 'Resume__Rishad.Ali.Mimo', 'Resume__Sagar.Saha', 'Resume__Saiful.Islam', 'Resume__Saleh.Ahammed', 'Resume__Salman.Hossen', 'Resume__Sanjoy.Kumar.Saha', 'Resume__Sanmoon.Yasmin', 'Resume__Shahida.Begum', 'Resume__Shaikh.Tojibul.Islam', 'Resume__Shajir.Uddin.Haider', 'Resume__Shariful.Islam', 'Resume__Shihan.Zaman', 'Resume__Shohag.Hossain', 'Resume__Syed.Mohidul.Islam', 'Resume__Syed.Mynul.Islam', 'Resume__Syed.Taslimur.Rahaman', 'Resume__Tanmoy.Chandra.Dhar', 'Resume__Tofiq.Akbar', 'Resume__Umme.Rumman.Usha'];
//  var file_names_to_work_on = ['Resume__Anisur.Rahman', 'Resume__Ashish.Kumar.Das', 'Resume__Ibrahim.Ibna.Md.Liaquat.Ullah', 'Resume__Manzur.Alam', 'Resume__Mashud.Karim', 'Resume__Md.Jakir.Hossain', 'Resume__Md.Jamal.Uddin', 'Resume__Md.Kamruzzaman.Tanim', 'Resume__Md.Murshid.Sarker', 'Resume__Md.Rezaul.Karim', 'Resume__Md.Robiul.Awoul', 'Resume__Md.Rokonuzzaman', 'Resume__Md.Sharafat.Hossain.Kamal', 'Resume__Mohammad.Main.Uddin', 'Resume__Mohammed.Kowsar.Rahman', 'Resume__Monjur.Ahmed', 'Resume__Saiful.Islam', 'Resume__Saleh.Ahammed', 'Resume__Sanjoy.Kumar.Saha', 'Resume__Shaikh.Tojibul.Islam', 'Resume__Shariful.Islam', 'Resume__Shihan.Zaman'];
//  var file_names_to_work_on = ['Resume__A.K.M.RakibulHasan', 'Resume__Abdur.Rab.Marjan', 'Resume__Akeed.Anjum', 'Resume__Amimul.Ahshan.Avi', 'Resume__Amiya.Ahmed', 'Resume__Anis.Bulbul', 'Resume__Aqib.Asifur.Rahman',
//                               'Resume__Arifur.Rahman', 'Resume__Arnab.Kumar.Ghosh', 'Resume__Asma.ul.Husna', 'Resume__Atiqur.Rahman', 'Resume__Azharul.Islam', 'Resume__Ekramul.Bari',  'Resume__Fahim.Shahriar',
//                               'Resume__G.M.Ataur.Rahman', 'Resume__Kamrun.Nahar', 'Resume__Karzon.Chowdhury', 'Resume__Khairul.AN-AM', 'Resume__Laboni.Das', 'Resume__Lutfunnahar.Lota', 'Resume__Md.Abdullah.Al.Mamun',
//                               'Resume__Md.Ahsanur.Rahman', 'Resume__Md.Asgor.Ali', 'Resume__Md.Asheq.Ullah', 'Resume__Md.Atikul.Islam', 'Resume__Md.Atiqur.Rahman', 'Resume__Md.Azizul.Hakim',  'Resume__Md.Hafizur.Rahman',
//                               'Resume__Md.Hasibur.Rahman', 'Resume__Md.Imtiaz.Morshed.Bin.Zaman', 'Resume__Md.Kaziul.Islam', 'Resume__Md.Mahabub.Al-Islam', 'Resume__Md.Mahasin.Alam',  'Resume__Md.Mazharul.Islam',
//                               'Resume__Md.Murshadul.Islam', 'Resume__Md.Najib.Hasan', 'Resume__Md.Nazmul.Hasan', 'Resume__Md.Rabiul.Islam', 'Resume__Md.Rejwan.Ull.Alam', 'Resume__Md.Rezaul.Islam',
//                               'Resume__Md.Saidur.Rahman.Shamim', 'Resume__Md.Sajal.Biswas', 'Resume__Md.Samim.Hosen', 'Resume__Md.Shahin.Sheikh', 'Resume__Md.Sirajul.Islam', 'Resume__Md.Tuhin.Reza', 'Resume__Md.Zahidul.Islam',
//                               'Resume__Mehedi.Hasan', 'Resume__Miskatun.Nahar', 'Resume__Mohammad.Ashraful.Islam', 'Resume__Muhammad.Aminur.Rahman', 'Resume__Muhammad.Ashraf.Uddin.Bhuiyan', 'Resume__Muhsinur.Rahman.Chowdhury',
//                               'Resume__Murshida.Mushfique', 'Resume__Mushfika.Faria', 'Resume__Nasima.Aktar', 'Resume__Nur-E-Asma.Tabassum', 'Resume__Nusrat.Jahan.Mahmud', 'Resume__Rajib.Chowdhury', 'Resume__Raqibul.Islam',
//                               'Resume__Rishad.Ali.Mimo', 'Resume__Sagar.Saha', 'Resume__Salman.Hossen', 'Resume__Sanmoon.Yasmin', 'Resume__Shahida.Begum', 'Resume__Shajir.Uddin.Haider', 'Resume__Shohag.Hossain',
//                               'Resume__Syed.Taslimur.Rahaman', 'Resume__Tanmoy.Chandra.Dhar', 'Resume__Tofiq.Akbar', 'Resume__Umme.Rumman.Usha'];

  var file_names_to_work_on = ['Resume__Tanmoy.Chandra.Dhar'];

  for (var i = 0; i < file_names_to_work_on.length; i++) {
    var file_name = file_names_to_work_on[i];
    var file = getUniqueFileByName(file_name);
    var folder_id = '1klZ3h7RmaY7TaPShcfNRseDvk9EeZrqM';
    var folder = DriveApp.getFolderById(folder_id);

    if (file != null) {
      // do some work on the files
      var new_name = file_name.replace('Resume__', 'Résumé__');
      var new_file = copyFileTo(file, new_name, folder);
      if (new_file == null) {
        Logger.log('Could not copy file : ' + file_name + ' to : ' + new_name);
      }
    }
  }
};

// get unique file by name
function getUniqueFileByName(file_name) {
  var files = DriveApp.getFilesByName(file_name);

  // return the first file if any, else return null
  if (files.hasNext()) {
    var file = files.next();
  }
  else {
    return null;
  }

  // if there are more files, report duplicate
  if (files.hasNext()) {
    Logger.log('There are more than one file with the name : ' + file_name);
    return null;
  }

  return file;
};

// copy a file with anew name and location
function copyFileTo(from_file, new_name, destination_folder_id) {
  var new_file = from_file.makeCopy(new_name, destination_folder_id);
  return new_file;
};
