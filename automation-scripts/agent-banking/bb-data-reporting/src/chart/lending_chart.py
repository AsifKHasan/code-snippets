#!/usr/bin/env python3
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

from chart.chart_base import ChartBase


class LendingChart(ChartBase):

    ''' constructor
    '''
    def __init__(self, data, config):
        super().__init__(data=data, config=config)



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'lending-urban', 'lending-rural', 'lending-male', 'lending-female', 'lending-othergender']]

        # rename columns
        dict = {
                'lending-urban' : 'urban', 
                'lending-rural' : 'rural', 
                'lending-male' : 'male', 
                'lending-female' : 'female', 
                'lending-othergender' : 'other'
            }
        
        self.data.rename(columns=dict, inplace=True)


        # calculate total
        self.data["total"] = self.data.rural + self.data.urban

        # merge less than 2% banks into Other Banks
        self.data["new_code"] = np.where(self.data.total > 100.00, self.data.code, "Other Banks")
        self.data = self.data.groupby(self.data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum'})
        self.data.rename(columns={'new_code': 'code'}, inplace=True)


        # pivot so that columns become rows
        self.pivot_data = self.data
        self.pivot_data['rural'] = self.pivot_data.rural / self.pivot_data.total * 100
        self.pivot_data['urban'] = self.pivot_data.urban / self.pivot_data.total * 100
        self.pivot_data['male'] = self.pivot_data.male / self.pivot_data.total * 100
        self.pivot_data['female'] = self.pivot_data.female / self.pivot_data.total * 100
        self.pivot_data['other'] = self.pivot_data.other / self.pivot_data.total * 100
        self.pivot_data = pd.melt(self.pivot_data, id_vars=['code'], value_vars=['urban', 'rural', 'male', 'female', 'other'])



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        new_data = self.data.sample(frac=1)
        new_data['explode'] = np.where(new_data.total > 500.00, 0, 0.3)

        chart, ax = plt.subplots()
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

        chart_path = f"{self.config['out-dir']}/lending__cumulative__top-banks.png"
        chart.savefig(fname=chart_path, dpi=150)



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

        chart_path = f"{self.config['out-dir']}/lending__cumulative__location-ratio__top-banks.png"
        chart.save(filename=chart_path, dpi=150)



    ''' distribution by gender by bank (percent bar chart)
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

        chart_path = f"{self.config['out-dir']}/lending__cumulative__gender-ratio__top-banks.png"
        chart.save(filename=chart_path, dpi=150)
