#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

''' deposit charts
'''
def deposit_charts_cumulative(data, config):

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

    p1_path = f"{config['out-dir']}/deposit__cumulative__top-banks.png"
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

    p1_path = f"{config['out-dir']}/deposit__cumulative__gender-ratio__top-banks.png"
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

    p2_path = f"{config['out-dir']}/deposit__cumulative__type-ratio__top-banks.png"
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

    p3_path = f"{config['out-dir']}/deposit__cumulative__location-ratio__top-banks.png"
    p3.save(filename=p3_path, dpi=150)
