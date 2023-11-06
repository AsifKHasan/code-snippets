#!/usr/bin/env python3
from plotnine import *

from helper.logger import *


class ChartBase(object):

    ''' constructor
    '''
    def __init__(self, cumulative_data, period_data, config):
        self.config = config

        self.setup_theme()
        self.setup_data(cumulative_data=cumulative_data, period_data=period_data)

        self.type = None

        # self.color_list = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown', 'khaki', 'steelblue']
        self.color_list = ['#d9ead3', '#d0e0e3', '#c9daf8', '#cfe2f3', '#d9d2e9', '#ead1dc', '#e6b8af', '#f4cccc', '#fce5cd', '#fff2cc', ]
        



    ''' ggplot theme setup
    '''
    def setup_theme(self):
        theme_set(theme_538())



    ''' setup data
    '''
    def setup_data(self, cumulative_data, period_data):
        pass
