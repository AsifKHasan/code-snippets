#!/usr/bin/env python3
'''
usage: ./salary-advice-cash.py --month Nov18 --wing Delivery/Acquisition/Operations
'''
import json
import os
import shutil
import sys
import time
import datetime
import argparse

import pygsheets
import num2words

from latex2pdf import Latex2Pdf

class SalaryAdviceCash(object):

    _CREDENTIAL = './conf/credential.json'
    _GOOGLE_SHEET_NAME = 'FAU__SalarySheet__2018__Test'
    _TEMPLATE = "./templates/salary-advice-cash.tex"
    _OUTPUT_PDF = './out/salary-advice-cash__{0}__{1}__{2}.pdf'
    _OUTPUT_DATA = './out/salary-advice-cash__{0}__{1}__{2}.json'

    def __init__(self, month, wing):
        self.start_time = int(round(time.time() * 1000))
        self._WORKSHEET_NAME = month
        self._WING = wing
        s = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d__%H-%M-%S")
        self._OUTPUT_PDF = self._OUTPUT_PDF.format(self._WING, self._WORKSHEET_NAME, s)
        self._OUTPUT_DATA = self._OUTPUT_DATA.format(self._WING, self._WORKSHEET_NAME, s)

    def process_data(self):
        ws = self.g_sheet.worksheet('title', self._WORKSHEET_NAME)
        vals = ws.get_all_values(returnas='matrix', majdim='ROWS', include_empty=True)
        self._data = list(map(lambda v: {"wing" : v[4].strip(), "unit" : v[5].strip(), "name" : v[2].strip(), "payable" : v[46].strip().replace('-', ''), "paythrough" : v[48].strip(), "paystatus" : v[49].strip()}, vals[5:]))
        self._data = list(filter(lambda v: v["wing"] == self._WING and v["paythrough"] == "Cash" and v["paystatus"] == "In Process", self._data))
        totalamount = sum(float(a['payable'].replace(',', '') or 0) for a in self._data)
        totalamountinwords = num2words.num2words(totalamount, to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')
        self._data = {"month" : self._WORKSHEET_NAME, "wing" : self._WING, "date": datetime.datetime.now().strftime('%B %d, %Y'), "totalamount": "{:,.2f}".format(totalamount), "totalamountinwords": totalamountinwords, "salary": self._data}
        with open(self._OUTPUT_DATA, "w") as f:
            f.write(json.dumps(self._data, sort_keys=False, indent=4))

    def generate(self):
        pdfgenerator = Latex2Pdf(self._TEMPLATE, self._OUTPUT_PDF)
        pdfgenerator.generate_pdf(self._data)

    def set_up(self):
        g = pygsheets.authorize(service_file=self._CREDENTIAL)
        self.g_sheet = g.open(self._GOOGLE_SHEET_NAME)

    def tear_down(self):
        self.end_time = int(round(time.time() * 1000))
        print("Script took {} seconds".format((self.end_time - self.start_time)/1000))

    def run(self):
        self.set_up()
        self.process_data()
        self.generate()
        self.tear_down()

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--month", required=True, help="Month for which the process is. Must be in the format MmmYY")
    ap.add_argument("-w", "--wing", required=True, help="Wing for which the process is. Must be any of Acquisition/Operations/Delivery")
    args = vars(ap.parse_args())

    generator = SalaryAdviceCash(args["month"], args["wing"])
    generator.run()
