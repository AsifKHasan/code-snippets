#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

''' outlet ratio
'''
def outlet_ratio_cumulative(input_data, config):
    data = input_data[['code', 'outlet-urban', 'outlet-rural']]
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
    p1_path = f"{config['out-dir']}/outlet-ratio__cumulative__top-{top_values_to_select}-banks.png"
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
    p2_path = f"{config['out-dir']}/outlet-ratio__cumulative__bottom-{bottom_values_to_select}-banks.png"
    p2.save(filename=p2_path)
