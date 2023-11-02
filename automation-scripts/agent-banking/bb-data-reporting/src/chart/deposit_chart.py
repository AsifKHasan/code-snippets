#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

from chart.chart_base import ChartBase

from helper.logger import *


class DepositChart(ChartBase):

    ''' constructor
    '''
    def __init__(self, data, config):
        super().__init__(data=data, config=config)
        self.type = 'deposit'



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'bank', 'outlet-urban', 'outlet-rural', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]

        # rename columns
        dict = {
                'outlet-urban' : 'urban_outlets', 
                'outlet-rural' : 'rural_outlets', 
                'deposit-urban' : 'urban', 
                'deposit-rural' : 'rural', 
                'deposit-male' : 'male', 
                'deposit-female' : 'female', 
                'deposit-othergender' : 'other', 
                'deposit-current' : 'current', 
                'deposit-savings' : 'savings', 
                'deposit-othertype' : 'others'
            }
        
        self.data = self.data.rename(columns=dict)


        # calculate total
        self.data['total_outlets'] = self.data.urban_outlets + self.data.rural_outlets
        self.data["total"] = self.data.rural + self.data.urban

        # per outlet data
        self.data_per_outlet = pd.DataFrame()
        self.data_per_outlet['code'] = self.data['code']
        self.data_per_outlet['bank'] = self.data['bank']
        self.data_per_outlet['total'] = self.data['total'] / self.data['total_outlets']
        self.data_per_outlet['rural'] = self.data['rural'] / self.data['rural_outlets']
        self.data_per_outlet['urban'] = self.data['urban'] / self.data['urban_outlets']
        self.data_per_outlet['male'] = self.data['male'] / self.data['total_outlets']
        self.data_per_outlet['female'] = self.data['female'] / self.data['total_outlets']
        self.data_per_outlet['other'] = self.data['other'] / self.data['total_outlets']
        self.data_per_outlet['current'] = self.data['current'] / self.data['total_outlets']
        self.data_per_outlet['savings'] = self.data['savings'] / self.data['total_outlets']
        self.data_per_outlet['others'] = self.data['others'] / self.data['total_outlets']
        # self.data_per_outlet = self.data_per_outlet.round()

        # keep the top N
        self.data_per_outlet = self.data_per_outlet.nlargest(8, 'total')
        self.data_per_outlet = pd.melt(self.data_per_outlet, id_vars=['code', 'bank'], value_vars=['total', 'urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


        # merge less than 2% banks into Other Banks
        self.data["new_code"] = np.where((self.data.total / self.data.total.sum() > 0.02), self.data.code, "Other Banks")
        self.data['new_bank'] = np.where((self.data.total / self.data.total.sum() > 0.02), self.data.bank, "Other Banks")
        self.data = self.data.groupby([self.data.new_code, self.data.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
        self.data.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)


        # pivot so that columns become rows
        self.data_in_percent = self.data.copy()
        self.data_in_percent['rural'] = self.data_in_percent.rural / self.data_in_percent.total * 100
        self.data_in_percent['urban'] = self.data_in_percent.urban / self.data_in_percent.total * 100
        self.data_in_percent['male'] = self.data_in_percent.male / self.data_in_percent.total * 100
        self.data_in_percent['female'] = self.data_in_percent.female / self.data_in_percent.total * 100
        self.data_in_percent['other'] = self.data_in_percent.other / self.data_in_percent.total * 100
        self.data_in_percent['current'] = self.data_in_percent.current / self.data_in_percent.total * 100
        self.data_in_percent['savings'] = self.data_in_percent.savings / self.data_in_percent.total * 100
        self.data_in_percent['others'] = self.data_in_percent.others / self.data_in_percent.total * 100
        self.data_in_percent = pd.melt(self.data_in_percent, id_vars=['code', 'bank'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        self.data['explode'] = np.where(self.data.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(
            self.data.total, 
            labels=self.data.code, 
            autopct='%1.2f%%',
            colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'yellow'],
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=self.data['explode'].tolist(),
            wedgeprops={'edgecolor': 'gray', 'linewidth': 1, 'antialiased': True}
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__distribution__by_bank__end-of__{self.config['last-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)

        # fig.show()



    ''' comparison by location by bank (percent bar chart)
    '''
    def comparison_by_location(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban']
        chart = (
            ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_location__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by gender by bank (percent bar chart)
    '''
    def comparison_by_gender(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        chart = (
            ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_gender__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by type by bank (percent bar chart)
    '''
    def comparison_by_type(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        chart = (
            ggplot(
                self.data_in_percent[self.data_in_percent.variable.isin(variables) & (self.data_in_percent.value > 0)], 
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
        )

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_type__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by location (bar chart)
    '''
    def per_outlet_comparison_by_location(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban', 'total']
        data = self.data_per_outlet[self.data_per_outlet.variable.isin(variables) & (self.data_per_outlet.value > 0)]

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
            lims(y=(-10, None)) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_location__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by gender (bar chart)
    '''
    def per_outlet_comparison_by_gender(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        data = self.data_per_outlet[self.data_per_outlet.variable.isin(variables) & (self.data_per_outlet.value > 0)]

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
            lims(y=(-10, None)) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_gender__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by account type (bar chart)
    '''
    def per_outlet_comparison_by_type(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        data = self.data_per_outlet[self.data_per_outlet.variable.isin(variables) & (self.data_per_outlet.value > 0)]

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
            lims(y=(-10, None)) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_type__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
