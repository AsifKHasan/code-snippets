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
        self.data = data[['code',  'account-urban', 'account-rural', 'account-male', 'account-female', 'account-othergender', 'account-current', 'account-savings', 'account-othertype']]

        # rename columns
        dict = {
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
        self.data["total"] = self.data.rural + self.data.urban

        # merge banks with less than 2% of total accounts into Other Banks
        self.data['new_code'] = np.where((self.data.total / self.data.total.sum() > 0.02), self.data.code, "Other Banks")
        self.data = self.data.groupby(self.data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
        self.data.rename(columns={'new_code': 'code'}, inplace=True)

        # pivot so that columns become rows
        self.pivot_data = self.data
        self.pivot_data['rural'] = self.pivot_data.rural / self.data.total * 100
        self.pivot_data['urban'] = self.pivot_data.urban / self.data.total * 100
        self.pivot_data['male'] = self.pivot_data.male / self.data.total * 100
        self.pivot_data['female'] = self.pivot_data.female / self.data.total * 100
        self.pivot_data['other'] = self.pivot_data.other / self.data.total * 100
        self.pivot_data['current'] = self.pivot_data.current / self.data.total * 100
        self.pivot_data['savings'] = self.pivot_data.savings / self.data.total * 100
        self.pivot_data['others'] = self.pivot_data.others / self.data.total * 100
        self.pivot_data = pd.melt(self.pivot_data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other', 'current', 'savings', 'others'])



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        self.data['explode'] = np.where(self.data.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
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

        chart_path = f"{self.config['out-dir']}/accounts__cumulative__top-banks.png"
        chart.savefig(fname=chart_path, dpi=150)

        # fig.show()



    ''' distribution by location by bank (percent bar chart)
    '''
    def distribution_by_location_by_bank(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['rural', 'urban']
        chart = ggplot(
                self.pivot_data[self.pivot_data.variable.isin(variables) & (self.pivot_data.value > 0)], 
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

        chart_path = f"{self.config['out-dir']}/accounts__cumulative__location-ratio__top-banks.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' distribution by gender by bank (percent bar chart)
        # https://plotnine.readthedocs.io/en/v0.12.3/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot
    '''
    def distribution_by_gender_by_bank(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['male', 'female', 'other']
        chart = ggplot(
                self.pivot_data[self.pivot_data.variable.isin(variables) & (self.pivot_data.value > 0)], 
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
                y=(-5, 70)
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

        chart_path = f"{self.config['out-dir']}/accounts__cumulative__gender-ratio__top-banks.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)



    ''' distribution by type by bank (percent bar chart)
    '''
    def distribution_by_type_by_bank(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        variables = ['current', 'savings', 'others']
        chart = ggplot(
                self.pivot_data[self.pivot_data.variable.isin(variables) & (self.pivot_data.value > 0)], 
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

        chart_path = f"{self.config['out-dir']}/accounts__cumulative__type-ratio__top-banks.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
