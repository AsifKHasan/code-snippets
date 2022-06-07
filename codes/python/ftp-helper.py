#!/usr/bin/env python3

import ftplib
from pprint import pprint

org = 'doer'
things = 'signature'

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd(f"/artifacts/{things}/{org}")
things_we_have = ftp.nlst()

things_we_need = [
    'signature__Abdullah.Al.Maruf.png',
    'signature__Abir.Ahmed.png',
    'signature__Abu.Zahed.Md.Shamshed.png',
    'signature__Ajoy.Kumar.Khan.png',
    'signature__Amjad.Hossain.Polock.png',
    'signature__Arun.Chakraborty.png',
    'signature__Ashfaq.Inteser.png',
    'signature__Ayesha.Siddika.png',
    'signature__Ayesha.Siddiqa.Asha.png',
    'signature__B.M.Ferdous.Mahmud.png',
    'signature__Fahadul.Islam.Shimak.png',
    'signature__Fahima.Rahman.png',
    'signature__Faisal.Ahmed.Anik.png',
    'signature__Farzana.Afrin.png',
    'signature__Gaffar.Khan.png',
    'signature__Hasibul.Hasan.Emon.png',
    'signature__Imran.Howlader.png',
    'signature__Ishrat.Fatima.png',
    'signature__Ishtiak.Ahmed.png',
    'signature__Istiak.Ahmed.png',
    'signature__Jahin.Khan.Shourov.png',
    'signature__Jashim.Uddin.Ahmed.png',
    'signature__K.M.Anisur.Rahman.png',
    'signature__Kanis.Fatema.Mariya.png',
    'signature__Mahamudul.Hasan.png',
    'signature__Mahmudul.Hasan.png',
    'signature__Maria.Nurjahanara.Bhuiyan.png',
    'signature__Md.Jafrul.Ahsan.png',
    'signature__Md.Jahidul.Islam.png',
    'signature__Md.Masud.Rana.(Tuhin).png',
    'signature__Md.Sahidur.Rahman.png',
    'signature__Md.Shamiul.Islam.png',
    'signature__Md.Zillur.Rahman.png',
    'signature__Md.Abdullah.Al.Salam.png',
    'signature__Md.Abdus.Samad.Patwary.png',
    'signature__Md.Arafat.Rahman.Sayed.png',
    'signature__Md.Bodrul.Alam.png',
    'signature__Md.Bony.Tasnim.Ibna.Razzak.png',
    'signature__Md.Golam.Kibria.png',
    'signature__Md.Habibur.Rahman.Tusher.png',
    'signature__Md.Humayun.Kabir.(BDEx).png',
    'signature__Md.Humayun.Kabir.(Software).png',
    'signature__Md.Izadul.Ala.Ala.Baksh.png',
    'signature__Md.Jalal.Uddin.png',
    'signature__Md.Kamal.Parvez.png',
    'signature__Md.Kamrul.Hasan.(BDEx).png',
    'signature__Md.Kamrul.Islam.png',
    'signature__Md.Kamruzzaman.png',
    'signature__Md.Khaleque.Rakibul.Haque.png',
    'signature__Md.Masum.Ahmmed.png',
    'signature__Md.Mokaddes.Hossain.Talukder.png',
    'signature__Md.Moktadir.Hosan.png',
    'signature__Md.Mokul.Arfan.png',
    'signature__Md.Moniruzzaman.Liton.png',
    'signature__Md.Nahhid.Uj.Jaman.Jisun.png',
    'signature__Md.Noor-E-Alom.Siddique.png',
    'signature__Md.Reasad.Islam.png',
    'signature__Md.Rezaul.Karim.Sarker.png',
    'signature__Md.Shabbir.Hossain.Bhuiya.png',
    'signature__Md.Siam.Samad.Prantik.png',
    'signature__Md.Sohan.Kabir.png',
    'signature__Md.Tauhid.Amir.png',
    'signature__Md.Thoufiq.Zumma.png',
    'signature__Mithun.Kumar.Debnath.png',
    'signature__Mohaiminul.Islam.png',
    'signature__Mohammad.Abul.Hasnat.png',
    'signature__Mohammad.Shahadat.Hossain.png',
    'signature__Mohammad.Ziaul.Hoq.png',
    'signature__Musaddiqur.Rahman.Ovi.png',
    'signature__Ommul.Khair.Musammat.Tahera.png',
    'signature__Palash.Kumar.Sinha.png',
    'signature__Polas.Hossain.png',
    'signature__Rafiqul.Islam.Reyad.png',
    'signature__Rahana.Akter.png',
    'signature__Rasheda.Akter.png',
    'signature__Redwan.Al.Rashed.png',
    'signature__Rizon.Ali.png',
    'signature__Rubel.Ahammed.png',
    'signature__S.M.Al-Amin.png',
    'signature__Sabiha.Afrin.Bithee.png',
    'signature__Salma.Afroze.png',
    'signature__Sathe.Khan.Majlish.png',
    'signature__Sayedthe.Kaniz.Fatema.png',
    'signature__Shaikh.Insad.Ibney.Amin.png',
    'signature__Shajidur.Rahman.Chowdury.png',
    'signature__Shanawaz.Durjoy.png',
    'signature__Subrata.Sanyal.png',
    'signature__Sufia.Khanom.png',
    'signature__Suman.Miah.png',
    'signature__Sumshur.Rahman.png',
    'signature__Syed.Ahmad.Mahdi.png',
    'signature__Syed.Ahmad.Rasul.png',
    'signature__Tanvir.Ahammed.Sobuj.png',
    'signature__Tanvir.Ahmed.png',
    'signature__Tanvir.Mallik.png',
    'signature__Umme.Habiba.Rita.png',
    'signature__Md.Imtiaz.Mahmood.Sayed.png',
    'signature__Md.Mizanur.Rahman.png',
]


print(f"we need {len(things_we_need)} {things}s for {org}")
print(f"we have {len(things_we_have)} {things}s for {org}")

# output_list = list(set(things_we_have).intersection(things_we_need))
# print(f"we have {len(output_list)} correct things")

output_list = list(set(things_we_have) - set(things_we_need))
print(f"we have {len(output_list)} extra/wrong things")

# output_list = list(set(things_we_need) - set(things_we_have))
# print(f"we have {len(output_list)} missing {things}s for {org}")

output_list.sort()
for i in range(0, len(output_list)):
    print(i+1, output_list[i])
