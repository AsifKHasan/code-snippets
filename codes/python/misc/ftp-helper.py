#!/usr/bin/env python3

import yaml
import ftplib
from pprint import pprint

# read ftp-helper.yml to get the list of things we need
helper_data = yaml.load(open('./ftp-helper.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
data = []
artifact = helper_data['artifact']
org = helper_data['org']
if 'level' in helper_data:
    ftp_directory = f"/artifacts/{artifact}/{org}/{helper_data['level']}/"
else:
    ftp_directory = f"/artifacts/{artifact}/{org}/"

things_we_need = helper_data['required-things']

# connect ftp
ftp = ftplib.FTP("ftp.spectrum-bd.biz")
ftp.login("spectrum@spectrum-bd.biz", "B@ngl@1427")

ftp.cwd(ftp_directory)
things_we_have = ftp.nlst()


# print(f"we need [{len(things_we_need)}] {artifact}s for [{org}]")
# print(f"we have [{len(things_we_have)}] {artifact}s for [{org}] in ftp [{ftp_directory}]")

# output_list = list(set(things_we_have).intersection(things_we_need))
# print(f"we have {len(output_list)} correct things")

# output_list = list(set(things_we_have) - set(things_we_need))
# print(f"we have {len(output_list)} extra/wrong things")

output_list = list(set(things_we_need) - set(things_we_have))
print(f"we have [{len(output_list)}] missing {artifact}s for [{org}] in ftp [{ftp_directory}]")

output_list.sort()
for i in range(0, len(output_list)):
    print(f"{i+1:>3}", output_list[i])
