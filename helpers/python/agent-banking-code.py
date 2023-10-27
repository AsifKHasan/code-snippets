import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# data_path = "/home/asif/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"
data_path = "D:/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"

image_dir = "C:/Users/Asif/Downloads"

last_q = '2023-Q2'


theme_set(theme_538())

all_data = pd.read_csv(data_path, sep='\t', thousands=',')

# the latest data is the last quarter data
latest_data = all_data[all_data['quarter'] == last_q] 

###
# BEGIN Customer Accounts

data = latest_data[['code',  'accounts-urban', 'accounts-rural', 'accounts-male', 'accounts-female', 'accounts-othergender', 'accounts-current', 'accounts-saving', 'accounts-othertype']]
# calculate accounts-total
data["accounts_total"] = data['accounts-rural'] + data['accounts-urban']

# merge less than 2% banks into Other Banks
data["new_code"] = np.where((data.accounts_total / data.accounts_total.sum() > 0.02), data["code"], "Other Banks")
new_data = data.groupby(data.new_code)["accounts_total"].agg(accounts_total='sum')
new_data.reset_index(names="code", inplace=True)

explode = (0.2, 0, 0, 0, 0, 0)
fig, ax = plt.subplots()
ax.pie(new_data.accounts_total, 
       labels=new_data.code, 
       autopct='%1.2f%%',
       colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue'],
    #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
       startangle=180,
       textprops={'size': 'smaller'}, 
       radius=1.5,
       explode=explode,
       wedgeprops = {"edgecolor":"gray", 
                    'linewidth': 1, 
                    'antialiased': True}
    )

p1_path = f"{image_dir}/accounts__cumulative__top-banks.png"
fig.savefig(p1_path)

fig.show()

# END Customer Accounts
###


###
# BEGIN Rural/Urban outlet ratio
data = latest_data[['code', 'outlets-urban', 'outlets-rural']]
data["outlets-ratio"] = data['outlets-rural'] / data['outlets-urban']

# the axes
x = 'code'
y = 'outlets-ratio'

top_values_to_select = 10
bottom_values_to_select = len(data) - top_values_to_select

color_dict = {'Agrani': '#5b0f00'}
colors = {code: color_dict.get(code, '#434343') for code in data['code'].tolist()}
# radius = {code:  for code in data['code'].tolist()}

# top N banks
p1 = ggplot(
        data.nlargest(top_values_to_select, 'outlets-ratio'), 
        aes(x=x, y=y, color='code')
    ) + \
    geom_point() + \
    geom_segment(aes(x=x, xend=x, y=0, yend=y)) + \
    geom_text(
        aes(label=y), size=7, angle=30, format_string="{:.2f}", nudge_x=0.3, nudge_y=5, 
        family="Arial", fontweight="light", fontstyle="normal"
    ) + \
    scale_color_manual(values=colors) + \
    guides(color = False, size = False)

p1 = p1 + theme(
            axis_text_x=element_text(family="Arial", weight="light", style="normal", size=8, color="black", angle=45, hjust=1)
        ) + \
    xlab("Banks") + \
    ylab("Rural/Urban outlet ratio")

# save as image
p1_path = f"{image_dir}/outlets-ratio__cumulative__top-{top_values_to_select}-banks.png"
p1.save(filename=p1_path)


# bottom M banks
p2 = ggplot(
        data.nsmallest(bottom_values_to_select, 'outlets-ratio'), 
        aes(x=x, y=y)
    ) + \
    geom_point() + \
    geom_segment(aes(x=x, xend=x, y=0, yend=y)) + \
    geom_text(
        aes(label=y), size=6, angle=30, format_string="{:.2f}", nudge_x=0.3, nudge_y=0.3, 
        family="Arial", fontweight="light", fontstyle="normal"
    )

p2 = p2 + theme(
            axis_text_x=element_text(family="Arial", weight="light", style="normal", size=7, color="black", angle=45, hjust=1)
        ) + \
        xlab("Banks") + \
        ylab("Rural/Urban outlet ratio")

# save as image
p2_path = f"{image_dir}/outlets-ratio__cumulative__bottom-{bottom_values_to_select}-banks.png"
p2.save(filename=p2_path)
# END Rural/Urban outlet ratio
###


