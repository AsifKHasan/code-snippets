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



    ''' ggplot theme setup
    '''
    def setup_theme(self):
        theme_set(theme_538())



    ''' setup data
    '''
    def setup_data(self, cumulative_data, period_data):
        pass
