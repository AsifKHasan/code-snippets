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
    def __init__(self, cumulative_data, period_data, config):
        super().__init__(cumulative_data=cumulative_data, period_data=period_data, config=config)
        self.type = 'outlet'



    ''' setup data
    '''
    def setup_data(self, cumulative_data, period_data):
        # rename columns
        dict = {
            'outlet_total' : 'total', 
            'outlet_urban' : 'urban', 
            'outlet_rural' : 'rural'
        }

        self.data_cumulative = cumulative_data[['outlet_total', 'outlet_urban', 'outlet_rural']]
        self.data_cumulative = self.data_cumulative.assign(outlet_ratio = self.data_cumulative.outlet_rural / self.data_cumulative.outlet_urban)
        self.data_cumulative = self.data_cumulative.rename(columns=dict)

        self.data_period = period_data[['outlet_total', 'outlet_urban', 'outlet_rural']]
        self.data_period = self.data_period.assign(outlet_ratio = self.data_period.outlet_rural / self.data_period.outlet_urban)
        self.data_period = self.data_period.rename(columns=dict)

        self.data_cumulative = self.data_cumulative.reset_index()
        self.data_period = self.data_period.reset_index()


        # merge banks with less than 2% of total outlets into Other Banks (for distribution)
        pct_threshold = 0.02
        self.data_cumulative_top_banks = self.data_cumulative.copy()
        self.data_cumulative_top_banks['new_code'] = np.where((self.data_cumulative_top_banks.total / self.data_cumulative_top_banks.total.sum() > pct_threshold), self.data_cumulative_top_banks.code, 'Other Banks')
        self.data_cumulative_top_banks['new_bank'] = np.where((self.data_cumulative_top_banks.total / self.data_cumulative_top_banks.total.sum() > pct_threshold), self.data_cumulative_top_banks.bank, 'Other Banks')
        self.data_cumulative_top_banks = self.data_cumulative_top_banks.groupby([self.data_cumulative_top_banks.new_code, self.data_cumulative_top_banks.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
        self.data_cumulative_top_banks.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)

        pct_threshold = 0.02
        self.data_period_top_banks = self.data_period.copy()
        self.data_period_top_banks['new_code'] = np.where((self.data_period_top_banks.total / self.data_period_top_banks.total.sum() > pct_threshold), self.data_period_top_banks.code, 'Other Banks')
        self.data_period_top_banks['new_bank'] = np.where((self.data_period_top_banks.total / self.data_period_top_banks.total.sum() > pct_threshold), self.data_period_top_banks.bank, 'Other Banks')
        self.data_period_top_banks = self.data_period_top_banks.groupby([self.data_period_top_banks.new_code, self.data_period_top_banks.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
        self.data_period_top_banks.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)


        print(self.data_cumulative)
        print(self.data_period)



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self, data_range):
        data = self.data_cumulative_top_banks if data_range == 'cumulative' else self.data_period_top_banks

        data = data[data.total > 0]
        explode = np.where(data.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(
            data.total, 
            labels=data.code, 
            autopct='%1.2f%%',
            colors=self.color_list,
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=explode,
            wedgeprops={'edgecolor': 'gray', 'linewidth': 1, 'antialiased': True}
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__distribution__by_bank__{data_range}__{self.config['current-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)



    ''' outlet ratio comparison (lollypop chart)
    '''
    def outlet_ratio_comparison(self, data_range):
        data = self.data_cumulative if data_range == 'cumulative' else self.data_period
        data = data.replace([np.inf, -np.inf], np.nan)
        data = data.dropna()
        data = data[data.outlet_ratio > 0]
        # print(data)

        # the axes
        x = 'code'
        y = 'outlet_ratio'

        top_values_to_select = 10
        bottom_values_to_select = len(data) - top_values_to_select

        color_dict = {'Agrani': '#5b0f00'}
        colors = {code: color_dict.get(code, '#434343') for code in data['code'].tolist()}
        # radius = {code: } for code in data['code'].tolist()}

        # top N banks
        p1 = (
            ggplot(
                data.nlargest(top_values_to_select, 'outlet_ratio'), 
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
            lims(y=(-10, None)) +
            theme(
                figure_size=(11.5, 5),
                axis_text_x=element_text(family="Arial", weight="light", style="normal", size=10, color="black", angle=45, hjust=1)
            )
        )

        # save as image
        p1_path = f"{self.config['out-dir']}/{self.type}__comparison__by_ratio__top-banks__{data_range}__{self.config['current-quarter']}.png"
        p1.save(filename=p1_path, dpi=150, verbose=False)


        # bottom M banks
        p2 = (
            ggplot(
                data.nsmallest(bottom_values_to_select, 'outlet_ratio'), 
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
            lims(y=(-10, None)) +
            theme(
                figure_size=(11.5, 5),
                axis_text_x=element_text(family="Arial", weight="light", style="normal", size=10, color="black", angle=45, hjust=1)
            )
        )

        # save as image
        p2_path = f"{self.config['out-dir']}/{self.type}__comparison__by_ratio__bottom-banks__{data_range}__{self.config['current-quarter']}.png"
        p2.save(filename=p2_path, dpi=150, verbose=False)
