#!/usr/bin/env python3
from plotnine import *

from helper.logger import *


class ChartBase(object):

    ''' constructor
    '''
    def __init__(self, current_data, previous_data, config):
        self.config = config

        self.setup_theme()
        self.setup_data(current_data=current_data, previous_data=previous_data)

        self.type = None



    ''' ggplot theme setup
    '''
    def setup_theme(self):
        theme_set(theme_538())



    ''' setup data
    '''
    def setup_data(self, current_data, previous_data):
        pass
