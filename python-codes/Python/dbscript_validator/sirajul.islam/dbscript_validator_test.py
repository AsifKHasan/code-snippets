#!/usr/local/bin/python3

'''
Usage: ./dbscript_validator_test.py
'''

import unittest
import dbscript_validator

class DbScriptValidatorTestCase(unittest.TestCase):

    def test_list_tables(self):
        self.assertEqual(7, dbscript_validator.list_tables('R01_00_00__antarika.sql').len())
        self.assertEqual(True, 'ClientResponseLog' in dbscript_validator.list_tables('R01_00_00__antarika.sql'))
        self.assertEqual(True, 'ClientResponseLog1' not in dbscript_validator.list_tables('R01_00_00__antarika.sql'))

if __name__ == '__main__':
    unittest.main()
