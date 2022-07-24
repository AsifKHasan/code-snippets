#!/usr/bin/env python3

import ftplib
from pprint import pprint

org = 'celloscope'
things = 'signature'

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd(f"/artifacts/{things}/{org}")
things_we_have = ftp.nlst()

things_we_need = [
'signature__Ahmed.Nafis.Fuad.png', 
'signature__Alif.Arfab.Pavel.png', 
'signature__Altaf.Hossain.png', 
'signature__Amiya.Ahamed.png', 
'signature__Arnab.Basak.png', 
'signature__Asiya.Khatun.(Papiya).png', 
'signature__Deboraj.Saha.png', 
'signature__Dip.Chowdhury.png', 
'signature__Farhana.Naz.png', 
'signature__Kamrun.Nahar.png', 
'signature__Kazi.Taqi.Tahmid.png', 
'signature__Khondoker.Tanvir.Hossain.png', 
'signature__Mainur.Rahman.Rasel.png', 
'signature__Maly.Mohsem.Ahmed.png', 
'signature__Md.Abu.Yousuf.Sajal.png', 
'signature__Md.Asif.Khan.Taj.png', 
'signature__MD.Fuad.Hasan.Chowdhury.png', 
'signature__Md.Hafizur.Rahman.png', 
'signature__Md.Jamal.Uddin.png', 
'signature__Md.Kamruzzaman.Tanim.png', 
'signature__Md.Naim.Reza.png', 
'signature__Md.Nazmul.Alam.png', 
'signature__Md.Samiul.Alim.png', 
'signature__Md.Shariar.Kabir.png', 
'signature__Mehedi.Hasan.png', 
'signature__Mohammad.Kamrul.Hasan.png', 
'signature__Mohammad.Mashud.Karim.png', 
'signature__Mohammad.Wakib.Hasan.png', 
'signature__Murshida.Mushfique.png', 
'signature__Mushfika.Faria.png', 
'signature__Nasima.Aktar.png', 
'signature__Rashida.Akter.png', 
'signature__Shafayat.Ahmed.png', 
'signature__Shah.Shafi.Mohammed.Shariful.Alam.png', 
'signature__Sharif.Tamjidur.Rahman.png', 
'signature__Syed.Mostofa.Monsur.png', 
'signature__Umme.Rumman.Usha.png', 
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
