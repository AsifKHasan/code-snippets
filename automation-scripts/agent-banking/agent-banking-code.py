#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# CSV_PATH = "/home/asif/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"
CSV_PATH = "D:/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"

# IMAGE_DIR = "/home/asif/Downloads"
IMAGE_DIR = "C:/Users/Asif/Downloads"


''' account charts
'''
def account_charts_cumulative(latest_data):
    data = latest_data[['code',  'account-urban', 'account-rural', 'account-male', 'account-female', 'account-othergender', 'account-current', 'account-savings', 'account-othertype']]

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
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge banks with less than 2% of total accounts into Other Banks
    data["new_code"] = np.where((data.total / data.total.sum() > 0.02), data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    data['explode'] = np.where(data.code == 'Agrani', 0.2, 0)
    fig, ax = plt.subplots()
    ax.pie(data.total, 
        labels=data.code, 
        autopct='%1.2f%%',
        colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue'],
        #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
        startangle=180,
        textprops={'size': 'smaller'}, 
        radius=1.4,
        explode=data['explode'].tolist(),
        wedgeprops = {"edgecolor":"gray", 
                        'linewidth': 1, 
                        'antialiased': True}
        )

    p1_path = f"{IMAGE_DIR}/accounts__cumulative__top-banks.png"
    fig.savefig(fname=p1_path, dpi=150)

    # fig.show()

    # customer account distribution by banks
    # pivot so that columns become rows
    data['rural'] = data.rural / data.total * 100
    data['urban'] = data.urban / data.total * 100
    data['male'] = data.male / data.total * 100
    data['female'] = data.female / data.total * 100
    data['other'] = data.other / data.total * 100
    data['current'] = data.current / data.total * 100
    data['savings'] = data.savings / data.total * 100
    data['others'] = data.others / data.total * 100
    pivot_data = pd.melt(data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


    # https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    dodge_text = position_dodge(width=0.9)
    ccolor = '#333333'

    # gender based
    variables = ['male', 'female', 'other']
    p1 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p1_path = f"{IMAGE_DIR}/accounts__cumulative__gender-ratio__top-banks.png"
    p1.save(filename=p1_path, dpi=150)


    # account type based
    variables = ['current', 'savings', 'others']
    p2 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p2_path = f"{IMAGE_DIR}/accounts__cumulative__type-ratio__top-banks.png"
    p2.save(filename=p2_path, dpi=150)


    # location based
    variables = ['rural', 'urban']
    p3 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p3_path = f"{IMAGE_DIR}/accounts__cumulative__location-ratio__top-banks.png"
    p3.save(filename=p3_path, dpi=150)



''' deposit charts
'''
def deposit_charts_cumulative(latest_data):
    data = latest_data[['code', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]

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
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where((data.total / data.total.sum() > 0.02), data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    data['explode'] = np.where(data.code == 'Agrani', 0.2, 0)
    fig, ax = plt.subplots()
    ax.pie(data.total, 
        labels=data.code, 
        autopct='%1.2f%%',
        colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'yellow'],
        #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
        startangle=180,
        textprops={'size': 'smaller'}, 
        radius=1.4,
        explode=data['explode'].tolist(),
        wedgeprops = {"edgecolor":"gray", 
                        'linewidth': 1, 
                        'antialiased': True}
        )

    p1_path = f"{IMAGE_DIR}/deposit__cumulative__top-banks.png"
    fig.savefig(fname=p1_path, dpi=150)

    # fig.show()

    # customer account distribution by banks
    # pivot so that columns become rows
    data['rural'] = data.rural / data.total * 100
    data['urban'] = data.urban / data.total * 100
    data['male'] = data.male / data.total * 100
    data['female'] = data.female / data.total * 100
    data['other'] = data.other / data.total * 100
    data['current'] = data.current / data.total * 100
    data['savings'] = data.savings / data.total * 100
    data['others'] = data.others / data.total * 100
    pivot_data = pd.melt(data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


    # https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    dodge_text = position_dodge(width=0.9)
    ccolor = '#333333'

    # gender based
    variables = ['male', 'female', 'other']
    p1 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p1_path = f"{IMAGE_DIR}/deposit__cumulative__gender-ratio__top-banks.png"
    p1.save(filename=p1_path, dpi=150)


    # account type based
    variables = ['current', 'savings', 'others']
    p2 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p2_path = f"{IMAGE_DIR}/deposit__cumulative__type-ratio__top-banks.png"
    p2.save(filename=p2_path, dpi=150)


    # location based
    variables = ['rural', 'urban']
    p3 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p3_path = f"{IMAGE_DIR}/deposit__cumulative__location-ratio__top-banks.png"
    p3.save(filename=p3_path, dpi=150)



''' lending charts
'''
def lending_charts_cumulative(latest_data):
    data = latest_data[['code', 'lending-urban', 'lending-rural', 'lending-male', 'lending-female', 'lending-othergender']]

    # rename columns
    dict = {
            'lending-urban' : 'urban', 
            'lending-rural' : 'rural', 
            'lending-male' : 'male', 
            'lending-female' : 'female', 
            'lending-othergender' : 'other'
        }
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where(data.total > 100.00, data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    new_data = data.sample(frac=1)
    new_data['explode'] = np.where(new_data.total > 500.00, 0, 0.3)

    fig, ax = plt.subplots()
    ax.pie(new_data.total, 
        labels=new_data.code, 
        autopct='%1.2f%%',
        colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'mistyrose', 'azure', 'lavenderblush', 'honeydew', 'aliceblue'],
        #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
        startangle=0,
        textprops={'size': 'smaller'}, 
        radius=1.2,
        explode=new_data["explode"].tolist(),
        wedgeprops = {"edgecolor":"gray", 
                        'linewidth': 1, 
                        'antialiased': True}
        )

    p1_path = f"{IMAGE_DIR}/lending__cumulative__top-banks.png"
    fig.savefig(fname=p1_path, dpi=150)

    # fig.show()

    # customer account distribution by banks
    # pivot so that columns become rows
    data['rural'] = data.rural / data.total * 100
    data['urban'] = data.urban / data.total * 100
    data['male'] = data.male / data.total * 100
    data['female'] = data.female / data.total * 100
    data['other'] = data.other / data.total * 100
    pivot_data = pd.melt(data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other'])


    # https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    dodge_text = position_dodge(width=0.9)
    ccolor = '#333333'

    # location based
    variables = ['rural', 'urban']
    p1 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p1_path = f"{IMAGE_DIR}/lending__cumulative__location-ratio__top-banks.png"
    p1.save(filename=p1_path, dpi=150)

    # gender based
    variables = ['male', 'female', 'other']
    p2 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p2_path = f"{IMAGE_DIR}/lending__cumulative__gender-ratio__top-banks.png"
    p2.save(filename=p2_path, dpi=150)



''' remittance charts
'''
def remittance_charts_cumulative(latest_data):
    data = latest_data[['code', 'remittance-urban', 'remittance-rural']]

    # rename columns
    dict = {
            'remittance-urban' : 'urban', 
            'remittance-rural' : 'rural'
        }
    
    data.rename(columns=dict, inplace=True)

    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where(data.total > 10000.00, data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    data['explode'] = np.where(data.code == 'Agrani', 0.2, 0)
    fig, ax = plt.subplots()
    ax.pie(data.total, 
        labels=data.code, 
        autopct='%1.2f%%',
        colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'mistyrose', 'azure', 'lavenderblush', 'honeydew', 'aliceblue'],
        #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
        startangle=180,
        textprops={'size': 'smaller'}, 
        radius=1.4,
        explode=data['explode'].tolist(),
        wedgeprops = {"edgecolor":"gray", 
                        'linewidth': 1, 
                        'antialiased': True}
        )

    p1_path = f"{IMAGE_DIR}/remittance__cumulative__top-banks.png"
    fig.savefig(fname=p1_path, dpi=150)

    # fig.show()

    # customer account distribution by banks
    # pivot so that columns become rows
    data['rural'] = data.rural / data.total * 100
    data['urban'] = data.urban / data.total * 100
    pivot_data = pd.melt(data, id_vars=['code'], value_vars=['urban', 'rural'])


    # https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    dodge_text = position_dodge(width=0.9)
    ccolor = '#333333'

    # location based
    variables = ['rural', 'urban']
    p1 = ggplot(
            pivot_data[pivot_data.variable.isin(variables) & (pivot_data.value > 0)], 
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

    p1_path = f"{IMAGE_DIR}/remittance__cumulative__location-ratio__top-banks.png"
    p1.save(filename=p1_path, dpi=150)



''' outlet ratio
'''
def outlet_ratio_cumulative(latest_data):
    data = latest_data[['code', 'outlet-urban', 'outlet-rural']]
    data['outlet-ratio'] = data['outlet-rural'] / data['outlet-urban']

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
    p1_path = f"{IMAGE_DIR}/outlet-ratio__cumulative__top-{top_values_to_select}-banks.png"
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
    p2_path = f"{IMAGE_DIR}/outlet-ratio__cumulative__bottom-{bottom_values_to_select}-banks.png"
    p2.save(filename=p2_path)



''' ggplot theme setup
'''
def setup_theme():
    theme_set(theme_538())



''' read data from csv file
'''
def read_csv_data(csv_path):
    return pd.read_csv(csv_path, sep='\t', thousands=',')



if __name__ == '__main__':
    all_data = read_csv_data(csv_path=CSV_PATH)
    setup_theme()

    # cumulative report upto a qyarter end
    LAST_Q = '2023-Q2'
    latest_data = all_data[all_data.quarter == LAST_Q] 

    account_charts_cumulative(latest_data=latest_data)
    deposit_charts_cumulative(latest_data=latest_data)
    lending_charts_cumulative(latest_data=latest_data)
    remittance_charts_cumulative(latest_data=latest_data)
    outlet_ratio_cumulative(latest_data=latest_data)
