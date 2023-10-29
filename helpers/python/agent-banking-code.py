import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

data_path = "/home/asif/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"
# data_path = "D:/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"

image_dir = "/home/asif/Downloads"
# image_dir = "C:/Users/Asif/Downloads"

last_q = '2023-Q2'

theme_set(theme_538())

all_data = pd.read_csv(data_path, sep='\t', thousands=',')

# the latest data is the last quarter data
latest_data = all_data[all_data['quarter'] == last_q] 


###
# BEGIN Lending

lending_data = latest_data[['code', 'lending-urban', 'lending-rural', 'lending-male', 'lending-female', 'lending-othergender']]

# rename columns
dict = {
        'lending-urban' : 'urban', 
        'lending-rural' : 'rural', 
        'lending-male' : 'male', 
        'lending-female' : 'female', 
        'lending-othergender' : 'other'
    }
 
lending_data.rename(columns=dict, inplace=True)


# calculate total
lending_data["total"] = lending_data.rural + lending_data.urban

# merge less than 2% banks into Other Banks
lending_data["new_code"] = np.where((lending_data.total / lending_data.total.sum() > 0.02), lending_data.code, "Other Banks")
lending_data = lending_data.groupby(lending_data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum'})
lending_data.rename(columns={'new_code': 'code'}, inplace=True)

explode = (0.2, 0, 0, 0, 0, 0, 0)
fig, ax = plt.subplots()
ax.pie(lending_data.total, 
       labels=lending_data.code, 
       autopct='%1.2f%%',
       colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'yellow'],
    #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
       startangle=180,
       textprops={'size': 'smaller'}, 
       radius=1.4,
       explode=explode,
       wedgeprops = {"edgecolor":"gray", 
                    'linewidth': 1, 
                    'antialiased': True}
    )

p1_path = f"{image_dir}/lending__cumulative__top-banks.png"
fig.savefig(fname=p1_path, dpi=150)

fig.show()

# customer account distribution by banks
# pivot so that columns become rows
lending_data['rural'] = lending_data.rural / lending_data.total * 100
lending_data['urban'] = lending_data.urban / lending_data.total * 100
lending_data['male'] = lending_data.male / lending_data.total * 100
lending_data['female'] = lending_data.female / lending_data.total * 100
lending_data['other'] = lending_data.other / lending_data.total * 100
lending_pivot = pd.melt(lending_data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other'])


# https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
dodge_text = position_dodge(width=0.9)
ccolor = '#333333'

# location based
variables = ['rural', 'urban']
p1 = ggplot(
        lending_pivot[lending_pivot.variable.isin(variables) & (lending_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p1_path = f"{image_dir}/lending__cumulative__location-ratio__top-banks.png"
p1.save(filename=p1_path, dpi=150)

# gender based
variables = ['male', 'female', 'other']
p2 = ggplot(
        lending_pivot[lending_pivot.variable.isin(variables) & (lending_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p2_path = f"{image_dir}/lending__cumulative__gender-ratio__top-banks.png"
p2.save(filename=p2_path, dpi=150)

# END Lending
###


###
# BEGIN Deposit

deposit_data = latest_data[['code', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]

# rename columns
dict = {
        'deposit-urban' : 'urban', 
        'deposit-rural' : 'rural', 
        'deposit-male' : 'male', 
        'deposit-female' : 'female', 
        'deposit-othergender' : 'other', 
        'deposit-current' : 'current', 
        'deposit-savings' : 'savings', 
        'deposit-othertype' : 'others'
    }
 
deposit_data.rename(columns=dict, inplace=True)


# calculate total
deposit_data["total"] = deposit_data.rural + deposit_data.urban

# merge less than 2% banks into Other Banks
deposit_data["new_code"] = np.where((deposit_data.total / deposit_data.total.sum() > 0.02), deposit_data.code, "Other Banks")
deposit_data = deposit_data.groupby(deposit_data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
deposit_data.rename(columns={'new_code': 'code'}, inplace=True)

explode = (0.2, 0, 0, 0, 0, 0, 0)
fig, ax = plt.subplots()
ax.pie(deposit_data.total, 
       labels=deposit_data.code, 
       autopct='%1.2f%%',
       colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'yellow'],
    #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
       startangle=180,
       textprops={'size': 'smaller'}, 
       radius=1.4,
       explode=explode,
       wedgeprops = {"edgecolor":"gray", 
                    'linewidth': 1, 
                    'antialiased': True}
    )

p1_path = f"{image_dir}/deposit__cumulative__top-banks.png"
fig.savefig(fname=p1_path, dpi=150)

fig.show()

# customer account distribution by banks
# pivot so that columns become rows
deposit_data['rural'] = deposit_data.rural / deposit_data.total * 100
deposit_data['urban'] = deposit_data.urban / deposit_data.total * 100
deposit_data['male'] = deposit_data.male / deposit_data.total * 100
deposit_data['female'] = deposit_data.female / deposit_data.total * 100
deposit_data['other'] = deposit_data.other / deposit_data.total * 100
deposit_data['current'] = deposit_data.current / deposit_data.total * 100
deposit_data['savings'] = deposit_data.savings / deposit_data.total * 100
deposit_data['others'] = deposit_data.others / deposit_data.total * 100
deposit_pivot = pd.melt(deposit_data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


# https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
dodge_text = position_dodge(width=0.9)
ccolor = '#333333'

# gender based
variables = ['male', 'female', 'other']
p1 = ggplot(
        deposit_pivot[deposit_pivot.variable.isin(variables) & (deposit_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p1_path = f"{image_dir}/deposit__cumulative__gender-ratio__top-banks.png"
p1.save(filename=p1_path, dpi=150)


# account type based
variables = ['current', 'savings', 'others']
p2 = ggplot(
        deposit_pivot[deposit_pivot.variable.isin(variables) & (deposit_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p2_path = f"{image_dir}/deposit__cumulative__type-ratio__top-banks.png"
p2.save(filename=p2_path, dpi=150)


# location based
variables = ['rural', 'urban']
p3 = ggplot(
        deposit_pivot[deposit_pivot.variable.isin(variables) & (deposit_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p3_path = f"{image_dir}/deposit__cumulative__location-ratio__top-banks.png"
p3.save(filename=p3_path, dpi=150)

# END Deposit
###


###
# BEGIN Customer Accounts

accounts_data = latest_data[['code',  'account-urban', 'account-rural', 'account-male', 'account-female', 'account-othergender', 'account-current', 'account-savings', 'account-othertype']]

# rename columns
dict = {
        'account-urban' : 'urban', 
        'account-rural' : 'rural', 
        'account-male' : 'male', 
        'account-female' : 'female', 
        'account-othergender' : 'other', 
        'account-current' : 'current', 
        'account-savings' : 'savings', 
        'account-othertype' : 'others'
    }
 
accounts_data.rename(columns=dict, inplace=True)


# calculate total
accounts_data["total"] = accounts_data.rural + accounts_data.urban

# merge less than 2% banks into Other Banks
accounts_data["new_code"] = np.where((accounts_data.total / accounts_data.total.sum() > 0.02), accounts_data.code, "Other Banks")
accounts_data = accounts_data.groupby(accounts_data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
accounts_data.rename(columns={'new_code': 'code'}, inplace=True)

explode = (0.2, 0, 0, 0, 0, 0)
fig, ax = plt.subplots()
ax.pie(accounts_data.total, 
       labels=accounts_data.code, 
       autopct='%1.2f%%',
       colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue'],
    #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
       startangle=180,
       textprops={'size': 'smaller'}, 
       radius=1.4,
       explode=explode,
       wedgeprops = {"edgecolor":"gray", 
                    'linewidth': 1, 
                    'antialiased': True}
    )

p1_path = f"{image_dir}/accounts__cumulative__top-banks.png"
fig.savefig(fname=p1_path, dpi=150)

fig.show()

# customer account distribution by banks
# pivot so that columns become rows
accounts_data['rural'] = accounts_data.rural / accounts_data.total * 100
accounts_data['urban'] = accounts_data.urban / accounts_data.total * 100
accounts_data['male'] = accounts_data.male / accounts_data.total * 100
accounts_data['female'] = accounts_data.female / accounts_data.total * 100
accounts_data['other'] = accounts_data.other / accounts_data.total * 100
accounts_data['current'] = accounts_data.current / accounts_data.total * 100
accounts_data['savings'] = accounts_data.savings / accounts_data.total * 100
accounts_data['others'] = accounts_data.others / accounts_data.total * 100
accounts_pivot = pd.melt(accounts_data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


# https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
dodge_text = position_dodge(width=0.9)
ccolor = '#333333'

# gender based
variables = ['male', 'female', 'other']
p1 = ggplot(
        accounts_pivot[accounts_pivot.variable.isin(variables) & (accounts_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 70)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p1_path = f"{image_dir}/accounts__cumulative__gender-ratio__top-banks.png"
p1.save(filename=p1_path, dpi=150)


# account type based
variables = ['current', 'savings', 'others']
p2 = ggplot(
        accounts_pivot[accounts_pivot.variable.isin(variables) & (accounts_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p2_path = f"{image_dir}/accounts__cumulative__type-ratio__top-banks.png"
p2.save(filename=p2_path, dpi=150)


# location based
variables = ['rural', 'urban']
p3 = ggplot(
        accounts_pivot[accounts_pivot.variable.isin(variables) & (accounts_pivot.value > 0)], 
        aes(x='code', y='value', fill='variable')
    ) + \
    geom_col(
        stat='identity', 
        position='dodge', 
        show_legend=False
    ) + \
    geom_text(
        aes(y=-.5, label='variable'),
        position=dodge_text,
        color=ccolor, 
        size=8, 
        angle=45, 
        va='top'
    ) + \
    geom_text(
        aes(label='value'),
        position=dodge_text,
        size=6, 
        va='bottom', 
        format_string='{:.1f}%'
    ) + \
    lims(
        y=(-5, 100)
    ) + \
    scale_fill_manual(
        values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
    ) + \
    theme(
        # panel_background=element_rect(fill='white'),
        axis_title_y=element_blank(),
        axis_line_y=element_blank(),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        axis_title_x=element_blank(),
        axis_line_x=element_line(color='black'),
        axis_text_x=element_text(color=ccolor),
        panel_grid=element_blank(),
        panel_border=element_blank()
    )

p3_path = f"{image_dir}/accounts__cumulative__location-ratio__top-banks.png"
p3.save(filename=p3_path, dpi=150)

# END Customer Accounts
###


###
# BEGIN Rural/Urban outlet ratio
data = latest_data[['code', 'outlet-urban', 'outlet-rural']]
data["outlet-ratio"] = data['outlet-rural'] / data['outlet-urban']

# the axes
x = 'code'
y = 'outlet-ratio'

top_values_to_select = 10
bottom_values_to_select = len(data) - top_values_to_select

color_dict = {'Agrani': '#5b0f00'}
colors = {code: color_dict.get(code, '#434343') for code in data['code'].tolist()}
# radius = {code:  for code in data['code'].tolist()}

# top N banks
p1 = ggplot(
        data.nlargest(top_values_to_select, 'outlet-ratio'), 
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
p1_path = f"{image_dir}/outlet-ratio__cumulative__top-{top_values_to_select}-banks.png"
p1.save(filename=p1_path)


# bottom M banks
p2 = ggplot(
        data.nsmallest(bottom_values_to_select, 'outlet-ratio'), 
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
p2_path = f"{image_dir}/outlet-ratio__cumulative__bottom-{bottom_values_to_select}-banks.png"
p2.save(filename=p2_path)
# END Rural/Urban outlet ratio
###


