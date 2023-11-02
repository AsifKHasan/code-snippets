#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

from chart.chart_base import ChartBase

from helper.logger import *


class RemittanceChart(ChartBase):

    ''' constructor
    '''
    def __init__(self, current_data, previous_data, config):
        super().__init__(current_data=current_data, previous_data=previous_data, config=config)
        self.type = 'remittance'



    ''' setup data
    '''
    def setup_data(self, current_data, previous_data):
        self.data_current = current_data[['code', 'bank', 'outlet-urban', 'outlet-rural', 'remittance-urban', 'remittance-rural']]

        # rename columns
        dict = {
                'outlet-urban' : 'urban_outlets', 
                'outlet-rural' : 'rural_outlets', 
                'remittance-urban' : 'urban', 
                'remittance-rural' : 'rural'
            }
        
        self.data_current = self.data_current.rename(columns=dict)

        # calculate total
        self.data_current['total_outlets'] = self.data_current.urban_outlets + self.data_current.rural_outlets
        self.data_current["total"] = self.data_current.rural + self.data_current.urban


        # per outlet data
        self.data_current_per_outlet = pd.DataFrame()
        self.data_current_per_outlet['code'] = self.data_current['code']
        self.data_current_per_outlet['bank'] = self.data_current['bank']
        self.data_current_per_outlet['total'] = self.data_current['total'] / self.data_current['total_outlets']
        self.data_current_per_outlet['rural'] = self.data_current['rural'] / self.data_current['rural_outlets']
        self.data_current_per_outlet['urban'] = self.data_current['urban'] / self.data_current['urban_outlets']
        # self.data_current_per_outlet = self.data_current_per_outlet.round()

        # keep the top N
        top_n = 8
        self.data_current_per_outlet = self.data_current_per_outlet.nlargest(top_n, 'total')
        self.data_current_per_outlet = pd.melt(self.data_current_per_outlet, id_vars=['code', 'bank'], value_vars=['total', 'urban', 'rural'])


        # merge less than 2% banks into Other Banks
        self.data_current["new_code"] = np.where(self.data_current.total > 10000.00, self.data_current.code, "Other Banks")
        self.data_current["new_bank"] = np.where(self.data_current.total > 10000.00, self.data_current.code, "Other Banks")
        self.data_current = self.data_current.groupby([self.data_current.new_code, self.data_current.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
        self.data_current = self.data_current.rename(columns={'new_code': 'code', 'new_bank': 'bank'})


        # pivot so that columns become rows
        self.data_current_in_percent = self.data_current
        self.data_current_in_percent['rural'] = self.data_current_in_percent.rural / self.data_current_in_percent.total * 100
        self.data_current_in_percent['urban'] = self.data_current_in_percent.urban / self.data_current_in_percent.total * 100
        self.data_current_in_percent = pd.melt(self.data_current_in_percent, id_vars=['code', 'bank'], value_vars=['urban', 'rural'])



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self, data_range):

        self.data_current['explode'] = np.where(self.data_current.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(
            self.data_current.total, 
            labels=self.data_current.code, 
            autopct='%1.2f%%',
            colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'mistyrose', 'azure', 'lavenderblush', 'honeydew', 'aliceblue'],
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=self.data_current['explode'].tolist(),
            wedgeprops={'edgecolor': 'gray', 'linewidth': 1, 'antialiased': True}
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__distribution__by_bank__{data_range}__{self.config['current-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)



    ''' comparison by location (percent bar chart)
    '''
    def comparison_by_location(self, data_range):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        # location based
        variables = ['rural', 'urban']
        chart = (
            ggplot(
                self.data_current_in_percent[self.data_current_in_percent.variable.isin(variables) & (self.data_current_in_percent.value > 0)], 
                aes(x='code', y='value', fill='variable')
            ) +
            geom_col(
                stat='identity', 
                position='dodge', 
                show_legend=False
            ) +
            geom_text(
                aes(y=-.5, label='variable'),
                position=dodge_text,
                color=ccolor, 
                size=10, 
                angle=45, 
                va='top'
            ) +
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=10, 
                va='bottom', 
                format_string='{:.1f}%'
            ) +
            scale_fill_manual(values=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']) +
            lims(y=(-10, None)) +
            theme(
                # panel_background=element_rect(fill='white'),
                figure_size=(11.5, 8.5),
                axis_title_y=element_blank(),
                axis_line_y=element_blank(),
                axis_text_y=element_blank(),
                axis_ticks_major_y=element_blank(),
                axis_title_x=element_blank(),
                axis_line_x=element_line(color='black'),
                axis_text_x=element_text(color=ccolor, size=14),
                panel_grid=element_blank(),
                panel_border=element_blank()
            )
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_location__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by location (bar chart)
    '''
    def per_outlet_comparison_by_location(self, data_range):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban', 'total']
        data = self.data_current_per_outlet[self.data_current_per_outlet.variable.isin(variables) & (self.data_current_per_outlet.value > 0)]

        chart = (
            ggplot(
                data, 
                aes(x='code', y='value', fill='variable')
            ) +
            geom_col(
                stat='identity', 
                position='dodge', 
                show_legend=False
            ) +
            geom_text(
                aes(y=-.5, label='variable'),
                position=dodge_text,
                color=ccolor, 
                size=11, 
                angle=45, 
                va='top'
            ) +
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=8, 
                va='bottom', 
                format_string='{:.2f}'
            ) +
            scale_fill_manual(values=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']) +
            lims(y=(-30, None)) +
            theme(
                # panel_background=element_rect(fill='white'),
                figure_size=(12, 8),
                axis_title_y=element_blank(),
                axis_line_y=element_blank(),
                axis_text_y=element_blank(),
                axis_ticks_major_y=element_blank(),
                axis_title_x=element_blank(),
                axis_line_x=element_line(color='black'),
                axis_text_x=element_text(color=ccolor, size=14, angle=45),
                panel_grid=element_blank(),
                panel_border=element_blank()
            )
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_location__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
