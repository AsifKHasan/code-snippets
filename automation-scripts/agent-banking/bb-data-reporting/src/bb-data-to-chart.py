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
    config = yaml.load(open("../conf/config.yml", 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    all_data = read_csv_data(csv_path=config["csv-path"])

    # cumulative report upto a quarter end
    latest_data = all_data[all_data.quarter == config["last-quarter"]]

    outlet_chart = OutletChart(data=latest_data, config=config)
    outlet_chart.distribution_by_bank()
    outlet_chart.outlet_ratio_comparison()

    account_chart = AccountChart(data=latest_data, config=config)
    account_chart.distribution_by_bank()
    account_chart.comparison_by_location()
    account_chart.comparison_by_gender()
    account_chart.comparison_by_type()
    account_chart.per_outlet_comparison_by_location()
    account_chart.per_outlet_comparison_by_gender()
    account_chart.per_outlet_comparison_by_type()

    deposit_chart = DepositChart(data=latest_data, config=config)
    deposit_chart.distribution_by_bank()
    deposit_chart.comparison_by_location()
    deposit_chart.comparison_by_gender()
    deposit_chart.comparison_by_type()
    deposit_chart.per_outlet_comparison_by_location()
    deposit_chart.per_outlet_comparison_by_gender()
    deposit_chart.per_outlet_comparison_by_type()


    lending_chart = LendingChart(data=latest_data, config=config)
    lending_chart.distribution_by_bank()
    lending_chart.comparison_by_location()
    lending_chart.comparison_by_gender()
    lending_chart.per_outlet_comparison_by_location()
    lending_chart.per_outlet_comparison_by_gender()

    remittance_chart = RemittanceChart(data=latest_data, config=config)
    remittance_chart.distribution_by_bank()
    remittance_chart.comparison_by_location()
    remittance_chart.per_outlet_comparison_by_location()
