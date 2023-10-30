#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

''' lending charts
'''
def lending_charts_cumulative(data, config):

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

    p1_path = f"{config['out-dir']}/lending__cumulative__top-banks.png"
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

    p1_path = f"{config['out-dir']}/lending__cumulative__location-ratio__top-banks.png"
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

    p2_path = f"{config['out-dir']}/lending__cumulative__gender-ratio__top-banks.png"
    p2.save(filename=p2_path, dpi=150)
