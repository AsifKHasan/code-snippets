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
    def __init__(self, data, config):
        super().__init__(data=data, config=config)



    ''' setup data
    '''
    def setup_data(self, data):
        self.data = data[['code', 'remittance-urban', 'remittance-rural']]

        # rename columns
        dict = {
                'remittance-urban' : 'urban', 
                'remittance-rural' : 'rural'
            }
        
        self.data = self.data.rename(columns=dict)

        # calculate total
        self.data["total"] = self.data.rural + self.data.urban

        # merge less than 2% banks into Other Banks
        self.data["new_code"] = np.where(self.data.total > 10000.00, self.data.code, "Other Banks")
        self.data = self.data.groupby(self.data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
        self.data = self.data.rename(columns={'new_code': 'code'})


        # pivot so that columns become rows
        self.pivot_data = self.data
        self.pivot_data['rural'] = self.pivot_data.rural / self.pivot_data.total * 100
        self.pivot_data['urban'] = self.pivot_data.urban / self.pivot_data.total * 100
        self.pivot_data = pd.melt(self.pivot_data, id_vars=['code'], value_vars=['urban', 'rural'])



    ''' distribution by bank (pie chart)
    '''
    def distribution_by_bank(self):

        self.data['explode'] = np.where(self.data.code == 'Agrani', 0.2, 0)
        chart, ax = plt.subplots()
        plt.figure(figsize=(10,10))
        ax.pie(self.data.total, 
            labels=self.data.code, 
            autopct='%1.2f%%',
            colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue', 'mistyrose', 'azure', 'lavenderblush', 'honeydew', 'aliceblue'],
            #    shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9},
            startangle=180,
            textprops={'size': 'smaller'}, 
            radius=1.4,
            explode=self.data['explode'].tolist(),
            wedgeprops = {"edgecolor":"gray", 
                            'linewidth': 1, 
                            'antialiased': True}
            )

        chart_path = f"{self.config['out-dir']}/remittance__distribution_by_bank__end-of__{self.config['last-quarter']}.png"
        chart.savefig(fname=chart_path, dpi=150)



    ''' comparison by location (percent bar chart)
    '''
    def comparison_by_location(self):

        dodge_text = position_dodge(width=0.9)
        ccolor = '#333333'

        # location based
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
                size=10, 
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

        chart_path = f"{self.config['out-dir']}/remittance__comparison_by_location__end-of__{self.config['last-quarter']}.png"
        chart.save(filename=chart_path, dpi=150, verbose=False)
