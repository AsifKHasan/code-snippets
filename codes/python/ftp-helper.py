#!/usr/bin/env python3

import ftplib
from pprint import pprint

org = 'ael'
things = 'signature'

# things we have
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

data = []
ftp.cwd(f"/artifacts/{things}/{org}")
things_we_have = ftp.nlst()

things_we_need = [
    'signature__Asadul.Haque.png', 'signature__Asif.Yusuf.png', 'signature__Assaduzzaman.png', 'signature__Dipankar.Kumar.Biswas.png', 'signature__Iqbal.Yusuf.png', 'signature__Md.Nasir.Uddin.png', 'signature__Md.Ahsan.Habib.Rocky.png', 'signature__Md.Atikur.Zaman.png', 'signature__Md.Faisal.Hossain.png', 'signature__Md.Mijanur.Rahman.png', 'signature__Md.Nahidul.Islam.Siddique.png', 'signature__Md.Sohel.Rana.png', 'signature__Md.Yousuf.Ali.png', 'signature__Mir.Erfan.Elahi.png', 'signature__Salman.Ahmed.Firoz.png', 'signature__Suday.Kumer.Ghosh.png', 'signature__Tanvir.Rahman.png'
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
