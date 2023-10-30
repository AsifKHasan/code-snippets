#!/usr/bin/env python3
import numpy as np
import pandas as pd


''' data for account
'''
def data_for_account(input_data):
    data = input_data[['code',  'account-urban', 'account-rural', 'account-male', 'account-female', 'account-othergender', 'account-current', 'account-savings', 'account-othertype']]

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
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge banks with less than 2% of total accounts into Other Banks
    data["new_code"] = np.where((data.total / data.total.sum() > 0.02), data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    return data



''' data for deposit
'''
def data_for_deposit(input_data):
    data = input_data[['code', 'deposit-urban', 'deposit-rural', 'deposit-male', 'deposit-female', 'deposit-othergender', 'deposit-current', 'deposit-savings', 'deposit-othertype']]

    # rename columns
    dict = {
            'deposit-urban' : 'urban', 
            'deposit-rural' : 'rural', 
            'deposit-male' : 'male', 
            'deposit-female' : 'female', 
            'deposit-othergender' : 'other', 
            'deposit-current' : 'current', 
            'deposit-savings' : 'savings', 
            'deposit-othertype' : 'others'
        }
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where((data.total / data.total.sum() > 0.02), data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum', 'current': 'sum', 'savings': 'sum', 'others': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    return data



''' data for lending
'''
def data_for_lending(input_data):
    data = input_data[['code', 'lending-urban', 'lending-rural', 'lending-male', 'lending-female', 'lending-othergender']]

    # rename columns
    dict = {
            'lending-urban' : 'urban', 
            'lending-rural' : 'rural', 
            'lending-male' : 'male', 
            'lending-female' : 'female', 
            'lending-othergender' : 'other'
        }
    
    data.rename(columns=dict, inplace=True)


    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where(data.total > 100.00, data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum', 'male': 'sum', 'female': 'sum', 'other': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    return data



''' data for remittance
'''
def data_for_remittance(input_data):
    data = input_data[['code', 'remittance-urban', 'remittance-rural']]

    # rename columns
    dict = {
            'remittance-urban' : 'urban', 
            'remittance-rural' : 'rural'
        }
    
    data.rename(columns=dict, inplace=True)

    # calculate total
    data["total"] = data.rural + data.urban

    # merge less than 2% banks into Other Banks
    data["new_code"] = np.where(data.total > 10000.00, data.code, "Other Banks")
    data = data.groupby(data.new_code, as_index=False).agg({'total': 'sum', 'urban': 'sum', 'rural': 'sum'})
    data.rename(columns={'new_code': 'code'}, inplace=True)

    return data


''' read data from csv file
'''
def read_csv_data(csv_path):
    return pd.read_csv(csv_path, sep='\t', thousands=',')
