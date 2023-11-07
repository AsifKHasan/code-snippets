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



''' setup data
'''
def setup_data(all_data, config):
    dict = {
        'outlet-urban' : 'outlet_urban', 
        'outlet-rural' : 'outlet_rural'
    }

    # get the previous quarter
    previous_quarter = config['quarters'][config['quarters'].index(config['current-quarter']) - 1]

    # get the latest and previous quarter data
    cumulative_data = all_data[all_data.quarter == config['current-quarter']].set_index(['code', 'bank'])
    previous_data = all_data[all_data.quarter == previous_quarter].set_index(['code', 'bank'])

    cumulative_data = cumulative_data.drop(columns=['quarter'])
    cumulative_data = cumulative_data.rename(columns=dict)

    cumulative_data['outlet_total'] = cumulative_data['outlet_rural'] + cumulative_data['outlet_urban']
    cumulative_data['account-total'] = cumulative_data['account-rural'] + cumulative_data['account-urban']
    cumulative_data['deposit-total'] = cumulative_data['deposit-rural'] + cumulative_data['deposit-urban']
    cumulative_data['lending-total'] = cumulative_data['lending-rural'] + cumulative_data['lending-urban']
    cumulative_data['remittance-total'] = cumulative_data['remittance-rural'] + cumulative_data['remittance-urban']

    previous_data = previous_data.drop(columns=['quarter'])
    previous_data = previous_data.rename(columns=dict)
    previous_data['outlet_total'] = previous_data['outlet_rural'] + previous_data['outlet_urban']
    previous_data['account-total'] = previous_data['account-rural'] + previous_data['account-urban']
    previous_data['deposit-total'] = previous_data['deposit-rural'] + previous_data['deposit-urban']
    previous_data['lending-total'] = previous_data['lending-rural'] + previous_data['lending-urban']
    previous_data['remittance-total'] = previous_data['remittance-rural'] + previous_data['remittance-urban']

    # period data diff of cumulative and previous
    period_data = cumulative_data.sub(previous_data)

    cumulative_data['current_outlet_rural'] = cumulative_data['outlet_rural']
    cumulative_data['current_outlet_urban'] = cumulative_data['outlet_urban'] 
    cumulative_data['current_outlet_total'] = cumulative_data['outlet_total']

    period_data['current_outlet_rural'] = cumulative_data['outlet_rural'] 
    period_data['current_outlet_urban'] = cumulative_data['outlet_urban'] 
    period_data['current_outlet_total'] = cumulative_data['outlet_total']

    return cumulative_data, period_data



if __name__ == '__main__':
    # configuration
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    all_data = read_csv_data(csv_path=config['csv-path'])
    cumulative_data, period_data = setup_data(all_data=all_data, config=config)

    # outlet_chart = OutletChart(cumulative_data=cumulative_data, period_data=period_data, config=config)
    # outlet_chart.distribution_by_bank(data_range='cumulative')
    # outlet_chart.outlet_ratio_comparison(data_range='cumulative')
    # outlet_chart.distribution_by_bank(data_range='period')
    # outlet_chart.outlet_ratio_comparison(data_range='period')

    account_chart = AccountChart(cumulative_data=cumulative_data, period_data=period_data, config=config)
    # account_chart.distribution_by_bank(data_range='cumulative')
    # account_chart.comparison_by_location(data_range='cumulative')
    # account_chart.comparison_by_gender(data_range='cumulative')
    # account_chart.comparison_by_type(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_gender(data_range='cumulative')
    # account_chart.per_outlet_comparison_by_type(data_range='cumulative')
    # account_chart.distribution_by_bank(data_range='period')
    account_chart.comparison_by_location(data_range='period')
    account_chart.comparison_by_gender(data_range='period')
    account_chart.comparison_by_type(data_range='period')
    # account_chart.per_outlet_comparison_by_location(data_range='period')
    # account_chart.per_outlet_comparison_by_gender(data_range='period')
    # account_chart.per_outlet_comparison_by_type(data_range='period')


    deposit_chart = DepositChart(cumulative_data=cumulative_data, period_data=period_data, config=config)
    # deposit_chart.distribution_by_bank(data_range='cumulative')
    # deposit_chart.comparison_by_location(data_range='cumulative')
    # deposit_chart.comparison_by_gender(data_range='cumulative')
    # deposit_chart.comparison_by_type(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_gender(data_range='cumulative')
    # deposit_chart.per_outlet_comparison_by_type(data_range='cumulative')
    # deposit_chart.distribution_by_bank(data_range='period')
    deposit_chart.comparison_by_location(data_range='period')
    deposit_chart.comparison_by_gender(data_range='period')
    deposit_chart.comparison_by_type(data_range='period')
    # deposit_chart.per_outlet_comparison_by_location(data_range='period')
    # deposit_chart.per_outlet_comparison_by_gender(data_range='period')
    # deposit_chart.per_outlet_comparison_by_type(data_range='period')


    lending_chart = LendingChart(cumulative_data=cumulative_data, period_data=period_data, config=config)
    # lending_chart.distribution_by_bank(data_range='cumulative')
    # lending_chart.comparison_by_location(data_range='cumulative')
    # lending_chart.comparison_by_gender(data_range='cumulative')
    # lending_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # lending_chart.per_outlet_comparison_by_gender(data_range='cumulative')
    # lending_chart.distribution_by_bank(data_range='period')
    lending_chart.comparison_by_location(data_range='period')
    lending_chart.comparison_by_gender(data_range='period')
    # lending_chart.per_outlet_comparison_by_location(data_range='period')
    # lending_chart.per_outlet_comparison_by_gender(data_range='period')


    remittance_chart = RemittanceChart(cumulative_data=cumulative_data, period_data=period_data, config=config)
    # remittance_chart.distribution_by_bank(data_range='cumulative')
    # remittance_chart.comparison_by_location(data_range='cumulative')
    # remittance_chart.per_outlet_comparison_by_location(data_range='cumulative')
    # remittance_chart.distribution_by_bank(data_range='period')
    remittance_chart.comparison_by_location(data_range='period')
    # remittance_chart.per_outlet_comparison_by_location(data_range='period')
