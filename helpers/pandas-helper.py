#!/usr/bin/env python3
# @@
import pandas as pd
#import wordcloud
#from PIL import Image
#import matplotlib.pyplot as plt

print('hi')

# @@
df_data = {
    "type": ["Software", "Software", "Software", "Software", "Software", "Software", "Software", "Software", "Software", "Infrastructure", "Software", "Software", "Software", "Software", "Software", "Software"],
    "key": ["Template", "ROBI-ROC", "CCC-CSSM", "uniVerge", "NBR-BI", "SCB-CBRM", "CityAgent", "CIB", "BACP", "SCB-OPCCMS", "BB-RTGS", "UGC-HEMIS", "RHD-TDMS", "OCAG-AMMS", "OAGN-NAMS", "RHD-MIS"],
    "link-to-pds": ["Template__PDS", "PDS__ROBI-ROC", "PDS__CCC-CSSM", "PDS__uniVerge", "PDS__NBR-BI", "PDS__SCB-CBRM", "PDS__CityAgent", "PDS__CIB", "PDS__BACP", "PDS__SCB-OPCCMS", "PDS__BB-RTGS", "PDS__UGC-HEMIS", "PDS__RHD-TDMS", "PDS__OCAG-AMMS", "PDS__OAGN-NAMS", "PDS__RHD-MIS"]
}

df = pd.DataFrame.from_dict(df_data)
df = df.set_index('type')

# @@
#dg = df.groupby(['type'], as_index=True)['key', 'link-to-pds']
def dictify(df):
    df = df.set_index('key')
    return df.groupby(df.index)['link-to-pds'].apply(lambda x: x.values.tolist()).to_dict()

dd = df.groupby(df.index)['key', 'link-to-pds'].apply(lambda x: x.groupby('key')['link-to-pds'].apply(lambda x: x.values.tolist()).to_dict()).to_dict()

# @@
xl = pd.ExcelFile('./data/names-result.xlsx')
df = xl.parse(sheet_name='clusters', skiprows=2, header=None, usecols='B:E', names=['cluster_freq', 'cluster_name', 'member_freq', 'member_name'])
df.sort_values(['cluster_freq', 'member_freq'], ascending=[1, 1], inplace = True)
dl = [g for _, g in df.groupby(['cluster_freq', 'cluster_name'])]
dl = list(filter(lambda x: all(x['member_freq'] < x['cluster_freq']), dl))
dl = list(map(lambda x: pd.DataFrame({'name': x['member_name'].append(pd.Series(x['cluster_name'].iloc[0])), 'freq' : x['member_freq'].append(pd.Series(x['cluster_freq'].iloc[0]))}), dl))

df = dl[39]
df['freq'] = df['freq'].apply(math.log1p).apply(math.ceil)
df.set_index('name', drop=True, inplace=True)
d = df.to_dict(orient='dict')['freq']
namecloud = wordcloud.WordCloud(background_color="white", prefer_horizontal=1.0, colormap="tab10", mode="RGBA").generate_from_frequencies(d)
plt.imshow(namecloud, interpolation="bilinear")
plt.axis("off")
plt.show()




d[d.keys()[-1]]


d.apply(lambda x: x['freq'].apply(math.log1p).apply(math.ceil), axis=1)
d = list(map(lambda d: d['freq'].apply(math.log1p).apply(math.ceil) , dl))

d = list(map(lambda d: d['freq'].apply(math.log1p).apply(math.ceil) , dl))


df['expertise'] = df['expertise'].replace('#', '\#')
df.replace(to_replace='#', value='\#', regex=True)
df = xl.parse(sheet_name='projects-and-roles', skiprows=2, header=None, usecols='B:G', names=['project', 'description', 'role', 'task', 'from', 'to'])


df.apply(lambda r: r['project'].upper(), axis=1)
df.apply(lambda r: datetime.datetime.strftime(r['from'], '%Y-%b'), axis=1)
df.apply(lambda r: datetime.datetime.strftime(r['to'], '%Y-%b'), axis=1)


image = namecloud.to_image()
image.show()
