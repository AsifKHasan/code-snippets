#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

from chart.chart_base import ChartBase

from helper.logger import *


class OutletChart(ChartBase):

    ''' constructor
    '''
    def __init__(self, data, config):
        super().__init__(data=data, config=config)



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'outlet-urban', 'outlet-rural']]
        self.data = self.data.assign(outlet_ratio = self.data['outlet-rural'] / self.data['outlet-urban'])



    ''' outlet ratio comparison (lollypop chart)
    '''
    def outlet_ratio_comparison(self):

        # the axes
        x = 'code'
        y = 'outlet_ratio'

        top_values_to_select = 10
        bottom_values_to_select = len(self.data) - top_values_to_select

        color_dict = {'Agrani': '#5b0f00'}
        colors = {code: color_dict.get(code, '#434343') for code in self.data['code'].tolist()}
        # radius = {code:  for code in self.data['code'].tolist()}

        # top N banks
        p1 = ggplot(
                self.data.nlargest(top_values_to_select, 'outlet_ratio'), 
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

        p1 = p1 + \
            theme(
                    axis_text_x=element_text(family="Arial", weight="light", style="normal", size=8, color="black", angle=45, hjust=1)
                ) + \
            xlab("Banks") + \
            ylab("Rural/Urban outlet ratio")

        # save as image
        p1_path = f"{self.config['out-dir']}/outlet-ratio__comparison__top-banks__end-of__{self.config['last-quarter']}.png"
        p1.save(filename=p1_path, dpi=150, verbose=False)


        # bottom M banks
        p2 = ggplot(
                self.data.nsmallest(bottom_values_to_select, 'outlet_ratio'), 
                aes(x=x, y=y)
            ) + \
            geom_point() + \
            geom_segment(aes(x=x, xend=x, y=0, yend=y)) + \
            geom_text(
                aes(label=y), size=6, angle=30, format_string="{:.2f}", nudge_x=0.3, nudge_y=0.3, 
                family="Arial", fontweight="light", fontstyle="normal"
            )

        p2 = p2 + \
            theme(
                axis_text_x=element_text(family="Arial", weight="light", style="normal", size=7, color="black", angle=45, hjust=1)
            ) + \
            xlab("Banks") + \
            ylab("Rural/Urban outlet ratio")

        # save as image
        p2_path = f"{self.config['out-dir']}/outlet-ratio__comparison__bottom-banks__end-of__{self.config['last-quarter']}.png"
        p2.save(filename=p2_path, dpi=150, verbose=False)
