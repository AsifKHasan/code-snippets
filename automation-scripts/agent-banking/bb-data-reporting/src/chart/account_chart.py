#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

from chart.chart_base import ChartBase

from helper.logger import *


class AccountChart(ChartBase):

    ''' constructor
    '''
    def __init__(self, data, config):
        super().__init__(data=data, config=config)



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'bank', 'outlet-urban', 'outlet-rural', 'account-urban', 'account-rural', 'account-male', 'account-female', 'account-othergender', 'account-current', 'account-savings', 'account-othertype']]

        # rename columns
        dict = {
                'outlet-urban' : 'urban_outlets', 
                'outlet-rural' : 'rural_outlets', 
                'account-urban' : 'urban', 
                'account-rural' : 'rural', 
                'account-male' : 'male', 
                'account-female' : 'female', 
                'account-othergender' : 'other', 
                'account-current' : 'current', 
                'account-savings' : 'savings', 
                'account-othertype' : 'others'
            }
        
        self.data = self.data.rename(columns=dict)


        # calculate total
        self.data['total_outlets'] = self.data.urban_outlets + self.data.rural_outlets
        self.data['total'] = self.data.rural + self.data.urban

        # per outlet data
        columns_to_update = ['total', 'urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others']
        self.data_per_outlet = pd.DataFrame()
        self.data_per_outlet['code'] = self.data['code']
        self.data_per_outlet['bank'] = self.data['bank']
        self.data_per_outlet['total'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['rural'] = self.data['rural'] / self.data['rural_outlets']
        self.data_per_outlet['urban'] = self.data['urban'] / self.data['urban_outlets']
        self.data_per_outlet['male'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['female'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['other'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['current'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['savings'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['others'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet = self.data_per_outlet.round()
        self.data_per_outlet = self.data_per_outlet.nlargest(16, 'total')

        self.data_per_outlet = pd.melt(self.data_per_outlet, id_vars=['code', 'bank'], value_vars=['total', 'urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


        # merge banks with less than 2% of total accounts into Other Banks
        self.data['new_code'] = np.where((self.data.total / self.data.total.sum() > 0.02), self.data.code, "Other Banks")
        self.data['new_bank'] = np.where((self.data.total / self.data.total.sum() > 0.02), self.data.bank, "Other Banks")
        self.data = self.data.groupby([self.data.new_code, self.data.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
        self.data.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)

        # pivot so that columns become rows (for percent bar charts)
        self.data_in_percent = self.data.copy()
        self.data_in_percent['rural'] = self.data_in_percent.rural / self.data.total * 100
        self.data_in_percent['urban'] = self.data_in_percent.urban / self.data.total * 100
        self.data_in_percent['male'] = self.data_in_percent.male / self.data.total * 100
        self.data_in_percent['female'] = self.data_in_percent.female / self.data.total * 100
        self.data_in_percent['other'] = self.data_in_percent.other / self.data.total * 100
        self.data_in_percent['current'] = self.data_in_percent.current / self.data.total * 100
        self.data_in_percent['savings'] = self.data_in_percent.savings / self.data.total * 100
        self.data_in_percent['others'] = self.data_in_percent.others / self.data.total * 100
        self.data_in_percent = pd.melt(self.data_in_percent, id_vars=['code', 'bank'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


        # print(self.data)
        # print(self.data_in_percent)
        # print(self.data_per_outlet)



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        self.data['explode'] = np.where(self.data.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(self.data.total, 
            labels=self.data.code, 
            autopct='%1.2f%%',
            colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue'],
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=self.data['explode'].tolist(),
            wedgeprops = {"edgecolor":"gray", 
                            'linewidth': 1, 
                            'antialiased': True}
        )

        chart_path = f"{self.config['out-dir']}/account__distribution_by_bank__end-of__{self.config['last-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)

        # fig.show()



    ''' comparison by location (percent bar chart)
        https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    '''
    def comparison_by_location(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban']
        chart = ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
                size=12, 
                angle=45, 
                va='top'
            ) + \
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=10, 
                va='bottom', 
                format_string='{:.1f}%'
            ) + \
            lims(
                y=(-10, 100)
            ) + \
            scale_fill_manual(
                values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
            ) + \
            theme(
                # panel_background=element_rect(fill='white'),
                figure_size=(10, 5),
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

        chart_path = f"{self.config['out-dir']}/account__comparison_by_location__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by gender (percent bar chart)
    '''
    def comparison_by_gender(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        chart = ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
                size=12, 
                angle=45, 
                va='top'
            ) + \
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=10, 
                va='bottom', 
                format_string='{:.1f}%'
            ) + \
            lims(
                y=(-10, 70)
            ) + \
            scale_fill_manual(
                values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
            ) + \
            theme(
                # panel_background=element_rect(fill='white'),
                figure_size=(10, 5),
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

        chart_path = f"{self.config['out-dir']}/account__comparison_by_gender__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by type (percent bar chart)
    '''
    def comparison_by_type(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        chart = ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
                size=12, 
                angle=45, 
                va='top'
            ) + \
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=10, 
                va='bottom', 
                format_string='{:.1f}%'
            ) + \
            lims(
                y=(-15, 100)
            ) + \
            scale_fill_manual(
                values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
            ) + \
            theme(
                # panel_background=element_rect(fill='white'),
                figure_size=(10, 5),
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

        chart_path = f"{self.config['out-dir']}/account__comparison_by_type__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by location (bar chart)
    '''
    def per_outlet_comparison_by_location(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban']
        data = self.data_per_outlet[self.data_per_outlet.variable.isin(variables) & (self.data_per_outlet.value > 0)]

        chart = ggplot(
                data, 
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
                size=11, 
                angle=45, 
                va='top'
            ) + \
            geom_text(
                aes(label='value'),
                position=dodge_text,
                size=8, 
                va='bottom', 
                format_string='{:.0f}'
            ) + \
            lims(
                y=(-40, 1500)
            ) + \
            scale_fill_manual(
                values = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
            ) + \
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

        chart_path = f"{self.config['out-dir']}/account__per_outlet_comparison_by_location__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
