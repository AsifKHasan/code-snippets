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
        self.type = 'outlet'



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'bank', 'outlet-urban', 'outlet-rural']]
        self.data = self.data.assign(total = self.data['outlet-rural'] + self.data['outlet-urban'])
        self.data = self.data.assign(outlet_ratio = self.data['outlet-rural'] / self.data['outlet-urban'])

        # merge banks with less than 2% of total outlets into Other Banks (for distribution)
        self.data_top_banks = self.data.copy()
        self.data_top_banks['new_code'] = np.where((self.data_top_banks.total / self.data_top_banks.total.sum() > 0.02), self.data_top_banks.code, "Other Banks")
        self.data_top_banks['new_bank'] = np.where((self.data_top_banks.total / self.data_top_banks.total.sum() > 0.02), self.data_top_banks.bank, "Other Banks")
        self.data_top_banks = self.data_top_banks.groupby([self.data_top_banks.new_code, self.data_top_banks.new_bank], as_index=False).agg({'total': 'sum', 'outlet-urban': 'sum', 'outlet-rural': 'sum'})
        self.data_top_banks.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        self.data_top_banks['explode'] = np.where(self.data_top_banks.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(
            self.data_top_banks.total, 
            labels=self.data_top_banks.code, 
            autopct='%1.2f%%',
            colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'mistyrose', 'azure', 'lavenderblush', 'honeydew', 'aliceblue'],
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=self.data_top_banks['explode'].tolist(),
            wedgeprops={'edgecolor': 'gray', 'linewidth': 1, 'antialiased': True}
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__distribution__by_bank__end-of__{self.config['last-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)



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
        p1 = (
            ggplot(
                self.data.nlargest(top_values_to_select, 'outlet_ratio'), 
                aes(x=x, y=y, color='code')
            ) +
            geom_point() +
            geom_segment(aes(x=x, xend=x, y=0, yend=y)) +
            geom_text(
                aes(label=y), size=10, angle=30, format_string="{:.2f}", nudge_x=0.3, nudge_y=0.3, 
                family="Arial", fontweight="light", fontstyle="normal"
            ) +
            scale_color_manual(values=colors) +
            guides(color = False, size = False) +
            xlab("Banks") +
            ylab("Rural/Urban outlet ratio") + 
            theme(
                figure_size=(10, 4),
                axis_text_x=element_text(family="Arial", weight="light", style="normal", size=10, color="black", angle=45, hjust=1)
            )
        )

        # save as image
        p1_path = f"{self.config['out-dir']}/{self.type}__comparison__by_ratio__top-banks__end-of__{self.config['last-quarter']}.png"
        p1.save(filename=p1_path, dpi=150, verbose=False)


        # bottom M banks
        p2 = (
            ggplot(
                self.data.nsmallest(bottom_values_to_select, 'outlet_ratio'), 
                aes(x=x, y=y)
            ) +
            geom_point() +
            geom_segment(aes(x=x, xend=x, y=0, yend=y)) +
            geom_text(
                aes(label=y), size=10, angle=30, format_string="{:.2f}", nudge_x=0.4, nudge_y=0.4, 
                family="Arial", fontweight="light", fontstyle="normal"
            ) +
            xlab("Banks") +
            ylab("Rural/Urban outlet ratio") +
            theme(
                figure_size=(10, 4),
                axis_text_x=element_text(family="Arial", weight="light", style="normal", size=10, color="black", angle=45, hjust=1)
            )
        )

        # save as image
        p2_path = f"{self.config['out-dir']}/{self.type}__comparison__by_ratio__bottom-banks__end-of__{self.config['last-quarter']}.png"
        p2.save(filename=p2_path, dpi=150, verbose=False)
