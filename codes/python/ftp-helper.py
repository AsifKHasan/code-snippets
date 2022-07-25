#!/usr/bin/env python3

import ftplib
from pprint import pprint

org = 'doer'
things = 'photo'

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd(f"/artifacts/{things}/{org}")
things_we_have = ftp.nlst()

things_we_need = [
'photo__Abdullah.Al.Maruf.png',
'photo__Abir.Ahmed.png',
'photo__Abu.Zahed.Md.Shamshed.png',
'photo__Ajoy.Kumar.Khan.png',
'photo__Amjad.Hossain.Polock.png',
'photo__Arun.Chakraborty.png',
'photo__Ashfaq.Inteser.png',
'photo__Ayesha.Siddika.png',
'photo__Ayesha.Siddiqa.Asha.png',
'photo__B.M.Ferdous.Mahmud.png',
'photo__Fahadul.Islam.Shimak.png',
'photo__Fahima.Rahman.png',
'photo__Faisal.Ahmed.Anik.png',
'photo__Farzana.Afrin.png',
'photo__Gaffar.Khan.png',
'photo__Hasibul.Hasan.Emon.png',
'photo__Imran.Howlader.png',
'photo__Ishrat.Fatima.png',
'photo__Ishtiak.Ahmed.png',
'photo__Istiak.Ahmed.png',
'photo__Jahin.Khan.Shourov.png',
'photo__Jashim.Uddin.Ahmed.png',
'photo__K.M.Anisur.Rahman.png',
'photo__Kanis.Fatema.Mariya.png',
'photo__Mahamudul.Hasan.png',
'photo__Mahmudul.Hasan.png',
'photo__Maria.Nurjahanara.Bhuiyan.png',
'photo__Md.Jafrul.Ahsan.png',
'photo__Md.Jahidul.Islam.png',
'photo__Md.Masud.Rana.(Tuhin).png',
'photo__Md.Sahidur.Rahman.png',
'photo__Md.Shamiul.Islam.png',
'photo__Md.Zillur.Rahman.png',
'photo__Md.Abdullah.Al.Salam.png',
'photo__Md.Abdus.Samad.Patwary.png',
'photo__Md.Arafat.Rahman.Sayed.png',
'photo__Md.Bodrul.Alam.png',
'photo__Md.Bony.Tasnim.Ibna.Razzak.png',
'photo__Md.Golam.Kibria.png',
'photo__Md.Habibur.Rahman.Tusher.png',
'photo__Md.Humayun.Kabir.(BDEx).png',
'photo__Md.Humayun.Kabir.(Software).png',
'photo__Md.Imtiaz.Mahmood.Sayed.png',
'photo__Md.Izadul.Ala.Ala.Baksh.png',
'photo__Md.Jalal.Uddin.png',
'photo__Md.Kamal.Parvez.png',
'photo__Md.Kamrul.Hasan.(BDEx).png',
'photo__Md.Kamrul.Islam.png',
'photo__Md.Kamruzzaman.png',
'photo__Md.Khaleque.Rakibul.Haque.png',
'photo__Md.Masum.Ahmmed.png',
'photo__Md.Mizanur.Rahman.png',
'photo__Md.Mokaddes.Hossain.Talukder.png',
'photo__Md.Moktadir.Hosan.png',
'photo__Md.Mokul.Arfan.png',
'photo__Md.Moniruzzaman.Liton.png',
'photo__Md.Nahhid.Uj.Jaman.Jisun.png',
'photo__Md.Noor-E-Alom.Siddique.png',
'photo__Md.Reasad.Islam.png',
'photo__Md.Rezaul.Karim.Sarker.png',
'photo__Md.Shabbir.Hossain.Bhuiya.png',
'photo__Md.Siam.Samad.Prantik.png',
'photo__Md.Sohan.Kabir.png',
'photo__Md.Tauhid.Amir.png',
'photo__Md.Thoufiq.Zumma.png',
'photo__Mithun.Kumar.Debnath.png',
'photo__Mohaiminul.Islam.png',
'photo__Mohammad.Abul.Hasnat.png',
'photo__Mohammad.Shahadat.Hossain.png',
'photo__Mohammad.Ziaul.Hoq.png',
'photo__Musaddiqur.Rahman.Ovi.png',
'photo__Ommul.Khair.Musammat.Tahera.png',
'photo__Palash.Kumar.Sinha.png',
'photo__Polas.Hossain.png',
'photo__Rafiqul.Islam.Reyad.png',
'photo__Rahana.Akter.png',
'photo__Rasheda.Akter.png',
'photo__Redwan.Al.Rashed.png',
'photo__Rizon.Ali.png',
'photo__Rubayat.Zaman.png',
'photo__Rubel.Ahammed.png',
'photo__S.M.Al-Amin.png',
'photo__Sabiha.Afrin.Bithee.png',
'photo__Salma.Afroze.png',
'photo__Sathe.Khan.Majlish.png',
'photo__Sayedthe.Kaniz.Fatema.png',
'photo__Shaikh.Insad.Ibney.Amin.png',
'photo__Shajidur.Rahman.Chowdury.png',
'photo__Shanawaz.Durjoy.png',
'photo__Subrata.Sanyal.png',
'photo__Sufia.Khanom.png',
'photo__Suman.Miah.png',
'photo__Sumshur.Rahman.png',
'photo__Syed.Ahmad.Mahdi.png',
'photo__Syed.Ahmad.Rasul.png',
'photo__Tanvir.Ahammed.Sobuj.png',
'photo__Tanvir.Ahmed.png',
'photo__Tanvir.Mallik.png',
'photo__Umme.Habiba.Rita.png',
]


print(f"we need {len(things_we_need)} {things}s for {org}")
print(f"we have {len(things_we_have)} {things}s for {org}")

# output_list = list(set(things_we_have).intersection(things_we_need))
# print(f"we have {len(output_list)} correct things")

# output_list = list(set(things_we_have) - set(things_we_need))
# print(f"we have {len(output_list)} extra/wrong things")

output_list = list(set(things_we_need) - set(things_we_have))
print(f"we have {len(output_list)} missing {things}s for {org}")

output_list.sort()
for i in range(0, len(output_list)):
    print(i+1, output_list[i])
