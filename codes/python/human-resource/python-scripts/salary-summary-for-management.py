#!/usr/bin/env python3
'''
usage:
./salary-summary-for-management.py --month Jan19
'''
import json
import os
import shutil
import sys
import time
import datetime
import argparse
import re
from io import StringIO

import pygsheets
import num2words
import pandas
from collections import defaultdict

from latex2pdf import Latex2Pdf

class SalarySummaryForManagement(object):

    _CREDENTIAL = './conf/credential.json'
    _GOOGLE_SHEET_NAME = 'FAU__SalarySheet__2018-2019'
    _TEMPLATE = './templates/salary-summary-for-management.tex'
    _OUTPUT_PDF = './out/salary-summary-for-management__{0}__{1}.pdf'
    _OUTPUT_DATA = './out/salary-summary-for-management__{0}__{1}.json'

    def __init__(self, month):
        self.start_time = int(round(time.time() * 1000))
        self._WORKSHEET_NAME = month
        s = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d__%H-%M-%S')
        self._OUTPUT_PDF = self._OUTPUT_PDF.format(self._WORKSHEET_NAME, s)
        self._OUTPUT_DATA = self._OUTPUT_DATA.format(self._WORKSHEET_NAME, s)

    def process_data(self):
        ws = self.g_sheet.worksheet('title', self._WORKSHEET_NAME)
        vals = ws.get_all_values(returnas='matrix', majdim='ROWS', include_empty=True)
        vals = list(map(lambda v: {'name' : v[2].strip(), 'wing' : v[4].strip(), 'unit' : v[5].strip(), 'grosssalary' : float(re.sub('[ ,-]', '', v[21]) or 0), 'benefits' : float(re.sub('[ ,-]', '', v[26]) or 0), 'payablethismonth' : float(re.sub('[ ,-]', '', v[61]) or 0)}, vals[5:]))

        # pandas DataFrame
        df = pandas.DataFrame(vals)
        # group by wings
        wdf = df.groupby('wing', as_index=False).agg({'name': 'count', 'grosssalary': sum, 'benefits': sum, 'payablethismonth': sum})
        wdf['grosssalaryavg'] = wdf.grosssalary / wdf.name
        # sum totals
        sums = wdf.select_dtypes(pandas.np.number).sum().rename('total')
        # group by units
        wings = wdf.to_dict(orient='records')
        for w in wings:
            udf = df[df['wing'] == w['wing']].groupby('unit', as_index=False).agg({'name': 'count', 'grosssalary': sum, 'benefits': sum, 'payablethismonth': sum})
            udf['grosssalaryavg'] = udf.grosssalary / udf.name
            w['units'] = udf.to_dict(orient='records')

        self._data = sums.to_dict()
        self._data['grosssalaryavg'] = self._data['grosssalary'] / self._data['name']
        self._data['month'], self._data['date'], self._data['wings'] = self._WORKSHEET_NAME, datetime.datetime.now().strftime('%B %d, %Y'), wings

        with open(self._OUTPUT_DATA, 'w') as f:
            f.write(json.dumps(self._data, sort_keys=False, indent=4))

    def generate(self):
        pdfgenerator = Latex2Pdf(self._TEMPLATE, self._OUTPUT_PDF)
        pdfgenerator.generate_pdf(self._data)

    def set_up(self):
        g = pygsheets.authorize(service_file=self._CREDENTIAL)
        self.g_sheet = g.open(self._GOOGLE_SHEET_NAME)

    def tear_down(self):
        self.end_time = int(round(time.time() * 1000))
        print('Script took {} seconds'.format((self.end_time - self.start_time)/1000))

    def run(self):
        self.set_up()
        self.process_data()
        self.generate()
        self.tear_down()

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--month', required=True, help='Month for which the report is. Must be in the format MmmYY')
    args = vars(ap.parse_args())

    report = SalarySummaryForManagement(args['month'])
    report.run()
