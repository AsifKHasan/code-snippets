#!/usr/bin/env python3
import yaml
import pandas as pd

from chart.outlet_chart import OutletChart
from chart.account_chart import AccountChart
from chart.deposit_chart import DepositChart
from chart.lending_chart import LendingChart
from chart.remittance_chart import RemittanceChart

from helper.logger import *


''' read data from csv file
'''
def read_csv_data(csv_path):
    return pd.read_csv(csv_path, sep='\t', thousands=',')



if __name__ == '__main__':
    # configuration
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    all_data = read_csv_data(csv_path=config['csv-path'])

    # get the previous quarter
    previous_quarter = config['quarters'][config['quarters'].index(config['current-quarter']) - 1]

    # get the latest and previous quarter data
    current_data = all_data[all_data.quarter == config['current-quarter']]
    previous_data = all_data[all_data.quarter == previous_quarter]

    # outlet_chart = OutletChart(current_data=current_data, previous_data=previous_data, config=config)
    # outlet_chart.distribution_by_bank(data_range='cumulative')
    # outlet_chart.outlet_ratio_comparison(data_range='cumulative')

    account_chart = AccountChart(current_data=current_data, previous_data=previous_data, config=config)
    # account_chart.distribution_by_bank(data_range='cumulative')
    # account_chart.comparison_by_location(data_range='cumulative')
    # account_chart.comparison_by_gender(data_range='cumulative')
    # account_chart.comparison_by_type(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_gender(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_type(data_range='cumulative')

    # deposit_chart = DepositChart(current_data=current_data, previous_data=previous_data, config=config)
    # deposit_chart.distribution_by_bank(data_range='cumulative')
    # deposit_chart.comparison_by_location(data_range='cumulative')
    # deposit_chart.comparison_by_gender(data_range='cumulative')
    # deposit_chart.comparison_by_type(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_gender(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_type(data_range='cumulative')

    # lending_chart = LendingChart(current_data=current_data, previous_data=previous_data, config=config)
    # lending_chart.distribution_by_bank(data_range='cumulative')
    # lending_chart.comparison_by_location(data_range='cumulative')
    # lending_chart.comparison_by_gender(data_range='cumulative')
    # lending_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # lending_chart.per_outlet_comparison_by_gender(data_range='cumulative')

    # remittance_chart = RemittanceChart(current_data=current_data, previous_data=previous_data, config=config)
    # remittance_chart.distribution_by_bank(data_range='cumulative')
    # remittance_chart.comparison_by_location(data_range='cumulative')
    # remittance_chart.per_outlet_comparison_by_location(data_range='cumulative')
