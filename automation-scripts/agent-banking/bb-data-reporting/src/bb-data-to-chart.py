#!/usr/bin/env python3
import yaml

from data.data_processor import *
from chart.chart_base import *
from chart.outlet_charts import *
from chart.account_charts import *
from chart.deposit_charts import *
from chart.lending_charts import *
from chart.remittance_charts import *


if __name__ == '__main__':
    # configuration
    config = yaml.load(open("../conf/config.yml", 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    all_data = read_csv_data(csv_path=config["csv-path"])
    setup_theme()

    # cumulative report upto a quarter end
    latest_data = all_data[all_data.quarter == config["last-quarter"]] 

    account_data = data_for_account(input_data=latest_data)
    account_charts_cumulative(data=account_data, config=config)

    deposit_data = data_for_deposit(input_data=latest_data)
    deposit_charts_cumulative(data=deposit_data, config=config)

    lending_data = data_for_lending(input_data=latest_data)
    lending_charts_cumulative(data=lending_data, config=config)

    remittance_data = data_for_remittance(input_data=latest_data)
    remittance_charts_cumulative(data=remittance_data, config=config)

    outlet_ratio_cumulative(input_data=latest_data, config=config)
