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
    def __init__(self, cumulative_data, period_data, config):
        super().__init__(cumulative_data=cumulative_data, period_data=period_data, config=config)
        self.type = 'deposit'



    ''' setup data
    '''
    def setup_data(self, cumulative_data, period_data):
        # rename columns
        dict = {
            'deposit-total' : 'total', 
            'deposit-urban' : 'urban', 
            'deposit-rural' : 'rural', 
            'deposit-male' : 'male', 
            'deposit-female' : 'female', 
            'deposit-othergender' : 'other', 
            'deposit-current' : 'current', 
            'deposit-savings' : 'savings', 
            'deposit-othertype' : 'others'
        }
        
        self.data_cumulative = cumulative_data[['current_outlet_total', 'current_outlet_rural', 'current_outlet_urban', 'outlet_total', 'outlet_urban', 'outlet_rural', 'deposit-total', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]
        self.data_cumulative = self.data_cumulative.rename(columns=dict)

        self.data_period = period_data[['current_outlet_total', 'current_outlet_rural', 'current_outlet_urban', 'outlet_total', 'outlet_urban', 'outlet_rural', 'deposit-total', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]
        self.data_period = self.data_period.rename(columns=dict)

        self.data_cumulative = self.data_cumulative.reset_index()
        self.data_period = self.data_period.reset_index()


        # per outlet data
        self.data_cumulative_per_outlet = pd.DataFrame()
        self.data_cumulative_per_outlet['code'] = self.data_cumulative['code']
        self.data_cumulative_per_outlet['bank'] = self.data_cumulative['bank']
        self.data_cumulative_per_outlet['total'] = self.data_cumulative['total'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['rural'] = self.data_cumulative['rural'] / self.data_cumulative['current_outlet_rural']
        self.data_cumulative_per_outlet['urban'] = self.data_cumulative['urban'] / self.data_cumulative['current_outlet_urban']
        self.data_cumulative_per_outlet['male'] = self.data_cumulative['male'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['female'] = self.data_cumulative['female'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['other'] = self.data_cumulative['other'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['current'] = self.data_cumulative['current'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['savings'] = self.data_cumulative['savings'] / self.data_cumulative['current_outlet_total']
        self.data_cumulative_per_outlet['others'] = self.data_cumulative['others'] / self.data_cumulative['current_outlet_total']
        # self.data_cumulative_per_outlet = self.data_cumulative_per_outlet.round()

        # per outlet data
        self.data_period_per_outlet = pd.DataFrame()
        self.data_period_per_outlet['code'] = self.data_period['code']
        self.data_period_per_outlet['bank'] = self.data_period['bank']
        self.data_period_per_outlet['total'] = self.data_period['total'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['rural'] = self.data_period['rural'] / self.data_period['current_outlet_rural']
        self.data_period_per_outlet['urban'] = self.data_period['urban'] / self.data_period['current_outlet_urban']
        self.data_period_per_outlet['male'] = self.data_period['male'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['female'] = self.data_period['female'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['other'] = self.data_period['other'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['current'] = self.data_period['current'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['savings'] = self.data_period['savings'] / self.data_period['current_outlet_total']
        self.data_period_per_outlet['others'] = self.data_period['others'] / self.data_period['current_outlet_total']
        # self.data_period_per_outlet = self.data_period_per_outlet.round()


        # keep the top N
        top_n = 8
        self.data_cumulative_per_outlet = self.data_cumulative_per_outlet.nlargest(top_n, 'total')
        self.data_cumulative_per_outlet = pd.melt(self.data_cumulative_per_outlet, id_vars=['code', 'bank'], value_vars=['total', 'urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])

        self.data_period_per_outlet = self.data_period_per_outlet.nlargest(top_n, 'total')
        self.data_period_per_outlet = pd.melt(self.data_period_per_outlet, id_vars=['code', 'bank'], value_vars=['total', 'urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


        # merge less than 2% banks into Other Banks
        pct_threshold = 0.02
        self.data_cumulative["new_code"] = np.where((self.data_cumulative.total / self.data_cumulative.total.sum() > pct_threshold), self.data_cumulative.code, 'Other Banks')
        self.data_cumulative['new_bank'] = np.where((self.data_cumulative.total / self.data_cumulative.total.sum() > pct_threshold), self.data_cumulative.bank, 'Other Banks')
        self.data_cumulative = self.data_cumulative.groupby([self.data_cumulative.new_code, self.data_cumulative.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
        self.data_cumulative.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)

        pct_threshold = 0.02
        self.data_period["new_code"] = np.where((self.data_period.total / self.data_period.total.sum() > pct_threshold), self.data_period.code, 'Other Banks')
        self.data_period['new_bank'] = np.where((self.data_period.total / self.data_period.total.sum() > pct_threshold), self.data_period.bank, 'Other Banks')
        self.data_period = self.data_period.groupby([self.data_period.new_code, self.data_period.new_bank], as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
        self.data_period.rename(columns={'new_code': 'code', 'new_bank': 'bank'}, inplace=True)


        # pivot so that columns become rows
        self.data_cumulative_in_percent = self.data_cumulative.copy()
        self.data_cumulative_in_percent['rural'] = self.data_cumulative_in_percent.rural / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['urban'] = self.data_cumulative_in_percent.urban / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['male'] = self.data_cumulative_in_percent.male / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['female'] = self.data_cumulative_in_percent.female / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['other'] = self.data_cumulative_in_percent.other / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['current'] = self.data_cumulative_in_percent.current / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['savings'] = self.data_cumulative_in_percent.savings / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent['others'] = self.data_cumulative_in_percent.others / self.data_cumulative_in_percent.total * 100
        self.data_cumulative_in_percent = pd.melt(self.data_cumulative_in_percent, id_vars=['code', 'bank'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])

        self.data_period_in_percent = self.data_period.copy()
        self.data_period_in_percent['rural'] = self.data_period_in_percent.rural / self.data_period_in_percent.total * 100
        self.data_period_in_percent['urban'] = self.data_period_in_percent.urban / self.data_period_in_percent.total * 100
        self.data_period_in_percent['male'] = self.data_period_in_percent.male / self.data_period_in_percent.total * 100
        self.data_period_in_percent['female'] = self.data_period_in_percent.female / self.data_period_in_percent.total * 100
        self.data_period_in_percent['other'] = self.data_period_in_percent.other / self.data_period_in_percent.total * 100
        self.data_period_in_percent['current'] = self.data_period_in_percent.current / self.data_period_in_percent.total * 100
        self.data_period_in_percent['savings'] = self.data_period_in_percent.savings / self.data_period_in_percent.total * 100
        self.data_period_in_percent['others'] = self.data_period_in_percent.others / self.data_period_in_percent.total * 100
        self.data_period_in_percent = pd.melt(self.data_period_in_percent, id_vars=['code', 'bank'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])


        # print(self.data_cumulative)
        # print(self.data_period)



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self, data_range):
        data = self.data_cumulative if data_range == 'cumulative' else self.data_period

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

        # fig.show()



    ''' comparison by location by bank (percent bar chart)
    '''
    def comparison_by_location(self, data_range):
        data = self.data_cumulative_in_percent if data_range == 'cumulative' else self.data_period_in_percent

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban']
        chart = (
            ggplot(
                data[data.variable.isin(variables) & (data.value > 0)], 
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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_location__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by gender by bank (percent bar chart)
    '''
    def comparison_by_gender(self, data_range):
        data = self.data_cumulative_in_percent if data_range == 'cumulative' else self.data_period_in_percent

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        chart = (
            ggplot(
                data[data.variable.isin(variables) & (data.value > 0)], 
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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_gender__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' comparison by type by bank (percent bar chart)
    '''
    def comparison_by_type(self, data_range):
        data = self.data_cumulative_in_percent if data_range == 'cumulative' else self.data_period_in_percent

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        chart = (
            ggplot(
                data[data.variable.isin(variables) & (data.value > 0)], 
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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__comparison__by_type__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by location (bar chart)
    '''
    def per_outlet_comparison_by_location(self, data_range):
        data = self.data_cumulative_per_outlet if data_range == 'cumulative' else self.data_period_per_outlet

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban', 'total']
        data = data[data.variable.isin(variables) & (data.value > 0)]

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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_location__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by gender (bar chart)
    '''
    def per_outlet_comparison_by_gender(self, data_range):
        data = self.data_cumulative_per_outlet if data_range == 'cumulative' else self.data_period_per_outlet

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        data = data[data.variable.isin(variables) & (data.value > 0)]

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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_gender__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' per outlet comparison by account type (bar chart)
    '''
    def per_outlet_comparison_by_type(self, data_range):
        data = self.data_cumulative_per_outlet if data_range == 'cumulative' else self.data_period_per_outlet

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        data = data[data.variable.isin(variables) & (data.value > 0)]

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
            scale_fill_manual(values=self.color_list) +
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

        chart_path = f"{self.config['out-dir']}/{self.type}__per_outlet__comparison__by_type__{data_range}__{self.config['current-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
