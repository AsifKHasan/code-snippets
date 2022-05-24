#!/usr/bin/env python3

import ftplib
from pprint import pprint

org = 'spectrum'
things = 'signature'

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd(f"/artifacts/{things}/{org}")
things_we_have = ftp.nlst()

things_we_need = [
    'signature__A.S.M.Estiuk.Sadick.png', 'signature__Aabid.Rahman.png', 'signature__Abdur.Rab.Marjan.png', 'signature__Abdur.Rahman.(Rokon).png', 'signature__Abed.Bin.Hossain.png', 'signature__Abu.Muhammad.Rashed.Mujib.Noman.png', 'signature__Adiat.Islam.Sahih.png', 'signature__Ahmed.Jahin.Akif.png', 'signature__Ahmed.Saquib.png', 'signature__Airin.Sultana.png', 'signature__Akeed.Anjum.png', 'signature__Anan.Aiman.Tuba.png', 'signature__Aqib.Asifur.Rahman.png', 'signature__Ashish.Kumar.Das.png', 'signature__Asma.Ul.Husna.png', 'signature__Atiqur.Rahman.png', 'signature__Delwar.Hossain.png', 'signature__Dipika.Debnath.png', 'signature__Faius.Mojumder.Nahin.png', 'signature__Ferdous.Ara.Ruma.png', 'signature__Ferdous.Rahman.png', 'signature__Hasib.Ahmed.Prince.png', 'signature__Hasib.Mahmud.png', 'signature__Ibrahim.Ibna.Md.Liaquat.Ullah.png', 'signature__Joy.Kabiraj.png', 'signature__Jumana.Ahmed.png', 'signature__Jyoti.Basu.Chakma.png', 'signature__K.M.Zabir.Tarique.png', 'signature__Kamrul.Islam.Sarek.png', 'signature__Karzon.Chowdhury.png', 'signature__Kazi.Rakibur.Rahman.png', 'signature__Khaja.Ajijul.Haque.(Mithu).png', 'signature__Khandakar.Asif.Hasan.png', 'signature__Lubna.Saha.png', 'signature__Mahim.Jahan.Mim.png', 'signature__Manzur.Alam.png', 'signature__Md.Abdullah.Al.Mamun.png', 'signature__Md.Ahsanur.Rahman.png', 'signature__Md.Al-Shahariar.png', 'signature__Md.Anamul.Haque.png', 'signature__Md.Anisur.Rahman.png', 'signature__Md.Anowarul.Islam.Rahat.png', 'signature__Md.Apon.Reza.png', 'signature__Md.Asgor.Ali.png', 'signature__Md.Ashaduzzaman.png', 'signature__Md.Ashraful.Hossain.png', 'signature__Md.Atikul.Islam.png', 'signature__Md.Azadul.Karim.png', 'signature__Md.Faizul.Bari.png', 'signature__Md.Farhad.Bhuiyan.png', 'signature__MD.Ferdous.Mahmud.png', 'signature__Md.Hasibur.Rahman.png', 'signature__Md.Humayun.Kabir.png', 'signature__Md.Ibrahim.Hossen.png', 'signature__Md.Ibrahim.Ullah.png', 'signature__Md.Istiyak.Ahamed.Milon.png', 'signature__Md.Jakir.Hossain.png', 'signature__Md.Jubaer.Hossain.png', 'signature__Md.Kamruzzaman.(O&M).png', 'signature__Md.Kazal.Pk.png', 'signature__Md.Khalid.Saifullah.Gazi.png', 'signature__Md.Mahabub.Al-Islam.png', 'signature__Md.Mahadi.Rahat.png', 'signature__Md.Mahasin.Alam.png', 'signature__Md.Mahmudul.Hasan.(Mukter).png', 'signature__Md.Mashrurul.Hakim.png', 'signature__Md.Mazharul.Islam.png', 'signature__Md.Mobusshar.Islam.png', 'signature__Md.Mominul.Islam.png', 'signature__Md.Monirul.Islam.png', 'signature__Md.Murshadul.Islam.png', 'signature__Md.Murshid.Sarker.png', 'signature__Md.Najmul.Hasan.Sharon.png', 'signature__Md.Nazmul.Hassan.png', 'signature__Md.Nazmul.Hossain.png', 'signature__Md.Nurujjaman.Sarker.png', 'signature__Md.Rabiul.Islam.png', 'signature__Md.Raqibul.Islam.png', 'signature__Md.Rezaul.Islam.png', 'signature__Md.Rokonuzzaman.png', 'signature__Md.Rony.Ahmed.png', 'signature__Md.Saidur.Rahman.(Shamim).png', 'signature__MD.Saiful.Islam.(DBA).png', 'signature__Md.Saiful.Islam.png', 'signature__Md.Salman.Hossen.png', 'signature__Md.Samim.Hosen.png', 'signature__Md.Sayeem.Khan.png', 'signature__Md.Shahin.Sheikh.png', 'signature__Md.Sharafat.Hossain.Kamal.png', 'signature__Md.Shariful.Islam.png', 'signature__Md.Shidratul.Islam.png', 'signature__Md.Shohag.Hossain.png', 'signature__Md.Shoheb.Ahamed.png', 'signature__Md.Siddiqur.Rahman.png', 'signature__Md.Sirajul.Islam.png', 'signature__Md.Tuhin.Reza.png', 'signature__Md.Zahidul.Islam.png', 'signature__Miskatun.Nahar.png', 'signature__Mohammad.Main.Uddin.png', 'signature__Monjur.Ahmed.png', 'signature__Muhammad.Myanuddin.png', 'signature__Mumtahina.Afroz.png', 'signature__Nur-E-Asma.Tabassum.png', 'signature__Rahat.Hussain.png', 'signature__Raihan.Ur.Rashid.png', 'signature__Rajib.Chowdhury.png', 'signature__Rifat.Ara.Swarna.png', 'signature__Rishad.Ali.Mimo.png', 'signature__Rizia.Aktar.png', 'signature__S.M.Azharul.Islam.png', 'signature__S.M.Touhidul.Islam.Al-Amin.png', 'signature__Sadia.Imam.Vasha.png', 'signature__Sagar.Saha.png', 'signature__Saiful.Islam.(Sonnet).png', 'signature__Saiful.Islam.(Sumon).png', 'signature__Sakib.Ibn.Abdullah.png', 'signature__Samin.Tawsib.Tanjim.png', 'signature__Sanjoy.Kumar.Saha.png', 'signature__Sanmoon.Yasmin.png', 'signature__Sarkar.Abul.Kalam.Azad.png', 'signature__Sayeda.Fatema.Ferdousi.png', 'signature__Sayeda.Tanjila.png', 'signature__Shaikh.Tojibul.Islam.png', 'signature__Shajir.Uddin.Haider.png', 'signature__Sharif.Mohmmad.Bin.Safi.png', 'signature__Shihan.Zaman.png', 'signature__Shuvo.Das.png', 'signature__SK.Maruf.Hosen.png', 'signature__Sonjoy.Kumar.png', 'signature__Soumen.Sikder.Shuvo.png', 'signature__Tanmoy.Chandra.Dhar.png', 'signature__Tasnim.Kabir.Ratul.png', 'signature__Tridib.Biswas.png'
]


print(f"we need {len(things_we_need)} {things}s for {org}")
print(f"we have {len(things_we_have)} {things}s for {org}")

# things_we_have_correct = set(things_we_have).intersection(things_we_need)
# print(f"we have {len(things_we_have_correct)} correct things")
# pprint(things_we_have_correct)

# things_we_have_wrong = set(things_we_have) - set(things_we_need)
# print(f"we have {len(things_we_have_wrong)} extra/wrong things")
# pprint(things_we_have_wrong)

things_we_are_missing = list(set(things_we_need) - set(things_we_have))
print(f"we have {len(things_we_are_missing)} missing {things}s for {org}")
for i in range(0, len(things_we_are_missing)):
    print(i+1, things_we_are_missing[i])
